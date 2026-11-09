# Frontend ↔ Agent Contract

**Version:** 1.0.0 · **Status:** implementation contract · **Date:** 2026-11-09

The frontend uses Agent's application HTTP API to review a ticket, answer questions, inspect evidence, request revisions, and explicitly approve a proposal for saving. Agent owns conversation state, authenticated identity, model orchestration, proposals, approvals, and jobs. The browser never calls MCP, RAG, or Jira directly.

See [JSON Schema](contract.schema.json), [examples](examples.json), [Agent ↔ MCP](../agent-mcp/README.md), [approval records](../mcp-agent-approvals/README.md), and the [workflow example](../../../docs/workflow-example.md). These files define payloads and behavior; they do not implement endpoints, authentication, workers, or UI.

## 1. API and Browser Session

Use `/api/v1` on the frontend's origin, routed to Agent by deployment configuration. The frontend may be a separate container behind this route. Use an authenticated browser session; the backend derives the user from that session. It never trusts a submitted author/user ID. Login/provider integration is outside this contract; a local demo can bind a configured demo author on the backend only.

The bootstrap response provides a session-bound CSRF token. All POST requests send it as `X-CSRF-Token`; Agent also validates the request origin. Browser session cookies must be protected from script access and use secure transport in non-local deployments. Internal service credentials and Jira tokens are never returned to the browser.

`GET /bootstrap` returns the authenticated user's display information and authorized project options. A `project_ref` is an opaque selection handle resolved by Agent to connection/project/RAG configuration. The initial v1 configuration supports up to 100 project options. Ticket selection is project selection plus entry of a Jira key/ID; this contract does not promise a Jira-wide issue-search endpoint.

Every session and nested resource is checked against the current user and project authorization. Unknown and inaccessible IDs share a 404 response. Authentication and authorization are checked before looking up idempotency receipts. Source text and model output are untrusted display content: render structured text/ADF safely, not as executable HTML.

## 2. Routes

All bodies/responses are JSON. POST bodies include `contract_version: "1.0"` and `command_id`. The table names definitions under `$defs` in the schema.

| Method and route, relative to `/api/v1` | Request | Success |
|---|---|---|
| `GET /bootstrap` | No body | 200 `BootstrapResponse` |
| `POST /sessions` | `CreateSessionRequest` | 202 `CommandReceipt` |
| `GET /sessions/{session_id}` | No body | 200 `SessionResponse` |
| `GET /sessions/{session_id}/messages?after=0&limit=50` | Validated query | 200 `MessagePage` |
| `POST /sessions/{session_id}/messages` | `MessageRequest` | 202 `CommandReceipt` |
| `GET /sessions/{session_id}/proposals/{proposal_id}` | No body | 200 `ProposalResponse` |
| `POST /sessions/{session_id}/revisions` | `RevisionRequest` | 202 `CommandReceipt` |
| `POST /sessions/{session_id}/approvals` | `ApproveRequest` | 202 `CommandReceipt` |
| `POST /sessions/{session_id}/approvals/{approval_id}/revoke` | `SessionCommand` | 200 `CommandReceipt` |
| `POST /sessions/{session_id}/reanalyze` | `SessionCommand` | 202 `CommandReceipt` |
| `GET /sessions/{session_id}/citations/{citation_id}` | No body | 200 `CitationResponse` |
| `GET /sessions/{session_id}/events?after=0&limit=100` | Validated query | 200 `EventPage` |

POST acceptance is not analysis completion or a successful ticket update. A receipt contains the accepted action, session ID/version, command ID, and `replayed`. The browser reads subsequent state through GET/events.

## 3. Commands, Concurrency, and Idempotency

The frontend generates a unique `command_id` per deliberate user action. Reuse the same ID and identical body when retrying after a timeout, double click, or lost response. Persist an in-flight command until its outcome can be recovered. Do not generate a fresh approval command on reconnect.

Agent stores a durable receipt keyed by authenticated user plus command ID, binding the method, route, and complete request body. The same command returns its original receipt with `replayed: true`; changed content/route returns `COMMAND_CONFLICT`. Do not enqueue a second job. V1 retains these bindings with the session/audit data and does not automatically expire them while the session remains accessible.

