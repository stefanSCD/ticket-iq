# MCP ↔ Jira Adapter Contract

**Version:** 1.0.0 · **Target:** Jira Cloud REST API v3 and a compatible mock · **Reviewed:** 2026-11-09

This contract defines the internal Python boundary between the MCP tool handlers and their Jira adapter. The adapter runs inside the MCP service; it is not a fourth backend service or a new public HTTP API. Both the real and mock implementations expose the same operations and payloads.

See the [JSON Schema](contract.schema.json), [example payloads](examples.json), [architecture](../../../docs/high-level-architecture.md), and [work allocation](../../../docs/work.md). This is a contract only; no Jira connection or adapter is implemented here.

## 1. Scope and Official API Mapping

We target Jira Cloud for the first implementation. Jira Data Center requires a separate adapter. The v1 write allowlist is `title`, `description`, and `acceptance_criteria`. Creating/deleting issues, transitions, assignments, comments, attachments, and arbitrary field updates are outside this contract.

| Adapter operation | Jira Cloud REST operation |
|---|---|
| `get_ticket(request)` | `GET /rest/api/3/issue/{issueIdOrKey}` with an explicit field selection |
| `get_edit_capabilities(request)` | `GET /rest/api/3/issue/{issueIdOrKey}/editmeta`, combined with configured field mappings |
| `update_ticket(request)` | `PUT /rest/api/3/issue/{issueIdOrKey}` followed by a verification read |
| Connection setup, not an agent tool | `GET /rest/api/3/field` to inspect field identifiers and schemas |

Jira accepts an issue ID or key for reads. Editing uses `fields`/`update`; `description` and textarea custom fields use ADF. Edit metadata describes available field operations. The documented edit responses include 204, or 200 with `returnIssue=true`. [Official issue operations](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/)

## 2. Configuration and Ownership

The MCP backend resolves a trusted `connection_id` to credentials and a configured Jira API base URL. It maps the application's `project_id` to a Jira project ID. Never accept a caller-supplied URL, credential, or arbitrary Jira field identifier in these operations.

Example configuration, containing no credentials:

```json
{
  "connection_id": "jira-demo",
  "project_id": "toolnest",
  "jira_project_id": "10000",
  "acceptance_criteria_field_id": "customfield_10042",
  "mapping_revision": "1"
}
```

`customfield_10042` is fictional, not a portable Jira identifier. For v1, acceptance criteria use an explicitly configured **textarea custom field**. Discover candidates through field metadata and configure the exact ID; never choose by display name alone. Field discovery is described in the [official field API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-fields/).

If the mapping is absent, reads report acceptance criteria as `unconfigured` and attempts to update that field fail. If configured with an incompatible field type, fail with `CONFIGURATION_ERROR`. Do not create a field automatically or silently append criteria to the description. Existing criteria embedded in the description remain available as part of that description.

