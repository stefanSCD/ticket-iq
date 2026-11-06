# ToolNest — hidden knowledge registry

**Answer key. Do not index this file, source/, review/, or SFT completions for retrieval.**

These are generator-authored labels, not independent expert judgements. Missing decisions were designed across the full authored corpus and completed history; automated absence checking cannot establish semantic absence.

Release 1.1 is active. Every deliberate conflict pairs two active statements with the same scope. There is no blanket precedence for business rules over FAQs. Historical outcomes are release-scoped.

## Feature inventory

| Area | Topic | Split |
|---|---|---|
| CAT | Catalog and asset lifecycle | train |
| RSV | Reservation intervals and availability | train |
| TRN | Training and borrower eligibility | validation |
| APR | Reservation approval | train |
| OUT | Pickup and checkout | validation |
| RET | Returns and condition inspection | test |
| EXT | Loan extensions | train |
| CAN | Cancellations and booking edits | train |
| WAI | Waiting lists and offers | train |
| NOS | Pickup deadlines and no-shows | validation |
| OVD | Overdue loans and account restrictions | test |
| DAM | Damage and missing-accessory incidents | train |
| MNT | Maintenance and service blocks | train |
| XFR | Movement between university labs | train |
| KIT | Equipment kits and bundled items | train |
| NTF | Notifications and delivery | validation |
| SEC | Authentication and lab-scoped permissions | validation |
| AUD | Audit records and data retention | test |
| INT | External API and webhook delivery | validation |
| RPT | Reports, calendars, and exports | test |

## resolved_by_documentation

### TN-502 — Reject scanning the wrong camera

Area: OUT. Sources: TN-OUT-BR-04, TN-OUT-API-03, TN-OUT-ADR-01.

Compare the scanned UUID with the assigned unit and return WRONG_ASSET instead of substituting silently.

### TN-504 — Do not expire requests awaiting approval

Area: NOS. Sources: TN-NOS-BR-01, TN-NOS-API-02.

Only Confirmed uncollected reservations may expire as no-shows; skip AwaitingApproval.

### TN-508 — Keep loan history after a camera is retired

Area: CAT. Sources: TN-CAT-BR-02, TN-CAT-ADR-02.

Retain the asset record and its historical references when moving it to Retired.

### TN-511 — Keep offer order stable when timestamps match

Area: WAI. Sources: TN-WAI-BR-02, TN-WAI-ADR-03.

Order by joinedAt and then entry UUID; notification order must not decide priority.

### TN-512 — Stop borrowers extending a past-due loan

Area: EXT. Sources: TN-EXT-BR-01, TN-EXT-API-02.

Reject extension after dueAt with LOAN_ALREADY_OVERDUE and preserve the current loan.

### TN-513 — Preserve borrower history when university email changes

Area: SEC. Sources: TN-SEC-API-04, TN-SEC-ADR-03, TN-SEC-FAQ-03.

Match the stable identity provider subject to the existing internal user ID instead of creating an account by email.

### TN-518 — Do not label reported damage as borrower liability

Area: DAM. Sources: TN-DAM-BR-02, TN-DAM-FAQ-02.

Show an incident reference without asserting liability; an observation alone is not a liability finding.

### TN-520 — Stop retrying permanently invalid email addresses

Area: NTF. Sources: TN-NTF-API-04, TN-NTF-FAQ-03.

Mark the attempt FailedPermanent and do not retry that permanent failure.

### TN-523 — Enforce grants for the asset lab rather than the selected header

Area: SEC. Sources: TN-SEC-BR-02, TN-SEC-API-03.

Read the target resource's actual lab and require a matching grant; a client-selected lab cannot confer access.

### TN-524 — Require a completed service checklist

Area: MNT. Sources: TN-MNT-BR-03, TN-MNT-API-02, TN-MNT-API-04.

Require checklist results, outcome, and technician attestation; reject incomplete checklists without completion.

### TN-529 — Roll back kit booking when one component conflicts

Area: KIT. Sources: TN-KIT-BR-02, TN-KIT-BR-03, TN-KIT-API-02, TN-KIT-ADR-01, TN-RSV-ADR-01.

Reject the kit with KIT_COMPONENT_UNAVAILABLE and leave no component reservation committed.

### TN-540 — Avoid duplicate cancellation notifications

Area: CAN. Sources: TN-CAN-API-02, TN-CAN-FAQ-03.

An already Cancelled request must return its existing state without another cancellation event.

### TN-541 — Apply revocation without requiring sign-out

Area: TRN. Sources: TN-TRN-WF-02, TN-TRN-ADR-01.

Read current certificate state at the action boundary so revocation affects subsequent checks.

### TN-546 — Reject stale integration updates

Area: INT. Sources: TN-INT-API-02.

Return 412 VERSION_MISMATCH for a stale If-Match rather than overwriting current state.

### TN-548 — Keep uninspected returns out of availability

Area: RET. Sources: TN-RET-BR-01, TN-RET-BR-02, TN-RET-API-01.

Record receipt as ReturnedPendingInspection and keep the unit unavailable until inspection completes.

### TN-553 — Prevent accepting an expired offer

Area: WAI. Sources: TN-WAI-API-02, TN-WAI-API-03.

Use server time to reject expired acceptance with OFFER_EXPIRED and create no reservation.

### TN-556 — Block reservations during repair

Area: RSV. Sources: TN-RSV-BR-05, TN-RSV-WF-01, TN-MNT-BR-01.

Exclude active maintenance intervals in the preview and recheck them during creation.

### TN-560 — Require destination authorization when receiving

Area: XFR. Sources: TN-XFR-WF-03, TN-XFR-API-03.

Require the receiving actor to hold a destination-lab staff grant and scan the expected asset UUID.

### TN-567 — Keep transactions successful when email delivery fails

Area: NTF. Sources: TN-NTF-BR-04, TN-NTF-ADR-01, TN-INT-ADR-02.

