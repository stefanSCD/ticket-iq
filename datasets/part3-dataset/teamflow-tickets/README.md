# TeamFlow tickets

200 synthetic Jira tickets, expected answers and review exports.

- `tickets.jsonl`: model input, no golden answers.
- `ticket_labels.jsonl`: classification and difficulty level (not model input).
- `golden_answers.jsonl`: the full expected answer and evidence (not model input).
- `TeamFlow_Jira_import_no_golden.csv`: CSV for Jira import (verify field mapping with your Jira instance).
- `TeamFlow_200_tickets_with_golden.json`: original combined dataset with metadata.
- `TeamFlow_200_tickets_review.csv`, `.xlsx`: reviewer-friendly formats.

Distribution: 60 resolved, 60 unresolved, 40 partially resolved, 20 conflicting, 20 already clear.
Synthetic dataset: human semantic review is needed before training or final evaluation.
For evidence indexing use [the source Markdown documentation](../teamflow-docs/TeamFlow_Project_Documentation_100_pages.md). Keep `knowledge-registry.md` and all golden/review files outside the retrieval index and agent input; they contain evaluation guidance and intentionally conflicting source references.
