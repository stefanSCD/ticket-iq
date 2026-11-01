#!/usr/bin/env python3
"""Check TicketIQ synthetic artifact integrity. Run from dataset root."""
import json, hashlib, collections, sys
from pathlib import Path

root=Path(__file__).resolve().parent.parent if Path(__file__).resolve().parent.name=='scripts' else Path.cwd()
def rows(path):return [json.loads(line) for line in (root/path).read_text(encoding='utf8').splitlines() if line.strip()]
def unique(records,key):
    ids=[x[key] for x in records]
    assert len(ids)==len(set(ids)), f'duplicate {key}'

docs=rows('global/documents.jsonl'); tickets=rows('global/tickets.jsonl'); anns=rows('global/decisions.jsonl'); sft=rows('global/sft_examples.jsonl')
chunks=rows('retrieval/structured_chunks.jsonl'); flat=rows('retrieval/flat_chunks.jsonl'); labels=rows('global/ticket_labels.jsonl')
unique(docs,'doc_id');unique(tickets,'ticket_id');unique(labels,'ticket_id');unique(anns,'annotation_id');unique(chunks,'chunk_id');unique(sft,'example_id')
assert len(docs)==285, len(docs)
assert len(tickets)==500, len(tickets)
assert len(anns)==900, len(anns)
assert len(sft)==500, len(sft)
assert len(chunks)==len(flat)
assert collections.Counter(t['project_id'] for t in tickets)=={k:100 for k in ['shopflow','carequeue','ledgercloud','learnspace','parcelroute']}
assert collections.Counter(t['class'] for t in labels)=={'resolved':150,'unresolved':150,'partially_resolved':100,'already_clear':50,'conflicting':50}
md={x['doc_id']:x for x in docs}; tm={x['ticket_id']:x for x in tickets}; aid={x['annotation_id']:x for x in anns}
for d in docs:
    p=root/d['source_path']; assert p.is_file(),p
    content=p.read_text(encoding='utf8')
    assert hashlib.sha256(content.encode()).hexdigest()==d['sha256'],d['doc_id']
    assert len(content.split())==d['word_count']
for t in tickets:
    assert all(a in aid for a in t['annotation_ids']),t['ticket_id']
    assert all(aid[a]['ticket_id']==t['ticket_id'] for a in t['annotation_ids'])
    assert 'ground_truth_ticket_class' not in t and not any(x in ['resolved','unresolved','conflicting','partially_resolved','already_clear'] for x in t['labels'])
    if next(l['class'] for l in labels if l['ticket_id']==t['ticket_id'])=='already_clear':assert not t['annotation_ids']
    else: assert len(t['annotation_ids'])==2
for a in anns:
    assert a['ticket_id'] in tm and a['project_id']==tm[a['ticket_id']]['project_id']
    assert a['should_ask']==(a['status']!='resolved')
    assert (a['suggested_clarification'] is not None)==a['should_ask']
    if a['status']=='conflicting':assert len(a['evidence'])==2
    if a['status']=='unresolved':assert not a['evidence']
    for e in a['evidence']:
        assert e['doc_id'] in md
        d=md[e['doc_id']]; assert d['project_id']==a['project_id']
        assert e['quote'] in (root/d['source_path']).read_text(encoding='utf8'),(a['annotation_id'],e)
splits={'train':{'shopflow','ledgercloud','parcelroute'},'validation':{'carequeue'},'test':{'learnspace'}}
for split,projects in splits.items():
    for kind,allrows,key in [('tickets',tickets,'ticket_id'),('decisions',anns,'annotation_id'),('sft',sft,'example_id')]:
        file=rows(f'splits/{split}_{kind}.jsonl')
        assert {x[key] for x in file}=={x[key] for x in allrows if x['project_id'] in projects}
for x in sft:
    assert x['example_id'] in tm
    assert x['split'] == next(name for name,ps in splits.items() if x['project_id'] in ps)
    assert all(d['status'] in {'resolved','unresolved','partially_resolved','conflicting'} for d in x['output']['decisions'])
for c,f in zip(chunks,flat):
    assert c['chunk_id']==f['chunk_id'] and c['text']==f['text'] and c['project_id']==f['project_id']
    assert c['doc_id'] in md and c['project_id']==md[c['doc_id']]['project_id']
for proj in {d['project_id'] for d in docs}:
    flattext=(root/'projects'/proj/'flat'/'all_project_docs.md').read_text(encoding='utf8')
    for d in docs:
        if d['project_id']==proj:assert (root/d['source_path']).read_text(encoding='utf8') in flattext
print('PASSED: 5 projects, 285 source docs, 500 tickets, 900 decisions, SFT splits, evidence and chunk alignment.')
