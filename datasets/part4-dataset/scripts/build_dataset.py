#!/usr/bin/env python3
"""Rebuild the fictional ToolNest dataset with Python's standard library only."""

import csv
import importlib.util
import json
import random
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from dataset_integrity import file_hash


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = '2026-11-06T12:00:00Z'
PUBLISHED = '2026-08-28T08:00:00Z'
SEED = 41106
FAMILIES = [
    ('br', 'BR', 'Business rules', 'Elena Varga, Product Owner'),
    ('wf', 'WF', 'Workflow', 'Iris Popa, Operations Lead'),
    ('api', 'API', 'API contract', 'Matei Ionescu, Tech Lead'),
    ('adr', 'ADR', 'Architecture decision', 'Matei Ionescu, Tech Lead'),
    ('faq', 'FAQ', 'Staff FAQ', 'Iris Popa, Operations Lead'),
]
CATEGORIES = {
    'resolved_by_documentation': 60, 'unresolved': 60,
    'partially_resolved': 40, 'conflicting_documentation': 20, 'already_clear': 20,
}
PEOPLE = ['Elena Varga', 'Matei Ionescu', 'Iris Popa', 'Nadia Marin',
          'Vlad Petrescu', 'Sara Pavel', 'Luca Dima', 'Ana Stoica']
SYSTEM = (
    'Review the supplied fictional ToolNest Jira ticket for implementation readiness. '
    'Use applicable documentation and completed history to supply decisions already made. '
    'Ask focused questions only for material decisions that remain unspecified. '
    'If active sources conflict for the requested scope, cite both and request a decision. '
    'Do not invent rules or treat workflow status as requirements quality. '
    'A narrow complete task may need no change. Return one JSON object with category, '
    'should_ask_questions, recommendation, expected_questions, and evidence. '
    'Evidence entries must contain source_id and exact_quote.'
)

# These examples need rules from more than one product area. Related target
# groups are kept together below; shared source-policy overlap is documented.
CROSS_REFS = {
    ('RSV', 2): ['MNT.BR1'],
    ('TRN', 0): ['OUT.BR1', 'OUT.API3'],
    ('APR', 1): ['RSV.BR2'],
    ('OUT', 1): ['INT.BR4', 'INT.ADR3'],
    ('OVD', 0): ['RET.BR1', 'RET.ADR1'],
    ('EXT', 0): ['RSV.API4'],
    ('NOS', 0): ['OUT.BR3'],
    ('MNT', 2): ['DAM.BR3', 'CAT.BR2'],
    ('KIT', 0): ['RSV.ADR1'],
    ('NTF', 0): ['INT.ADR2'],
    ('AUD', 2): ['DAM.BR4'],
    ('RPT', 0): ['RET.BR1'],
}
# Group related features as well as exact paraphrases. Target labels and answers
# for validation/test never appear in the training SFT file.
SPLIT_AREAS = {
    'train': ['CAT', 'RSV', 'APR', 'EXT', 'CAN', 'WAI', 'DAM', 'MNT', 'KIT', 'XFR'],
    'validation': ['TRN', 'OUT', 'NOS', 'SEC', 'INT', 'NTF'],
    'test': ['RET', 'OVD', 'AUD', 'RPT'],
}
# AUD uses DAM evidence, but not DAM target examples. This mirrors retrieval
# of shared source rules; explicit target scenarios remain feature-disjoint.
SPLIT_NOTES = (
    'Train/validation/test are 100/60/40 target tickets, grouped by product area. '
    'Related booking, maintenance, and kit cases stay in train; checkout, identity, '
    'and integration cases stay in validation; return, overdue, audit, and reporting '
    'cases stay in test. Audit cases may cite shared incident-access source rules '
    'from the training documentation. All project docs and pre-cutoff completed '
    'history may be indexed at evaluation time. This is a within-project feature '
    'holdout, not an unseen-project benchmark.'
)


def load_source(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'source' / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    # Avoid pycache files in the distributed authored sources.
    exec(compile(spec.loader.get_source(name), str(spec.origin), 'exec'), module.__dict__)
    return module


def write_text(path, text):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + '\n', encoding='utf-8', newline='\n')