Keep the committed reservation and process notification delivery asynchronously through the outbox.

### TN-568 — Keep the borrowed kit checklist after definition edits

Area: KIT. Sources: TN-KIT-BR-04, TN-KIT-API-03, TN-KIT-FAQ-02.

Use the checkout composition snapshot for existing loans and apply definition edits only to future borrowing.

### TN-570 — Preserve receipt time when staff rescan

Area: RET. Sources: TN-RET-API-03, TN-RET-ADR-01, TN-RET-FAQ-03.

Return the existing receipt on a repeated receive action and leave the original receivedAt unchanged.

### TN-571 — Stop no-show expiry after a completed checkout

Area: NOS. Sources: TN-NOS-BR-03, TN-NOS-WF-02, TN-NOS-ADR-02, TN-OUT-BR-03.

Serialize checkout and expiry; once checkout succeeds, expiry must not release the occupied unit.

### TN-572 — Permit back-to-back bookings

Area: RSV. Sources: TN-RSV-BR-01, TN-RSV-FAQ-03.

Treat the interval end as exclusive so adjacent bookings are accepted.

### TN-576 — Prevent self-approval by managers

Area: APR. Sources: TN-APR-BR-02, TN-APR-API-04.

Reject self-approval with SELF_APPROVAL_FORBIDDEN regardless of the actor's manager grant.

### TN-579 — Keep the original reservation after extension

Area: EXT. Sources: TN-EXT-BR-04, TN-EXT-API-04.

Change loan.dueAt, retain oldDueAt in the extension event, and leave the original reservation interval intact.

### TN-581 — Preserve independent safety blocks after repair

Area: MNT. Sources: TN-MNT-BR-04, TN-MNT-API-03, TN-MNT-ADR-01, TN-DAM-BR-03, TN-CAT-BR-02.

Remove only the completed job's block and continue to respect independent safety and lifecycle restrictions.

### TN-582 — Keep unsafe equipment blocked after closing its loan

Area: DAM. Sources: TN-DAM-BR-03, TN-DAM-ADR-03, TN-DAM-FAQ-03.

Retain the safety block until a lab manager records an explicit safety disposition.

### TN-584 — Prevent a loan when identity verification fails

Area: OUT. Sources: TN-OUT-BR-02, TN-OUT-WF-03.

Require successful university ID verification; preserve the reservation and create no loan when verification fails.

### TN-585 — Invalidate approval when booking dates change

Area: APR. Sources: TN-APR-BR-04, TN-APR-FAQ-02, TN-RSV-BR-02.

Return changed asset or interval requests to AwaitingApproval; display-note edits alone do not invalidate approval.

### TN-589 — Handle duplicate webhook events safely

Area: INT. Sources: TN-INT-BR-02, TN-INT-BR-03, TN-INT-FAQ-02.

Treat delivery as at least once and deduplicate by eventId without requiring borrower personal data.

### TN-591 — Protect CSV exports from formula execution

Area: RPT. Sources: TN-RPT-BR-04.

Prepend a single quote to free-text values beginning with the documented formula prefixes before CSV export.

### TN-594 — Reject approval from a stale browser tab

Area: APR. Sources: TN-APR-WF-02, TN-APR-API-01, TN-APR-API-02.

Require the current request version and return 412 VERSION_MISMATCH without mutation for a stale decision.

### TN-599 — Do not move a reservation pickup lab during transfer

Area: XFR. Sources: TN-XFR-BR-04, TN-XFR-ADR-01, TN-XFR-FAQ-03.

Keep the confirmed reservation's pickup lab unchanged unless its normal edit workflow changes it.

### TN-604 — Use the checkout accessory snapshot at return

Area: RET. Sources: TN-RET-ADR-02, TN-RET-BR-03.

Build the return checklist from the loan's checkout accessory snapshot and require a result for every item.

### TN-605 — Warn about confirmed bookings before scheduling repair

Area: MNT. Sources: TN-MNT-BR-02, TN-MNT-API-01, TN-MNT-WF-01.

Show the overlap and reject with MAINTENANCE_BOOKING_CONFLICT; staff must resolve the booking separately.

### TN-606 — Retain in-app updates when email is disabled

Area: NTF. Sources: TN-NTF-BR-02, TN-NTF-API-03, TN-NTF-FAQ-02.

Apply optionalEmailEnabled only to optional email copies and retain in-app transaction notifications.

### TN-607 — Revoke staff access in an already open tab

Area: SEC. Sources: TN-SEC-BR-04, TN-SEC-ADR-02.

Use current server-side grants on the next request so revoked permissions take effect without a new login.

### TN-612 — Handle lost checkout responses safely

Area: OUT. Sources: TN-OUT-API-01, TN-OUT-API-02, TN-OUT-FAQ-03, TN-INT-BR-04, TN-INT-ADR-03.

Reuse the same checkout idempotency key and payload so a retry returns the original loan.

### TN-613 — Skip ineligible borrowers without deleting entries

Area: WAI. Sources: TN-WAI-WF-01, TN-WAI-FAQ-03.

Check training and suspension before offering, skip the ineligible entry for that offer, and retain the entry.

### TN-615 — Reject an extension that crosses the next booking

Area: EXT. Sources: TN-EXT-BR-03, TN-EXT-API-03, TN-EXT-ADR-03, TN-RSV-API-04.

Check interval conflicts transactionally and return EXTENSION_CONFLICT without changing the due time.

### TN-620 — Block account deletion during pending return inspection

Area: AUD. Sources: TN-AUD-BR-04, TN-AUD-API-03, TN-AUD-FAQ-02.

Return ACTIVE_BORROWING_EXISTS until pending inspection is completed; receipt alone does not unblock deletion.

### TN-622 — Scope service access independently from its creator

Area: INT. Sources: TN-INT-BR-01, TN-INT-FAQ-03.

Authorize the service credential using its explicit lab and operation scopes, not the creator's current grants.

