# TicketIQ Frontend

**Owner:** Frontend workstream.

## Responsibilities

- Select a ticket and display its description and acceptance criteria.
- Show agent assessments, evidence sources, clarification questions, and progress.
- Collect answers and proposal revision requests.
- Display the exact proposed changes and collect explicit approval.
- Show confirmed update results and actionable errors.

## Interfaces

Implement the [Frontend ↔ Agent contract](../contracts/frontend-agent/README.md): authenticated sessions, questions/messages, immutable proposal review, explicit approval/revocation, and progress polling. Use its example payloads as mocks while the backend is under development.

Recover the existing session after refresh and preserve command IDs across retries. Never turn a repeated approval request into a second save. V1 uses durable event polling; a streaming transport can be added later.

A clarification answer does not approve an update. Show success only after the backend confirms that the ticket was saved.

Display requirement provenance from retrieved citations and the author's stored clarification, revision, or explicit decision messages. A revision that replaces an earlier decision must point to the new supporting message. Render citations from document-read pages in the same way as search citations; none of these evidence or message references replaces explicit approval of the current proposal.

Display assessment and question citations before a proposal exists, including both sides of conflicting documentation. Apply the [assessment rubric](../../docs/assessment-rubric.md) and backend action flags: partial proposals are not approvable in v1. Show evidence refresh and operator recovery as distinct blocked states. The session owning an uncertain save cannot mutate its conversation; other sessions may draft but cannot approve that target until recovery finishes. Use the [integration scenarios](../../docs/integration-scenarios.md) for UI mock coverage.

See the [workflow example](../../docs/workflow-example.md).

Status: scaffold only. The frontend framework and build setup have not been selected. Add the application, dependencies, and container/build configuration here.
