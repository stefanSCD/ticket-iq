# TicketIQ Save Reconciliation v1

This runbook defines the administrative recovery workflow to implement for active or unknown writes. It is not a browser action, model tool, or implemented command. Agent owns approval/session state; MCP owns dispatch evidence. The MCP/Jira workstream owns the incident investigation; the Agent workstream owns approval and session recovery. A named deployment operator, authenticated with separate administrative permissions, coordinates both. Service credentials for ordinary tool calls do not grant reconciliation rights.

## Preserve the blocked operation

1. Identify the exact connection, issue, approval, operation, and attempt from durable records. Stop/fence workers for that operation and acquire its MCP dispatch guard before investigation. Do not kill unrelated operations or clear the ledger. Prevent late workers from dispatching after recovery begins.
2. Keep the Agent target guard active. Do not release it on expiry, elapsed time, matching Jira content, or a missing process. Reads remain available. In the affected session, messages, revisions, reanalysis, approval, and revocation remain disabled. Other sessions may read, analyze, and draft the same ticket, but cannot approve/save while the target guard is active.
3. Preserve original attempt authorizations, results, receipts, provider acknowledgements, and any verification reads. Check immutable target/operation bindings before associating provider evidence with an attempt. Never resend the original PUT as a diagnostic action.

## Classify the evidence

| Finding | Required evidence | Resolution |
|---|---|---|
| Exact durable result exists in MCP; Agent has not recorded a result | The original adapter result and attempt binding | Resume ordinary result reporting with the same identifiers; no recovery replacement and no PUT. |
| Verified success established after an uncertain result | Evidence attributing the accepted write to this attempt, plus a verification result matching the exact approved replacements | Administrative `verified_succeeded`; retain the verified adapter `UpdateResponse`. |
| Definitely not applied | Fenced ledger proves no worker crossed the dispatch guard, or a correlated definitive provider rejection proves no write occurred | Administrative `verified_not_applied`; retain a definitive non-retryable adapter error with `not_attempted` or `rejected`. |
| Applied but verification differs, or outcome cannot be attributed | Conflicting/insufficient evidence, including a current read merely matching the proposal | Leave blocked. A current match alone does not establish which writer applied it; no automatic retry or forced success. |

The successful recovery result must satisfy the same target, approved value, field-set, and operation checks as an ordinary result. A later read that differs from a previously verified success does not erase that historical success; show its verified snapshot and require a fresh read for further work. An unresolved incident remains open until sufficient evidence exists; v1 deliberately has no “force unblock” path.

## Record recovery across both services

Use an operator-reviewed `RecoveryDecision` artifact defined in the approval contract. It contains a unique recovery ID, the approval/operation/attempt IDs, operator identity, reason, immutable evidence references, timestamp, one of the two verified outcomes above, and the supporting adapter result. Evidence references identify retained audit artifacts, not arbitrary URLs to fetch. Both services validate the same artifact and exact immutable proposal binding. Existing attempt results and receipts are never overwritten.

1. **MCP prepare:** under the dispatch guard, persist the decision as pending recovery and permanently close that operation to further dispatch. Export its exact artifact for Agent. Reusing the recovery ID with different content fails.
2. **Agent record:** through an administrative operation owned by Agent, atomically append the recovery decision, set approval state to `succeeded` or `failed`, invalidate obsolete proposals as appropriate, and retain the target guard pending MCP acknowledgement. Store the decision in `ApprovalRecord.recovery`; preserve `last_result` as the original attempt result. Publish a session event explaining that recovery synchronization is pending. An identical replay returns the same administrative receipt.
3. **MCP acknowledge:** durably record Agent's receipt against the prepared decision. A duplicate acknowledgement does not reopen the operation. Return acknowledgement of that exact recovery ID/artifact.
4. **Agent finalize:** durably record MCP's acknowledgement, release the reconciliation target guard, and atomically publish the final session/save state and events. For verified success, use `updated`/`succeeded` and the recovered verified result. For verified non-application, use `blocked`/`failed`, clear the current proposal, and enable reanalysis. Any later save needs a fresh ticket read, proposal, and approval; never reuse the recovered operation.

Each step is idempotent by recovery ID and exact content. A crash between steps leaves the guard in place; resume at the first unacknowledged step. Ordinary authorization checks both active/unknown approvals and pending recovery guards, even if the approval state is already terminal. Old result-report replays return their original receipts and cannot overwrite recovery or release its guard. GET returns current approval state, original `last_result`, and the separate recovery decision.

Deployment must provide administrative operations implementing these service-owned transitions before real Jira writes are enabled. They may be local administrative commands in v1; they are not part of the public API. Never implement recovery by manually editing both databases or deleting an approval row. The mock integration must exercise interruption between every step and demonstrate that no additional PUT occurs.