### TN-624 — Avoid duplicate no-show events on retries

Area: NOS. Sources: TN-NOS-BR-02, TN-NOS-API-03.

Write one expiry transition and event; later processing must not append another.

### TN-625 — Hide in-transit units from pickup availability

Area: XFR. Sources: TN-XFR-BR-02, TN-XFR-FAQ-02.

Mark dispatched units InTransit and exclude them from pickup inventory until destination receipt.

### TN-626 — Block borrowing while another loan is overdue

Area: OVD. Sources: TN-OVD-BR-03, TN-OVD-API-01.

Check outstanding overdue loans during both reservation creation and checkout and return OVERDUE_RESTRICTION.

### TN-628 — Handle simultaneous requests for one unit

Area: RSV. Sources: TN-RSV-API-01, TN-RSV-API-04, TN-RSV-ADR-01, TN-RSV-WF-02.

Commit at most one booking, return RESERVATION_CONFLICT for the loser, and retain the entered form values.

### TN-629 — Reject duplicate asset tags on import

Area: CAT. Sources: TN-CAT-BR-01, TN-CAT-API-01.

Enforce university-wide tag uniqueness and return 409 ASSET_TAG_EXISTS for a duplicate.

### TN-632 — Stop overdue time when equipment reaches the desk

Area: OVD. Sources: TN-OVD-BR-02, TN-OVD-API-02, TN-OVD-FAQ-02, TN-RET-BR-01, TN-RET-ADR-01.

Stop the overdue interval at receivedAt regardless of inspection completion.

### TN-635 — Count received equipment before inspection finishes

Area: RPT. Sources: TN-RPT-BR-01, TN-RPT-ADR-01, TN-RPT-FAQ-02, TN-RET-BR-01.

Include loans by recorded receipt time, even when inspection remains pending, and attribute them to the pickup lab.

### TN-640 — Release the slot when staff cancel

Area: CAN. Sources: TN-CAN-BR-02, TN-CAN-ADR-01.

Release the blocking interval atomically with the Cancelled transition while retaining reservation history.

### TN-641 — Retain original incident observations after a correction

Area: DAM. Sources: TN-DAM-WF-03, TN-DAM-API-04, TN-DAM-ADR-01.

Append a correction entry instead of replacing or deleting the original evidence.

### TN-656 — Recheck training at collection

Area: TRN. Sources: TN-TRN-BR-03, TN-TRN-API-03, TN-TRN-FAQ-02, TN-OUT-BR-01, TN-OUT-API-03.

Recheck training at actual checkout and reject expired training with TRAINING_REQUIRED.

### TN-662 — Do not expose incident evidence through audit access

Area: AUD. Sources: TN-AUD-ADR-02, TN-AUD-FAQ-03, TN-DAM-BR-04.

Audit access may show the action metadata but must not bypass incident_reader permissions for evidence.

### TN-675 — Explain why retirement is blocked

Area: CAT. Sources: TN-CAT-BR-03, TN-CAT-WF-03, TN-CAT-API-03.

Reject retirement with ASSET_IN_USE and show the blocking reservation reference to the authorized manager.

### TN-677 — Keep a manual suspension after an overdue return

Area: OVD. Sources: TN-OVD-BR-04, TN-OVD-API-03, TN-OVD-FAQ-03.

Clear the overdue-derived restriction when appropriate while preserving the independent manual suspension.

### TN-682 — Remove purpose text from audit payloads

Area: AUD. Sources: TN-AUD-BR-01, TN-AUD-BR-03.

Keep the defined audit metadata and exclude the full borrower free-text purpose field.

### TN-684 — Guide collected reservations to returns

Area: CAN. Sources: TN-CAN-BR-03, TN-CAN-API-03, TN-CAN-FAQ-02.

Reject cancellation with USE_RETURN_WORKFLOW and direct staff or the borrower to the return process.

### TN-686 — Use local dates correctly across daylight-saving changes

Area: RPT. Sources: TN-RPT-WF-01, TN-RPT-BR-02, TN-RPT-ADR-03.

Convert local date boundaries with the lab's IANA time zone and query the resulting half-open UTC interval.

### TN-697 — Protect individually listed kit components from double booking

Area: KIT. Sources: TN-KIT-ADR-02, TN-KIT-BR-02.

Apply interval constraints to the shared component UUID for both individual and kit reservations.

### TN-700 — Stop managers issuing certificates without training access

Area: TRN. Sources: TN-TRN-BR-05, TN-TRN-API-02, TN-TRN-FAQ-03.

Require training_officer even when the actor is a lab manager, and record the acting staff ID.


## unresolved

### TN-501 — Cancel reservations when a course is withdrawn

Area: CAN. Sources: TN-CAN-BR-01, TN-CAN-ADR-02.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Which bookings count as course-related, and should staff review them before cancellation?
### TN-503 — Waive restrictions during campus disruption

Area: OVD. Sources: TN-OVD-BR-03, TN-OVD-BR-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Who may authorize a closure-related waiver, which loans qualify, and how long does it apply?
### TN-506 — Create emergency staff access

Area: SEC. Sources: TN-SEC-BR-02, TN-SEC-WF-02.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Who may activate emergency access, for how long, and which actions are permitted and reviewed?
### TN-509 — Grace period after training expiry

Area: TRN. Sources: TN-TRN-BR-01, TN-TRN-BR-03.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Is a training-expiry grace period permitted, for which users and equipment, and for how long?
### TN-514 — Deliver reminders through SMS

Area: NTF. Sources: TN-NTF-BR-01, TN-NTF-WF-02.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Which SMS provider, consent rules, and event types should the new channel support?
### TN-516 — Reserve a unit before its transfer arrives

Area: XFR. Sources: TN-XFR-BR-02, TN-XFR-FAQ-02.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Can an incoming unit be booked before receipt, and how should a late or failed delivery affect those reservations?
### TN-517 — Bulk import legacy serial numbers

