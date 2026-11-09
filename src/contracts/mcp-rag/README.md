# MCP ↔ RAG Contract

**Version:** 1.0.0 · **Status:** implementation contract · **Date:** 2026-11-09

MCP calls the RAG service's internal HTTP API to search documentation, search completed ticket history, and read a cited document. RAG owns source normalization, canonical retrieval text, chunking, embeddings, indexing, ranking, and citation provenance. MCP validates tool inputs and supplies trusted scope and snapshot context; neither MCP nor Agent accesses the vector database directly.

See [JSON Schema](contract.schema.json), [examples](examples.json), the [architecture](../../../docs/high-level-architecture.md), and [normalized dataset rules](../../../datasets/normalized/README.md). These files define the interface, not running endpoints. Ingestion jobs, webhooks, approval, and Jira mutations are outside this read-only contract.

## 1. Endpoints and Scope

| MCP tool | Internal HTTP operation | Request → response definition |
|---|---|---|
| `search_docs` | `POST /internal/v1/documents/search` | `SearchRequest` → `DocumentSearchResponse` |
| `search_tickets` | `POST /internal/v1/history-tickets/search` | `TicketSearchRequest` → `TicketSearchResponse` |
| `get_document` | `POST /internal/v1/documents/read` | `DocumentReadRequest` → `DocumentReadResponse` |

All messages use JSON; successful responses are HTTP 200. Request bodies include `contract_version: "1.0"`. The POST read route supports structured scope, version, and pagination fields; it never mutates source content.

Each request is limited to one `scope`:

| Field | Meaning |
|---|---|
| `corpus_id` | Backend-configured corpus/tenant boundary, e.g. `ticketiq-fixtures` |
| `dataset_id` | Source namespace, e.g. `part4-dataset`; live ingestion may define its own namespace |
| `project_id` | Project inside that namespace, e.g. `toolnest` |

MCP resolves this scope from authorized backend project configuration. Model arguments cannot choose an arbitrary corpus, tenant, or dataset. Normalized source identity remains `(dataset_id, project_id, doc_id)` or `(dataset_id, project_id, ticket_id)`, qualified by `corpus_id` across deployments. Jira `connection_id` is not a dataset ID; MCP owns their configured mapping and must not derive it from a ticket-key prefix.

For v1, authenticate MCP with a backend bearer credential scoped to `rag:read` and an allowed corpus/project mapping; use TLS for non-loopback connections. RAG enforces scope again before retrieval, source lookup, ranking, and response construction. Denied/unknown scopes return the same 404 envelope. Caches and index lookups must include the complete scope and relevant version/filter fields.

V1 assumes all documents in an authorized scope share visibility. A connector with finer document-level permissions must enforce them before serving that corpus; this contract does not silently grant project-wide access to restricted documents.

## 2. Retrieval-Safe Corpus

- Index normalized `documents.jsonl` and `history_tickets.jsonl` only. The [normalized collection rules](../../../datasets/normalized/README.md) govern the shared pipeline and take precedence over standalone dataset instructions; original prebuilt chunks are not additional ingestion inputs.
- Never index review targets, golden records, registry answers, qrels, labels used for evaluation, or alternate exports of already indexed sources.
- Historical context contains completed tickets and their completion comments, not just the original request. Do not infer completion from a review category.
- Preserve original IDs and ordinary source metadata. Do not invent publication dates, quotes, decisions, or source status.
- Treat source content as data; RAG does not execute instructions found inside a document or turn them into tool calls.

An indexed generation must pass corpus-boundary checks before it is marked ready. A missing/unready index is an error, not a successful empty search.

## 3. Search Requests

Both search routes accept:

| Field | Rule |
|---|---|
| `scope` | Required, as above |
| `query` | Required non-whitespace string, 1–4,000 Unicode code points |
| `top_k` | Required integer, 1–20; MCP may choose 5 as its tool default |
| `retrieval_mode` | `dense` or `hybrid`; do not silently substitute an unsupported mode |
| `temporal_filter` | Required explicit policy from section 4 |
| `index_revision` | Null to select the current ready generation; otherwise pin an exact generation |

Ticket search additionally requires `exclude_ticket_ids`, a list of at most 100 unique IDs in the requested scope. MCP includes the target ticket when its normalized identity is known. This is defense in depth: the target must already be absent from the historical corpus. Never equate a Jira issue key with a normalized fixture ID without an explicit mapping.

