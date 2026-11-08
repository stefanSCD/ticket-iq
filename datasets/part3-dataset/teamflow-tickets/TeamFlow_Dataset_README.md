# TeamFlow — 200 Synthetic Jira Tickets + Golden Answers

Based on the TeamFlow 100-page synthetic documentation (v1.0).

## Dataset distribution

| Category | Count | Purpose |
|---|---:|---|
| resolved_by_documentation | 60 | Agent finds rule; no questions |
| unresolved | 60 | Agent asks for a missing decision |
| partially_resolved | 40 | Agent uses known rule and asks only about remaining gap |
| conflicting_documentation | 20 | Agent identifies contradictory source references and requests arbitration |
| already_clear | 20 | Ticket fully specifies requested change; no questions |

## What do 'labels' and 'levels' mean?

- Jira labels: `teamflow`, `synthetic`, and `area-...` are non-answer topic labels for filtering.
- Difficulty level (in golden dataset only): `L1` simple, `L2` moderate, `L3` complex.
- Golden category: the five target behaviors above; this is *not* a difficulty level.

## Files

- `TeamFlow_200_tickets_with_golden.json`: canonical dataset. Each ticket has category, reference IDs, exact excerpts, level, correct questions, explanation.
- `TeamFlow_200_tickets_review.csv`: spreadsheet-friendly export **with** golden fields; never use as raw agent input.
- `TeamFlow_Jira_import_no_golden.csv`: input-only CSV without golden labels. Map fields in the Jira CSV importer; label separators may need adjustment according to your Jira setup.
- `TeamFlow_200_tickets_levels.xlsx`: review workbook (summary, searchable ticket table, conflicts).
- `TeamFlow_Project_Documentation_100_pages.md`: source text held separately from ground truth.

## Source fidelity

Each cited evidence ID appears in the source corpus. Five verified contradictions are reused in four separate application scenarios each: BR-03-R06 vs GL-06-R05, BR-15-R03 vs FAQ-02-Q4, BR-21-R04 vs FAQ-03-Q2, BR-29-R03 vs FAQ-04-Q3, BR-10-R02 vs BR-28-R03. These 20 tickets should not be treated as 20 independent documentation contradictions.

## Quality controls performed

Count check (60/60/40/20/20); no repeated summaries; valid referenced source IDs; golden questions present only where required. This is a synthetic baseline, **not** a human-adjudicated golden benchmark. Review ambiguous cases and identify accidental matches elsewhere in the corpus before training/evaluation.

## Evaluation recommendation

Train and test splits must not leak question answers: do not show `golden.*` or category/level in the agent prompt. Split by underlying decision/topic (especially all four tickets for each contradiction) rather than random per-row split to avoid near-duplicate leakage.