All POSTs except session creation include `expected_session_version`, the integer version of the snapshot the user acted on. Check existing identical command receipts **before** this version check so an accepted retry still succeeds after the session advances. Otherwise perform version/state checks and mutation atomically. A conflict returns `SESSION_VERSION_CONFLICT`; reload the session and let the user review its new state before creating a new action.

Commit the domain change, command receipt, relevant event(s), and any queued work atomically, using a durable outbox or equivalent. Do not hold a database transaction open during model/MCP calls. Agent increments session version for each committed UI-visible state change; multiple events from one transaction may share that version.

## 4. Session Snapshot and Conversation

Creating a session binds the authenticated author, `project_ref`, and target `ticket_selector`, then starts analysis. Agent resolves all MCP invocation context and snapshot/retrieval settings internally. The browser cannot submit corpus IDs, model settings, golden labels, service credentials, approval IDs to create, or write-operation IDs.

`SessionResponse.session` contains:

| Field | Purpose |
|---|---|
| `session_id`, `version`, `created_at`, `updated_at` | Identity and concurrency |
| `project`, `ticket_selector` | User-visible project and original selection |
| `state` | Workflow state below, not Jira workflow status |
| `ticket` | Current verified ticket view or null while loading |
| `assessment` | Readiness verdict, explanation, and questions, or null |
| `current_proposal_id` | Current proposal to load, or null |
| `save` | Public save/approval summary or null |
| `actions` | Server-computed booleans for send-message, revise, approve, revoke, and reanalyze |
| `last_error` | Sanitized asynchronous error or null |
| `last_event_sequence`, `last_message_sequence` | Consistent log cursors for refresh/reconnect |

`TicketView` projects the adapter's ID/key, title, original ADF description/criteria, criteria availability, status, labels, timestamp, and version. It excludes connection credentials and backend field mappings. The version remains an opaque string.

| State | Frontend behavior |
|---|---|
| `analyzing` | Show progress; await durable results |
| `awaiting_clarification` | Display open questions and accept answers |
| `proposal_ready` | Load and render the current proposal for review |
| `saving` | Show actual save stage; do not infer success from a pending request |
| `updated` | Verified update and successful approval-result recording completed |
| `complete` | Assessment complete with no proposed change; no ticket write occurred |
| `blocked` | Explain missing evidence, stale proposal, or unresolved write; use allowed actions |
| `failed` | Analysis/dependency failure; show recovery action if enabled |

Readiness values are `ready`, `needs_clarification`, and `insufficient_evidence`, corresponding to the milestone's display labels. Readiness and workflow state are separate: `ready` can still require reviewing a proposed clarification of the ticket. The frontend must not derive button permissions solely from a readiness verdict or enable an action the server forbids.

The [assessment rubric](../../../docs/assessment-rubric.md) is normative for verdicts, question handling, proposal eligibility, action availability, and evaluation. V1 exposes no approvable partial proposal: `proposal_ready` and approval require a ready assessment with no open questions and all backend guards satisfied. Evidence-related abstention uses `blocked`; dependency execution failures use `failed` rather than an invented verdict.

An assessment includes its ticket version and questions with stable IDs, text, state (`open`/`answered`), and answer-message reference. `MessageRequest` is either a `clarification_answer` with `question_id`, or a `comment` with no question ID. Text is 1–8,000 code points and cannot be whitespace-only. The server rejects answers to stale/closed questions. A comment such as “yes”, “approved”, or “go ahead” is still only a conversation message; it never authorizes saving.

Assessments also include unique `citation_ids`, `author_message_ids`, and `blocking_reasons` lists. Questions include unique `citation_ids`. Agent stores evidence before publishing references, and every question citation belongs to the assessment's citation list. Both sides of a documented conflict must be linked. An empty citation list is valid for a missing decision with no documentary evidence; it is not proof of global absence. The frontend loads `/citations/{citation_id}` and renders evidence next to the assessment/question before a proposal exists. Author-message IDs resolve in the session transcript. Do not require the user to reach proposal review to inspect conflicting evidence. Missing/revoked evidence must display as unavailable, never as an uncited assertion that the original source is still accessible.

