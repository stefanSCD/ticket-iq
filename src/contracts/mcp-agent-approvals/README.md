# MCP ↔ Agent Approval Records Contract

**Version:** 1.0.0 · **Status:** implementation contract · **Date:** 2026-11-09

Agent owns approval records. MCP verifies and reserves approval through Agent's internal HTTP API before calling the Jira adapter, then reports the outcome. This contract complements the [MCP ↔ Jira Adapter contract](../mcp-jira-adapter/README.md), [Agent ↔ MCP tool contract](../agent-mcp/README.md), and [Frontend ↔ Agent approval API](../frontend-agent/README.md). Browser approval creation and internal MCP authorization remain separate operations.

See [JSON Schema](contract.schema.json) and [example messages](examples.json). No endpoints, storage, or authentication are implemented here.

## 1. Ownership and Trust

| Agent service | MCP service |
|---|---|
| Stores immutable proposals and authenticated author approval events | Resolves the trusted caller/session context and current Jira field mapping |
| Owns approval state, expiry, revocation, and the internal API | Verifies/reserves approval before any Jira mutation |
| Atomically binds approval to one save operation | Owns a durable operation/dispatch ledger and per-issue serialization |
| Records reported results and displays them to the author | Calls the adapter and durably records its result before reporting it |

Approval creation is a deterministic backend action triggered by the authenticated author's explicit approval of the displayed proposal. A model response, clarification answer, supplied `approval_id`, or `approved: true` flag cannot create approval. Agent resolves `approved_by` and `session_id` from the authenticated session, not model-generated arguments. The approved author is the authorized owner of that refinement session; Jira credentials alone do not establish this identity.

Internal endpoints require an authenticated MCP service identity. For v1, use a deployment-provisioned bearer credential scoped to `approval:read`, `approval:authorize`, and/or `approval:report`; protect non-loopback connections with TLS. The credential lives in backend secrets, never in prompts or browser code. The implementation must validate credential expiry/rotation and allowed connection/project scope. These are TicketIQ design choices, not Jira API requirements.

MCP resolves `actor_id` and `session_id` from trusted invocation context provided by the authenticated Agent backend. They are not editable model tool arguments. Agent independently compares them with the stored approval. A shared service credential authenticates MCP, not the human author.

The Agent runtime must remain able to serve internal requests while awaiting MCP tool results; do not hold an approval database transaction or lock across a remote tool call.

## 2. Approval Record

`ApprovalRecord` contains:

| Field | Meaning |
|---|---|
| `approval_id` | Opaque backend-generated identifier; not a bearer token |
| `proposal_id` | Immutable proposal identifier; revised content gets a new ID |
| `session_id`, `approved_by` | Refinement session and authenticated author |
| `approval_event_id` | Stored explicit author action, retained for audit |
| `approved_at`, `expires_at` | Server timestamps; v1 default validity is 30 minutes, configurable at creation |
| `proposal` | Exact approved target, snapshot, mapping, and field replacements |
| `state` | Lifecycle state described below |
| `operation_id` | Generated and permanently bound when Agent creates approval and the queued save job |
| `attempt_id` | Initially null; current/most recent dispatch attempt within that operation |
| `last_result` | Latest recorded Jira adapter update/error response, or null |
| `recovery` | Separate administrative `RecoveryDecision`, or null; never overwrites an attempt result |

The `proposal` contains `connection_id`, `project_id`, immutable `ticket_id`, `expected_version`, `mapping_revision`, `acceptance_criteria_field_id` (string or null), and `changes`. Reuse the Jira adapter's `Changes` and `Version` schemas. The accepted update allowlist and ADF rules are unchanged.

Store the final structured changes **before** displaying the proposal for approval. The UI must represent the full replacement, including removed content and explicit nulls. Do not approve plain text and then generate different ADF after approval. Object key order is irrelevant; list order, whitespace inside strings, null values, and omitted fields are significant. Compare deterministic JSON bytes using the serialization specified in the Jira adapter contract; no fuzzy text or semantic comparison is allowed.

