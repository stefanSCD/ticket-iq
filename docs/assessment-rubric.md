# TicketIQ Assessment Rubric v1

This is the shared decision policy for Agent, frontend behavior, and evaluation. Assess only the requested ticket scope using the reviewed ticket version, eligible retrieved evidence, and recorded author decisions. Do not add unrelated product features to make a ticket look more complete.

## Verdicts and precedence

| Verdict | Decision rule | Example | Workflow |
|---|---|---|---|
| `ready` | No known implementation-blocking decision remains, and the evidence needed for this scoped assessment is available. Rules may already be explicit in the ticket or resolved by sources/author messages. | Cancellation eligibility is documented and the author has chosen the notification channel. | `proposal_ready` if a grounded change is needed and editable; otherwise `complete` if no change is needed. |
| `needs_clarification` | The agent can identify at least one concrete blocking decision for the author, without guessing the missing answer. | The notification channel is unspecified, or two active rules conflict. | `awaiting_clarification`; no approvable proposal. |
| `insufficient_evidence` | A material evidence gap prevents a defensible assessment of the requested scope. It is not merely an identified product decision awaiting an answer. | The ticket refers to an inaccessible specification containing the behavior to implement. | `blocked`; explain the gap and allow repair/reanalysis when no save guard applies. |

A material evidence gap takes precedence over known open decisions: return `insufficient_evidence`, retain any useful questions, and state what evidence is missing. Otherwise concrete open decisions yield `needs_clarification`; only their absence permits `ready`. `blocking_reasons` is empty for `ready`; use `open_decision` and/or `conflicting_evidence` for clarification, and `missing_required_context` for insufficient evidence (additional known decision reasons may coexist).

An empty successful search does not prove absence everywhere. If the ticket itself identifies a concrete missing decision, ask it; if the task cannot be assessed without an unavailable referenced source, abstain. A narrow self-contained ticket can be ready without retrieval. Missing edit permission affects saving, not readiness. A transport/storage/model failure is a failed run (`failed`, with an error), not a fabricated assessment or a successful empty search. Retain the prior assessment, if any, as prior evidence; do not present it as a fresh result.

## Evidence and questions

Agent persists cited evidence before publishing an assessment. `assessment.citation_ids` contains the union of supporting and conflicting retrieved evidence used in the assessment, including every question's `citation_ids`. `assessment.author_message_ids` identifies owner-authored decisions used in it. Both are unique lists scoped to the session. An empty list is valid when the ticket itself establishes the relevant facts or the question concerns an undocumented decision; never invent a citation for absence.

Each question references its supporting/conflicting citations. For a documented conflict, include both sides and explain the incompatible statements. A missing decision may have no citations. Evidence references support an explanation; a numerical similarity score does not establish a requirement's truth.

Answers are appended as messages, then the agent reassesses. `answered` means a response was recorded, not that the response resolved the decision. An ambiguous response generates a focused follow-up question with a new ID; retain the old question/answer in the transcript. Stable open questions may retain their IDs across reassessment when their meaning is unchanged. Superseded question IDs cannot accept new answers. Explicit later decisions replace earlier ones in the current assessment while preserving the audit trail.

## Proposal and action policy

V1 does not offer partial proposals for saving. While blockers remain, show the assessment and questions; any partial draft is internal and cannot become `current_proposal_id`. A proposal is offered only after a `ready` assessment, no open questions, valid provenance for all changes, and matching edit capabilities. A ready assessment needing edits that cannot be made results in `blocked`, with an actionable explanation. Existing proposal snapshots remain readable for audit but are invalidated when no longer current.

Approval requires the current ready assessment, the exact current proposal, and all existing version/access/save guards. A new substantive message or revision invalidates the old unsaved proposal and enters `analyzing`; reassessment may return any verdict. `ready` does not itself approve a write. After a save, `updated` means verified saving; it is distinct from readiness.

For `awaiting_clarification`, allow answers/comments and reanalysis, but not approval or proposal revision. For evidence-related `blocked`, allow comments supplying explicit decisions or explaining restored access and allow reanalysis; supplied URLs are not automatically fetched or trusted. For `proposal_ready`, allow messages, revisions, approval, and reanalysis subject to backend guards. During `analyzing`, disable mutating conversation actions until the current result commits. Save guards and reconciliation rules take precedence over this table.

## Evaluation protocol

Evaluate the initial assessment against the golden reference before supplying simulated author answers. Golden questions and answers are never agent inputs. Map `resolved_by_documentation` and `already_clear` to `ready`; map the other three categories to `needs_clarification`. Report by dataset and preserve the agreed held-out partitions. Conversational completion, approvals, and saves are measured separately by scripted scenarios.

Use macro-F1 over the two gold classes as the primary readiness F1, reporting each class's precision/recall/F1 too. For class c, compute `2*TP_c / (2*TP_c + FP_c + FN_c)`; an `insufficient_evidence` prediction contributes a false negative to its gold class and no true positive to either class. Never drop abstentions from the primary denominator. Report zero for an undefined class F1, and show class support. Operational failures likewise count as missed gold-class predictions in the end-to-end score and are reported separately from model abstention.

Also report abstention rate, operational failure rate, coverage (the fraction with a `ready` or `needs_clarification` prediction), a two-gold-class by four-outcome confusion table (ready/clarification/abstention/failure), and conditional F1 on covered examples with its sample count. If coverage is zero, conditional F1 is N/A. This prevents a model from improving its primary score by abstaining on difficult examples.

Freeze clarification-topic judgments and citation checks before comparing models. Count questions about already documented/explicit decisions as unnecessary. Score required clarification-topic recall against golden topics, not exact wording. Validate citation identity, exact quotation, source eligibility, and semantic support separately; report retrieval Recall@k against available reference evidence, acknowledging that those judgments may be incomplete. Keep prompts, retrieval generation/profile, tool budgets, and evaluation examples fixed for baseline versus fine-tuned comparisons.