Messages have IDs, per-session integer sequences, author role (`user`/`assistant`), a typed purpose, text, optional question reference, and creation time. Return them in ascending sequence order. Transcript messages are append-only; a new assessment may supersede question/proposal state, but must not rewrite the author's recorded answer. A substantive new message invalidates an obsolete unsaved proposal and schedules reassessment when the action is allowed.

## 5. Proposal Review and Evidence

`ProposalResponse` separates immutable `proposal` content from its current status (`current`, `superseded`, `approved`, `applied`, or `invalidated`). Only a current proposal whose session allows approval is approvable.

The immutable content includes `proposal_id`, creation time, the reviewed `ticket_version`, `base`, exact `changes`, complete `preview`, and requirement-level provenance. `base` and `preview` contain title, description ADF, and acceptance-criteria ADF. `preview` must equal `base` with only the supplied `changes` replaced. Omitted fields stay unchanged; explicit null clears a field. The stored mapping is internal and follows the approval contract.

The frontend renders before/after content and identifies removals/clears. Use the stored ADF rather than reconstructing the proposal from an assistant message. If the renderer cannot faithfully display a proposal's content, disable approval and report that limitation; never let the user approve unseen content. Field validation/edit capabilities are checked by the backend before offering approval.

V1 revisions are text requests through `/revisions`, bound to `proposal_id` and session version. When accepting a revision, Agent atomically appends the exact author text to the session transcript as a user message with kind `revision_request`, assigns its `message_id`, and retains the command and original proposal binding before scheduling reassessment. Replaying the command returns its existing receipt and does not append another message. The backend generates a new immutable proposal ID and supersedes the old proposal. Direct browser-supplied ADF replacements are not accepted by this endpoint. Neither revision requests nor clarifications save anything.

Each added or changed requirement contains human-readable text, affected fields, and sources referencing either a `citation_id` or the exact author-message `message_id`. Citation IDs must resolve inside this session. An author-message source must refer to an immutable message from the authenticated session owner, with kind `clarification_answer`, `revision_request`, or `comment`, whose actual text explicitly supports the requirement. A comment may record a decision without answering a pending question; its kind remains `comment`. Agent validates the message's ownership, kind, and supporting content before accepting it as provenance. Assistant messages and approval events are not requirement sources, and an ambiguous suggestion requires clarification rather than being treated as a decision.

The provenance discriminator is `kind: "citation"` with `citation_id`, or `kind: "author_message"` with `message_id`; it covers all three author message kinds above. Stored citation records also include `retrieval_profile_id`, preserving the RAG identity context.

When an author explicitly replaces an earlier decision, the new proposal cites the replacing message and retains both messages and the superseded proposal in the audit trail. Do not carry the old decision forward as support for the replacement. A request that conflicts with retrieved project rules must be surfaced for resolution; recording its provenance does not silently override those rules. Existing unchanged ticket content remains represented by the proposal's `base` and `ticket_version`; it does not need a fabricated author message. Every added or changed requirement must have supporting provenance before the proposal is offered for approval.

For example, a revision saying “Use SMS instead of email for the cancellation notification” is stored as a `revision_request`. The revised notification requirement cites that message's ID. It does not cite the earlier email answer as support for SMS, and saving still requires the separate **Approve and save** action on the new proposal.