MCP obtains the mapping from its trusted configuration. The Jira adapter's capabilities response exposes `mapping.revision` and `mapping.acceptance_criteria_field_id`; [Agent ↔ MCP `get_ticket`](../agent-mcp/README.md) relays this backend context before proposal creation. Agent captures it with the proposal and must not guess it. A mapping change or a new snapshot requires a new proposal and approval. The `proposal` content, author, session, and expiry are immutable after creation. State, binding, and result history are mutable only through backend lifecycle operations.

## 3. Internal HTTP API

All bodies are JSON. Requests carrying a body include `contract_version: "1.0"`. Route IDs must be opaque URL-encoded values; they must not determine an arbitrary backend URL. The Agent base URL comes from MCP configuration.

| Method and route | Request definition | Successful response definition |
|---|---|---|
| `GET /internal/v1/approvals/{approval_id}` | No body | `RecordResponse` (200) |
| `POST /internal/v1/approvals/{approval_id}/authorize` | `AuthorizeRequest` | `AuthorizeResponse` (200) |
| `POST /internal/v1/approvals/{approval_id}/result` | `ResultRequest` | `ResultResponse` (200) |

`GET` is for reconciliation/audit; reading an approved record is not permission to write. All endpoints enforce the service credential's scope against the stored connection/project. Return 404 for unknown or out-of-scope records without revealing the distinction.

### Authorize and reserve

The request includes `actor_id`, `session_id`, `proposal_id`, the current `mapping_revision` and `acceptance_criteria_field_id`, a backend-generated `attempt_id`, and `update`, which is the **unchanged Jira adapter `UpdateRequest`**.

Agent performs the following atomically against its approval store, using a shared guard for the target `(connection_id, ticket_id)` as well as the record:

1. Resolve the path ID and check it equals `update.approval_id`.
2. Match author, session, proposal ID, target scope, immutable issue ID, snapshot, mapping, and every field in `changes` against the stored record.
3. Check state and `expires_at` using the Agent server clock. For a new attempt, `now >= expires_at` is expired. Approval must be `approved`.
4. Reject with `TARGET_BLOCKED` if a different approval for the same target is `in_progress` or `unknown`, or any administrative recovery guard exists for that target. This also applies to approvals created before that competing attempt started.
5. Require the operation ID bound at approval creation. All attempts must use that same operation and identical update payload. Bind `attempt_id`, move to `in_progress`, and persist the authorization before replying.

The response includes `approval_id`, `operation_id`, `attempt_id`, `authorized_at`, `state: "in_progress"`, and `replayed`.

An identical authorize request for the same active attempt returns its existing authorization with `replayed: true`, even if the approval's original expiry has since passed. It is a retransmission of a previously committed authorization, not a new authorization. A different attempt while one is active returns `APPROVAL_IN_PROGRESS`; a different operation returns `OPERATION_CONFLICT`. A terminal approval cannot authorize a new write.

Attempt IDs are unique within the bound operation and are never reused after a result has been recorded. Reusing a completed attempt ID for authorization returns `ATTEMPT_MISMATCH`.

**MCP must not equate an authorization response with a fresh dispatch instruction.** Before PUT, it atomically changes its durable attempt ledger from `authorized` to `dispatching`. Only one worker may make that transition. Replayed authorizations, concurrent handlers, and process restarts never reset `dispatching` or authorize another PUT. If a crashed attempt might have dispatched, reconcile it instead of retrying it.

### Report the result

`ResultRequest` contains `operation_id`, `attempt_id`, and `result`, the exact adapter `UpdateResponse` or `ErrorResponse`. MCP persists this result in its own ledger before sending it to Agent. If reporting times out, retry **reporting**, not the Jira update.

Agent checks the binding and validates successful responses against the approved target, `approval_id`, `operation_id`, changed-field set, and approved replacement values. The returned ticket has a fresh snapshot token; it need not equal `expected_version`. Reject inconsistent results as `RESULT_MISMATCH` and leave the approval blocked for reconciliation.

