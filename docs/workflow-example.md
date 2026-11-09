# Example: Reservation Cancellation Ticket Refinement

This illustrative workflow follows a ticket from its initial request to an update approved by its author. The ticket, documentation excerpt, and source ID below are fictional.

## 1. Read the initial ticket

**Title:** Allow reservation cancellation

**Description:** Add the ability to cancel a reservation.

**Acceptance criteria:** Not specified.

## 2. Retrieve project context

The agent searches the project's documentation and finds the following rule:

> Only reservations that have not yet been collected can be cancelled.

**Source:** `RES-BR-01` — Reservation cancellation rules.

This answers the eligibility question. The agent cites the source and does not ask the author to restate a documented rule.

## 3. Identify an unresolved decision

The retrieved documentation does not specify whether cancellation should trigger a notification, who should receive it, or which channel to use.

The agent treats this as an open decision rather than inventing a notification policy.

## 4. Ask a focused clarification question

**Agent:** When a reservation is cancelled, should a notification be sent? If so, to whom and through which channel?

**Author:** Yes. Send an email to the person who made the reservation.

The agent records this answer as the source for the notification requirement. The answer clarifies the requirement; it does not yet approve the final ticket update.

## 5. Present the proposed ticket update

**Agent:** I propose updating the ticket as follows. Please review and approve these changes before I save them.

**Title:** Allow reservation cancellation

**Description:** Allow cancellation of reservations that have not yet been collected. After a successful cancellation, send an email to the person who made the reservation.

**Acceptance criteria:**

1. A reservation that has not been collected can be cancelled.
2. A reservation that has already been collected cannot be cancelled.
3. After a successful cancellation, an email notification is sent to the person who made the reservation.

**Requirement sources:**

- Cancellation eligibility and acceptance criteria 1–2: `RES-BR-01`.
- Email notification and acceptance criterion 3: the author's clarification in step 4.

## 6. Obtain explicit approval

**Author:** I approve the proposed description and acceptance criteria. Update the ticket.

Until this approval is received, the ticket remains unchanged. If the author requests revisions, the agent presents a revised proposal for approval before saving it.

## 7. Update the ticket and confirm the result

The agent saves the approved description and acceptance criteria through the ticket integration. Once the integration confirms success, the agent reports:

**Agent:** The ticket has been updated with the description and acceptance criteria you approved.

The workflow trace preserves the original ticket, retrieved evidence, clarification question and answer, proposed changes, explicit approval, and update result.

## 8. Alternative paths before approval

**A rule found after reading more of a document.** Suppose search returns only the introduction of `RES-BR-01`. The agent calls `get_document` and finds the eligibility rule on a later page. RAG returns that page's exact text, source version, offsets, and citation ID. MCP validates and registers the citation, then Agent retains it with the retrieval context. The proposal cites this page's ID, not the original introduction's citation. If a shorter quote is needed, another read requests that exact span and RAG issues its citation. See the [document-read citation rules](../src/contracts/mcp-rag/README.md#6-reading-a-document-and-index-consistency).

**The author changes a decision during proposal review.** Instead of approving step 5, the author requests: “Use SMS instead of email for the cancellation notification.” Agent stores the exact request as a `revision_request` message and retains the original proposal binding. If the request leaves implementation details open, Agent asks for those details before offering the revision for approval. The resulting proposal has a new ID and cites the revision message for the channel decision, while retaining the earlier email answer and proposal in the audit trail. The author must review and explicitly approve the new proposal; the revision request does not save the ticket. See the [author-message provenance rules](../src/contracts/frontend-agent/README.md#5-proposal-review-and-evidence).