def write_json(path, value):
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def write_jsonl(path, records):
    write_text(path, '\n'.join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in records))


def write_csv(path, records, fields):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        for record in records:
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v
                             for k, v in record.items() if k in fields})


def stamp(dt):
    return dt.replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')


def document(doc_id, title, owner, facts, path, family, area_id, context):
    passages = [dict(source_id=f'{doc_id}-{i:02d}', exact_quote=fact)
                for i, fact in enumerate(facts, 1)]
    body = '\n\n'.join(f'### {p["source_id"]}\n\n{p["exact_quote"]}' for p in passages)
    markdown = (
        f'# {title}\n\n'
        f'Document ID: `{doc_id}`  \nOwner: {owner}  \nStatus: Active  \n'
        f'Applies to: ToolNest 1.1  \nPublished: {PUBLISHED}\n\n'
        f'## Context\n\n{context}\n\n## Requirements and guidance\n\n{body}\n'
    )
    write_text(path, markdown)
    return dict(document_id=doc_id, project_id='toolnest', title=title, owner=owner,
                family=family, area_id=area_id, status='Active', applies_to='1.1',
                published_at=PUBLISHED, path=path, text=markdown, passages=passages)


def resolve_ref(area, ref, source_index):
    if '.' in ref:
        area, ref = ref.split('.', 1)
    for _, prefix, _, _ in FAMILIES:
        if ref.startswith(prefix):
            source_id = f'TN-{area}-{prefix}-{int(ref[len(prefix):]):02d}'
            return source_index[source_id]
    raise ValueError(f'Unknown reference: {area}.{ref}')