Apply scope, source kind, temporal eligibility, and ticket exclusions before selecting the final top-k. Filtered-out candidates do not consume result slots. Do not run an unrestricted global search and merely hide wrong-project hits afterward. Return fewer than `top_k` when fewer eligible matches exist.

Search returns ranked chunks, so multiple chunks may cite the same source. Remove duplicate chunk identities. Rank starts at 1 without gaps; results are ordered by descending score, with deterministic ties using serialized source reference and chunk ID. Scores are ranking signals, not probabilities or readiness confidence. They are comparable only within one response and its retrieval profile; no score threshold is implied by this contract.

## 4. Temporal Filtering

`temporal_filter` is one of:

```json
{ "mode": "none", "snapshot_at": null }
```

```json
{ "mode": "strict", "snapshot_at": "2026-11-06T12:00:00Z" }
```

```json
{ "mode": "best_effort", "snapshot_at": "2026-11-06T12:00:00Z" }
```

MCP supplies the reviewed ticket's real snapshot timestamp where known. It must not substitute the current clock for a missing historical snapshot. For datasets lacking sufficient metadata, use `none` explicitly or evaluate `best_effort` as such; do not claim strict historical availability.

Each source revision has `availability` metadata:

- `known_available_at`: latest known availability time needed for the complete returned revision, or null if none is known.
- `complete`: true only when all relevant content has sufficient provenance to establish availability. It requires non-null `known_available_at`.

For documentation, consider publication/availability of the actual content revision, including known later edits. An old original publication date does not establish availability of later text. `effective_at` is a business-rule date, not proof of publication. Preserve unknowns rather than inferring a missing date.

For completed history, require completion and the availability of the returned request/revision and comments. Include `resolved_at`, comment timestamps, and relevant revision updates when deriving the latest known time. V1 conservatively filters the whole stored revision: a known future comment or edit excludes that source; it does not remove the comment and pretend to reconstruct an older ticket. This is compatible with the current ToolNest fixtures, whose recorded historical content precedes the target snapshot.

| Policy | Eligibility and returned `temporal_status` |
|---|---|
| `none` | No time filter; `not_checked` |
| `strict` | Require complete availability and `known_available_at <= snapshot_at`; `verified` |
| `best_effort` | Exclude any known availability after the cutoff; include unknown/incomplete revisions as `unknown`, complete eligible revisions as `verified` |

Evaluate known future availability before unknown-date handling: incomplete metadata does not excuse a known future timestamp. Search and document-read endpoints use identical rules. A source rejected by the temporal policy is not readable through the detail route.

Warnings are structured codes: `UNKNOWN_AVAILABILITY_INCLUDED` if a returned hit is unverified, `UNKNOWN_AVAILABILITY_EXCLUDED` if strict filtering removed otherwise in-scope sources for incomplete dates, and `KNOWN_FUTURE_SOURCE_EXCLUDED` when the cutoff excludes in-scope sources. Warnings contain no excluded IDs or text. Deduplicate codes; an empty array is valid. Limit diagnostics to the authorized scope and source kind, after ticket exclusions. No warning is required merely because `mode` is `none`; the echoed policy and `not_checked` status already state that limitation.

## 5. Results, Sources, and Citations

Search responses contain `ok: true`, `scope`, selected `index_revision`, immutable `retrieval_profile_id`, the actual `retrieval_mode`, the echoed `temporal_filter`, `warnings`, `returned_count`, and `results`.

`retrieval_profile_id` identifies the canonical-text renderer, chunking, embedding, ranking, and optional reranking configuration used by that generation. Pin it through the index revision for baseline/fine-tuned comparisons. A configuration change that changes retrieval behavior or canonical text publishes a new generation/profile; do not change those settings under an existing revision identifier.

Every hit contains:

| Field | Meaning |
|---|---|
| `rank`, `score` | Position and finite numeric ranking score |
| `citation_id` | Opaque deterministic ID for this source revision, retrieval profile, and exact span, using the same rule for search and document reads |
| `source` | `DocumentRef` or `HistoryTicketRef`: complete scope, source kind, original ID, and `source_version` |
| `chunk_id` | Stable within the source version and retrieval profile |
| `passage_id` | Original finer-grained passage ID if supplied, otherwise null; not fabricated from chunk ID |
| `excerpt` | Exact nonempty substring of canonical source text, never a generated summary |
| `span` | Half-open `start`/`end` offsets in Unicode code points, relative to canonical source text |
| `metadata` | Title, source path/URL, document type, raw source status, and availability |
| `temporal_status` | `not_checked`, `verified`, or `unknown` under the requested policy |