Record one immutable result receipt per attempt. An identical repeated report returns the original receipt with `replayed: true`. A different result for an already reported attempt returns `RESULT_CONFLICT`. Check saved receipts before current-state checks: retrying an old receipt after a newer attempt must not rewind the current record.

The receipt contains `recorded_state`, `recorded_at`, and attempt/operation/approval IDs. `recorded_state` is the state at the time of that report, not necessarily the current state; use GET for current state. An HTTP 200 here acknowledges recording, not successful Jira saving. The contained adapter result determines whether a write succeeded.

## 4. Lifecycle, Revocation, and Retry

| State | Meaning / allowed transition |
|---|---|
| `approved` | Explicit approval exists; may authorize, expire, or be revoked |
| `in_progress` | One attempt reserved the approval; no competing attempt may start |
| `succeeded` | Verified adapter update recorded; terminal, no new writes |
| `failed` | Definite non-retryable failure recorded; terminal, new approval required |
| `unknown` | Write may have occurred or verification is unresolved; blocks automatic retries |
| `revoked` | Author revoked approval before reservation; terminal |
| `expired` | No new attempt may start after expiry; terminal |

Result transitions from `in_progress`:

- Verified `UpdateResponse` → `succeeded`.
- `write_outcome` of `unknown` or `applied_unverified` → `unknown`, regardless of error code.
- `not_attempted` or `rejected`, with `retryable: false` → `failed`.
- `not_attempted` or `rejected`, with `retryable: true` → `approved` if still valid, otherwise `expired`. Keep the same operation binding. A retry uses a new attempt ID, repeats authorization and Jira preflight checks, and respects the adapter's retry delay.

Revocation and authorization use the same transactional state guard. If revocation wins, authorization fails. If authorization wins, revocation returns `APPROVAL_IN_PROGRESS` and must not promise cancellation of that attempt. Editing a proposal while it is still `approved` revokes that approval; while an attempt is active, wait for/reconcile its result before approving a replacement for the same ticket.

Expiry is checked for new attempts only. It does not cancel an already authorized attempt or prevent its result from being recorded. Enforce expiry on read/authorization as well as any scheduled cleanup; correctness must not depend on a timer running.

There is no lease that automatically releases an abandoned attempt. A missing heartbeat, network timeout, or process restart does not prove Jira was untouched. Keep `in_progress` blocked until a durable result is available. If the outcome is uncertain, MCP reports the corresponding adapter error and Agent records `unknown`.

An `unknown` result cannot be replaced through the normal result endpoint. V1 has no automatic recovery endpoint: use the [operator reconciliation runbook](../../../docs/save-reconciliation.md), including fencing, evidence classification, and the MCP prepare → Agent record → MCP acknowledge → Agent finalize sequence. A matching current Jira field value alone is not proof that this operation succeeded. Block new approvals for the same connection/issue while an earlier save or recovery remains unresolved. Reads remain available; freeze conversation mutations in the owning session, while other authorized sessions may analyze/draft but cannot approve/save.

`RecoveryDecision` is an administrative audit artifact, not a request accepted by the normal approval API. It contains `recovery_id`, `approval_id`, `operation_id`, `attempt_id`, `operator_id`, `decided_at`, `reason`, nonempty `evidence_refs`, `outcome` (`verified_succeeded` or `verified_not_applied`), and `result` (the supporting adapter response). A success requires a matching `UpdateResponse`; non-application requires an `ErrorResponse` with `retryable: false` and `write_outcome` of `not_attempted` or `rejected`. Administrative handlers independently validate evidence and exact proposal bindings, not just this shape. Unresolved investigations create no terminal decision and keep the target blocked.