def main():
    authored = load_source('toolnest_content')
    history_source = load_source('toolnest_history').HISTORY
    areas = authored.AREAS
    rng = random.Random(SEED)
    source_index, documents = {}, []
    for p in authored.PROJECT_DOCS:
        path = f'docs/project/{p["id"].lower()}.md'
        documents.append(document(p['id'], p['title'], p['owner'], p['facts'], path,
                                  'project', 'PROJECT', 'Shared project context for the active ToolNest baseline.'))
    for area in areas:
        for key, prefix, family, owner in FAMILIES:
            doc_id = f'TN-{area["code"]}-{prefix}'
            path = f'docs/topics/{area["code"].lower()}/{key}.md'
            documents.append(document(doc_id, f'{area["name"]} — {family}', owner,
                                      area[key], path, family, area['code'], area['context']))
    for d in documents:
        for p in d['passages']:
            source_index[p['source_id']] = dict(
                **p, document_id=d['document_id'], document_section=d['document_id'],
                title=d['title'], path=d['path'], published_at=d['published_at'])
    write_jsonl('corpus/documents.jsonl', documents)

    history, history_provenance, area_history = [], [], {}
    for ai, area in enumerate(areas):
        code = area['code']
        area_history[code] = []
        for hi, (summary, request, completion, refs) in enumerate(history_source[code]):
            number = ai * 2 + hi + 1
            if ai < 6 and hi == 0:
                created = datetime(2026, 3, 2, 10) + timedelta(days=ai)
                closed = datetime(2026, 3, 20, 15) + timedelta(days=ai)
                version = '1.0'
            else:
                created = datetime(2026, 6, 1, 10) + timedelta(days=ai * 2 + hi)
                closed = datetime(2026, 8, 1, 15) + timedelta(days=ai + hi)
                version = '1.1'
            ticket = dict(ticket_id=f'TN-{number:03d}', project_id='toolnest',
                          issue_type='Story' if hi == 0 else 'Task', summary=summary,
                          description=request, component=area['component'], status='Done',
                          priority='Medium', reporter=PEOPLE[ai % len(PEOPLE)],
                          assignee=PEOPLE[(ai + 2) % len(PEOPLE)], created=stamp(created),
                          updated=stamp(closed), resolved_at=stamp(closed),
                          fix_version=version, labels=[f'area-{code.lower()}'],
                          comments=[dict(author=PEOPLE[(ai + 3) % len(PEOPLE)],
                                         created=stamp(closed), body=completion)],
                          resolution='Done')
            history.append(ticket)
            area_history[code].append(ticket)
            # Provenance is audit-only, not metadata attached to history retrieval.
            history_provenance.append(dict(ticket_id=ticket['ticket_id'],
                source_ids=[resolve_ref(code, ref, source_index)['source_id'] for ref in refs.split()],
                original_request_style='underspecified' if hi == 0 else 'explicit'))
    write_jsonl('corpus/history_tickets.jsonl', history)
    write_jsonl('review/history_provenance.jsonl', history_provenance)

    cases = [(area, ci, c) for area in areas for ci, c in enumerate(area['cases'])]
    rng.shuffle(cases)
    split_lookup = {area: split for split, codes in SPLIT_AREAS.items() for area in codes}
    tickets, labels, golden, qrels, audit = [], [], [], [], []
    split_rows = {name: dict(tickets=[], labels=[], golden=[], sft=[]) for name in SPLIT_AREAS}
    for i, (area, ci, c) in enumerate(cases):
        code, category = area['code'], c['category']
        created = datetime(2026, 9, 1, 9) + timedelta(days=(i * 17) % 60, minutes=i % 60)
        updated = created + timedelta(days=i % 4)
        ticket_id = f'TN-{501 + i:03d}'
        refs = c['refs'] + CROSS_REFS.get((code, ci), [])
        evidence = [resolve_ref(code, ref, source_index) for ref in refs]
        level = ('L3' if (code, ci) in CROSS_REFS else
                 'L1' if category == 'already_clear' or (category == 'resolved_by_documentation' and len(evidence) == 1)
                 else 'L2')
        ticket = dict(ticket_id=ticket_id, project_id='toolnest',
                      issue_type=rng.choice(['Bug', 'Task']) if category in ['resolved_by_documentation', 'conflicting_documentation']
                      else rng.choice(['Story', 'Task']) if category != 'already_clear' else 'Task',
                      summary=c['summary'], description=c['description'], component=area['component'],
                      priority=rng.choice(['High', 'Medium', 'Medium', 'Low']),
                      status=rng.choice(['To Do', 'In Progress', 'Blocked', 'In Review']),
                      reporter=rng.choice(PEOPLE), assignee=rng.choice(PEOPLE),
                      created=stamp(created), updated=stamp(updated), snapshot_at=stamp(updated),
                      fix_version='1.2', labels=[f'area-{code.lower()}', 'release-1.2'])
        answer = dict(ticket_id=ticket_id, category=category, difficulty_level=level,
                      should_ask_questions=bool(c['questions']), expected_questions=c['questions'],
                      missing_decisions=c['questions'], recommendation=c['recommendation'],
                      evidence=evidence,
                      conflict_sources=[e['source_id'] for e in evidence] if category == 'conflicting_documentation' else [])
        label = dict(ticket_id=ticket_id, category=category, difficulty_level=level,
                     area_id=code, split=split_lookup[code])
        source_ids = {e['source_id'] for e in evidence}
        # Only history with facts actually cited by this case receives relevance credit.
        relevant_history = [h['ticket_id'] for h in history_provenance
                            if h['ticket_id'] in {t['ticket_id'] for t in area_history[code]}
                            and source_ids.intersection(h['source_ids'])]
        relevant_chunks = sorted({e['document_id'] + ':chunk:01' for e in evidence}
                                 | {f'HIST:{tid}:chunk:01' for tid in relevant_history})
        qrels.append(dict(ticket_id=ticket_id, relevant_source_ids=sorted(source_ids),
                          relevant_chunk_ids=relevant_chunks, relevant_history_ticket_ids=relevant_history,
                          coverage='authored_support_set_not_exhaustive'))
        audit.append(dict(ticket_id=ticket_id, area_id=code, category=category,
                          gap_representation='explicit_open_decision' if c['explicit_gap'] else
                          'not_specified_in_authored_corpus' if c['questions'] and category != 'conflicting_documentation'
                          else 'not_applicable',
                          reviewed_source_documents=[d['document_id'] for d in documents],
                          reviewed_history_ticket_ids=[h['ticket_id'] for h in history],
                          absence_check_status='generator_author_review_only_not_independent_human_review',
                          questions=c['questions']))
        completion = {k: answer[k] for k in ['category', 'should_ask_questions', 'recommendation', 'expected_questions']}
        completion['evidence'] = [{k: e[k] for k in ['source_id', 'exact_quote']} for e in evidence]
        sft_context = dict(ticket=ticket, documentation_excerpts=evidence,
                           completed_history=area_history[code], as_of=ticket['snapshot_at'],
                           context_mode='oracle_documentation_with_same_area_historical_context')
        sft = dict(ticket_id=ticket_id, messages=[
            dict(role='system', content=SYSTEM),
            dict(role='user', content=json.dumps(sft_context, ensure_ascii=False, sort_keys=True)),
            dict(role='assistant', content=json.dumps(completion, ensure_ascii=False, sort_keys=True))])
        tickets.append(ticket)
        labels.append(label)
        golden.append(answer)
        target = split_rows[split_lookup[code]]
        for name, record in [('tickets', ticket), ('labels', label), ('golden', answer), ('sft', sft)]:
            target[name].append(record)

    write_jsonl('tickets/tickets.jsonl', tickets)
    write_jsonl('review/ticket_labels.jsonl', labels)
    write_jsonl('review/golden_answers.jsonl', golden)
    write_jsonl('review/decision_audit.jsonl', audit)
    write_jsonl('review/qrels.jsonl', qrels)
    write_csv('tickets/toolnest_jira_import.csv', tickets,
              ['ticket_id', 'issue_type', 'summary', 'description', 'component', 'priority', 'status',
               'reporter', 'assignee', 'created', 'updated', 'fix_version', 'labels'])
    write_csv('corpus/history_jira.csv', history,
              ['ticket_id', 'issue_type', 'summary', 'description', 'component', 'priority', 'status',
               'reporter', 'assignee', 'created', 'updated', 'resolved_at', 'fix_version', 'labels', 'comments'])
    label_by_id = {r['ticket_id']: r for r in labels}
    write_csv('review/toolnest_review.csv', [dict(**ticket, **{k: v for k, v in answer.items() if k != 'ticket_id'},
                                                 split=label_by_id[ticket['ticket_id']]['split'])
                                            for ticket, answer in zip(tickets, golden)],
              ['ticket_id', 'summary', 'description', 'status', 'category', 'difficulty_level', 'split',
               'recommendation', 'expected_questions', 'evidence'])
    for split, records in split_rows.items():
        for name, rows in records.items():
            write_jsonl(f'splits/{split}_{name}.jsonl', rows)

    chunks = [dict(chunk_id=d['document_id'] + ':chunk:01', project_id='toolnest',
                   source_kind='documentation', document_id=d['document_id'], path=d['path'],
                   title=d['title'], area_id=d['area_id'], available_at=d['published_at'],
                   source_ids=[p['source_id'] for p in d['passages']], text=d['text']) for d in documents]
    chunks += [dict(chunk_id=f'HIST:{h["ticket_id"]}:chunk:01', project_id='toolnest',
                    source_kind='completed_ticket', ticket_id=h['ticket_id'],
                    available_at=h['resolved_at'], applies_to=h['fix_version'],
                    title=h['summary'], text=json.dumps(h, ensure_ascii=False, sort_keys=True)) for h in history]
    write_jsonl('retrieval/chunks.jsonl', chunks)
    write_json('schema.json', schema())
    write_text('knowledge-registry.md', registry(areas, tickets, golden, labels))
    write_text('README.md', readme(documents, tickets, history, labels))
    write_text('methodology.md', methodology())
    write_text('review/examples.md', examples(tickets, golden))
    write_text('docs/INDEX.md', '# ToolNest documentation index\n\n'
               'Fictional active release 1.1 documentation. Publication: 2026-08-28. '
               'The numbered source IDs in each file identify exact citable passages.\n\n'
               + '\n'.join(f'- [{d["document_id"]} — {d["title"]}]({d["path"].removeprefix("docs/")})'
                           for d in documents))
    write_json('splits/split_manifest.json', dict(seed=SEED, strategy='within_project_feature_group_holdout',
                areas=SPLIT_AREAS, notes=SPLIT_NOTES,
                counts={s: dict(tickets=len(r['tickets']), categories=dict(Counter(x['category'] for x in r['labels'])))
                        for s, r in split_rows.items()}))
    # Archives are convenience copies; don't index both ZIP contents and loose copies.
    zip_paths('toolnest-docs.zip', [p for p in sorted((ROOT / 'docs').rglob('*')) if p.is_file()]
              + [ROOT / 'corpus/documents.jsonl'])
    zip_paths('toolnest-tickets.zip', [ROOT / 'README.md', ROOT / 'methodology.md', ROOT / 'knowledge-registry.md',
              ROOT / 'schema.json', ROOT / 'corpus/history_tickets.jsonl', ROOT / 'corpus/history_jira.csv',
              ROOT / 'retrieval/chunks.jsonl']
              + [p for folder in ['tickets', 'review', 'splits'] for p in sorted((ROOT / folder).rglob('*')) if p.is_file()])
    files = [p for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name != 'manifest.json'
             and '__pycache__' not in p.parts and not p.name.startswith('.')]
    write_json('manifest.json', dict(dataset='toolnest', version='1.0', fictional=True,
                generated_for_date='2026-11-06', snapshot_at=SNAPSHOT, seed=SEED,
                counts=dict(documents=len(documents), passages=len(source_index),
                            documentation_words=sum(len(d['text'].split()) for d in documents),
                            target_tickets=len(tickets), completed_history_tickets=len(history),
                            categories=dict(Counter(g['category'] for g in golden)),
                            retrieval_chunks=len(chunks)),
                hash_format='sha256-text-lf-v1',
                files={p.relative_to(ROOT).as_posix(): file_hash(p) for p in files}))
    print(json.dumps(dict(documents=len(documents), target_tickets=len(tickets), history=len(history),
                          categories=dict(Counter(g['category'] for g in golden)),
                          splits={s: len(r['tickets']) for s, r in split_rows.items()}), indent=2))


