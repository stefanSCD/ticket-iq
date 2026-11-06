#!/usr/bin/env python3
"""Validate dataset integrity; this does not replace independent semantic review."""

import csv
import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
CHECKS = 0
CATEGORIES = {
    'resolved_by_documentation': 60,
    'unresolved': 60,
    'partially_resolved': 40,
    'conflicting_documentation': 20,
    'already_clear': 20,
}
FORBIDDEN_INPUT_KEYS = {
    'category', 'difficulty_level', 'expected_questions', 'should_ask_questions',
    'recommendation', 'missing_decisions', 'conflict_sources', 'registry_refs',
    'evidence', 'split', 'original_request_style', 'gap_representation',
}


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def rows(path):
    text = (ROOT / path).read_text(encoding='utf-8')
    check(bool(text.strip()), f'Empty JSONL: {path}')
    result = []
    for number, line in enumerate(text.splitlines(), 1):
        try:
            result.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f'{path}:{number}: {exc}') from exc
    return result


def time(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    check(parsed.tzinfo is not None, f'Timestamp lacks offset: {value}')
    return parsed


def unique(records, key, name):
    values = [r[key] for r in records]
    check(len(values) == len(set(values)), f'Duplicate {key} in {name}')
    return {r[key]: r for r in records}


def input_keys(value, path):
    if isinstance(value, dict):
        check(not FORBIDDEN_INPUT_KEYS.intersection(value), f'Answer metadata in input {path}')
        for key, child in value.items():
            input_keys(child, f'{path}.{key}')
    elif isinstance(value, list):
        for child in value:
            input_keys(child, path)


def main():
    manifest = read_json('manifest.json')
    cutoff = time(manifest['snapshot_at'])
    documents = rows('corpus/documents.jsonl')
    history = rows('corpus/history_tickets.jsonl')
    tickets = rows('tickets/tickets.jsonl')
    labels = rows('review/ticket_labels.jsonl')
    golden = rows('review/golden_answers.jsonl')
    chunks = rows('retrieval/chunks.jsonl')
    qrels = rows('review/qrels.jsonl')
    audit = rows('review/decision_audit.jsonl')
    provenance = rows('review/history_provenance.jsonl')
    split_manifest = read_json('splits/split_manifest.json')
    schema = read_json('schema.json')

    check(len(documents) == 105, 'Expected 105 source documents')
    check(len(tickets) == len(labels) == len(golden) == len(qrels) == len(audit) == 200,
          'Expected 200 targets and one record in each supervision file')
    check(len(history) == len(provenance) == 40, 'Expected 40 historical tickets with provenance')
    check(len(chunks) == 145, 'Expected 145 retrieval chunks')
    docs_by_id = unique(documents, 'document_id', 'documentation')
    tickets_by_id = unique(tickets, 'ticket_id', 'targets')
    history_by_id = unique(history, 'ticket_id', 'history')
    labels_by_id = unique(labels, 'ticket_id', 'labels')
    golden_by_id = unique(golden, 'ticket_id', 'golden answers')
    qrels_by_id = unique(qrels, 'ticket_id', 'qrels')
    audit_by_id = unique(audit, 'ticket_id', 'decision audit')
    provenance_by_id = unique(provenance, 'ticket_id', 'history provenance')
    chunks_by_id = unique(chunks, 'chunk_id', 'retrieval')
    check(not tickets_by_id.keys() & history_by_id.keys(), 'A target is also historical context')
    for mapping in [labels_by_id, golden_by_id, qrels_by_id, audit_by_id]:
        check(mapping.keys() == tickets_by_id.keys(), 'Supervision does not cover exactly the target IDs')
    check(provenance_by_id.keys() == history_by_id.keys(), 'History provenance IDs differ')
    check(Counter(g['category'] for g in golden) == CATEGORIES, 'Wrong category distribution')
    check(len({t['description'] for t in tickets}) == 200, 'Duplicate target descriptions')
    check(len({t['summary'] for t in tickets + history}) == 240, 'Duplicate ticket summaries')

    sources = {}
    for d in documents:
        path = ROOT / d['path']
        check(path.is_relative_to(ROOT / 'docs') and path.is_file(), f'Bad documentation path: {path}')
        check(path.read_text(encoding='utf-8') == d['text'], f'Stale Markdown copy: {path}')
        check(d['status'] == 'Active' and d['applies_to'] == '1.1', f'Unexpected source scope: {d["document_id"]}')
        check(time(d['published_at']) <= cutoff, 'Future-dated document')
        check(len(d['passages']) >= 3, f'Source document lacks substantive passages: {d["document_id"]}')
        for p in d['passages']:
            check(p['source_id'] not in sources, f'Duplicate source ID: {p["source_id"]}')
            check(f'### {p["source_id"]}\n\n{p["exact_quote"]}' in d['text'], 'Passage does not match Markdown')
            sources[p['source_id']] = (d, p)
        chunk = chunks_by_id[d['document_id'] + ':chunk:01']
        check(chunk['text'] == d['text'] and chunk['source_kind'] == 'documentation', 'Documentation chunk mismatch')
        check(chunk['source_ids'] == [p['source_id'] for p in d['passages']], 'Chunk passage registry mismatch')
        check(chunk['available_at'] == d['published_at'], 'Document availability mismatch')
    check(manifest['counts']['passages'] == len(sources), 'Manifest passage count is wrong')
    check(manifest['counts']['documentation_words'] == sum(len(d['text'].split()) for d in documents),
          'Manifest word count is wrong')

    for h in history:
        input_keys(h, h['ticket_id'])
        check(h['status'] == h['resolution'] == 'Done', 'Historical ticket is not completed')
        check(time(h['created']) <= time(h['resolved_at']) <= cutoff, 'Invalid historical chronology')
        check(h['updated'] == h['resolved_at'], 'Historical snapshot timestamp mismatch')
        check(len(h['comments']) == 1 and h['comments'][0]['body'].strip(), 'History needs an accepted completion note')
        check(time(h['comments'][0]['created']) <= time(h['resolved_at']), 'History contains a future comment')
        chunk = chunks_by_id[f'HIST:{h["ticket_id"]}:chunk:01']
        check(json.loads(chunk['text']) == h, 'Historical chunk differs from completed record')
        check(chunk['available_at'] == h['resolved_at'], 'History available before completion')
        for sid in provenance_by_id[h['ticket_id']]['source_ids']:
            check(sid in sources, f'Unrecognized history provenance {sid}')
    check(Counter(p['original_request_style'] for p in provenance) == {'underspecified': 20, 'explicit': 20},
          'History original-request styles differ from description')

    target_schema = schema['$defs']['target_ticket']
    expected_keys = set(target_schema['required'])
    for t in tickets:
        tid = t['ticket_id']
        input_keys(t, tid)
        check(set(t) == expected_keys, f'Unexpected input schema on {tid}')
        for key, constraint in target_schema['properties'].items():
            expected_type = list if constraint['type'] == 'array' else str
            check(isinstance(t[key], expected_type), f'Invalid input field type: {tid}.{key}')
        check(t['status'] in ['To Do', 'In Progress', 'Blocked', 'In Review'], f'Target has invalid ongoing status: {tid}')
        check(not set(t['labels']) & set(CATEGORIES), f'Class leaked through ordinary labels: {tid}')
        as_of = time(t['snapshot_at'])
        check(time(t['created']) <= time(t['updated']) == as_of <= cutoff, f'Bad target chronology: {tid}')
        check(all(time(d['published_at']) <= as_of for d in documents), f'Future source for {tid}')
        check(all(time(h['resolved_at']) <= as_of for h in history), f'Future history for {tid}')
        g, label = golden_by_id[tid], labels_by_id[tid]
        check(g['category'] == label['category'], f'Label/answer category mismatch: {tid}')
        check(g['difficulty_level'] == label['difficulty_level'] and g['difficulty_level'] in ['L1', 'L2', 'L3'],
              f'Invalid difficulty on {tid}')
        check(g['should_ask_questions'] is bool(g['expected_questions']), f'Question flag mismatch: {tid}')
        check(g['missing_decisions'] == g['expected_questions'], f'Missing-decision question mismatch: {tid}')
        check(g['recommendation'].strip(), f'Empty recommendation: {tid}')
        check(g['should_ask_questions'] == (g['category'] in ['unresolved', 'partially_resolved', 'conflicting_documentation']),
              f'Wrong question/category behavior: {tid}')
        for e in g['evidence']:
            check(e['source_id'] in sources, f'Unknown evidence source: {tid}')
            d, passage = sources[e['source_id']]
            check(e['exact_quote'] == passage['exact_quote'], f'Inexact quotation: {tid}/{e["source_id"]}')
            check(e['document_id'] == e['document_section'] == d['document_id'], f'Evidence document mismatch: {tid}')
            check(e['path'] == d['path'] and e['title'] == d['title'], f'Evidence metadata mismatch: {tid}')
            check(e['published_at'] == d['published_at'], f'Evidence publication timestamp mismatch: {tid}')
        if g['category'] == 'already_clear':
            check(not g['evidence'], f'Already-clear scope unexpectedly depends on external evidence: {tid}')
        else:
            check(bool(g['evidence']), f'Non-clear target has no topical/supporting evidence: {tid}')
        if g['category'] == 'conflicting_documentation':
            check(len({e['document_id'] for e in g['evidence']}) >= 2, f'Conflict lacks two active documents: {tid}')
            check(g['conflict_sources'] == [e['source_id'] for e in g['evidence']], f'Conflict sources disagree: {tid}')
            check(len({e['exact_quote'] for e in g['evidence']}) >= 2, f'Conflict quotes are identical: {tid}')
        else:
            check(not g['conflict_sources'], f'Unexpected conflict sources: {tid}')
        if g['difficulty_level'] == 'L3':
            check(len({sources[e['source_id']][0]['area_id'] for e in g['evidence']}) >= 2,
                  f'L3 does not compose cross-area evidence: {tid}')
        q = qrels_by_id[tid]
        check(set(q['relevant_source_ids']) == {e['source_id'] for e in g['evidence']}, f'Qrels/evidence mismatch: {tid}')
        expected_chunks = {e['document_id'] + ':chunk:01' for e in g['evidence']}
        expected_chunks |= {f'HIST:{hid}:chunk:01' for hid in q['relevant_history_ticket_ids']}
        check(set(q['relevant_chunk_ids']) == expected_chunks, f'Wrong qrel chunk set: {tid}')
        for cid in q['relevant_chunk_ids']:
            check(cid in chunks_by_id and time(chunks_by_id[cid]['available_at']) <= as_of, f'Invalid qrel availability: {tid}')
        a = audit_by_id[tid]
        check(a['questions'] == g['expected_questions'] and a['category'] == g['category'], f'Decision audit mismatch: {tid}')
        check(set(a['reviewed_source_documents']) == set(docs_by_id), f'Incomplete declared absence-review scope: {tid}')
        check(set(a['reviewed_history_ticket_ids']) == set(history_by_id), f'Incomplete history review scope: {tid}')

    all_split_ids, area_split = set(), {}
    for split in ['train', 'validation', 'test']:
        st = rows(f'splits/{split}_tickets.jsonl')
        sl = rows(f'splits/{split}_labels.jsonl')
        sg = rows(f'splits/{split}_golden.jsonl')
        ss = rows(f'splits/{split}_sft.jsonl')
        ids = {t['ticket_id'] for t in st}
        check(len(st) == len(ids) == split_manifest['counts'][split]['tickets'], f'Wrong split size: {split}')
        check(not all_split_ids & ids, f'Target leakage across splits: {split}')
        all_split_ids |= ids
        for records in [sl, sg, ss]:
            check({r['ticket_id'] for r in records} == ids and len(records) == len(ids), f'Split record mismatch: {split}')
        check(Counter(r['category'] for r in sl) == split_manifest['counts'][split]['categories'], f'Split category mismatch: {split}')
        for t in st:
            check(t == tickets_by_id[t['ticket_id']], f'Split ticket copy differs: {split}')
        for label in sl:
            check(label == labels_by_id[label['ticket_id']] and label['split'] == split, f'Split label copy differs: {split}')
            previous = area_split.setdefault(label['area_id'], split)
            check(previous == split, f'Feature family leaks across splits: {label["area_id"]}')
            check(label['area_id'] in split_manifest['areas'][split], f'Feature assignment differs: {split}')
        for g in sg:
            check(g == golden_by_id[g['ticket_id']], f'Split golden copy differs: {split}')
        for record in ss:
            tid = record['ticket_id']
            messages = record['messages']
            check([m['role'] for m in messages] == ['system', 'user', 'assistant'], f'Invalid SFT role order: {tid}')
            context, output = json.loads(messages[1]['content']), json.loads(messages[2]['content'])
            check(context['ticket'] == tickets_by_id[tid], f'SFT target differs: {tid}')
            check(context['documentation_excerpts'] == golden_by_id[tid]['evidence'], f'Oracle evidence mismatch: {tid}')
            input_keys(context['ticket'], tid)
            for h in context['completed_history']:
                check(h == history_by_id[h['ticket_id']], f'SFT history altered: {tid}')
                check(time(h['resolved_at']) <= time(context['as_of']), f'Future SFT history: {tid}')
            check(len(context['completed_history']) == 2, f'Expected two same-area historical examples: {tid}')
            check(not FORBIDDEN_INPUT_KEYS.intersection(context), f'Supervision key appears in SFT user context: {tid}')
            g = golden_by_id[tid]
            for key in ['category', 'should_ask_questions', 'recommendation', 'expected_questions']:
                check(output[key] == g[key], f'SFT completion differs from golden {tid}.{key}')
            check(output['evidence'] == [{k: e[k] for k in ['source_id', 'exact_quote']} for e in g['evidence']],
                  f'SFT completion quotes differ: {tid}')
    check(all_split_ids == set(tickets_by_id), 'Splits do not cover every target exactly once')

    for chunk in chunks:
        check(chunk['project_id'] == 'toolnest', 'Wrong project filter')
        check(chunk['source_kind'] in ['documentation', 'completed_ticket'], 'Answer key or target in retrieval corpus')
        if chunk['source_kind'] == 'completed_ticket':
            check(chunk['ticket_id'] not in tickets_by_id, 'Target ticket appears in retrieval')
            input_keys(json.loads(chunk['text']), chunk['chunk_id'])
        check('should_ask_questions' not in chunk['text'], 'Golden review appears in retrieval text')

    for csv_path, expected in [('tickets/toolnest_jira_import.csv', tickets), ('corpus/history_jira.csv', history)]:
        with (ROOT / csv_path).open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            check(not FORBIDDEN_INPUT_KEYS.intersection(reader.fieldnames), f'Golden columns in {csv_path}')
            actual = list(reader)
        check(len(actual) == len(expected), f'CSV row count differs: {csv_path}')
        for csv_row, record in zip(actual, expected):
            for key, value in csv_row.items():
                check(json.loads(value) == record[key] if isinstance(record[key], (list, dict)) else value == record[key],
                      f'CSV content differs: {csv_path}/{record["ticket_id"]}/{key}')

    for name in ['toolnest-docs.zip', 'toolnest-tickets.zip']:
        with ZipFile(ROOT / name) as archive:
            check(archive.testzip() is None, f'Archive CRC failure: {name}')
            names = archive.namelist()
            check(len(names) == len(set(names)), f'Duplicate archive entry: {name}')
            for member in names:
                path = ROOT / member
                check(path.is_relative_to(ROOT) and '..' not in Path(member).parts, 'Unsafe archive path')
                check(path.is_file() and path.read_bytes() == archive.read(member), f'Stale archive entry: {name}/{member}')
                if name == 'toolnest-docs.zip':
                    check(member.startswith('docs/') or member == 'corpus/documents.jsonl', 'Answer key in documentation ZIP')
            if name == 'toolnest-tickets.zip':
                check('tickets/tickets.jsonl' in names and 'review/golden_answers.jsonl' in names,
                      'Ticket archive lacks inputs or separated answers')

    actual_files = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
                    and p.name != 'manifest.json' and '__pycache__' not in p.parts and not p.name.startswith('.')}
    check(actual_files == set(manifest['files']), 'Manifest file inventory differs; rebuild after edits')
    for name, expected_hash in manifest['files'].items():
        check(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected_hash, f'Integrity hash mismatch: {name}')

    print(json.dumps(dict(result='PASS', integrity_checks=CHECKS,
                          documents=len(documents), source_passages=len(sources), targets=len(tickets),
                          completed_history=len(history), retrieval_chunks=len(chunks),
                          categories=dict(Counter(g['category'] for g in golden)),
                          semantic_review='Not independently human-reviewed; see methodology.md'), indent=2))


if __name__ == '__main__':
    main()
