# Methodology and quality caveats

## Annotation unit

Ground truth contains a ticket-level stratum and individual question-level decisions. Ticket status is not the same as issue workflow status. A single ticket can contain several decisions with different statuses. Resolved decisions cite exact normative wording; incomplete decisions cite their known partial wording; conflict decisions cite both incompatible active values; unresolved decisions have no positive quote.

## Retrieval versus evidence verification

Use oracle excerpts to test the SLM decision behavior separately from retrieval. Next compare actual structured or flat chunks with the oracle; calculate Recall@k only where a positive relevant evidence excerpt exists. An unresolved example has no positive document, so focus on false positive citations instead. Don't claim that a negative result proves complete absence in a real organization.

## Limits of generated examples

Templates, repeated architecture patterns and explicit numeric contradictions make shortcuts possible. Distribution is balanced by design, unlike production Jira data. Some documents may be repetitive; editorial review and iterative rewriting are recommended. The corpus is synthetically consistent by construction except planted conflicts, but there is no formal semantics engine proving every negative example. Questions are curated from domain facts during generation, not independently supplied by product owners.

## Verification

The validator checks unique IDs, project ownership, source file existence, SHA-256 integrity, exact quote substrings, split isolation, expected class distribution, and consistency of structured versus flat text. It cannot prove the semantically correct label on every synthetic ticket.

## Suggested future extension

Add multi-hop examples where two different docs jointly resolve a decision, conflicting dated/archived docs, code-awareness, stakeholder answers, edited ticket versions, realistic incomplete acceptance criteria, and blinded annotation by independent reviewers.