def zip_paths(name, paths):
    with ZipFile(ROOT / name, 'w', compression=ZIP_DEFLATED) as z:
        for path in paths:
            info = ZipInfo(path.relative_to(ROOT).as_posix(), date_time=(2026, 11, 6, 12, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, path.read_bytes())


def schema():
    # A single schema describes the record kinds without imposing a new team-wide format.
    ticket_properties = {k: {'type': 'string'} for k in [
        'ticket_id', 'project_id', 'issue_type', 'summary', 'description', 'component', 'priority',
        'status', 'reporter', 'assignee', 'created', 'updated', 'snapshot_at', 'fix_version']}
    ticket_properties['labels'] = {'type': 'array', 'items': {'type': 'string'}}
    return {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        'title': 'ToolNest dataset record schemas',
        '$defs': {
            'target_ticket': {'type': 'object', 'additionalProperties': False,
                              'required': list(ticket_properties), 'properties': ticket_properties},
            'label': {'type': 'object', 'required': ['ticket_id', 'category', 'difficulty_level', 'area_id', 'split'],
                      'properties': {'category': {'enum': list(CATEGORIES)}, 'difficulty_level': {'enum': ['L1', 'L2', 'L3']}}},
            'evidence': {'type': 'object', 'required': ['source_id', 'document_id', 'exact_quote', 'path', 'published_at'],
                         'properties': {'source_id': {'type': 'string'}, 'exact_quote': {'type': 'string'}}},
            'golden_answer': {'type': 'object', 'required': ['ticket_id', 'category', 'difficulty_level', 'should_ask_questions',
                                                          'recommendation', 'expected_questions', 'evidence', 'conflict_sources'],
                              'properties': {'category': {'enum': list(CATEGORIES)}, 'should_ask_questions': {'type': 'boolean'},
                                             'expected_questions': {'type': 'array', 'items': {'type': 'string'}},
                                             'evidence': {'type': 'array', 'items': {'$ref': '#/$defs/evidence'}}}},
        },
        'description': 'Select the appropriate $defs entry for each JSONL artifact. This is a part-4 schema; no central schema migration is implied.'
    }


def registry(areas, tickets, golden, labels):
    ticket_lookup = {t['ticket_id']: t for t in tickets}
    label_lookup = {l['ticket_id']: l for l in labels}
    lines = ['# ToolNest — hidden knowledge registry', '',
             '**Answer key. Do not index this file, source/, review/, or SFT completions for retrieval.**', '',
             'These are generator-authored labels, not independent expert judgements. Missing decisions were designed across '
             'the full authored corpus and completed history; automated absence checking cannot establish semantic absence.', '',
             'Release 1.1 is active. Every deliberate conflict pairs two active statements with the same scope. '
             'There is no blanket precedence for business rules over FAQs. Historical outcomes are release-scoped.', '',
             '## Feature inventory', '', '| Area | Topic | Split |', '|---|---|---|']
    for a in areas:
        split = next(s for s, codes in SPLIT_AREAS.items() if a['code'] in codes)
        lines.append(f'| {a["code"]} | {a["name"]} | {split} |')
    for category in CATEGORIES:
        lines += ['', f'## {category}', '']
        for g in golden:
            if g['category'] != category:
                continue
            tid = g['ticket_id']
            sources = ', '.join(e['source_id'] for e in g['evidence']) or 'Ticket text only'
            lines += [f'### {tid} — {ticket_lookup[tid]["summary"]}', '',
                      f'Area: {label_lookup[tid]["area_id"]}. Sources: {sources}.', '', g['recommendation'], '']
            lines += [f'- {q}' for q in g['expected_questions']]
    return '\n'.join(lines)


def readme(documents, tickets, history, labels):
    words = sum(len(d['text'].split()) for d in documents)
    return f'''# ToolNest — TicketIQ part 4

An entirely fictional university equipment-lending project for evidence-grounded Jira ticket review. All policies, people, institutions, incidents, and completed work are synthetic. Language: English. Dataset version: 1.0. Snapshot cutoff: {SNAPSHOT}.

The active product lends cameras, laptops, lab tools, and kits. It launched as a single-lab pilot and grew into a multi-lab service. The fictional stack is React/TypeScript, FastAPI, PostgreSQL, Redis, background workers, and private object storage. This dataset contains documentation and ticket artifacts, not an implementation of that application.

## Contents

- **{len(documents)} substantive Markdown source sections**, {words:,} whitespace-delimited words, covering 20 product areas plus 5 shared project documents. These are sections/files, not 105 rendered pages.
- **{len(tickets)} ongoing review targets**, with To Do, In Progress, Blocked, or In Review workflow status.
- **{len(history)} completed historical tickets**, including original requests and accepted completion comments. Half start with deliberately underspecified requests and half with explicit requests. Completion notes resolve their recorded scope.
- **200 golden reviews**, exact source quotations, focused questions, and recommendations for improving readiness.
- **145 retrieval chunks**: one per short source document and one per completed historical ticket.
- Input-only Jira-style CSV, JSONL, feature-group splits, chat-message SFT records, a source registry, integrity hashes, and reproducible generation/validation scripts.

| Review category | Targets | Expected behavior |
|---|---:|---|
| resolved_by_documentation | 60 | Supply the documented decision; ask no redundant question. |
| unresolved | 60 | Ask for a missing policy or feature decision; do not invent it. |
| partially_resolved | 40 | Supply the documented part and ask only for what remains open. |
| conflicting_documentation | 20 | Cite incompatible active statements and request a decision. |
| already_clear | 20 | Accept the narrow, testable ticket without adding scope. |

`resolved_by_documentation` is a review category, **not** Jira status. All 40 Done tickets are historical retrieval context; the 200 review targets are ongoing. Review labels never appear as ordinary ticket fields or labels.

## Files and boundaries

```text
docs/                         RAG-safe Markdown, including INDEX.md
corpus/documents.jsonl         same documentation as structured records
corpus/history_tickets.jsonl   RAG-safe completed history with dated comments
corpus/history_jira.csv        completed-history CSV
retrieval/chunks.jsonl         index this prebuilt corpus once
tickets/tickets.jsonl          200 input-only review targets
tickets/toolnest_jira_import.csv
review/                       answer keys, evidence, qrels, decision audit, examples
splits/*_tickets.jsonl         input-only target partitions
splits/*_labels.jsonl          separated labels
splits/*_golden.jsonl          separated golden answers
splits/*_sft.jsonl             oracle-context chat messages, including expected outputs
knowledge-registry.md         hidden answer key, never RAG content
source/                       authored content AND answer keys, never RAG content
scripts/                      reproducible builder and validator
manifest.json, schema.json, methodology.md
toolnest-docs.zip              optional generated copy of source docs
toolnest-tickets.zip           optional generated copy of inputs, history, and SEPARATE keys
```

**Retrieval:** index `retrieval/chunks.jsonl` with `project_id=toolnest`. Do not also index loose Markdown or the archived copies. Enforce `available_at <= ticket.snapshot_at`. Only the 40 completed history tickets belong in the prebuilt corpus; the review targets do not. All recorded source publication and history completion dates precede every target snapshot. Historical outcomes do not override active release rules.

**Fine-tuning:** use `splits/train_sft.jsonl`; reserve validation and test files for evaluation. SFT user messages include selected oracle documentation excerpts and the two same-area completed tickets. The assistant message is the expected review. This tests evidence use with supplied context, not retrieval quality. For end-to-end evaluation, retrieve context yourself and keep all labels and completions hidden.

**Splits:** {SPLIT_NOTES}

**Jira CSV:** these are Jira-style exports with explicit columns. Map columns in your importer; an import into a real Jira instance has not been tested. Labels are JSON arrays in the CSV. The input CSV has no golden answers.

## Reproduce and validate

From this directory:

```sh
python3 scripts/build_dataset.py
python3 scripts/validate_dataset.py
```

Both scripts use only the Python standard library. Generation is deterministic, including archive timestamps. Edit `source/` and rebuild rather than editing generated copies. The validator checks counts, schemas, citations and exact quotes, temporal availability, split membership, question/category rules, input/key separation, and file hashes. Archive copies are optional in the repository: the builder generates them, and the validator checks their boundaries and contents when present. Text hashes normalize CRLF to LF so Windows and Unix checkouts validate consistently; ZIP hashes remain byte-exact.

## Review before research use

The data is handcrafted synthetic content assembled by a deterministic builder. It has no independent human semantic review. The 20 deliberate conflicts use numeric policy boundaries and the same business-rule/FAQ pairing, and several readiness patterns repeat. These regularities can make classification easier than real Jira review. Qrels are authored support sets, not exhaustive relevance judgements. Difficulty tiers are heuristic, not human-calibrated. See `methodology.md` for evaluation limits and the semantic review checklist.
'''


def methodology():
    return f'''# ToolNest generation and evaluation methodology

## Goal and scope

The task is to decide whether the requested implementation has sufficient requirements, using the target text, active project sources, and completed history. A ticket can omit a detail that is already specified elsewhere. Ask only if a material decision remains genuinely open; do not invent a default or expand a complete small task.

Twenty feature families contain ten authored scenarios each: three resolved, three unresolved, two partial, one conflict, and one already clear. Ticket order, people, priorities, dates, and ongoing workflow statuses are shuffled with seed {SEED}. Ticket descriptions and expected reviews are authored individually; the builder does not call an external model. This produces controlled coverage rather than a natural prevalence estimate.

Five short source documents per family cover rules, workflow, API, architecture, and FAQ; five shared documents describe product scope, architecture, chronology, calendars, and readiness. Passage IDs are stable and exact quotes are mechanically verified. No claim is made that these are formatted pages. Fictional API behavior is a project contract, not a claim about third-party software.

## Decision design

Resolved examples require applying a specified rule to a sparse request. Unresolved examples introduce an exception or new behavior whose implementation policy is absent. The first unresolved case per family explicitly mentions an open decision in the docs; the other gaps are implicit. Partial examples combine an established constraint and an undecided design dimension. Conflicts pair incompatible active rules for the same scope; neither publication date nor document family resolves them. Already-clear cases describe a limited presentation, documentation, or test change with an observable check.

Evidence for an unresolved case is topical context, **not proof of absence**. `review/decision_audit.jsonl` lists the full reviewed corpus scope and whether the gap is explicit or implicit. Its status states that this is generator-author review only. Independently review all other files and historical comments before trusting an absence label. Automated citation validity does not prove semantic correctness, necessity of a question, or completeness of a proposed answer.

Each conflict has one target, so the same exact conflict is not repeated in several target splits. All conflicts nevertheless share a deliberate numeric business-rule/FAQ pattern. A classifier may exploit this; use broader source patterns and authentic anonymized cases before drawing generalization conclusions.

## Time and history

The active source snapshot is 2026-08-28. Historical tickets completed between March and August 2026; 1.0 pilot work precedes launch, and 1.1 work precedes the multi-lab release. Target snapshots are September through early November 2026 and all precede the dataset cutoff. The history retrieval unit includes completion comments and becomes available only at resolved_at. Earlier releases remain historical evidence, not superior source authority. No target answer is inserted into a future ticket comment or indexed as retrieval context.

Historical requests alternate between underspecified and explicit originals. Their accepted completion comments are legitimate project evidence. The 200 target requests use ongoing workflow statuses independently of quality category; none is presented as a completed historical task. The model must not infer a ground-truth category from a status field.

## Splits and leakage

{SPLIT_NOTES}

Sharing source policies and historical context is intentional in a RAG feature-holdout setting. Target paraphrases and siblings stay within one area partition. Documents, passage IDs, and historical facts are not held out from retrieval. The resulting scores do not establish cross-project generalization: all partitions use the same fictional university, source style, stack, and generator. Combine this part with project-disjoint team datasets for that question, and check overlap before concatenating examples.

Only `retrieval/chunks.jsonl` is the recommended search index. `review/`, `source/`, `knowledge-registry.md`, SFT assistant messages, and split golden/label files are hidden supervision. Even oracle user context selects passages using the answer key, so oracle SFT accuracy must be reported separately from retrieval-plus-review accuracy. Oracle context contains same-area history as distractors as well as supporting passages.

## Difficulty and metrics

L1 describes already-clear narrow work or a single-source resolved rule. L2 covers local multi-source rules, explicit and implicit gaps, partial decisions, and same-scope conflicts. L3 is reserved for explicitly authored cross-area rule composition. These are heuristic tags and do not claim measured human difficulty.

Report category macro-F1, false-resolved rate on unresolved/conflicting cases, unnecessary-question rate on resolved/already-clear cases, missing-decision coverage, citation validity, and unsupported-rule rate. For retrieval, report Recall@k against the authored qrels and inspect false negatives manually because qrels are not exhaustive. Exact question wording is not a required match; judge the decision being requested. Sample outputs across areas and classes, not just overall accuracy.

## Independent semantic review checklist

- Confirm every cited passage actually supports the recommendation in the target's scope.
- Search all docs and completed comments for purportedly missing decisions; a topical quote is insufficient.
- Verify that each conflict concerns the same actors, release, operation, and time boundary.
- Check that partial answers neither ask again about a known rule nor silently choose a new exception.
- Accept narrow complete requests without requiring unrelated product details.
- Confirm that history contains no later resolution of a target's open decision.
- Add lexical variation, nonnumeric conflicts, obsolete sources, mixed-quality multi-decision tickets, and independent reviewer judgements before treating the set as a benchmark.
'''


def examples(tickets, golden):
    lines = ['# ToolNest worked examples — hidden supervision', '',
             'Do not index this file for retrieval. These examples are existing targets, not additional records.']
    for category in CATEGORIES:
        i = next(i for i, g in enumerate(golden) if g['category'] == category)
        t, g = tickets[i], golden[i]
        lines += ['', f'## {category}: {t["ticket_id"]}', '', f'**{t["summary"]}**', '',
                  t['description'], '', g['recommendation'], '']
        lines += [f'- Question: {q}' for q in g['expected_questions']]
        lines += [f'- `{e["source_id"]}`: {e["exact_quote"]}' for e in g['evidence']]
    return '\n'.join(lines)


if __name__ == '__main__':
    main()
