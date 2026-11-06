# ToolNest generation and evaluation methodology

## Goal and scope

The task is to decide whether the requested implementation has sufficient requirements, using the target text, active project sources, and completed history. A ticket can omit a detail that is already specified elsewhere. Ask only if a material decision remains genuinely open; do not invent a default or expand a complete small task.

Twenty feature families contain ten authored scenarios each: three resolved, three unresolved, two partial, one conflict, and one already clear. Ticket order, people, priorities, dates, and ongoing workflow statuses are shuffled with seed 41106. Ticket descriptions and expected reviews are authored individually; the builder does not call an external model. This produces controlled coverage rather than a natural prevalence estimate.

Five short source documents per family cover rules, workflow, API, architecture, and FAQ; five shared documents describe product scope, architecture, chronology, calendars, and readiness. Passage IDs are stable and exact quotes are mechanically verified. No claim is made that these are formatted pages. Fictional API behavior is a project contract, not a claim about third-party software.

## Decision design

Resolved examples require applying a specified rule to a sparse request. Unresolved examples introduce an exception or new behavior whose implementation policy is absent. The first unresolved case per family explicitly mentions an open decision in the docs; the other gaps are implicit. Partial examples combine an established constraint and an undecided design dimension. Conflicts pair incompatible active rules for the same scope; neither publication date nor document family resolves them. Already-clear cases describe a limited presentation, documentation, or test change with an observable check.

Evidence for an unresolved case is topical context, **not proof of absence**. `review/decision_audit.jsonl` lists the full reviewed corpus scope and whether the gap is explicit or implicit. Its status states that this is generator-author review only. Independently review all other files and historical comments before trusting an absence label. Automated citation validity does not prove semantic correctness, necessity of a question, or completeness of a proposed answer.

Each conflict has one target, so the same exact conflict is not repeated in several target splits. All conflicts nevertheless share a deliberate numeric business-rule/FAQ pattern. A classifier may exploit this; use broader source patterns and authentic anonymized cases before drawing generalization conclusions.

## Time and history

The active source snapshot is 2026-08-28. Historical tickets completed between March and August 2026; 1.0 pilot work precedes launch, and 1.1 work precedes the multi-lab release. Target snapshots are September through early November 2026 and all precede the dataset cutoff. The history retrieval unit includes completion comments and becomes available only at resolved_at. Earlier releases remain historical evidence, not superior source authority. No target answer is inserted into a future ticket comment or indexed as retrieval context.

Historical requests alternate between underspecified and explicit originals. Their accepted completion comments are legitimate project evidence. The 200 target requests use ongoing workflow statuses independently of quality category; none is presented as a completed historical task. The model must not infer a ground-truth category from a status field.

## Splits and leakage

Train/validation/test are 100/60/40 target tickets, grouped by product area. Related booking, maintenance, and kit cases stay in train; checkout, identity, and integration cases stay in validation; return, overdue, audit, and reporting cases stay in test. Audit cases may cite shared incident-access source rules from the training documentation. All project docs and pre-cutoff completed history may be indexed at evaluation time. This is a within-project feature holdout, not an unseen-project benchmark.

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
