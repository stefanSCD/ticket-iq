# ToolNest — TicketIQ part 4

An entirely fictional university equipment-lending project for evidence-grounded Jira ticket review. All policies, people, institutions, incidents, and completed work are synthetic. Language: English. Dataset version: 1.0. Snapshot cutoff: 2026-11-06T12:00:00Z.

The active product lends cameras, laptops, lab tools, and kits. It launched as a single-lab pilot and grew into a multi-lab service. The fictional stack is React/TypeScript, FastAPI, PostgreSQL, Redis, background workers, and private object storage. This dataset contains documentation and ticket artifacts, not an implementation of that application.

## Contents

- **105 substantive Markdown source sections**, 13,283 whitespace-delimited words, covering 20 product areas plus 5 shared project documents. These are sections/files, not 105 rendered pages.
- **200 ongoing review targets**, with To Do, In Progress, Blocked, or In Review workflow status.
- **40 completed historical tickets**, including original requests and accepted completion comments. Half start with deliberately underspecified requests and half with explicit requests. Completion notes resolve their recorded scope.
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
toolnest-docs.zip              convenience copy of source docs
toolnest-tickets.zip           convenience copy of inputs, history, and SEPARATE keys
```

**Retrieval:** index `retrieval/chunks.jsonl` with `project_id=toolnest`. Do not also index loose Markdown or the archived copies. Enforce `available_at <= ticket.snapshot_at`. Only the 40 completed history tickets belong in the prebuilt corpus; the review targets do not. All recorded source publication and history completion dates precede every target snapshot. Historical outcomes do not override active release rules.

**Fine-tuning:** use `splits/train_sft.jsonl`; reserve validation and test files for evaluation. SFT user messages include selected oracle documentation excerpts and the two same-area completed tickets. The assistant message is the expected review. This tests evidence use with supplied context, not retrieval quality. For end-to-end evaluation, retrieve context yourself and keep all labels and completions hidden.

**Splits:** Train/validation/test are 100/60/40 target tickets, grouped by product area. Related booking, maintenance, and kit cases stay in train; checkout, identity, and integration cases stay in validation; return, overdue, audit, and reporting cases stay in test. Audit cases may cite shared incident-access source rules from the training documentation. All project docs and pre-cutoff completed history may be indexed at evaluation time. This is a within-project feature holdout, not an unseen-project benchmark.

**Jira CSV:** these are Jira-style exports with explicit columns. Map columns in your importer; an import into a real Jira instance has not been tested. Labels are JSON arrays in the CSV. The input CSV has no golden answers.

## Reproduce and validate

From this directory:

```sh
python3 scripts/build_dataset.py
python3 scripts/validate_dataset.py
```

Both scripts use only the Python standard library. Generation is deterministic, including archive timestamps. Edit `source/` and rebuild rather than editing generated copies. The validator checks counts, schemas, citations and exact quotes, temporal availability, split membership, question/category rules, input/key separation, archive boundaries, and file hashes.

## Review before research use

The data is handcrafted synthetic content assembled by a deterministic builder. It has no independent human semantic review. The 20 deliberate conflicts use numeric policy boundaries and the same business-rule/FAQ pairing, and several readiness patterns repeat. These regularities can make classification easier than real Jira review. Qrels are authored support sets, not exhaustive relevance judgements. Difficulty tiers are heuristic, not human-calibrated. See `methodology.md` for evaluation limits and the semantic review checklist.