`CitationResponse` provides a stored evidence record: original source reference/version, title and metadata, exact excerpt/span, index revision, and temporal policy/status. It is the evidence used for this assessment, not a claim that the live source is unchanged. Preserve its quote and source identity from RAG. Citations may originate from search hits or the `citation` returned with a nonempty document-read page, following the [MCP ↔ RAG citation rules](../mcp-rag/README.md#6-reading-a-document-and-index-consistency). Agent stores either kind of evidence before referencing its ID in a proposal; a search hit's citation cannot be reused for text found elsewhere in the document. Apply current session/project and any connector-specific visibility checks before returning retained evidence; retention must not bypass revoked access. The v1 UI displays the excerpt and optional connector URL; full-document browsing is not a separate public endpoint here.

## 6. Explicit Approval and Saving

The dedicated **Approve and save** action sends only:

```json
{
  "contract_version": "1.0",
  "command_id": "cmd-approve-001",
  "expected_session_version": 4,
  "proposal_id": "proposal-001"
}
```

Agent validates current author/project access, session version, current proposal status, write capabilities, and unresolved operations for the same ticket. It loads the immutable proposal itself; the browser does not resubmit changes, invent an approval ID, or choose the write operation.

It also requires the current assessment to be `ready`, with no open questions or blocking reasons. A ready verdict alone is insufficient: provenance, editability, and proposal/snapshot freshness checks still apply.

Atomically create the explicit approval event, approval record with the configured expiry, one stable operation ID, and one queued save job; mark the session `saving`. Duplicate approval commands reuse this result. A different command for an already approved/applied proposal is rejected rather than creating another save.

The worker uses the exact approved proposal through the Agent ↔ MCP contract. Its public `save` summary includes approval/operation IDs, stage, expiry, any verified update summary, and a sanitized error. Stages are `queued`, `in_progress`, `reporting_pending`, `succeeded`, `failed`, `unknown`, `revoked`, and `expired`.

- `queued` does not mean MCP has reserved approval yet; revocation may still succeed.
- `in_progress` means an attempt is authorized; revocation cannot promise cancellation.
- `reporting_pending` may include a verified Jira update while final bookkeeping is pending. Show that distinction without retrying the write.
- `succeeded` and session `updated` require both verified Jira success and the approval-result acknowledgement.
- `unknown` or `applied_unverified` downstream outcomes produce public stage `unknown` and block new saves pending reconciliation.
- Definite failures expose the appropriate recovery; a stale Jira version requires rereading/reviewing, not automatically approving the new version.

Populate `verified_update` only from an authenticated, validated adapter result durably known to Agent, never by parsing a model/progress sentence. If that evidence is not available, keep the stage `in_progress` or `unknown` as appropriate; the UI need not observe every intermediate stage.

Revocation uses the same transactional guard as MCP authorization. If it wins before reservation, the approval becomes revoked and queued workers cannot dispatch it. If authorization already won, return `APPROVAL_IN_PROGRESS`; do not display “cancelled.” Revoking a saved/terminal approval is not an undo operation. The browser closing, refreshing, or disconnecting does not revoke approval or roll back a write.

Reanalysis creates a new assessment/run and invalidates obsolete unsaved proposals. It cannot bypass an active or unknown save. Retryable known rejections are handled by the existing backend operation/attempt protocol; the browser does not create an extra approval merely to retry reporting or a transient provider failure.

When a pinned retrieval generation/source becomes unavailable, Agent owns refresh according to the [Agent ↔ MCP recovery policy](../agent-mcp/README.md#6-timeouts-cancellation-and-evaluation). The frontend sees `analyzing` during the bounded restart and `blocked` with `EVIDENCE_REFRESH_REQUIRED` if evidence cannot stabilize. No old proposal remains approvable during refresh.

Uncertain saves follow the [reconciliation runbook](../../../docs/save-reconciliation.md). Pending administrative recovery keeps the affected session blocked with save stage `unknown`, no `verified_update`, and `RECOVERY_PENDING`; final success appears only after both services acknowledge the recovered result. Verified non-application ends with save stage `failed`, session `blocked`, no current proposal, and reanalysis enabled. The original result remains in the audit trail. Ordinary successful-save reporting still uses `reporting_pending` as described above.

## 7. Progress, Polling, and Reconnect

V1 uses **polling**, avoiding a second streaming transport for the first integration. Poll `/events` approximately every 1–2 seconds while active, with a configurable slower interval while waiting for the author. The same event envelopes can support a later streaming transport; SSE is not required by this contract.

Events are durable invalidation notifications with `sequence`, `session_id`, `session_version`, timestamp, `type`, and `resource_id`. Types are `session.changed`, `message.created`, `assessment.changed`, `proposal.created`, `approval.changed`, and `save.changed`. The resource identifies the affected session/message/proposal/approval/operation. On an event, fetch the corresponding snapshot/message/proposal; do not construct an approved proposal from streamed text fragments.

Events and messages use separate monotonically increasing, per-session sequences starting at 1. `after` is exclusive, defaults to 0, and must be nonnegative; `limit` is 1–100 (messages default 50, events default 100). Each page returns `next_after`, the last returned sequence or the supplied cursor for an empty page, plus `has_more`. Do not claim every integer exists; sequence gaps are allowed. Cursors beyond the current high-water mark are invalid. V1 retains these logs for the lifetime of an accessible session.

On reconnect: authenticate, fetch the session snapshot, load transcript pages from the last applied message cursor (or 0 on a fresh browser), load the current proposal if present, then request events after the snapshot's `last_event_sequence`. The snapshot and its cursors must come from one consistent committed view. Deduplicate message/event sequences and never let an older GET response replace a newer displayed session version. A receipt replay contains the originally accepted version and must not roll back the current UI.

A disconnected browser recovers the existing session/save state. It never interprets a missing network response as proof that the save did not happen. On HTTP errors, back off as instructed; disable mutating controls while authentication/state is uncertain.

## 8. Errors and Action Availability

Errors use `{ "ok": false, "error": { "code", "message", "retryable" } }`, optionally with `retry_after_seconds`. Messages are safe for display. GET snapshot success remains HTTP 200 even if the session's background analysis/save failed; inspect `state`, `last_error`, and `save`.

| HTTP | Codes / meaning |
|---|---|
| 400 | `INVALID_REQUEST`: invalid body, unsupported fields, or invalid pagination |
| 401 | `UNAUTHENTICATED`: browser session missing/expired |
| 403 | `CSRF_INVALID`: invalid CSRF token/origin |
| 404 | `NOT_FOUND_OR_INACCESSIBLE`: resource absent or not visible to this user |
| 409 | `SESSION_VERSION_CONFLICT`, `COMMAND_CONFLICT`, `INVALID_STATE` |
| 409 | `QUESTION_NOT_OPEN`, `PROPOSAL_STALE`, `APPROVAL_IN_PROGRESS`, `TARGET_BLOCKED` |
| 422 | `PROPOSAL_NOT_APPROVABLE`: missing edit capability, invalid content, or unsupported changes |
| 429 | `RATE_LIMITED`: include retry delay |
| 503 | `SERVICE_UNAVAILABLE`: command/read could not complete now |

Background errors may additionally use `DEPENDENCY_UNAVAILABLE`, `TICKET_CHANGED`, `SAVE_REJECTED`, `SAVE_OUTCOME_UNKNOWN`, `EVIDENCE_REFRESH_REQUIRED`, or `RECOVERY_PENDING`. The last two have `retryable: false`: evidence refresh is an explicit new reanalysis action, while recovery is operator-owned. `retryable` on an HTTP error permits a bounded retry of the **same** request/command; it is not permission for a new save. Async recovery is controlled by server-computed `actions`, not that flag. A 409 requires refreshed state and review rather than silently changing the expected version.

Compute actions from current author access, session state, question/proposal freshness, edit capability, approval lifecycle, and per-target save guards. Do not accept messages/revisions/reanalysis while a save is active or unknown. A ready unchanged ticket can finish with `complete` and no approval. An author may review a revised proposal after a revoked pre-dispatch approval, but saving again requires another explicit action.

The conversation freeze applies to the session owning the active/unknown save, including pending recovery. Other authorized sessions for that ticket may analyze and draft, but their approve action is disabled while the target guard exists. They must revalidate ticket/proposal freshness after the guard clears. Reads and audit views remain available in every authorized session.

Implementation checks cover exact proposal rendering, answer-versus-approval separation, revision-message provenance and deduplication, explicit decisions in comments, rejection of unsupported or cross-session message references, replacement of earlier decisions, document-read citations, stale browser tabs, duplicate commands, owner isolation, polling/reconnect, revocation races, unknown writes, and correct final success reporting. Schemas validate shapes; they do not implement those guarantees.
