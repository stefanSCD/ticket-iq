# PCON tickets (200)

| File | Content |
|---|---|
| pcon_tickets.jsonl | All tickets with labels (one JSON per line) |
| pcon_tickets_labeled.csv | Same, as CSV (lists joined with " | ") |
| pcon_tickets_input.csv | Only what the SLM sees: id, type, summary, description, component, priority, reporter, created, labels |

Distribution: resolved 60, unresolved 60, partially_resolved 40, conflicting 20, already_clear 20.

Label fields:
- `category` – one of the five classes
- `registry_refs` – items in `_meta/knowledge-registry.md` (R-/U-/P-/C-)
- `relevant_pages` – pages a retriever should find (PC-xxx)
- `expected_behavior` – what the SLM should do
- `expected_questions` – the questions the SLM should ask (empty for resolved / already_clear)
- `evidence` – what the documentation already answers

Every U-, P- and C-item in the registry is covered by at least one ticket. Ticket order is shuffled (seed 42).