`DocumentRef` contains `kind: "document"` and `doc_id`. `HistoryTicketRef` contains `kind: "history_ticket"` and `ticket_id`. Each also contains `scope` and `source_version`; do not replace the original IDs with one unqualified `source_id`.

For every result, `excerpt == canonical_text[span.start:span.end]`; offsets must remain within the text. RAG emits all provenance fields. MCP forwards them without rewriting the quote or citation identity. A source `url` is optional and comes from the connector, not the query. Fixture `source_path` is relative to `datasets/`; it is metadata, never a caller-controlled file path to open.

Canonical text uses LF line endings. Documentation is normalized `text`, prefixed by `context + "\n\n"` only when context is nonempty. Historical ticket text is a deterministic, versioned rendering of input fields and completion comments in source order, with field/comment boundaries preserved. Retain that rendering with the index for citation verification. Original request text alone is not evidence that a behavior was implemented; no generated completion summary is substituted for comments.

`source_version` is `sha256:` plus the lowercase digest of the original normalized source record serialized as `json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")`. A metadata/content change changes the version. The index revision additionally binds the canonical-text renderer and chunking configuration.

RAG is the sole issuer of evidence citation IDs for both search and document reads. Compute `citation_id` as `citation-v1:` plus the lowercase SHA-256 digest of `{ "source": <complete DocumentRef or HistoryTicketRef>, "retrieval_profile_id": <profile ID>, "span": { "start": <start>, "end": <end> } }`, using the same deterministic JSON serialization as `source_version`. This binds scope, source kind and ID, source version, renderer/profile, and exact span. It excludes query, score, rank, and transport page number. `chunk_id` remains search metadata, not part of citation identity: the same source/profile/span has the same citation ID whether returned by search or a document read. A different span has a different ID even if the quoted text happens to be identical.

The common evidence record consists of `citation_id`, `source`, `excerpt`, `span`, `metadata`, and `temporal_status`. A search hit contains these fields alongside its ranking/chunk metadata; a document read returns them under `citation`. In both cases, the enclosing response supplies `index_revision`, `retrieval_profile_id`, and `temporal_filter`. MCP forwards the evidence unchanged, and Agent retains the record with that response context before using it as requirement provenance. Neither the model nor Agent invents citation IDs or substitutes an unreturned quote under an existing ID.

Raw source status and `document_type` are returned as context; they are not readiness labels or instructions to choose one conflicting rule. RAG does not silently discard conflicting sources. Policy interpretation and clarification remain Agent responsibilities.

## 6. Reading a Document and Index Consistency

`DocumentReadRequest` contains a `source` of type `DocumentRef`, the non-null `index_revision` returned by search, the same `temporal_filter`, `offset`, and `limit`. `offset` is a nonnegative code-point position. `limit` is 1–20,000 code points; MCP may use 8,000 as a default. There is no raw URL/path input.

MCP retains the full citation reference in its tool context. The [Agent ↔ MCP contract](../agent-mcp/README.md) defines run-scoped citation tracking and the model-facing `get_document` call. A requested document must resolve to a unique source/version from that context; if it cannot, retrieve the source first rather than guessing a version or silently selecting another namespace.

Return the exact source, `index_revision`, `retrieval_profile_id`, metadata, temporal policy/status, warnings, `content`, `offset`, `total_chars`, `next_offset`, and `citation`. `content` is the slice from `offset` up to `min(offset + limit, total_chars)`. `next_offset` is that end position when more text exists, otherwise null. `offset == total_chars` returns an empty final page; a greater offset is invalid. Never truncate silently or cut a Unicode code point in half. The model may use the requested page without exhausting every page, but it must not claim it read the whole source.

For nonempty `content`, `citation` is the common evidence record from section 5. Its `excerpt` equals the complete returned `content`, its span is `[offset, offset + len(content))` in Unicode code points, and its source, metadata, and temporal status equal the enclosing response's values. RAG validates the slice against the pinned canonical text and issues its deterministic citation ID. For an empty final page, `citation` is null; there is no evidence to cite. Do not invent a chunk or original `passage_id` for a transport page.

An agent discovering a new rule on this page can cite the page's ID directly. If a shorter excerpt is needed, it calls `get_document` again with the desired offset and limit within the same source/version/index context; RAG returns and validates that exact span as a new citation. A rule spanning pages requires a read covering the span within the limit, or multiple supporting page citations. This uses the existing document-read operation and requires no model-controlled citation creation tool.