Area: CAT. Sources: TN-CAT-WF-01, TN-CAT-BR-01.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Should duplicate manufacturer serial numbers be accepted, rejected, or flagged for review during import?
### TN-525 — Place selected records under legal hold

Area: AUD. Sources: TN-AUD-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Who may place and release a legal hold, and which event and evidence records fall within its scope?
### TN-530 — Schedule servicing by checkout count

Area: MNT. Sources: TN-MNT-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- What checkout-count threshold triggers service and does it supplement or replace the calendar schedule?
### TN-532 — Introduce daily late fees

Area: OVD. Sources: TN-OVD-WF-03.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- What rates, grace periods, caps, and collection process should the new late-fee policy use?
### TN-533 — Rank the best-performing borrowers

Area: RPT. Sources: TN-RPT-BR-03.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Is borrower ranking permitted, who may see it, and which scoring and fairness rules should it use?
### TN-534 — Penalize repeated cancellations

Area: CAN. Sources: TN-CAN-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- What cancellation frequency triggers a restriction, over which period, and what restriction applies?
### TN-535 — Use an external courier between labs

Area: XFR. Sources: TN-XFR-WF-01, TN-XFR-ADR-02.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- What courier integration and custody evidence are required, and who handles loss in transit?
### TN-536 — Delegate approvals during leave

Area: APR. Sources: TN-APR-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Who may receive approval delegation, for which labs, and when does it expire?
### TN-537 — Let a colleague collect equipment

Area: OUT. Sources: TN-OUT-BR-01, TN-OUT-BR-02.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Is proxy collection permitted, and what delegation and identity evidence must the proxy provide?
### TN-542 — Define external API request quotas

Area: INT. Sources: TN-INT-BR-01, TN-INT-ADR-01.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- What per-token and per-lab quotas, burst allowances, and retry guidance should the rate limit use?
### TN-543 — Allow borrowers to return to a different lab

Area: XFR. Sources: TN-XFR-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Which lab records receipt and performs inspection for a cross-lab return, and how is custody transferred?
### TN-547 — Send damage evidence to insurers

Area: DAM. Sources: TN-DAM-BR-04, TN-DAM-ADR-02.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Which insurer interface and evidence-sharing permissions should the submission use?
### TN-550 — Route returns through a courier

Area: RET. Sources: TN-RET-WF-01, TN-RET-ADR-01.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Does return occur at courier handover or lab receipt, and who bears responsibility while the parcel is in transit?
### TN-551 — Allow a kit to be returned in pieces

Area: KIT. Sources: TN-KIT-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- How should partial return change loan state, component availability, and overdue duration?
### TN-552 — Require two approvals for premium equipment

Area: APR. Sources: TN-APR-BR-02, TN-APR-ADR-01.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Which devices require two approvals, and must the approvers have different roles?
### TN-561 — Let borrowers build custom bundles

Area: KIT. Sources: TN-KIT-ADR-03, TN-KIT-API-01.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- What bundle size, eligibility, and approval rules apply to borrower-created bundles?
### TN-565 — Provide a borrower data portability package

Area: AUD. Sources: TN-AUD-BR-03, TN-AUD-BR-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Which data categories and format belong in the portability package, and how should third-party data be excluded?
### TN-566 — Allow staff to excuse a no-show

Area: NOS. Sources: TN-NOS-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Who may excuse a no-show, what evidence is required, and how does that affect borrowing restrictions?
### TN-569 — Substitute a component in a kit

Area: KIT. Sources: TN-KIT-BR-01, TN-KIT-BR-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Which substitute components are acceptable, who approves the swap, and how is the loan snapshot updated?
### TN-574 — Reschedule service automatically for urgent teaching use

Area: MNT. Sources: TN-MNT-BR-01, TN-MNT-BR-02.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Which maintenance can be postponed, who authorizes it, and how far may the service be deferred?
### TN-577 — Support pickup during a network outage

Area: OUT. Sources: TN-OUT-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- What local authorization, conflict handling, and synchronization guarantees are required for offline checkout?
### TN-578 — Reserve across a future semester boundary

Area: RSV. Sources: TN-RSV-BR-03, TN-RSV-BR-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Should semester-spanning reservations be permitted, and what duration exception applies to them?
### TN-583 — Rotate webhook signing secrets without downtime

Area: INT. Sources: TN-INT-WF-03, TN-INT-API-01.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- How long should old and new signing secrets overlap, and how will receivers identify the active secret?
### TN-586 — Record warranty repair claims

Area: MNT. Sources: TN-MNT-WF-02, TN-MNT-WF-03.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Which warranty eligibility fields and supplier claim process should ToolNest support?
### TN-587 — Move checkout to an unattended locker

Area: OUT. Sources: TN-OUT-BR-01, TN-OUT-WF-01.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- How should locker access verify identity and accessory condition without the currently required staff handover?
### TN-588 — Send a daily borrowing digest

Area: NTF. Sources: TN-NTF-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Which event types belong in the digest, at what cutoff time, and in which time zone?
### TN-593 — Escalate ignored approvals

Area: APR. Sources: TN-APR-WF-01.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- After what delay should a pending request escalate, and who is the department lead for each lab?
### TN-598 — Cancel all future bookings after repeated no-shows

Area: NOS. Sources: TN-NOS-BR-04, TN-NOS-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- How many no-shows trigger action, over which period, and should existing future reservations be cancelled?
### TN-608 — Let borrowers report a late arrival

Area: NOS. Sources: TN-NOS-WF-01, TN-NOS-ADR-01.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Does reporting a late arrival extend the pickup hold, and what limits or staff approval apply?
### TN-609 — Charge for a missing charger

Area: DAM. Sources: TN-DAM-WF-04, TN-DAM-BR-02.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Who decides liability and replacement value, and what appeal process applies before a charge is assessed?
### TN-610 — Onboard visiting researchers without university SSO

