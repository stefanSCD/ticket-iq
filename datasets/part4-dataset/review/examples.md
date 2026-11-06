# ToolNest worked examples — hidden supervision

Do not index this file for retrieval. These examples are existing targets, not additional records.

## resolved_by_documentation: TN-502

**Reject scanning the wrong camera**

Two identical camera models sit on the desk. Checkout accepted the unit that was not assigned to the booking.

Compare the scanned UUID with the assigned unit and return WRONG_ASSET instead of substituting silently.

- `TN-OUT-BR-04`: The scanned asset must match the reservation's assigned unit; mismatch does not silently substitute another unit.
- `TN-OUT-API-03`: An asset mismatch returns 409 WRONG_ASSET and an eligibility failure creates no loan.
- `TN-OUT-ADR-01`: QR labels encode opaque asset UUIDs rather than borrower identifiers or authorization tokens.

## unresolved: TN-501

**Cancel reservations when a course is withdrawn**

If a student withdraws from a course, cancel their course-related bookings automatically.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Question: Which bookings count as course-related, and should staff review them before cancellation?
- `TN-CAN-BR-01`: A borrower can cancel their own Draft, AwaitingApproval, or Confirmed reservation before it becomes Collected.
- `TN-CAN-ADR-02`: Cancellation publication uses the transactional outbox so a committed cancellation can trigger wait-list processing.

## partially_resolved: TN-510

**Add push notifications for existing events**

Keep the current transaction notification events and add a mobile push copy.

Use the existing event recipients and per-channel deduplication; device and consent behavior is unspecified.

- Question: How are push devices registered and revoked, and can borrowers disable push independently of email?
- `TN-NTF-BR-01`: Reservation approval, staff cancellation, waiting-list offer, and overdue events create in-app notification intents for the affected borrower.
- `TN-NTF-WF-03`: The delivery worker deduplicates intents using domain event ID, recipient ID, and channel.

## conflicting_documentation: TN-505

**Add a triage due date to new incidents**

Show lab managers when each new damage or missing-accessory incident must be triaged. Calculate the due date using the standard business-day allowance.

The active rule requires 1 business day and the FAQ allows 2 business days for triage.

- Question: Should new incidents be triaged within 1 or 2 business days?
- `TN-DAM-BR-05`: A new incident must be triaged by a lab manager within 1 business day.
- `TN-DAM-FAQ-01`: Managers have 2 business days to triage a new damage or missing-accessory incident.

## already_clear: TN-507

**Add a missing reservation form test**

Add a regression test that submits startAt=2026-11-09T10:00:00Z and endAt=2026-11-09T09:00:00Z. Assert HTTP 422 and fieldErrors.endAt.code=END_BEFORE_START; no reservation row is created. The endpoint already returns this payload.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.
