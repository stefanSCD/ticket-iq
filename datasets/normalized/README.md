# Normalized TicketIQ datasets


From the repository root:

```sh
python scripts/normalize_datasets.py
python -m unittest discover -s tests -p "test_normalize_datasets.py"
```

The script also accepts `--datasets-root PATH` and `--output PATH`. Paths default to this repository regardless of the current working directory. PCON and TeamFlow must already be extracted; the script finds their source files recursively and rejects ambiguous duplicate copies.

## Output files

| File | Records | Usage |
|---|---:|---|
| `documents.jsonl` | 590 | Documentation for retrieval: 285 part 1 documents, 100 PCON pages, 100 TeamFlow sections, 105 ToolNest documents. |
| `tickets.jsonl` | 1,100 | Input-only review targets: 500 / 200 / 200 / 200 by dataset. Do not index as historical context. |
| `history_tickets.jsonl` | 40 | Completed ToolNest tickets, including accepted completion comments, for historical retrieval. Same schema as target tickets. |
| `golden.jsonl` | 1,100 | Evaluation only: categories, questions, evidence, decisions, and existing splits. Never index or include as agent input. |
| `manifest.json` | — | Counts, field lists, source/output hashes, validation warnings, and limitations. |

All rows include `dataset_id`, `project_id`, and `source_path`. Source paths are relative to `datasets/`. IDs retain their original spelling; use `(dataset_id, project_id, ticket_id)` or `(dataset_id, project_id, doc_id)` as the lookup key. Filter by project during retrieval.

## Canonical fields

- **`title`** replaces ticket `summary`; documents also use `title`.
- **`label`** is always a list of ordinary ticket labels, replacing `labels` and `jira_labels`. It does not contain evaluation categories.
- **`doc_id`** identifies documents and evidence references, replacing `document_id` and `document_section`. **`passage_id`** preserves finer-grained source identifiers when supplied; a passage and its parent document are different entities.
- **`category`** is used only in golden records and their decision annotations. Values are `resolved_by_documentation`, `unresolved`, `partially_resolved`, `conflicting_documentation`, and `already_clear`. Original `resolved` and `conflicting` map to the longer names. These categories are not Jira workflow status.
- **`document_type`** retains source documentation classifications (for example `business_rules` or `BR`); these are not readiness categories.
- Missing scalar values remain `null`; missing lists are `[]`. No dates, decisions, exact quotations, or train/test assignments are invented.

Ticket rows share a single schema, including optional story, acceptance criteria, workflow fields, timestamps, and comments. Document rows share a single schema containing text, title, source metadata, and optional passages. The original TeamFlow preamble is retained in `context`, and its 100 logical sections become separate documents; PDF/DOCX copies are not ingested again.

Golden evidence always has `{doc_id, passage_id, quote}`. PCON provides relevant pages and an explanatory string rather than exact quotations: its `quote` values remain `null`, and the original explanation is stored in `evidence_summary`. References to its hidden registry stay in `registry_refs` for review only. They are never retrieval documents. PCON does not explicitly identify conflict pairs; these are not inferred from its page lists.

Part 1's 900 individual decision annotations remain in `decisions`; ticket-level evidence and expected questions are aggregated without discarding those annotations. Other datasets leave `decisions` empty. Source-provided reasoning/recommendations use `rationale`; missing reasoning is not generated.

## Evaluation and retrieval boundaries

Part 1 retains its project-based splits; ToolNest retains its feature-group splits. PCON and TeamFlow have `split: null` until the team defines suitable partitions. The combined counts are 400 train, 160 validation, 140 test, and 400 unassigned. Do not treat this mixed split as a single cross-project benchmark without defining an evaluation protocol.

Read history comments along with the original historical request when constructing retrieval text. Exclude review targets and all golden records from that corpus. Index one representation of each source; prebuilt chunks and alternate exports are not copied into this normalized collection. Chunk the normalized sources with the chosen common strategy and derive retrieval judgments from golden evidence as needed.

`effective_at`, `updated_at`, `published_at`, and `available_at` are distinct. Only ToolNest documents supply an explicit publication date used as `available_at`; other unknown availability dates remain null. Do not infer publication from an effective date or silently apply temporal filtering to datasets without sufficient metadata. Use ToolNest history's `resolved_at` and comment dates when enforcing its snapshot boundary.

The converter validates uniform fields, duplicate IDs, target/golden correspondence, existing split coverage, and evidence references within each project. It reports nonmatching source quotations without changing them. It validates all data before writing outputs and produces deterministic JSONL files. Tests also check leakage boundaries and repeatability. Structural validation does not establish semantic correctness of synthetic labels; human review is still required.

Edit original sources and regenerate instead of editing the generated JSONL files.
