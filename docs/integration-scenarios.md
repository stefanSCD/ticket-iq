# TicketIQ Contract Integration Scenarios

These scenarios are the shared acceptance plan for the four workstreams. JSON examples under `src/contracts/*/examples.json` are payload fixtures, not running services. The checks in `tests/test_contracts.py` validate shapes, references, citation spans/IDs, provenance links, and selected cross-boundary invariants. Service implementation must additionally prove persistence, authorization, concurrency, semantic evidence support, and the absence of duplicate writes.

## Payload validation

From the repository root, install development dependencies and run all checks:

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests
```

All five contracts remain unpublished v1 drafts; these changes replace the draft payloads together. There is no deployed-client compatibility claim. Implementations must use the current README, schema, and examples as a set. Source-version and Jira snapshot hashes in fixtures are illustrative because full original/provider records are not supplied; citation IDs and excerpts are computed and checked against the included canonical RAG fixtures.

## Scenarios and observable outcomes

| Scenario | Fixture anchors | Required integration behavior |
|---|---|---|
| Normal clarification and save | Frontend `refinement`; Agent–MCP `refinement`; approval `successful_retry` | Evidence → answer → ready proposal → explicit approval → one verified save; retries do not create another PUT. |
| Conflict before proposal | Frontend `conflicting_evidence`; RAG “Retrieve both sides of an active conflict” | Both sources are inspectable beside the question, with no approvable proposal. |
| Rule found by reading more | RAG “Read a new exact rule beyond the initial search excerpt”; frontend `document_read` | The new span gets its own RAG citation and survives MCP forwarding and Agent storage. Empty final pages add no evidence. |
| Author replaces a decision | Frontend `revision` | Persist one revision message despite command replay; new proposal cites that message and requires a new explicit approval. |
| Author records a decision in a comment | Frontend `author_decision` | Retain the exact user message and cite it as provenance; the comment never creates approval. |
| Context unavailable | Frontend `insufficient_evidence` | `blocked` with `missing_required_context`; no partial proposal, invented rule, or false empty-search claim. |
| Index evicted | Agent–MCP and frontend `evidence_refresh` | MCP propagates the failure; Agent invalidates stale drafts and bootstraps a new run with the same scope/cutoff. One automatic restart maximum; evaluation pins never drift. |
| Unknown save | Approval and frontend `unknown_outcome` | Preserve attempt evidence; freeze owning-session mutations and all same-target approvals. Other sessions may draft, but cannot save. |
| Verified recovery success | Approval and frontend `recovery_success` | Preserve the original uncertain result; keep the guard during every interrupted recovery phase; publish success only after both services acknowledge. No new PUT. |
| Verified non-application | Approval and frontend `recovery_not_applied` | Close the old operation; clear obsolete proposal and permit reanalysis. A new save requires a new snapshot/proposal/approval. |
| Insufficient recovery evidence | [Reconciliation runbook](save-reconciliation.md) | Matching current Jira text alone never unlocks the target. No terminal recovery artifact is accepted. |

For runtime tests, inject interruption after authorization, before/after dispatch, after result persistence, after report acknowledgement, and between every recovery phase. Verify original receipts remain replayable and never overwrite newer state. Include empty searches, deleted sources, wrong-project citations, ambiguous author replies, stale browser tabs, and unsupported proposal content. Mock Jira must simulate the documented preflight-only concurrency limitation rather than claim atomic external writes.

Use the [assessment rubric](assessment-rubric.md) for verdict assertions and scoring, and the [reconciliation runbook](save-reconciliation.md) for recovery ownership and state transitions. Fixture labels select scenarios; they are not model inputs or retrieval content.
