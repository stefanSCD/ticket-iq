# TicketIQ synthetic dataset v1.0

Generated: 2026-10-28. Language: English. **Every project, ticket, policy and document is fictional and generated. No Jira/Confluence customer data and no independent expert annotations.**

## Coverage

- 5 projects: ShopFlow (e-commerce), CareQueue (healthcare appointments — scheduling only), LedgerCloud (invoicing), LearnSpace (university LMS), ParcelRoute (delivery logistics).
- 285 Markdown documentation files, 67,286 words total (approximately 168 page-equivalents at 400 words/page; not actual formatted pages).
- 500 Jira-like tickets, 100 per project; 900 grounded decision-level annotations; 500 ticket-level SFT examples; 1990 searchable chunks.
- Categories: `functional`, `business_rules`, `api_specs`, `faq`, `architecture_decisions`, plus project-level `overview`, `security`, `integration`, `non_functional`, `runbooks`, `governance`, `testing`.
- Ticket distribution: {'resolved': 150, 'unresolved': 150, 'partially_resolved': 100, 'already_clear': 50, 'conflicting': 50}.

## Structure

```text
ticketiq_synthetic_v1/
  projects/<project>/structured/<category>/*.md
  projects/<project>/flat/all_project_docs.md
  projects/<project>/tickets.jsonl
  projects/<project>/annotations.jsonl
  global/documents.jsonl
  global/tickets.jsonl
  global/ticket_labels.jsonl       # separate from the model input
  global/decisions.jsonl
  global/sft_examples.jsonl
  global/ticket_summary.csv
  examples.md                       # 5 worked examples, not RAG content
  retrieval/structured_chunks.jsonl
  retrieval/flat_chunks.jsonl
  retrieval/qrels.jsonl             # annotation-to-evidence ground truth
  splits/{train,validation,test}_{tickets,decisions,sft,chatml}.jsonl
  scripts/validate_dataset.py
  manifest.json, schema.json, methodology.md
```

## How to use

**RAG:** embed `retrieval/structured_chunks.jsonl` into a vector store with a strict `project_id` filter. Search additional tickets using `global/tickets.jsonl`, excluding the target ticket. Use source IDs in `global/documents.jsonl` for citations. For metadata-ablation experiments use `flat_chunks.jsonl` instead. Its text and chunk IDs are identical to structured chunks, but category and source-path metadata are stripped. The flattened Markdown file is for browsing; do not index both document representations at once.

**Leakage protection:** ground-truth ticket classes are stored in `global/ticket_labels.jsonl` and omitted from the Jira-like ticket records and their ordinary labels. Do not concatenate the annotation files into retrieval corpora.

**Fine-tuning:** train a small instruction model using `splits/train_sft.jsonl` (each input includes ticket and **oracle evidence excerpts**, output is the expected decision list). `validation_sft.jsonl` and `test_sft.jsonl` are held out. For an end-to-end RAG evaluation, replace oracle excerpts with actual retrieval results. This cleanly separates evidence verification from search quality. Documentation pages are **RAG context**, not facts to memorize in weights.

**Project-level split:** Train = ShopFlow, LedgerCloud, ParcelRoute (300 tickets); Validation = CareQueue (100); Test = LearnSpace (100). The held-out project's docs may be indexed at evaluation time, while the labels and completions remain hidden from training.

**Metrics:** Retrieval Recall@k, citation exactness, decision macro-F1, false-resolved rate, unnecessary-question rate and unresolved-decision recall. Reports should include results by project/class, not just overall accuracy.

## Ground-truth design

- `resolved`: ticket leaves a rule implicit but the business document answers it. No clarification question required for that decision.
- `unresolved`: an important feature-specific boundary has no specified answer in the generated corpus. Asking is appropriate.
- `partially_resolved`: a FAQ discusses safe recovery but lacks a requested quantitative or process boundary.
- `conflicting`: the business-rules page and FAQ contain intentionally incompatible **active** statements. Both exact quotes are cited, and the intended rule cannot be safely inferred.
- `already_clear`: a deliberately narrow ticket explicitly quotes the rule being ported, so zero outstanding decisions are annotated.

**Limitations:** controlled templates repeat across projects, conflicts are deliberately engineered, and the same writing voice appears everywhere. Labels are generator-defined (not verified by a product owner). Great for an initial technical pipeline or controlled comparison, **not a standalone scientific benchmark for real-world generalization**. Have a human requirements engineer review samples and introduce authentic anonymized examples before making strong research claims.

Run `python3 scripts/validate_dataset.py` from the dataset root to verify counts, links and evidence excerpts.

## Additional exports

`retrieval/qrels.jsonl` maps questions to evidence document IDs and relevant chunk IDs, enabling retrieval evaluation. `splits/*_chatml.jsonl` offers ready-to-use chat-message fine-tuning records. `examples.md` gives five annotated sample tickets; never put qrels, examples or labels into the retrieval corpus.