Area: SEC. Sources: TN-SEC-WF-04, TN-SEC-BR-01.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Who sponsors and verifies visiting accounts, and when must their access expire?
### TN-611 — Escalate long-overdue equipment to security

Area: OVD. Sources: TN-OVD-WF-02.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- What overdue duration triggers security escalation and what borrower information may be shared?
### TN-616 — Expose catalog entries to visitors

Area: CAT. Sources: TN-CAT-ADR-03.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Which asset fields and availability details may be visible to unauthenticated visitors?
### TN-621 — Accept equipment in an unattended drop box

Area: RET. Sources: TN-RET-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- What event establishes the authoritative return time, and what evidence must the drop box capture?
### TN-631 — Allow borrowers to undo a cancellation

Area: CAN. Sources: TN-CAN-BR-02, TN-CAN-ADR-01.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- How long is cancellation undo available, and what happens if someone else has already acquired the released interval?
### TN-634 — Allow research-loan extension exceptions

Area: EXT. Sources: TN-EXT-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- What limits and approver permissions apply to research-loan extension exceptions?
### TN-642 — Pseudonymize completed loan histories

Area: AUD. Sources: TN-AUD-BR-04, TN-AUD-ADR-03.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Which identifiers should be removed or replaced, and what reidentification risk and retention rules apply to research history?
### TN-647 — Prioritize accessibility accommodation requests

Area: WAI. Sources: TN-WAI-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- What priority ordering applies to accommodation requests, and who authorizes that status?
### TN-650 — Let staff extend several loans in one action

Area: EXT. Sources: TN-EXT-BR-01, TN-EXT-API-01.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Who can perform a course-wide extension and should one conflicting loan block the entire operation?
### TN-658 — Forecast future equipment demand

Area: RPT. Sources: TN-RPT-ADR-02, TN-RPT-BR-01.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- What forecast horizon, aggregation level, and error measure are required for demand prediction?
### TN-668 — Require stronger verification for sensitive actions

Area: SEC. Sources: TN-SEC-ADR-01, TN-SEC-BR-01.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Which actions require step-up verification and what identity-provider assurance level is sufficient?
### TN-673 — Offer a different interval to waiting borrowers

Area: WAI. Sources: TN-WAI-BR-01, TN-WAI-ADR-02.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- What time flexibility may borrowers specify and how should alternative intervals be ranked?
### TN-676 — Replay historical webhook events

Area: INT. Sources: TN-INT-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Who may authorize replay and what maximum historical range and event filters are supported?
### TN-678 — Reserve an extension in advance

Area: EXT. Sources: TN-EXT-BR-03, TN-EXT-ADR-03.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Does an extension option block availability, and when must the borrower exercise or release it?
### TN-679 — Introduce equipment utilization percentages

Area: RPT. Sources: TN-RPT-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- What numerator, denominator, and maintenance-time treatment define equipment utilization?
### TN-681 — Book a weekly series

Area: RSV. Sources: TN-RSV-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- If one occurrence conflicts, should the whole recurring series fail or should the available occurrences be booked?
### TN-683 — Restore retired equipment

Area: CAT. Sources: TN-CAT-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- What approval and inspection steps are required to reactivate a retired unit?
### TN-685 — Let borrowers dispute inspection results

Area: RET. Sources: TN-RET-WF-03, TN-RET-ADR-03.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- What is the dispute window, who adjudicates it, and does a dispute pause incident handling?
### TN-687 — Let borrowers pause waiting-list offers

Area: WAI. Sources: TN-WAI-BR-02, TN-WAI-BR-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Does a paused entry retain its original joinedAt, and how is a pause started and ended?
### TN-690 — Automate refresher course enrollment

Area: TRN. Sources: TN-TRN-WF-01, TN-TRN-WF-03.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Which course system and course-selection rules should automatic refresher enrollment use?
### TN-692 — Add quiet hours for optional email

Area: NTF. Sources: TN-NTF-BR-02, TN-NTF-API-03.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- What quiet-hour configuration is supported and should deferred messages be combined or sent individually?
### TN-695 — Accept certificates from partner universities

Area: TRN. Sources: TN-TRN-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Which external issuers and certificate verification criteria are accepted?
### TN-696 — Reserve by equipment model

Area: RSV. Sources: TN-RSV-ADR-03.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- When and by what policy should the system assign a physical unit to a model-level request?
### TN-698 — Let borrowers upload counter-evidence

Area: DAM. Sources: TN-DAM-WF-03, TN-DAM-WF-04.

Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.

- Who can view borrower counter-evidence, when can it be submitted, and who adjudicates a disputed incident?

## partially_resolved

### TN-510 — Add push notifications for existing events

Area: NTF. Sources: TN-NTF-BR-01, TN-NTF-WF-03.

Use the existing event recipients and per-channel deduplication; device and consent behavior is unspecified.

- How are push devices registered and revoked, and can borrowers disable push independently of email?
### TN-526 — Prioritize the incident queue

Area: DAM. Sources: TN-DAM-BR-03.

Preserve safety blocks; the queue urgency scale is not defined by the safety disposition rule.

- Which severity levels and tie-breakers determine incident queue priority?
### TN-544 — Show a notification delivery health panel

Area: NTF. Sources: TN-NTF-WF-02, TN-NTF-ADR-02.

Use IDs, attempt times, and response codes without exposing rendered email bodies; health thresholds need definition.

- What failure rate or queue age should mark delivery health as degraded?
### TN-545 — Show nearby equivalents for an unavailable camera

Area: CAT. Sources: TN-CAT-BR-01, TN-CAT-BR-02.

Suggestions must identify individual Active units; the definition of equivalence still needs a decision.

- Which attributes define an equivalent unit, and may suggestions include another lab?
### TN-554 — Show pickup deadlines on calendar cards

Area: NOS. Sources: TN-NOS-API-01, TN-NOS-WF-01.

Use pickupDeadlineAt and the owning lab time zone; the warning lead time is unspecified.

