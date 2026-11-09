# Agent ↔ MCP Contract

**Version:** 1.0.0 · **Status:** implementation contract · **Date:** 2026-11-09

Agent is the MCP client; the MCP service exposes five tools and delegates to the [Jira adapter](../mcp-jira-adapter/README.md), [RAG service](../mcp-rag/README.md), and [Agent approval API](../mcp-agent-approvals/README.md). This document defines that client/server boundary, including the trusted backend context absent from model-generated arguments.

See [JSON Schema](contract.schema.json) and [examples](examples.json). This is an interface specification, not an implemented MCP server or model integration.

## 1. MCP Transport and Lifecycle

The v1 interoperability target is MCP protocol revision **2025-11-25**, chosen explicitly rather than claiming to track the latest revision. Use Streamable HTTP at the configured `/mcp` endpoint. Agent sends `initialize`, verifies the negotiated revision and `tools` capability, sends `notifications/initialized`, and then uses `tools/list` and `tools/call`. Incompatible versions fail before business calls. See the official [MCP lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle).

Send UTF-8 JSON-RPC 2.0 messages. HTTP POST accepts `application/json` and `text/event-stream`; include the negotiated `MCP-Protocol-Version` on subsequent requests. If the server assigns `MCP-Session-Id`, preserve it on subsequent transport requests. A transport session is not a TicketIQ user/session/run identifier. Validate supplied Origin headers and authenticate the caller. Implement these details through a compatible SDK following the [official transport specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports).

For this private service deployment, authenticate the Agent backend with a provisioned service credential restricted to configured connections/projects and read/write capabilities. Credentials are never model inputs. Do not describe this private deployment profile as implementing public OAuth discovery. Any external client integration needs its own supported MCP authorization profile.

The server advertises `tools: { "listChanged": false }`. V1 uses ordinary tool calls; it does not require sampling, elicitation, resources, prompts, or experimental task support. Human clarification and approval remain in the Agent/frontend workflow.

## 2. Tool Catalog and Model Boundary

| Name | Arguments definition | Structured output definition | Invocation in v1 |
|---|---|---|---|
| `get_ticket` | `GetTicketArguments` | `GetTicketOutput` | Backend bootstrap and model read |
| `search_docs` | `SearchArguments` | `SearchDocsOutput` | Model read |
| `search_tickets` | `SearchArguments` | `SearchTicketsOutput` | Model read |
| `get_document` | `GetDocumentArguments` | `GetDocumentOutput` | Model read |
| `update_ticket` | `UpdateTicketArguments` | `UpdateTicketOutput` | Deterministic backend call after explicit approval |

All names and schemas are returned by `tools/list`. Agent exposes only the four read tools to the model. After the author approves, Agent loads the immutable stored proposal and invokes `update_ticket` itself; it does not ask the model to reconstruct the approved changes or select approval/operation identifiers. The server still checks approval independently.

Use `readOnlyHint: true`, `destructiveHint: false`, and `idempotentHint: true` for the read tools. For `update_ticket`, use `readOnlyHint: false`, `destructiveHint: true`, and conservatively `idempotentHint: false`; deduplication is the explicit operation protocol below. Use `openWorldHint: true`. Annotations are client hints, never authorization checks.