Record recovery separately from the original immutable attempt receipt and `last_result`. Before finalization, GET may show terminal approval state plus `recovery`, but the independent recovery guard still prevents authorization and UI success. Only finalization publishes a new administrative `ResultResponse` receipt for replay of the recovered operation, carrying the original attempt/operation/approval IDs, the recovered terminal state, and the finalization timestamp. It is retained in recovery history, not in place of the original result receipt. Replays of the normal result endpoint continue returning the original receipt and cannot reverse recovery.

## 5. Error Envelope and MCP Mapping

Errors use `{ "ok": false, "error": { "code", "message", "retryable" } }`, with optional `retry_after_seconds`. These are approval-service errors, not Jira adapter errors. Do not return credentials, the full proposal, or another user's record in an error message.

| HTTP | Code | Meaning |
|---|---|---|
| 400 | `INVALID_REQUEST` | Invalid JSON, schema, or path/body approval-ID mismatch |
| 401 | `UNAUTHENTICATED` | Missing/invalid service credential |
| 403 | `FORBIDDEN` | Authenticated service lacks the endpoint capability |
| 404 | `APPROVAL_NOT_FOUND` | Unknown or inaccessible record |
| 409 | `APPROVAL_MISMATCH` | Caller, proposal, target, snapshot, mapping, or changes differ |
| 409 | `APPROVAL_EXPIRED` / `APPROVAL_REVOKED` | Approval cannot authorize a new attempt |
| 409 | `APPROVAL_IN_PROGRESS` | Another attempt already holds the approval |
| 409 | `TARGET_BLOCKED` | Another approval has an active or unresolved save for the same ticket |
| 409 | `APPROVAL_TERMINAL` | Approval already succeeded, failed, or has an unknown result |
| 409 | `OPERATION_CONFLICT` | Different operation ID or changed payload under an existing binding |
| 409 | `ATTEMPT_MISMATCH` | Report refers to an unrecognized/unreserved attempt |
| 409 | `RESULT_MISMATCH` / `RESULT_CONFLICT` | Result does not match the approved update or an existing receipt |
| 503 | `SERVICE_UNAVAILABLE` | Store/service temporarily unavailable; fail closed |

Only `SERVICE_UNAVAILABLE` is retryable in this v1 error envelope. Transport timeouts are handled like unavailable responses, with the same identifiers and identical body on retransmission. Authentication failures require configuration repair; business-state conflicts require inspecting the record, not blind retry.

If authorization is unavailable or denied, do not invoke the adapter. Map semantic approval denials to the existing adapter-facing `APPROVAL_INVALID` with `write_outcome: "not_attempted"`; map active/different operation conflicts and `TARGET_BLOCKED` to `OPERATION_CONFLICT`. An authorization-service outage before dispatch may use `UPSTREAM_ERROR`, `retryable: true`, `not_attempted` at the MCP tool boundary. These envelopes do not change the adapter interface.

If authorization committed but its response was lost, retry authorization with the same attempt ID and consult the MCP dispatch ledger. If reporting fails after a Jira write, retain the real adapter result and retry reporting. Never describe a confirmed saved ticket as an unsent update merely because approval bookkeeping is pending. The final tool response is released once result recording is acknowledged; progress can indicate that saving is confirmed and audit synchronization is pending.

## 6. Required Implementation Checks

- Create records only from explicit authenticated approval of the immutable proposal.
- Reject wrong authors/sessions, altered ADF, omitted-versus-null changes, stale mappings, and path/body ID mismatches.
- Resolve concurrent authorization/revocation with one atomic winner.
- Handle repeated authorization without duplicate Jira dispatch.
- Allow a known rejected retry with the same operation and a new attempt; reject a changed payload.
- Accept a late result for an authorized attempt even after expiry.
- Make repeated result reports idempotent without overwriting a newer attempt's state.
- Keep lost acknowledgements, unknown writes, and expired approvals from enabling another PUT.
- Reject false success payloads and mismatched field values.

JSON Schema validates message shapes. Identity, exact proposal matching, lifecycle transitions, atomicity, and durable dispatch require implementation checks; example fixtures do not implement those guarantees.