- How long before the pickup deadline should the warning appear?
### TN-555 — Show upcoming training problems before booking

Area: TRN. Sources: TN-TRN-BR-03, TN-TRN-FAQ-02, TN-TRN-WF-01.

Explain the checkout recheck and identify the affected category; renewal lead time is unspecified.

- How far before expiry should the renewal warning appear?
### TN-558 — Recover availability after a worker outage

Area: NOS. Sources: TN-NOS-BR-02, TN-NOS-ADR-03.

Record actual processing time separately and release intervals through expiry; summary grouping is not specified.

- Should the catch-up summary be grouped by lab, worker run, or calendar day, and who receives it?
### TN-562 — Offer alternatives after a slot conflict

Area: RSV. Sources: TN-RSV-WF-02.

Preserve the borrower's form and explain the conflict; automatic alternative ranking is not specified.

- How far ahead should alternative slots be searched, and how should they be ranked?
### TN-563 — Add setup time to reservations

Area: RSV. Sources: TN-RSV-BR-01, TN-RSV-API-04, TN-RSV-ADR-02.

Retain transactional overlap protection; ordinary bookings currently have no implicit buffer, so the requested setup policy is a change.

- Does setup time block time before pickup, after return, or both, and how long is each buffer?
### TN-573 — Display an overdue appeal action

Area: OVD. Sources: TN-OVD-WF-01, TN-OVD-API-03.

Retain the recorded overdue duration and distinguish the restriction reason; appeal handling is not specified.

- Who reviews an appeal, and does submitting one pause the overdue restriction?
### TN-575 — Upload several equipment photographs

Area: CAT. Sources: TN-CAT-BR-05, TN-CAT-FAQ-01.

JPEG and PNG are agreed formats. This ticket does not change per-file size behavior; clarify only the gallery size.

- What is the maximum number of photographs allowed per asset?
### TN-596 — Add supplier service attachments

Area: MNT. Sources: TN-MNT-BR-03, TN-MNT-API-02.

A supplier report cannot replace the checklist and attestation; its permitted file types and size are undecided.

- Which file types and maximum size are allowed for supplier service reports?
### TN-597 — Add a transfer delay alert

Area: XFR. Sources: TN-XFR-BR-02, TN-XFR-WF-02.

InTransit units remain unavailable and transfer timestamps are distinct; the lateness rule needs definition.

- What planned-versus-actual timestamp and tolerance determine that a transfer is late?
### TN-600 — Add a cancellation survey

Area: CAN. Sources: TN-CAN-WF-03.

Keep actor, cancellation time, and recorded reason; the optional survey content and storage period are undecided.

- Which survey questions are required and how long should responses be retained?
### TN-601 — Auto-close low-risk inspections

Area: RET. Sources: TN-RET-BR-03, TN-RET-BR-04.

Every required accessory still needs a result; automatic clean-condition classification has no defined eligibility rules.

- Which categories qualify for automatic inspection and what evidence establishes a clean condition?
### TN-603 — Send repeated reminders for late equipment

Area: OVD. Sources: TN-OVD-API-04, TN-OVD-WF-04.

Use unique reminder stages and recheck receipt before publishing; repeat cadence is undefined.

- What is the repeat reminder cadence and maximum number of reminders?
### TN-618 — Show estimated repair completion to borrowers

Area: MNT. Sources: TN-MNT-BR-01, TN-MNT-WF-03.

Continue enforcing service blocks; estimate source, confidence, and borrower presentation need a decision.

- Who supplies repair estimates and how should unknown or missed estimates be displayed?
### TN-619 — Track temperature during sensitive equipment movement

Area: XFR. Sources: TN-XFR-ADR-02, TN-XFR-WF-02.

Retain append-only custody events; environmental measurement thresholds and sensor integration are undecided.

- Which sensor source, sampling interval, and temperature thresholds apply to sensitive transfers?
### TN-623 — Provide rejection reason templates

Area: APR. Sources: TN-APR-BR-03, TN-APR-API-03.

A nonempty reason of at most 500 characters is required; the standard reason set is undecided.

- Which standard rejection reasons should be offered, and may managers edit their wording?
### TN-630 — Explain which kit component is unavailable

Area: KIT. Sources: TN-KIT-BR-03, TN-KIT-API-02.

Commit no partial booking and return KIT_COMPONENT_UNAVAILABLE; disclosure detail needs a decision.

- Should borrowers see the conflicting component identity, just its category, or a generic kit-unavailable message?
### TN-633 — Create a training officer dashboard

Area: TRN. Sources: TN-TRN-API-01, TN-TRN-API-04.

Training officers may inspect eligibility reasons; urgency is not an established ranking.

- How should renewal urgency be calculated and which borrowers belong in the dashboard?
### TN-636 — Export incident records for an internal committee

Area: DAM. Sources: TN-DAM-ADR-01, TN-DAM-BR-04, TN-DAM-ADR-02.

Keep the append-only evidence history and enforce incident-reader access; committee export content needs definition.

- Which committee roles may export incidents and which borrower fields must be omitted or pseudonymized?
### TN-637 — Compare labs across a shared local date range

Area: RPT. Sources: TN-RPT-BR-03, TN-RPT-WF-01.

Respect lab grants and IANA conversions; a shared cross-lab date interpretation needs a decision.

- Should the comparison use each lab's local dates or one chosen reference time zone?
### TN-639 — Alert when an audit retention run fails

Area: AUD. Sources: TN-AUD-API-04.

Report aggregate counts without duplicating deleted bodies; failure and alert thresholds need definition.

- How many failed or delayed retention runs trigger an alert, and which operations destination receives it?
### TN-644 — Search audit events by staff display name

Area: AUD. Sources: TN-AUD-BR-02, TN-AUD-BR-01.

Enforce audit_reader and retain stable actorId references; name-history matching is unspecified.

- Should name search use current directory names, names at event time, or both?
### TN-652 — Version kit definitions in the catalog