`inputSchema` describes only `params.arguments`. It does not include the trusted metadata below. `outputSchema` describes `result.structuredContent`, not the entire JSON-RPC response. These follow the [official MCP tools specification](https://modelcontextprotocol.io/specification/2025-11-25/server/tools).

The repository schema reuses sibling contracts through relative `$ref` references. Before publishing `tools/list`, bundle each input/output schema into a self-contained schema with only same-document references. Do not send filesystem references to clients or expose the entire multi-message contract as one tool's schema. The `x-ticketiq-tools` catalog in the schema identifies the definitions and annotations to publish; it is repository metadata, not a wire-format MCP field.

## 3. Trusted Invocation Context

Agent's backend injects `params._meta["ticketiq/context"]` on every tool call. This TicketIQ-specific metadata is separate from the model's arguments. Its schema is `InvocationContext`:

| Field | Source and purpose |
|---|---|
| `contract_version` | `"1.0"` for this application contract |
| `run_id` | Backend-generated identifier for one assessment/retrieval context |
| `session_id`, `actor_id` | Authenticated refinement session and author; never copied from generated text |
| `connection_id`, `project_id` | Authorized backend Jira/application project selection |
| `ticket_selector` | Target selected by the user/backend: Jira key or immutable ID |
| `rag_scope` | Configured corpus/dataset/project mapping; must match the application project |
| `target_corpus_ticket_id` | Mapped normalized target ID or null; used for history exclusion |
| `temporal_filter` | Actual snapshot policy from the RAG contract; no fabricated snapshot |
| `retrieval_mode` | Backend-selected `dense` or `hybrid`, fixed for the run |
| `initial_index_revision` | A pinned generation for evaluation, or null for the first live retrieval |

Update calls additionally include `params._meta["ticketiq/write"]` with `proposal_id` and a stable `operation_id`, both loaded/generated by the backend. MCP creates and persists its own `attempt_id` for each allowed dispatch attempt. No attempt ID is a model argument.

The Agent client ignores/rejects model-supplied metadata and injects its own values. MCP accepts this delegation only from the authenticated allowlisted Agent backend, checks its connection/project scope, and validates the metadata against server configuration. `_meta` is not inherently trusted because it has that name. A service credential identifies the Agent service; the approval API independently binds the declared human identity to the recorded author action.

Store run state by authenticated client identity plus run ID, with actor/session/scope bound immutably. A changed binding returns `CONTEXT_MISMATCH`; another user's run must never be discoverable. Changing the selected target, retrieval policy, namespace, or evaluation revision creates a new run. Keep per-call metadata out of mutable global SDK state so simultaneous conversations cannot share identity accidentally.

`get_ticket` bootstraps the run and records the resolved immutable issue ID/current key. Other tools require that bootstrap for reads and new writes. A model may reread that target by its bound selector or previously resolved ID/key; it cannot use `get_ticket` to silently change the reviewed ticket. Missing read state after a restart requires bootstrap again, while durable write-operation records must survive independently. Replaying a completed operation or resuming its result reporting may use the operation's persisted caller/context binding even if ephemeral read state is gone; it never grants permission for a fresh dispatch.

## 4. Tool Behavior

### `get_ticket(ticket_id)`

Resolve the selector within the trusted connection/project through the Jira adapter. Read edit capabilities as well. Return:

```text
{ ok: true, ticket: JiraTicket,
  edit_capabilities: CapabilitiesResponse | null,
  capability_error: ToolError | null }
```

Capabilities and ticket must refer to the same scope, immutable issue ID, and version. If they differ, reread once; never attach a newer field mapping to an older ticket snapshot. A further mismatch produces a null capability result with `TICKET_CHANGED_DURING_READ`. A capability-read error may likewise leave ticket reading successful; preserve its error separately. If capabilities are present, `capability_error` must be null; if absent, an explanatory error is required.

The agent can assess a readable ticket without edit permission. It cannot create an updatable approval until matching capabilities and mapping metadata are available. `edit_capabilities.mapping.revision` and `.acceptance_criteria_field_id` populate the proposal's mapping binding. Neither is guessed or taken from the model. Ticket-read failure itself returns a tool error.

Agent retains the exact ADF and opaque ticket version. A model-oriented text projection may be produced above this boundary, but the original rich text is retained for proposal rendering and exact approval. A detected ticket change invalidates a draft based on the old snapshot; already-running writes follow their existing approval lifecycle.

### `search_docs(project_id, query, top_k=5)`

### `search_tickets(project_id, query, top_k=5)`

`project_id` is an assertion against the trusted context, not authority to switch projects. Validate query and result bounds using the RAG contract. Supply scope, temporal policy, retrieval mode, and pinned index revision from run state. For history search, add the known normalized target ID to `exclude_ticket_ids`, otherwise send an empty list.

Serialize the first retrieval for a run. If `initial_index_revision` is null, pin the generation from the first successful search before any other search starts. An empty successful search still establishes the pin. Later searches use that same generation and must report the same retrieval profile. Parallel reads are allowed only after this initial binding. A version/profile mismatch is an upstream contract error, not permission to merge results from different generations.

Forward the RAG success payload unchanged, including warnings, temporal policy, source versions, scores, excerpts, and citation IDs. Store document references with their generation and policy in the run's citation registry. Agent selects sources/queries and owns its retrieval-round budget; MCP does not perform undisclosed follow-up searches or silently switch retrieval modes.

### `get_document(project_id, doc_id, offset=0, limit=8000)`

Resolve the requested document to a unique reference from the run's citation registry. If absent, return `CITATION_NOT_FOUND`; if ambiguous, return `CITATION_AMBIGUOUS`. Never guess a namespace or source version. Call the RAG document-read endpoint with that reference, pinned generation, original temporal filter, and validated page bounds. Forward the response unchanged.

Document reads return `retrieval_profile_id` and a RAG-issued `citation` for each nonempty page, as defined by the [MCP ↔ RAG contract](../mcp-rag/README.md#6-reading-a-document-and-index-consistency). MCP validates the source/generation/profile binding and checks that the citation excerpt equals `content`, its span matches the returned offset and length, and its source/metadata/temporal status match the response. It registers that citation with the same run context before forwarding it. An empty final page has `citation: null` and adds no evidence. Agent stores the validated citation and response context in the session evidence store before referencing it in a proposal.

The model uses the page's citation ID for newly discovered evidence, rather than reusing the original search hit's ID for a different passage. To obtain a shorter exact citation it requests that span through the same `get_document` tool. Neither MCP nor Agent creates a replacement ID or rewrites a RAG-issued excerpt; malformed evidence is an upstream contract error.

The caller follows `next_offset` to read more pages. Offsets are Unicode code points as defined by RAG. A stale/deleted source or evicted generation remains an explicit error. To refresh evidence, Agent starts a new retrieval run, reassesses affected requirements, and obtains new approval for any revised proposal; do not silently refresh an existing citation.

### `update_ticket(ticket_id, changes, approval_id, expected_version)`

The backend supplies the stored proposal's immutable ticket ID, exact `Changes` payload, approval reference, and snapshot token. Add the trusted connection/project plus stable operation ID to form the existing Jira adapter `UpdateRequest`; no alternate field mapping or rewritten ADF is accepted.

MCP performs the following:

1. Validate argument/context bindings and the stable operation ledger. An operation ID reused with different update content or different actor/session/proposal is rejected.
2. For a new attempt, read current mapping, build `AuthorizeRequest` with trusted actor/session/proposal metadata and a new durable attempt ID, and call Agent's approval API. Follow its reservation and per-target blocking rules.
3. Invoke the Jira adapter only after authorization. Follow its scope/version/capability preflight and the durable dispatch guard from the approval contract.
4. Persist the exact adapter update/error result, then report it to Agent's approval API. Retry reporting with the same identifiers if its acknowledgement is lost; never repeat the PUT for this reason.
5. Return success only for a verified adapter update and an acknowledged result receipt whose `recorded_state` is `succeeded`.

`UpdateTicketSuccess` contains `ok: true`, `update` (the unchanged adapter `UpdateResponse`), `approval_receipt` (the approval API `ResultResponse`), and `replayed` indicating whether a previously completed operation was returned. The receipt must match the update's approval/operation IDs and the saved attempt.

A completed duplicate is served from the durable ledger after checking caller/context and exact payload binding, without authorizing or writing again. It returns the original verified result, not a claim that Jira has remained unchanged since then. A known retryable rejection uses the same operation and a new attempt, reauthorizes, and repeats preflight. A timeout/unknown outcome never causes automatic redispatch.

If Jira has saved successfully but result reporting is pending, retain that distinction. The ordinary final tool response remains pending until the report is acknowledged, as required by the approval contract; progress may state that saving succeeded and audit synchronization is pending. A client deadline/disconnect does not turn that state into an unsent update. Resuming the same operation continues reporting or returns the saved result, not a new PUT. Store enough invocation binding with the operation to recover safely after an MCP transport-session restart.

## 5. Results and Error Surfaces

For every completed tool call, return one MCP `CallToolResult` with:

- `structuredContent`: the corresponding output object, including `{ok: false, ...}` on execution failure.
- `content`: one text block containing a JSON serialization of exactly the same object.
- `isError`: false for `ok: true`, true for `ok: false`.

This profile intentionally uses object-shaped results. Agent validates the declared output schema and the agreement between these fields before using a result. Citation text is not paraphrased during wrapping. See [MCP structured output and execution errors](https://modelcontextprotocol.io/specification/2025-11-25/server/tools).

Execution errors use `ToolError`: `{ "ok": false, "source": "mcp" | "jira" | "rag", "error": { ... } }`. Jira and RAG errors retain the respective downstream `error` object unchanged; `source` disambiguates identically named codes. Approval denials map to Jira adapter-facing `APPROVAL_INVALID`, active/operation conflicts to `OPERATION_CONFLICT`, and approval-service outages before dispatch to `UPSTREAM_ERROR`, following the existing approval contract. Do not expose internal service credentials or confuse a Jira authentication error with authentication to MCP.

MCP-local errors are:

| Code | Meaning |
|---|---|
| `INVALID_ARGUMENTS` | Known tool received invalid arguments or unknown argument keys |
| `CONTEXT_REQUIRED` | Backend invocation/write metadata is missing or malformed |
| `CONTEXT_MISMATCH` | Actor/session/target/project/scope assertions disagree |
| `RUN_NOT_INITIALIZED` | Bootstrap the target with `get_ticket` before using run-bound reads/new writes |
| `CITATION_NOT_FOUND` / `CITATION_AMBIGUOUS` | No unique tracked document reference |
| `TICKET_CHANGED_DURING_READ` | Could not obtain a coherent ticket/capability snapshot |
| `UPSTREAM_CONTRACT_ERROR` | Downstream response failed schema or scope/version consistency checks |

These local errors have `retryable: false` and `write_outcome: "not_attempted"`. They are only used before dispatch or for read failures. Never label a possibly dispatched update with one of these errors. Malformed update acknowledgements must instead be persisted/reported as an uncertain adapter outcome; reporting failures after a known result preserve that result in the ledger.

Malformed JSON-RPC envelopes, unsupported methods, and unknown tool names use protocol errors, not a fabricated business success. V1 uses `-32700` for JSON parse failures, `-32600` for invalid requests, `-32601` for unknown methods, and `-32602` for an unknown tool. An unavailable/invalid service credential fails at HTTP authentication before tool execution. A valid call to a known tool with invalid business arguments returns `isError: true` and `INVALID_ARGUMENTS`. The [official tools specification](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) distinguishes protocol from execution errors.

An HTTP 200, a text block, or an approval reservation alone is not proof of a successful save. Agent uses `structuredContent.ok`, `isError`, and the verified update/receipt together.

## 6. Timeouts, Cancellation, and Evaluation

Read retries preserve scope, snapshot, citation, and pinned generation. Retry only retryable downstream errors with bounded backoff; do not reinterpret a dependency outage as empty evidence. Cancellation/disconnection does not roll back a Jira write. A call whose acknowledgement was lost is reconciled using its existing operation, never a newly generated operation ID. JSON-RPC request IDs correlate messages; they are not durable idempotency identifiers.

For `INDEX_REVISION_UNAVAILABLE` or `SOURCE_VERSION_UNAVAILABLE`, MCP forwards the RAG error unchanged and performs no recovery search. Agent invalidates the unsaved proposal and revokes any unreserved approval before creating a new run ID, bootstrapping the ticket, and retrieving with `initial_index_revision: null`. Preserve authorized scope and the original temporal policy; never broaden access or remove a historical cutoff to recover results. Pin the new generation on its first successful search. Previous citations remain audit evidence but cannot be silently relabeled as current evidence. Reassess all affected requirements and obtain new approval for any replacement proposal.

Allow at most one automatic evidence-refresh restart per interactive analysis job. A second revision failure yields `blocked`/`EVIDENCE_REFRESH_REQUIRED`, with explicit reanalysis available. A source-not-found/inaccessible response does not trigger repeated automatic retrieval or prove a rule absent; apply the assessment rubric to the remaining evidence. For evaluation with a configured pinned generation, never move to the latest generation: fail the run and report an operational failure. Active/unknown writes or pending reconciliation prevent refresh in their owning session; recover the existing write first. Agent's retrieval budget counts the restart separately in traces and latency reports.

Uncertain writes follow the [reconciliation runbook](../../../docs/save-reconciliation.md). Replaying an operation recovered administratively returns its recovered verified result and matching receipt only after recovery finalization; until then it remains blocked. Original attempt result receipts remain immutable. Administrative recovery never permits another dispatch of that operation.

For evaluation, use backend-configured fixture mappings, snapshot policies, retrieval mode, and pinned generation. Golden labels/answers never enter tool arguments, invocation metadata, retrieval content, or model inputs. Agent enforces no-RAG/fixed-RAG/agent-selected retrieval policies through its tool allowlist and orchestration. Keep model comparison settings fixed as described in the work allocation.

Implementation checks cover context injection, cross-run isolation, capability-version coherence, self-contained tool schemas, first-search pinning, exact citation forwarding, registration and validation of document-read citations, document pagination, output/error consistency, approval denial, duplicate saves, and lost acknowledgements. The schema and examples do not implement these checks or replace integration testing.