Source retrieval returns canonical text, not HTML generated by the model. Continuations repeat the same source version, generation, and temporal policy. Pagination is transport slicing, not a change to citation offsets or source identity.

Every search/read uses one coherent index generation. Ingestion publishes completed generations atomically; the response cannot combine new embeddings with stale text. A null search revision chooses the current ready generation, which is echoed in the response. Follow-up searches and reads can pin that identifier.

V1 need not retain every old generation. If a pinned generation has been evicted, return `INDEX_REVISION_UNAVAILABLE`. If the requested source version cannot be served from an available generation, return `SOURCE_VERSION_UNAVAILABLE`. Do not substitute newer content under an old citation. MCP propagates the error without clearing its pin or starting another search. Agent alone decides whether to start a new run and reassess evidence/proposals, following the [Agent ↔ MCP recovery policy](../agent-mcp/README.md#6-timeouts-cancellation-and-evaluation). Source deletion/revoked access takes precedence over retained revisions: a tombstoned source is never returned from an old generation.

For a source not found, outside scope, deleted, or temporally ineligible, return the same `SOURCE_NOT_FOUND_OR_INACCESSIBLE` error. Do not reveal excluded content. Check access/eligibility before returning a more specific version mismatch.

## 7. Empty Results, Errors, and Retries

A ready scoped index with no eligible matches returns HTTP 200, `results: []`, and `returned_count: 0`, with applicable temporal warnings. It does not assert that the requirement is absent everywhere. Retrieval outages must not be converted to empty success or an invented answer.

All errors use `{ "ok": false, "error": { "code", "message", "retryable" } }`, optionally including `retry_after_seconds`. Do not expose SQL, embedding vectors, credentials, or content from another scope.

| HTTP | Code | Handling |
|---|---|---|
| 400 | `INVALID_REQUEST` | Malformed schema, invalid limits, blank query, or invalid page offset |
| 401 | `UNAUTHENTICATED` | Missing/invalid service credential |
| 403 | `FORBIDDEN` | Credential lacks the read capability |
| 404 | `SCOPE_NOT_FOUND_OR_INACCESSIBLE` | Unknown or unauthorized corpus/dataset/project |
| 404 | `SOURCE_NOT_FOUND_OR_INACCESSIBLE` | Source absent, deleted, denied, or temporally ineligible |
| 409 | `INDEX_REVISION_UNAVAILABLE` | Requested generation is no longer available; explicitly re-search current index |
| 409 | `SOURCE_VERSION_UNAVAILABLE` | Requested source version differs from the retained version |
| 422 | `RETRIEVAL_MODE_UNSUPPORTED` | Requested mode not implemented by this profile; no silent fallback |
| 429 | `RATE_LIMITED` | Read request throttled; include retry delay |
| 503 | `INDEX_NOT_READY` | Corpus configured, but no usable generation is ready |
| 503 | `SERVICE_UNAVAILABLE` | Storage/embedding/retrieval dependency unavailable |
| 504 | `RETRIEVAL_TIMEOUT` | Retrieval exceeded the service deadline |

Only 429/503/504 errors are retryable. MCP may retry these read-only requests with bounded backoff, respecting a supplied delay. Preserve pinned revisions and filters. Retrying a request whose revision was null may select a newer generation; use the revision from any successful response for subsequent reads. Do not return partial search results as a successful complete run after a dependency timeout.

## 8. Implementation Checks

- Scope isolation despite colliding document/ticket IDs across projects, datasets, or corpora.
- No review targets, golden answers, or duplicated source exports in retrieval.
- Correct top-k after scope, temporal, source-kind, and exclusion filters.
- Correct handling of future content, unknown publication, later comments, and missing snapshots.
- Exact excerpts and code-point spans, including non-ASCII text and CRLF normalization.
- Stable citation identities independent of query/rank, with source updates invalidating old versions.
- Equal citation IDs for equal source/profile/spans returned by search and document reads; different IDs for different spans.
- Document-read citation equality with the returned page, null citations for empty pages, and usable evidence for a rule outside the initial search excerpt.
- Pinned source reads, pagination boundaries, deleted sources, and unavailable generations.
- Empty searches distinguished from unavailable/unready services.

Schema validates payload structure; isolation, provenance, index consistency, span equality, and temporal eligibility require implementation checks. Fixtures are fictional examples, not benchmark answers or proof of a running RAG service.