Area: KIT. Sources: TN-KIT-BR-04, TN-KIT-API-03.

Do not alter existing loan snapshots; historical definition retention and comparison scope are unspecified.

- How many definition versions should be retained and which fields should the comparison show?
### TN-653 — Add digital borrower acknowledgement

Area: OUT. Sources: TN-OUT-BR-02, TN-OUT-ADR-03.

Keep staff verification and avoid storing an ID document image; signature capture and retention are undecided.

- What form of acknowledgement is required, and how long should it be retained?
### TN-655 — Retry undelivered offer notifications

Area: WAI. Sources: TN-WAI-BR-03, TN-WAI-FAQ-02.

A hold belongs to the offer and reading a notification does not accept it; retries must not invent a new acceptance.

- May a notification failure extend the offer deadline, and if so by how much?
### TN-657 — Batch approve the inbox

Area: APR. Sources: TN-APR-API-01, TN-APR-API-02, TN-APR-WF-02.

Each approval must recheck authorization and request version; batch failure semantics need a decision.

- Should a batch fail as a whole or return independent results when one request is stale or unauthorized?
### TN-659 — Offer a shorter extension when the requested end conflicts

Area: EXT. Sources: TN-EXT-BR-03, TN-EXT-FAQ-03.

Protect the next reservation and leave the loan unchanged on conflict; the fallback suggestion needs a product rule.

- What minimum extra duration makes a shorter extension worth suggesting, and should the borrower confirm it?
### TN-660 — Add a webhook failure escalation

Area: INT. Sources: TN-INT-WF-02.

Retain attempt timestamps and response status; escalation cadence and ownership are not defined.

- What consecutive-failure threshold triggers escalation and how is the integration owner selected?
### TN-661 — Offer unit substitution at pickup

Area: OUT. Sources: TN-OUT-BR-04, TN-OUT-API-03, TN-OUT-FAQ-02.

Do not silently swap the unit; retain WRONG_ASSET until an explicit substitution is approved.

- Who can authorize a substitution and which equivalence and availability checks must it pass?
### TN-663 — Expose an event preview when creating subscriptions

Area: INT. Sources: TN-INT-BR-02, TN-INT-WF-01.

The preview must use the documented envelope and omit borrower names and emails; sample coverage is unspecified.

- Which event types require sample payloads and should samples be synthetic or derived from redacted live events?
### TN-665 — Remind borrowers about extension eligibility

Area: EXT. Sources: TN-EXT-BR-01, TN-EXT-BR-02.

Only an own Open loan before dueAt is eligible and only one ordinary extension is allowed; reminder timing needs a decision.

- When should the extension reminder be sent and through which channel?
### TN-666 — Preview role changes before saving

Area: SEC. Sources: TN-SEC-BR-02, TN-SEC-API-01.

Compute effective permissions from lab-scoped grants; risky combinations are not defined.

- Which grant combinations should be flagged and should a flagged edit be blocked or merely warned about?
### TN-667 — Schedule the existing completed-loans export

Area: RPT. Sources: TN-RPT-BR-01, TN-RPT-WF-02.

Keep receipt-based inclusion and current access checks; scheduling and delivery are not established.

- What schedule and time zone apply, and should the email contain an attachment or an authorized download link?
### TN-669 — Explain access denial in the staff interface

Area: SEC. Sources: TN-SEC-WF-03, TN-SEC-WF-02.

Distinguish unauthenticated from insufficient permissions without returning protected data; recovery routing needs definition.

- Should a 403 screen offer a grant request, a lab switch, or contact details, and where should each action lead?
### TN-670 — Show waiting-list position estimates

Area: WAI. Sources: TN-WAI-BR-02.

The queue order has a documented tie-breaker; an expected-wait calculation is not defined.

- How should expected waiting time account for eligibility changes and future cancellations?
### TN-691 — Notify staff about unfinished inspections

Area: RET. Sources: TN-RET-BR-02.

Preserve the inspection availability block; backlog escalation thresholds and recipients need definition.

- What backlog size or age triggers escalation, and which staff receive it?
### TN-693 — Suggest an alternative when staff cancel

Area: CAN. Sources: TN-CAN-BR-04, TN-CAN-WF-02.

Include the staff reason in the borrower notification; alternative selection and commitment need definition.

- Which units qualify as alternatives and should the substitute be held or only suggested?

## conflicting_documentation

### TN-505 — Add a triage due date to new incidents

Area: DAM. Sources: TN-DAM-BR-05, TN-DAM-FAQ-01.

The active rule requires 1 business day and the FAQ allows 2 business days for triage.

- Should new incidents be triaged within 1 or 2 business days?
### TN-521 — Enforce the supported size of a kit

Area: KIT. Sources: TN-KIT-BR-05, TN-KIT-FAQ-01.

The kit rule caps required tracked components at 12 while the FAQ allows 16.

- Should a kit support at most 12 or 16 required tracked units?
### TN-522 — Enable pickup shortly before a booking starts

Area: OUT. Sources: TN-OUT-BR-05, TN-OUT-FAQ-01.

The checkout rules allow 15 minutes early, but the active FAQ allows 30 minutes.

- Should normal early collection begin 15 or 30 minutes before the reservation start?
### TN-527 — Expire unattended approval requests

Area: APR. Sources: TN-APR-BR-05, TN-APR-FAQ-01.

The current approval rules state 24 hours and the FAQ states 48 hours for the same undecided requests.

- Should undecided approval requests expire after 24 or 48 hours?
### TN-538 — Expire completed REST idempotency records

Area: INT. Sources: TN-INT-BR-05, TN-INT-FAQ-01.

The REST rule retains idempotency records for 24 hours and the FAQ promises 48 hours.

- Should REST idempotency records be retained for 24 or 48 elapsed hours?
### TN-549 — Show when a return inspection is due

Area: RET. Sources: TN-RET-BR-05, TN-RET-FAQ-01.

