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