For a private development connection, email + API token is supported by [Atlassian's basic-auth guidance](https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/). A distributed integration should use OAuth 2.0 (3LO), following the [authentication and URL guidance](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/). Credentials stay in backend configuration. TicketIQ approval is separate from the Jira identity used to execute a request.

## 3. Operations and Common Rules

Implement an asynchronous Python interface with these signatures:

```python
async def get_ticket(request: TicketRequest) -> TicketResponse | ErrorResponse: ...
async def get_edit_capabilities(request: TicketRequest) -> CapabilitiesResponse | ErrorResponse: ...
async def update_ticket(request: UpdateRequest) -> UpdateResponse | ErrorResponse: ...
```

The named types are defined in `contract.schema.json` under `$defs`; these signatures describe the interface, not executable type declarations. Known validation/provider failures return `ErrorResponse`. Unexpected programming errors remain internal service errors.

All requests have `contract_version: "1.0"` and:

| Field | Meaning |
|---|---|
| `connection_id` | Backend-selected Jira connection; also scopes mock data |
| `project_id` | Application project ID, such as `toolnest`, resolved to the configured Jira project |
| `ticket_id` | ID or key for reads; immutable Jira issue ID for writes |

Resolve a read selector first, then verify the returned issue belongs to the configured project. Return the resolved ID and current key. For writes, reject a project mismatch before any mutation. The adapter repeats this scope check even if the MCP handler already checked it.

### `get_ticket`

Return `{ "ok": true, "ticket": Ticket }`. A ticket contains:

| Field | Type / mapping |
|---|---|
| `connection_id`, `project_id` | Strings identifying the configured scope |
| `ticket_id`, `key` | Jira issue `id` and current `key` |
| `jira_project_id` | `fields.project.id` |
| `title` | `fields.summary`, string |
| `description` | Original ADF document or `null` |
| `acceptance_criteria` | Original configured custom-field ADF or `null` |
| `acceptance_criteria_state` | `available`, `unconfigured`, or `unavailable` |
| `status` | `{id, name}` from `fields.status`; read-only |
| `label` | String list from `fields.labels`; read-only |
| `updated_at` | `fields.updated`, normalized to an RFC 3339 timestamp |
| `version` | Opaque adapter snapshot token; not a Jira issue field |

Request `summary,description,project,status,labels,updated` and the configured acceptance-criteria field. Missing required fields produce `UPSTREAM_ERROR` rather than invented values. A present null acceptance-criteria field is `available` but empty; an omitted configured field is `unavailable`. Do not treat inaccessible/missing fields as empty content.

ADF is preserved as structured JSON, including existing marks and nodes. Rendering and model-oriented text extraction happen above this adapter. The adapter must not flatten rich content and then overwrite it with a lossy reconstruction. Atlassian publishes an ADF schema and supported node documentation in its [document-format reference](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/). Our schema checks the document envelope only; implementations must also validate supported ADF content before writes.

### `get_edit_capabilities`

Return scope, immutable ticket ID, current `version`, `concurrency: "preflight_only"`, `mapping` with the configured `revision` and `acceptance_criteria_field_id` (string or null), and an entry for each writable field with `editable`, `clearable`, and a reason (`null`, `not_configured`, `not_available`, `not_editable`, or `unsupported_type`). Use the same ticket shape/version calculation as `get_ticket`. Mapping metadata is backend context for binding proposals and approvals, not an editable model argument.

`editable` requires the appropriate configured field and a supported `set` operation from metadata. `clearable` additionally requires an optional field; title is never clearable under this contract. This is TicketIQ's conservative edit policy, even where a direct Jira edit may accept a field absent from an edit screen. Capabilities are advisory and must be refreshed before a write. An unavailable acceptance-criteria value cannot be safely replaced under this contract.

### `update_ticket`

Additional request fields:

| Field | Meaning |
|---|---|
| `expected_version` | Snapshot token returned with the reviewed ticket |
| `approval_id` | Reference to approval already verified by the MCP backend |
| `operation_id` | Stable identifier for one approved save attempt; used for local duplicate suppression |
| `changes` | Nonempty object containing only `title`, `description`, and/or `acceptance_criteria` |

Omitted fields remain unchanged. Included fields are full replacements. `description: null` or `acceptance_criteria: null` explicitly clears that field, if clearable and approved. Title must contain non-whitespace text. No trimming, rewriting, or added requirements are permitted after approval.

The MCP handler verifies the approval record against the author, connection, project, immutable issue ID, expected version, and exact structured `changes`. Bind it to the field mapping revision as well. The adapter is callable only through that trusted handler; `approval_id` alone is not proof of authorization and is never a Jira request parameter. The [MCP ↔ Agent Approval Records contract](../mcp-agent-approvals/README.md) defines the internal HTTP authorization/reservation and result-reporting protocol, including dispatch-attempt deduplication.

The handler stores an operation record keyed by `(connection_id, operation_id)` and binds it to the full approved request. Reuse with different content returns `OPERATION_CONFLICT`. A completed duplicate returns the saved result without another PUT; pending or uncertain attempts must be reconciled before any resend. This is a TicketIQ guarantee, not a claimed Jira idempotency feature.

## 4. Write Procedure and Concurrency Limit

1. Validate the request and verified approval; acquire a per-connection, per-issue lock shared across MCP replicas.
2. Read the current issue and current edit capabilities. Verify project, mapping revision, and `expected_version`. On mismatch return `VERSION_CONFLICT` without writing.
3. Reject unsupported, unavailable, non-editable, or non-clearable changes. Validate ADF before sending anything.
4. Map only approved keys into a Jira `fields` object: `title` → `summary`, `description` → `description`, `acceptance_criteria` → configured custom-field ID. Do not round-trip all fields from the GET response.
5. Submit one PUT using the immutable issue ID. Do not override editability or screen security. Leave Jira's notification behavior at its default; email policy in ticket requirements is unrelated to Jira edit notifications.
6. After a successful provider response, reread the issue. Compare each changed field with the approved value using structural JSON equality (object key order ignored, array order preserved).
7. Return `status: "updated"`, `operation_id`, `approval_id`, `changed_fields`, and the fresh `ticket` only if verification matches. If it differs, return `VERIFICATION_FAILED`; do not claim rollback or retry the old proposal. If the verification read fails, return `UPDATE_OUTCOME_UNKNOWN`.

The `version` token is an adapter-generated SHA-256 fingerprint of the object `{ "ticket": <Ticket without version>, "mapping_revision": <configured string>, "acceptance_criteria_field_id": <configured string or null> }`. This includes scope, immutable issue ID, current key, `updated_at`, rich content, and acceptance-criteria availability. Serialize using Python's `json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")`; preserve array order and perform no Unicode normalization. Prefix the lowercase SHA-256 hex digest with `snapshot-v1:`. Consumers treat it as opaque; mapping changes invalidate earlier snapshots.

**Real Jira concurrency is best-effort.** The documented Cloud edit operation does not specify an issue revision precondition or `If-Match` mechanism. Therefore, this contract uses a preflight comparison and reports `preflight_only`; it does not invent a `fields.version` request field. A change made directly in Jira between the check and PUT can still be overwritten. A post-write read cannot prove that no intervening change was lost. This is a limitation inferred from the [documented edit request](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-issueidorkey-put), not a guarantee of atomic compare-and-swap.

The lock serializes TicketIQ writers only. The mock should simulate stale reads, intervening edits, and verification failures rather than implying the real provider has stronger guarantees. If strict atomic concurrency is required, real Jira writes need a different verified mechanism before that requirement can be claimed as satisfied.

## 5. Errors and Retry Behavior

All failures use `{ "ok": false, "error": { ... } }` with `code`, a sanitized `message`, `retryable`, `write_outcome`, optional `upstream_status`, optional `retry_after_seconds`, and optional `field_errors` keyed by the three canonical writable names.

`write_outcome` is `not_attempted`, `rejected`, `unknown`, or `applied_unverified`. `retryable: true` means a bounded retry is safe after the stated delay and renewed checks; it never authorizes blindly replaying an uncertain write. Read operations always use `not_attempted`.

| Code | Meaning / handling |
|---|---|
| `INVALID_REQUEST` | Invalid shape, empty changes, bad ADF, or forbidden fields; no write |
| `CONFIGURATION_ERROR` | Missing connection/project configuration or incompatible field mapping |
| `AUTHENTICATION_FAILED` | Jira 401; fix credentials |
| `PERMISSION_DENIED` | Jira 403; do not bypass permissions |
| `NOT_FOUND_OR_INACCESSIBLE` | Jira 404; do not assert that the ticket does not exist |
| `PROJECT_MISMATCH` | Resolved issue is outside the configured project |
| `APPROVAL_INVALID` | MCP gate rejected missing, expired, revoked, or mismatched approval; adapter is not invoked |
| `FIELD_NOT_EDITABLE` | Changed field is unconfigured, unavailable, non-editable, or cannot be cleared |
| `VERSION_CONFLICT` | Preflight token mismatch or Jira 409; reread, review, and obtain approval for the revised snapshot |
| `VALIDATION_FAILED` | Jira 400/422 rejected values; preserve safe field-level feedback |
| `RATE_LIMITED` | Jira 429; preserve `Retry-After`, use bounded backoff, and repeat preflight before retrying |
| `UPSTREAM_ERROR` | Read/network failure or malformed provider response; bounded read retries allowed |
| `OPERATION_CONFLICT` | Reused operation ID with different input, or an operation already pending reconciliation |
| `UPDATE_OUTCOME_UNKNOWN` | PUT timeout/connection loss/5xx after possible dispatch, or failed post-write read; no automatic write retry |
| `VERIFICATION_FAILED` | Provider acknowledged the write but reread differs; report `applied_unverified` and stop |

For `UPDATE_OUTCOME_UNKNOWN`, use `unknown` if PUT acknowledgement was lost; use `applied_unverified` if Jira acknowledged the write but verification failed to run. A later read matching the proposal alone does not prove which writer applied it. Keep the operation unresolved until reconciliation establishes its result; never report it as this operation's success solely on matching content.

Read retries use capped exponential backoff with jitter. For 429, honor the provider's delay and retain it in the error result. See [official Jira rate-limit guidance](https://developer.atlassian.com/cloud/jira/platform/rate-limiting/). Rejected edits leave the current proposal unsaved; do not change it silently to make a retry pass.

## 6. Mock Implementation Checklist

The mock implements the same three methods, canonical fields, ADF payloads, scope checks, snapshot tokens, and error envelope. Use the fictional examples as fixtures; their snapshot tokens are illustrative, not computed hashes.

Cover these scenarios when implementing the adapters:

- Read by key and ID, including an updated key and a wrong-project request.
- Missing acceptance-criteria mapping versus an available field with a null value.
- Description/criteria updates, explicit clearing, and preservation of omitted fields and ADF nodes.
- Invalid approval, stale snapshot, non-editable field, and invalid ADF rejected before mutation.
- Successful verified update and an identical duplicate returning the recorded result.
- Reused operation ID with different changes rejected.
- 401/403/404, field validation errors, 409, and 429 with a retry delay.
- PUT timeout, an applied write followed by failed verification, and an intervening external edit.

The schema describes payload structure, while this document defines cross-field invariants, approval, deduplication, and provider behavior. Examples are not evidence of a tested live Jira integration.