One active source requires inspection within 4 staffed hours and the other allows 8 staffed hours.

- Should the inspection deadline be 4 or 8 staffed operating hours after receipt?
### TN-559 — Expire staff sessions after inactivity

Area: SEC. Sources: TN-SEC-BR-05, TN-SEC-FAQ-01.

The active session rule expires after 30 minutes and the FAQ allows 45 minutes after the same last request.

- Should inactive sessions expire after 30 or 45 minutes?
### TN-564 — Calculate the pickup deadline for uncollected reservations

Area: NOS. Sources: TN-NOS-BR-05, TN-NOS-FAQ-01.

The active expiry rule uses 30 elapsed minutes and the FAQ promises 45 elapsed minutes.

- Should normal pickup expire 30 or 45 elapsed minutes after startAt?
### TN-580 — Calculate the next preventive service date

Area: MNT. Sources: TN-MNT-BR-05, TN-MNT-FAQ-01.

The maintenance rules specify 90 calendar days while the FAQ specifies 120 calendar days.

- Should preventive service be due after 90 or 120 calendar days?
### TN-595 — Delete ordinary audit events after their retention window

Area: AUD. Sources: TN-AUD-BR-05, TN-AUD-FAQ-01.

The ordinary retention rule is 180 calendar days and the FAQ says 365 calendar days.

- Should ordinary operational audit events be retained for 180 or 365 calendar days?
### TN-649 — Schedule the first overdue email

Area: OVD. Sources: TN-OVD-BR-05, TN-OVD-FAQ-01.

The overdue rules specify 2 elapsed hours and the FAQ specifies 4 elapsed hours after dueAt.

- Should the first overdue email be scheduled 2 or 4 elapsed hours after dueAt?
### TN-651 — Validate photograph sizes in the asset editor

Area: CAT. Sources: TN-CAT-BR-05, TN-CAT-FAQ-01.

The active catalog rule specifies 8 MiB while the staff FAQ specifies 10 MiB; neither is marked superseded.

- Should the common maximum photograph size be 8 MiB or 10 MiB?
### TN-654 — Validate the reason in self-service cancellation

Area: CAN. Sources: TN-CAN-BR-05, TN-CAN-FAQ-01.

The rule requires at least 10 characters, while the FAQ explicitly permits an empty self-service reason.

- Should self-service cancellation require a reason of at least 10 characters or allow no reason?
### TN-671 — Flag transfer deliveries awaiting acknowledgement

Area: XFR. Sources: TN-XFR-BR-05, TN-XFR-FAQ-01.

The rule specifies 4 staffed operating hours and the FAQ allows 8 staffed operating hours.

- Should destination acknowledgement be due within 4 or 8 staffed operating hours after delivery?
### TN-672 — Cap the length of an ordinary equipment booking

Area: RSV. Sources: TN-RSV-BR-03, TN-RSV-FAQ-01.

The active rules cap ordinary bookings at 72 hours, while the FAQ allows 96 hours.

- Which maximum duration should ordinary reservations enforce: 72 or 96 hours?
### TN-674 — Limit the extra time requested for a loan

Area: EXT. Sources: TN-EXT-BR-05, TN-EXT-FAQ-01.

The extension rule allows 24 additional hours while the FAQ allows 48 additional hours.

- Should the ordinary extension cap be 24 or 48 additional hours?
### TN-680 — Handle training expiry at the collection instant

Area: TRN. Sources: TN-TRN-BR-02, TN-TRN-FAQ-01.

The rule excludes the expiry instant, while the active FAQ includes that exact instant.

- Should a checkout exactly at validUntil be accepted or rejected?
### TN-689 — Apply the ordinary report export row limit

Area: RPT. Sources: TN-RPT-BR-05, TN-RPT-FAQ-01.

The reporting rule caps data rows at 10000 and the FAQ allows 25000, both excluding the header.

- Should an ordinary CSV report allow at most 10000 or 25000 data rows?
### TN-694 — Release an unanswered waiting-list offer

Area: WAI. Sources: TN-WAI-BR-05, TN-WAI-FAQ-01.

The active waiting-list rules specify 20 minutes while the FAQ specifies 30 minutes.

- Should an offer expire after 20 or 30 minutes from creation?
### TN-699 — Stop email retries when the retry budget is exhausted

Area: NTF. Sources: TN-NTF-BR-05, TN-NTF-FAQ-01.

The rule allows 3 retries after the initial attempt and the FAQ allows 5 retries after the initial attempt.

- Should a transient email failure receive at most 3 or 5 retries after the initial attempt?

## already_clear

### TN-507 — Add a missing reservation form test

Area: RSV. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-515 — Rename maintenance completion action

Area: MNT. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-519 — Correct the eligibility help link

Area: TRN. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-528 — Use precise kit checklist headings

Area: KIT. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-531 — Rename the asset tag field label

Area: CAT. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-539 — Format extension timestamps consistently in history

Area: EXT. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-557 — Remove a misleading permission tooltip

Area: SEC. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-590 — Show audit event identifiers as copyable text

Area: AUD. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-592 — Make cancellation confirmation explicit

Area: CAN. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-602 — Correct the overdue duration unit label

Area: OVD. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-614 — Document the existing webhook header names

Area: INT. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-617 — Show a clear waiting-list leave action

Area: WAI. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-627 — Clarify the correction entry heading

Area: DAM. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-638 — Make unread notification text accessible

Area: NTF. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-643 — Expose the existing report truncation flag

Area: RPT. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-645 — Show the existing rejection reason in details

Area: APR. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-646 — Add an empty state to the return queue

Area: RET. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-648 — Distinguish transfer timestamps in details

Area: XFR. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-664 — Clarify the expired booking badge

Area: NOS. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.

### TN-688 — Keep scanner focus after a successful lookup

Area: OUT. Sources: Ticket text only.

The ticket specifies a narrow, testable change. No clarification or additional scope is needed.
