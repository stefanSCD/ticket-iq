"""Authored fictional content. This file includes answer keys: never index it for RAG."""


def case(category, summary, description, refs, recommendation, questions=(), explicit_gap=False):
    return dict(category=category, summary=summary, description=description,
                refs=refs.split(), recommendation=recommendation,
                questions=list(questions), explicit_gap=explicit_gap)


def R(summary, description, refs, recommendation):
    return case('resolved_by_documentation', summary, description, refs, recommendation)


def U(summary, description, refs, question, explicit=False):
    return case('unresolved', summary, description, refs,
                'Clarify the requested behavior before adding acceptance criteria; the available sources do not decide it.',
                [question], explicit)


def P(summary, description, refs, recommendation, question):
    return case('partially_resolved', summary, description, refs, recommendation, [question])


def C(summary, description, refs, recommendation, question):
    return case('conflicting_documentation', summary, description, refs, recommendation, [question])


def A(summary, description):
    return case('already_clear', summary, description, '',
                'The ticket specifies a narrow, testable change. No clarification or additional scope is needed.')


AREAS = [
    dict(code='CAT', name='Catalog and asset lifecycle', component='Asset Catalog',
         context='A department can own several physical units of the same equipment model. The catalog must distinguish a model description from a uniquely tracked unit; changing a display label must never change a reservation reference.',
         br=[
             'Each physical unit has an immutable asset UUID and a university-wide unique asset tag; display names are not identifiers.',
             'Only Active units can enter a new reservation; Retired units remain readable on existing loans and audit entries.',
             'A lab manager may retire a unit only when it has no open loan, future confirmed reservation, or outstanding maintenance job.',
             'Model-level specification edits do not overwrite a unit-specific condition note.',
             'Catalog photographs accept JPEG and PNG only, with a maximum size of 8 MiB per file.'
         ],
         wf=[
             'The asset creation form requires model, owning lab, asset tag, serial number, and initial condition; serial number may be explicitly recorded as unknown.',
             'Catalog filters combine lab, equipment category, and lifecycle state using AND semantics; the default lifecycle filter is Active.',
             'A retirement attempt displays the blocking loan, reservation, or maintenance reference to an authorized lab manager.',
             'Reactivation of a retired unit is an open product decision; no reactivation workflow is approved.'
         ],
         api=[
             'POST /v1/assets assigns the UUID server-side and returns 409 ASSET_TAG_EXISTS when the asset tag is already used.',
             'PATCH /v1/assets/{id} accepts displayName and conditionNote; assetId and assetTag are immutable after creation.',
             'POST /v1/assets/{id}/retire returns 409 ASSET_IN_USE when any retirement precondition fails.',
             'GET /v1/assets excludes Retired units unless lifecycle=all is explicitly requested by an authorized staff member.'
         ],
         adr=[
             'Asset UUIDs are foreign keys in reservations and loans so that a renamed model cannot detach its transaction history.',
             'Retirement is a lifecycle transition rather than a physical database deletion.',
             'Photo objects are stored privately; catalog responses return short-lived authorized download links.'
         ],
         faq=[
             'The staff photo uploader accepts JPEG and PNG files up to 10 MiB per file.',
             'Two units may share a model name; resolve a checkout lookup using the asset tag or UUID.',
             'If a retirement is blocked, complete or cancel the linked work through its owning workflow rather than deleting the asset.'
         ],
         cases=[
             R('Keep loan history after a camera is retired', 'The photography lab needs to retire an old camera. Ensure its previous loans still appear in staff history.', 'BR2 ADR2', 'Retain the asset record and its historical references when moving it to Retired.'),
             R('Reject duplicate asset tags on import', 'The equipment registration screen currently creates two units with the same asset tag. Bring the create operation into line with the asset contract.', 'BR1 API1', 'Enforce university-wide tag uniqueness and return 409 ASSET_TAG_EXISTS for a duplicate.'),
             R('Explain why retirement is blocked', 'A lab manager gets a generic error when retiring a laptop that has a confirmed reservation for next week. Display an actionable explanation.', 'BR3 WF3 API3', 'Reject retirement with ASSET_IN_USE and show the blocking reservation reference to the authorized manager.'),
             U('Restore retired equipment', 'Some retired oscilloscopes have been refurbished. Add a way to put them back into circulation.', 'WF4', 'What approval and inspection steps are required to reactivate a retired unit?', True),
             U('Bulk import legacy serial numbers', 'Support importing a spreadsheet from the old inventory system where several rows contain the same manufacturer serial number.', 'WF1 BR1', 'Should duplicate manufacturer serial numbers be accepted, rejected, or flagged for review during import?'),
             U('Expose catalog entries to visitors', 'The outreach team wants prospective students to browse available equipment without signing in.', 'ADR3', 'Which asset fields and availability details may be visible to unauthenticated visitors?'),
             P('Show nearby equivalents for an unavailable camera', 'When the selected camera is unavailable, suggest equivalent units, including equipment in another lab.', 'BR1 BR2', 'Suggestions must identify individual Active units; the definition of equivalence still needs a decision.', 'Which attributes define an equivalent unit, and may suggestions include another lab?'),
             P('Upload several equipment photographs', 'Let lab managers attach a small gallery to an asset instead of a single photograph. Keep the supported formats.', 'BR5 FAQ1', 'JPEG and PNG are agreed formats. This ticket does not change per-file size behavior; clarify only the gallery size.', 'What is the maximum number of photographs allowed per asset?'),
             C('Validate photograph sizes in the asset editor', 'Apply the supported per-file photograph size limit when a manager adds an image to an asset. Show a helpful validation message for an oversized file.', 'BR5 FAQ1', 'The active catalog rule specifies 8 MiB while the staff FAQ specifies 10 MiB; neither is marked superseded.', 'Should the common maximum photograph size be 8 MiB or 10 MiB?'),
             A('Rename the asset tag field label', 'On the asset details screen, replace the visible label "Inventory code" with "Asset tag". Keep the stored field and API payload unchanged. Verify the label in both read and edit views.')
         ]),
    dict(code='RSV', name='Reservation intervals and availability', component='Reservations',
         context='Borrowers reserve a physical unit for a bounded interval. Availability is computed from committed reservations and operational blocks, so the calendar and the create endpoint must agree when two people compete for the same unit.',
         br=[
             'Reservation intervals are half-open: [startAt, endAt); one booking may start exactly when the preceding booking ends.',
             'Confirmed and AwaitingApproval reservations block their assigned unit; Draft and Cancelled reservations do not block availability.',
             'A normal reservation must last at least 30 minutes and no more than 72 hours.',
             'Reservation timestamps are stored as UTC instants and displayed in the owning lab time zone.',
             'A unit cannot be reserved across an active maintenance block.'
         ],
         wf=[
             'The availability calendar previews a selected unit and interval, but creation performs a fresh conflict check before commitment.',
             'When another borrower wins a slot during submission, preserve the losing borrower\'s form values and show that the slot is no longer available.',
             'The server rejects an endAt that is not later than startAt before evaluating availability.',
             'Recurring reservations are under discussion; the team has not chosen all-or-nothing versus partial series acceptance.'
         ],
         api=[
             'POST /v1/reservations requires assetId, startAt, endAt, and purpose; an overlap returns 409 RESERVATION_CONFLICT.',
             'GET /v1/availability accepts explicit UTC offsets in both interval parameters and returns blocking intervals in UTC.',
             'A successful create returns 201 with the reservation ID and its initial state; clients must not infer success from an availability preview.',
             'Reservation conflicts are enforced inside the same database transaction that creates the reservation.'
         ],
         adr=[
             'PostgreSQL exclusion constraints protect unit intervals from concurrent overlapping writes.',
             'The application expands no implicit cleaning buffer around an ordinary reservation.',
             'A reservation owns one assigned unit; substitution is an explicit operation rather than a change to the model name.'
         ],
         faq=[
             'Borrowers may reserve equipment for up to 96 hours in one ordinary reservation.',
             'A calendar preview is advisory; the submission result is authoritative when simultaneous requests compete.',
             'Adjacent bookings are allowed because the ending instant belongs only to the later interval.'
         ],
         cases=[
             R('Permit back-to-back bookings', 'A camera returned at 12:00 cannot currently be booked by the next borrower from 12:00. Correct the overlap check.', 'BR1 FAQ3', 'Treat the interval end as exclusive so adjacent bookings are accepted.'),
             R('Handle simultaneous requests for one unit', 'Two students submitted the same available interval and both received confirmation. Fix the race and give the loser useful feedback.', 'API1 API4 ADR1 WF2', 'Commit at most one booking, return RESERVATION_CONFLICT for the loser, and retain the entered form values.'),
             R('Block reservations during repair', 'The calendar is showing a soldering station as bookable while it has an active maintenance block. Align availability with reservation creation.', 'BR5 WF1', 'Exclude active maintenance intervals in the preview and recheck them during creation.'),
             U('Book a weekly series', 'Teaching assistants need to reserve the same camera every Tuesday for six weeks. Let them submit the series together.', 'WF4', 'If one occurrence conflicts, should the whole recurring series fail or should the available occurrences be booked?', True),
             U('Reserve by equipment model', 'A student should be able to request any laptop of a selected model without selecting a physical unit.', 'ADR3', 'When and by what policy should the system assign a physical unit to a model-level request?'),
             U('Reserve across a future semester boundary', 'Allow researchers to book an experiment that starts this semester and ends in the next one.', 'BR3 BR4', 'Should semester-spanning reservations be permitted, and what duration exception applies to them?'),
             P('Offer alternatives after a slot conflict', 'Keep the entered booking when the slot is lost, and offer another time automatically.', 'WF2', 'Preserve the borrower\'s form and explain the conflict; automatic alternative ranking is not specified.', 'How far ahead should alternative slots be searched, and how should they be ranked?'),
             P('Add setup time to reservations', 'The media lab needs a configurable setup period around camera reservations. Keep normal overlap protection.', 'BR1 API4 ADR2', 'Retain transactional overlap protection; ordinary bookings currently have no implicit buffer, so the requested setup policy is a change.', 'Does setup time block time before pickup, after return, or both, and how long is each buffer?'),
             C('Cap the length of an ordinary equipment booking', 'Enforce the ordinary reservation duration limit when a borrower selects a long interval. The calendar and submission endpoint should both use the supported maximum.', 'BR3 FAQ1', 'The active rules cap ordinary bookings at 72 hours, while the FAQ allows 96 hours.', 'Which maximum duration should ordinary reservations enforce: 72 or 96 hours?'),
             A('Add a missing reservation form test', 'Add a regression test that submits startAt=2026-11-09T10:00:00Z and endAt=2026-11-09T09:00:00Z. Assert HTTP 422 and fieldErrors.endAt.code=END_BEFORE_START; no reservation row is created. The endpoint already returns this payload.')
         ]),
    dict(code='TRN', name='Training and borrower eligibility', component='Eligibility',
         context='Some tools require a current training certificate. Eligibility is evaluated for the borrower, equipment category, and intended checkout instant rather than being a permanent flag on the account.',
         br=[
             'A restricted equipment category requires a certificate whose category matches the unit and whose validUntil is later than the checkout instant.',
             'A certificate expiring exactly at checkout time is invalid.',
             'Creating a reservation checks current eligibility; checkout checks eligibility again using the actual checkout instant.',
             'A suspended borrower cannot create reservations or check out equipment even when their training certificate is valid.',
             'Only a training officer can record or revoke a training certificate; a lab manager role alone does not grant that permission.'
         ],
         wf=[
             'The borrower sees the missing training category and an instruction to contact a training officer when eligibility fails.',
             'Certificate revocation takes effect for subsequent eligibility checks without waiting for a user session to expire.',
             'The training officer records course reference, category, completedAt, validUntil, and the borrower ID.',
             'Cross-university certificate equivalence is not approved; accepted external issuers and verification rules remain undecided.'
         ],
         api=[
             'GET /v1/eligibility requires borrowerId, assetId, and checkoutAt and returns eligible plus machine-readable blocking reasons.',
             'POST /v1/training-certificates requires the training_officer grant and records the acting staff ID.',
             'Checkout fails with 403 TRAINING_REQUIRED when a required certificate is missing or expired.',
             'GET /v1/me/eligibility exposes the signed-in borrower\'s own reasons; other borrowers require the training_officer grant.'
         ],
         adr=[
             'Eligibility reads certificate state from PostgreSQL at the action boundary; it is not copied into a long-lived access token.',
             'Training categories are stable IDs shared by equipment models and certificates.',
             'Training checks do not bypass account suspension checks.'
         ],
         faq=[
             'A certificate remains usable through the end of its validUntil instant, including a checkout exactly at that instant.',
             'A reservation does not guarantee later eligibility if training expires before physical pickup.',
             'A lab manager who also holds the training_officer grant can record training; the manager role on its own is insufficient.'
         ],
         cases=[
             R('Recheck training at collection', 'A student reserved a soldering station while certified, but the certificate expired before collection. Prevent checkout in that situation.', 'BR3 API3 FAQ2', 'Recheck training at actual checkout and reject expired training with TRAINING_REQUIRED.'),
             R('Stop managers issuing certificates without training access', 'A lab manager can currently mark any borrower trained. Limit certificate creation to the intended staff permission.', 'BR5 API2 FAQ3', 'Require training_officer even when the actor is a lab manager, and record the acting staff ID.'),
             R('Apply revocation without requiring sign-out', 'A revoked certificate still works until the student signs in again. Make the next eligibility check use the revocation immediately.', 'WF2 ADR1', 'Read current certificate state at the action boundary so revocation affects subsequent checks.'),
             U('Accept certificates from partner universities', 'Visiting researchers should be able to use safety training issued by their home university.', 'WF4', 'Which external issuers and certificate verification criteria are accepted?', True),
             U('Grace period after training expiry', 'Teaching staff want borrowers to keep collecting equipment briefly after their training expires.', 'BR1 BR3', 'Is a training-expiry grace period permitted, for which users and equipment, and for how long?'),
             U('Automate refresher course enrollment', 'When training expires, automatically enroll the borrower in a refresher course.', 'WF1 WF3', 'Which course system and course-selection rules should automatic refresher enrollment use?'),
             P('Show upcoming training problems before booking', 'Warn borrowers whose certificates will expire before pickup, and tell them how early to renew.', 'BR3 FAQ2 WF1', 'Explain the checkout recheck and identify the affected category; renewal lead time is unspecified.', 'How far before expiry should the renewal warning appear?'),
             P('Create a training officer dashboard', 'Show training officers the missing eligibility reasons and let them sort borrowers by urgency.', 'API1 API4', 'Training officers may inspect eligibility reasons; urgency is not an established ranking.', 'How should renewal urgency be calculated and which borrowers belong in the dashboard?'),
             C('Handle training expiry at the collection instant', 'Add the checkout eligibility check for a certificate whose validUntil is exactly the actual handover time. Use the established expiry boundary.', 'BR2 FAQ1', 'The rule excludes the expiry instant, while the active FAQ includes that exact instant.', 'Should a checkout exactly at validUntil be accepted or rejected?'),
             A('Correct the eligibility help link', 'On the TRAINING_REQUIRED error panel, change the link destination from /help/courses-old to /help/training. Keep the link text "View training options". Verify keyboard activation and the destination URL.')
         ]),
    dict(code='APR', name='Reservation approval', component='Approvals',
         context='High-value equipment uses a staff approval gate. An approval belongs to a specific request version; it is neither a standing privilege for a borrower nor permission to ignore an availability conflict.',
         br=[
             'Equipment with requiresApproval=true creates an AwaitingApproval reservation and blocks its assigned interval while waiting.',
             'Approval requires a lab_manager grant for the owning lab; a borrower cannot approve their own reservation.',
             'Rejection records a mandatory reason, transitions the reservation to Rejected, and releases its interval.',
             'Changing the assigned asset or reservation interval invalidates an existing approval and returns the request to AwaitingApproval.',
             'An approval request expires 24 hours after creation if no decision has been recorded.'
         ],
         wf=[
             'The approval inbox lists the borrower, purpose, asset, requested interval, and request version for the manager\'s labs.',
             'Before approving, the server rechecks the actor\'s grant and verifies that the request version has not changed.',
             'Approval and rejection both append an audit event with the decision maker and the request version.',
             'Delegation to a temporary approver is being explored; delegation scope and expiry have not been agreed.'
         ],
         api=[
             'POST /v1/reservations/{id}/approve requires If-Match with the current request version.',
             'A stale approval attempt returns 412 VERSION_MISMATCH without changing the reservation.',
             'POST /v1/reservations/{id}/reject requires a nonempty reason of at most 500 characters.',
             'Self-approval returns 403 SELF_APPROVAL_FORBIDDEN even if the borrower also holds the required manager grant.'
         ],
         adr=[
             'Approvals are versioned decisions stored with the reservation, not mutable boolean fields on user accounts.',
             'A transaction releases the interval at the same time that rejection becomes visible.',
             'The expiry worker uses server time and a compare-and-set transition so a completed approval cannot also expire.'
         ],
         faq=[
             'Undecided approval requests remain open for 48 hours before they expire.',
             'Changing only a borrower-facing display note does not invalidate approval; changing the asset or interval does.',
             'Managers cannot approve their own borrowing request; another manager for that lab must decide it.'
         ],
         cases=[
             R('Prevent self-approval by managers', 'A manager requested a camera for personal use and approved it from the same account. Enforce the approval separation rule.', 'BR2 API4', 'Reject self-approval with SELF_APPROVAL_FORBIDDEN regardless of the actor\'s manager grant.'),
             R('Invalidate approval when booking dates change', 'Approved reservations currently stay approved after the borrower changes the collection date. Restore the intended approval state.', 'BR4 FAQ2', 'Return changed asset or interval requests to AwaitingApproval; display-note edits alone do not invalidate approval.'),
             R('Reject approval from a stale browser tab', 'A manager opened the inbox before a booking was edited and approved the old version. Protect the decision against stale data.', 'WF2 API1 API2', 'Require the current request version and return 412 VERSION_MISMATCH without mutation for a stale decision.'),
             U('Delegate approvals during leave', 'A lab manager needs to delegate the inbox while away for a conference.', 'WF4', 'Who may receive approval delegation, for which labs, and when does it expire?', True),
             U('Require two approvals for premium equipment', 'The department wants particularly expensive devices to require a second staff approval.', 'BR2 ADR1', 'Which devices require two approvals, and must the approvers have different roles?'),
             U('Escalate ignored approvals', 'Requests that nobody handles should be sent to a department lead.', 'WF1', 'After what delay should a pending request escalate, and who is the department lead for each lab?'),
             P('Provide rejection reason templates', 'Keep the rejection reason mandatory but let managers pick a standard reason to speed up review.', 'BR3 API3', 'A nonempty reason of at most 500 characters is required; the standard reason set is undecided.', 'Which standard rejection reasons should be offered, and may managers edit their wording?'),
             P('Batch approve the inbox', 'Let a manager approve several waiting requests together while retaining protection against stale edits.', 'API1 API2 WF2', 'Each approval must recheck authorization and request version; batch failure semantics need a decision.', 'Should a batch fail as a whole or return independent results when one request is stale or unauthorized?'),
             C('Expire unattended approval requests', 'Add scheduled cleanup for approval requests that have waited beyond their allowed lifetime without a manager decision. Preserve the request in history after expiry.', 'BR5 FAQ1', 'The current approval rules state 24 hours and the FAQ states 48 hours for the same undecided requests.', 'Should undecided approval requests expire after 24 or 48 hours?'),
             A('Show the existing rejection reason in details', 'In the reservation details view, render the stored rejectionReason under a "Reason for rejection" heading when state=Rejected. Hide the entire section for other states. Display it as plain text and preserve line breaks.')
         ]),
    dict(code='OUT', name='Pickup and checkout', component='Checkout',
         context='Physical handover creates a loan from a confirmed reservation. Staff scan a unit label and verify the borrower rather than treating possession of a reservation number as sufficient identity proof.',
         br=[
             'Checkout requires a Confirmed reservation, its assigned asset, a present borrower, and a lab_technician or lab_manager grant for the pickup lab.',
             'The technician verifies the borrower using the university ID and records the result before committing checkout.',
             'A successful checkout atomically changes the reservation to Collected and creates one Open loan.',
             'The scanned asset must match the reservation\'s assigned unit; mismatch does not silently substitute another unit.',
             'Normal checkout can begin 15 minutes before the reservation start instant.'
         ],
         wf=[
             'The checkout screen shows the borrower name, assigned asset tag, accessories checklist, and current eligibility result.',
             'Staff confirm that every required accessory is present or record a pre-existing exception before handover.',
             'A failed identity verification leaves the reservation unchanged and creates no loan.',
             'Offline checkout has no approved synchronization or trust model; it is tracked as a future design decision.'
         ],
         api=[
             'POST /v1/checkouts requires reservationId, scannedAssetId, identityVerified=true, and an Idempotency-Key.',
             'A repeated checkout with the same actor, key, and payload returns the original loan; a changed payload returns 409 IDEMPOTENCY_MISMATCH.',
             'An asset mismatch returns 409 WRONG_ASSET and an eligibility failure creates no loan.',
             'The server uses actual server time for the checkout window; a client-provided timestamp cannot move that window.'
         ],
         adr=[
             'QR labels encode opaque asset UUIDs rather than borrower identifiers or authorization tokens.',
             'Checkout is one database transaction so a collected reservation cannot exist without its loan.',
             'A university ID verification is recorded as an attestation; ToolNest stores no image of the identity document.'
         ],
         faq=[
             'Equipment may be collected from 30 minutes before the reservation starts.',
             'Scanning a different unit does not replace the reservation assignment; ask staff to use the explicit substitution workflow.',
             'If the confirmation response is lost, retry the same checkout request with the same Idempotency-Key.'
         ],
         cases=[
             R('Prevent a loan when identity verification fails', 'The checkout form currently creates a loan even after staff report that the borrower ID did not match. Stop the handover transaction.', 'BR2 WF3', 'Require successful university ID verification; preserve the reservation and create no loan when verification fails.'),
             R('Handle lost checkout responses safely', 'At the pickup desk a timeout led the operator to submit checkout twice. Make the retry return the existing loan.', 'API1 API2 FAQ3', 'Reuse the same checkout idempotency key and payload so a retry returns the original loan.'),
             R('Reject scanning the wrong camera', 'Two identical camera models sit on the desk. Checkout accepted the unit that was not assigned to the booking.', 'BR4 API3 ADR1', 'Compare the scanned UUID with the assigned unit and return WRONG_ASSET instead of substituting silently.'),
             U('Support pickup during a network outage', 'The lab loses Wi-Fi intermittently. Allow technicians to complete handovers offline and sync them later.', 'WF4', 'What local authorization, conflict handling, and synchronization guarantees are required for offline checkout?', True),
             U('Let a colleague collect equipment', 'Researchers want a colleague to collect a reserved camera on their behalf.', 'BR1 BR2', 'Is proxy collection permitted, and what delegation and identity evidence must the proxy provide?'),
             U('Move checkout to an unattended locker', 'Allow borrowers to collect equipment from a locker without a technician present.', 'BR1 WF1', 'How should locker access verify identity and accessory condition without the currently required staff handover?'),
             P('Offer unit substitution at pickup', 'When staff scan another unit of the same model, offer a substitution action instead of only showing an error.', 'BR4 API3 FAQ2', 'Do not silently swap the unit; retain WRONG_ASSET until an explicit substitution is approved.', 'Who can authorize a substitution and which equivalence and availability checks must it pass?'),
             P('Add digital borrower acknowledgement', 'Preserve staff identity verification and ask the borrower to sign the checkout record.', 'BR2 ADR3', 'Keep staff verification and avoid storing an ID document image; signature capture and retention are undecided.', 'What form of acknowledgement is required, and how long should it be retained?'),
             C('Enable pickup shortly before a booking starts', 'Students sometimes reach the desk before their booking begins. Enable normal early collection within the approved pickup window and explain when they must wait.', 'BR5 FAQ1', 'The checkout rules allow 15 minutes early, but the active FAQ allows 30 minutes.', 'Should normal early collection begin 15 or 30 minutes before the reservation start?'),
             A('Keep scanner focus after a successful lookup', 'After a successful asset lookup on /staff/checkout, return focus to the input with id=asset-scan and select its full value. Do not clear the borrower selection. Verify this behavior using a keyboard-only interaction.')
         ]),
    dict(code='RET', name='Returns and condition inspection', component='Returns',
         context='A return records physical receipt separately from condition inspection. Staff need to stop the loan clock when equipment arrives without prematurely making an uninspected unit available to the next borrower.',
         br=[
             'Recording receipt changes an Open loan to ReturnedPendingInspection and records receivedAt using server time.',
             'A returned unit remains unavailable until staff finish its condition inspection.',
             'Inspection must record a condition result for the unit and a present or missing result for every required accessory.',
             'A clean inspection closes the loan and makes the unit available unless another reservation or maintenance block applies.',
             'A return inspection is due within 4 staffed operating hours after receipt.'
         ],
         wf=[
             'The return desk first scans the asset, confirms its open loan, and records receipt; condition inspection is a separate action.',
             'A missing accessory creates an incident linked to the loan and prevents a clean inspection result.',
             'Inspection notes distinguish damage observed at return from a condition exception recorded at checkout.',
             'Unattended drop-box receipt is proposed; the authoritative receipt timestamp and evidence requirements are not agreed.'
         ],
         api=[
             'POST /v1/loans/{id}/receive returns the receipt ID and receivedAt without marking the unit Active or available.',
             'POST /v1/return-inspections requires receiptId, conditionResult, and one result for each required accessory.',
             'A second receive action for a loan already received returns the existing receipt and does not change receivedAt.',
             'An incomplete accessories checklist returns 422 INCOMPLETE_INSPECTION and leaves the inspection unfinished.'
         ],
         adr=[
             'Receipt time is immutable; inspection completion time is a separate timestamp.',
             'The loan record keeps the checkout accessory list as a snapshot so later catalog edits do not change return obligations.',
             'A condition problem is routed through the incident workflow rather than overwriting the original checkout condition.'
         ],
         faq=[
             'Staff should complete a return inspection within 8 staffed operating hours after receiving the unit.',
             'A borrower has returned the unit when receipt is recorded even if staff inspect it later; inspection delay does not extend the loan.',
             'A scan repeated after receipt shows the original receipt time, not a new return time.'
         ],
         cases=[
             R('Keep uninspected returns out of availability', 'A returned camera is becoming bookable immediately when scanned at the desk, before staff inspect it.', 'BR1 BR2 API1', 'Record receipt as ReturnedPendingInspection and keep the unit unavailable until inspection completes.'),
             R('Use the checkout accessory snapshot at return', 'A catalog edit removed a charger while the laptop was on loan. The return checklist should still include what the borrower received.', 'ADR2 BR3', 'Build the return checklist from the loan\'s checkout accessory snapshot and require a result for every item.'),
             R('Preserve receipt time when staff rescan', 'A technician scanned the same return twice and the second scan made the borrower appear late.', 'API3 ADR1 FAQ3', 'Return the existing receipt on a repeated receive action and leave the original receivedAt unchanged.'),
             U('Accept equipment in an unattended drop box', 'Students want to return laptops after the staffed desk closes using a secure drop box.', 'WF4', 'What event establishes the authoritative return time, and what evidence must the drop box capture?', True),
             U('Let borrowers dispute inspection results', 'Add a way for a student to contest damage noted during the return inspection.', 'WF3 ADR3', 'What is the dispute window, who adjudicates it, and does a dispute pause incident handling?'),
             U('Route returns through a courier', 'Researchers working off campus need a courier return option.', 'WF1 ADR1', 'Does return occur at courier handover or lab receipt, and who bears responsibility while the parcel is in transit?'),
             P('Auto-close low-risk inspections', 'Keep full accessory checks, but automatically close returns from selected low-risk equipment categories.', 'BR3 BR4', 'Every required accessory still needs a result; automatic clean-condition classification has no defined eligibility rules.', 'Which categories qualify for automatic inspection and what evidence establishes a clean condition?'),
             P('Notify staff about unfinished inspections', 'Returned units should remain unavailable while awaiting inspection, and staff should receive escalations when a backlog grows.', 'BR2', 'Preserve the inspection availability block; backlog escalation thresholds and recipients need definition.', 'What backlog size or age triggers escalation, and which staff receive it?'),
             C('Show when a return inspection is due', 'Add an inspection due time to each returned unit in the staff queue. Calculate it from receipt using the normal staffed-hours inspection deadline.', 'BR5 FAQ1', 'One active source requires inspection within 4 staffed hours and the other allows 8 staffed hours.', 'Should the inspection deadline be 4 or 8 staffed operating hours after receipt?'),
             A('Add an empty state to the return queue', 'When the selected lab has zero returned units awaiting inspection, show "No returns awaiting inspection" and hide the inspection table. Retain the lab selector. Verify the zero-row and one-row cases.')
         ]),
    dict(code='EXT', name='Loan extensions', component='Loan Extensions',
         context='An extension modifies the due time of an existing loan. It must preserve the original reservation history and protect the next borrower from an overlapping use of the same physical unit.',
         br=[
             'A borrower can request an extension only for their own Open loan before its current dueAt.',
             'An ordinary loan may receive at most one approved extension.',
             'An extension must not overlap a confirmed reservation, an awaiting-approval reservation, or an active maintenance block.',
             'Extension approval updates loan.dueAt and records the prior dueAt without rewriting the original reservation interval.',
             'An ordinary extension may add at most 24 hours to the current dueAt.'
         ],
         wf=[
             'The extension screen shows the current due time and the requested new due time before submission.',
             'A failed extension preserves the current dueAt and shows the blocking reason without exposing another borrower\'s identity.',
             'The server rechecks availability inside the due-time update transaction.',
             'A separate research-loan extension exception has been requested, but its limits and authorized approvers remain undecided.'
         ],
         api=[
             'POST /v1/loans/{id}/extensions requires requestedDueAt and the current loan version.',
             'A past-due extension request returns 409 LOAN_ALREADY_OVERDUE.',
             'An overlapping extension returns 409 EXTENSION_CONFLICT without modifying the loan.',
             'An extension event records oldDueAt, newDueAt, actorId, and loanId.'
         ],
         adr=[
             'The availability constraint includes the occupied interval of an Open loan after its due time is extended.',
             'The approved-extension counter belongs to the loan, not to the borrower\'s lifetime account.',
             'Loan extension and reservation creation serialize their interval checks against the same unit.'
         ],
         faq=[
             'A borrower may add up to 48 hours through the ordinary extension action.',
             'Returning and borrowing a different unit creates a different loan; it does not reset the extension count on the original loan.',
             'An extension does not silently move another borrower\'s reservation.'
         ],
         cases=[
             R('Reject an extension that crosses the next booking', 'A borrower extended a camera loan into another student\'s confirmed reservation. Prevent the collision.', 'BR3 API3 ADR3', 'Check interval conflicts transactionally and return EXTENSION_CONFLICT without changing the due time.'),
             R('Keep the original reservation after extension', 'Reports currently show an edited original reservation when a loan is extended. Preserve the original booking interval.', 'BR4 API4', 'Change loan.dueAt, retain oldDueAt in the extension event, and leave the original reservation interval intact.'),
             R('Stop borrowers extending a past-due loan', 'The extension button still succeeds after the due time has passed. Enforce the documented eligibility boundary.', 'BR1 API2', 'Reject extension after dueAt with LOAN_ALREADY_OVERDUE and preserve the current loan.'),
             U('Allow research-loan extension exceptions', 'Long-running experiments need staff-approved extensions beyond normal loan limits.', 'WF4', 'What limits and approver permissions apply to research-loan extension exceptions?', True),
             U('Let staff extend several loans in one action', 'At semester end, staff want to extend all loans for a selected course together.', 'BR1 API1', 'Who can perform a course-wide extension and should one conflicting loan block the entire operation?'),
             U('Reserve an extension in advance', 'A borrower wants to book an extension option at checkout and decide later whether to use it.', 'BR3 ADR3', 'Does an extension option block availability, and when must the borrower exercise or release it?'),
             P('Remind borrowers about extension eligibility', 'Before a loan is due, show whether the borrower can still request the one ordinary extension and send a reminder.', 'BR1 BR2', 'Only an own Open loan before dueAt is eligible and only one ordinary extension is allowed; reminder timing needs a decision.', 'When should the extension reminder be sent and through which channel?'),
             P('Offer a shorter extension when the requested end conflicts', 'Do not move another booking. Instead, suggest the latest valid end time when a requested extension overlaps it.', 'BR3 FAQ3', 'Protect the next reservation and leave the loan unchanged on conflict; the fallback suggestion needs a product rule.', 'What minimum extra duration makes a shorter extension worth suggesting, and should the borrower confirm it?'),
             C('Limit the extra time requested for a loan', 'Validate the new due time in the ordinary extension form and explain the maximum extra duration. Keep the normal one-extension-per-loan restriction.', 'BR5 FAQ1', 'The extension rule allows 24 additional hours while the FAQ allows 48 additional hours.', 'Should the ordinary extension cap be 24 or 48 additional hours?'),
             A('Format extension timestamps consistently in history', 'In the loan history component, render oldDueAt and newDueAt with the same existing formatDateTime helper already used by the loan details header. Include both labels, "Previous due time" and "New due time". Add no new date formatting rule.')
         ]),
    dict(code='CAN', name='Cancellations and booking edits', component='Cancellations',
         context='Cancelling a booking is a reservation operation and is distinct from returning borrowed equipment. The system must release inventory promptly while retaining enough history to explain who cancelled the request and why.',
         br=[
             'A borrower can cancel their own Draft, AwaitingApproval, or Confirmed reservation before it becomes Collected.',
             'Cancellation changes the reservation to Cancelled and releases its interval in one transaction.',
             'A Collected reservation cannot be cancelled; equipment must be handled through the loan return workflow.',
             'A lab manager may cancel a reservation in their lab and must provide a reason visible to the borrower.',
             'A borrower cancellation requires a reason of at least 10 characters.'
         ],
         wf=[
             'The confirmation dialog identifies the asset and interval that will be cancelled.',
             'When a staff cancellation commits, the borrower receives the reason in the in-app notification.',
             'The reservation history retains actorId, cancelledAt, and the cancellation reason.',
             'Automatic penalties for repeated cancellations are not defined; the product team has not chosen a threshold or sanction.'
         ],
         api=[
             'POST /v1/reservations/{id}/cancel requires the current reservation version.',
             'Cancelling an already Cancelled reservation returns its existing state and does not append another cancellation event.',
             'Cancelling a Collected reservation returns 409 USE_RETURN_WORKFLOW.',
             'A failed cancellation leaves both the reservation state and the availability interval unchanged.'
         ],
         adr=[
             'Cancelled reservations are retained for history and are excluded from blocking interval queries.',
             'Cancellation publication uses the transactional outbox so a committed cancellation can trigger wait-list processing.',
             'A cancellation is not represented as deletion of the reservation row.'
         ],
         faq=[
             'Borrowers can leave the cancellation reason empty; reasons are optional for self-service cancellation.',
             'If the reservation has already been collected, record a return instead of cancelling it.',
             'A repeat click on Cancel shows the completed cancellation rather than creating a duplicate event.'
         ],
         cases=[
             R('Release the slot when staff cancel', 'A manager cancelled a damaged unit\'s booking but its interval remained blocked. Fix the cancellation transaction.', 'BR2 ADR1', 'Release the blocking interval atomically with the Cancelled transition while retaining reservation history.'),
             R('Guide collected reservations to returns', 'The borrower can cancel a booking even after picking up the equipment. Correct that action and explain the next step.', 'BR3 API3 FAQ2', 'Reject cancellation with USE_RETURN_WORKFLOW and direct staff or the borrower to the return process.'),
             R('Avoid duplicate cancellation notifications', 'Double-clicking Cancel produces two cancellation entries and two borrower notifications. Make repeated cancellation safe.', 'API2 FAQ3', 'An already Cancelled request must return its existing state without another cancellation event.'),
             U('Penalize repeated cancellations', 'Frequent cancellations are leaving camera slots unused. Introduce a restriction for repeat offenders.', 'WF4', 'What cancellation frequency triggers a restriction, over which period, and what restriction applies?', True),
             U('Cancel reservations when a course is withdrawn', 'If a student withdraws from a course, cancel their course-related bookings automatically.', 'BR1 ADR2', 'Which bookings count as course-related, and should staff review them before cancellation?'),
             U('Allow borrowers to undo a cancellation', 'Students sometimes cancel by mistake. Provide an Undo action immediately afterwards.', 'BR2 ADR1', 'How long is cancellation undo available, and what happens if someone else has already acquired the released interval?'),
             P('Suggest an alternative when staff cancel', 'Keep the mandatory staff cancellation reason, but also offer the borrower another suitable unit.', 'BR4 WF2', 'Include the staff reason in the borrower notification; alternative selection and commitment need definition.', 'Which units qualify as alternatives and should the substitute be held or only suggested?'),
             P('Add a cancellation survey', 'Retain the cancellation history and ask borrowers a short survey when they cancel.', 'WF3', 'Keep actor, cancellation time, and recorded reason; the optional survey content and storage period are undecided.', 'Which survey questions are required and how long should responses be retained?'),
             C('Validate the reason in self-service cancellation', 'Implement the cancellation reason field for borrowers cancelling their own uncollected reservations. Apply the current requirement for an empty or short response.', 'BR5 FAQ1', 'The rule requires at least 10 characters, while the FAQ explicitly permits an empty self-service reason.', 'Should self-service cancellation require a reason of at least 10 characters or allow no reason?'),
             A('Make cancellation confirmation explicit', 'Change the confirmation dialog title to "Cancel this reservation?" and the primary button to "Cancel reservation". The secondary button remains "Keep reservation". Verify that Escape closes the dialog without sending a cancellation request.')
         ]),
    dict(code='WAI', name='Waiting lists and offers', component='Waiting List',
         context='The waiting list offers a newly freed interval to an eligible borrower. An offer is a temporary hold rather than an automatic reservation; the borrower still has to accept before its deadline.',
         br=[
             'Waiting-list entries are scoped to an equipment model, pickup lab, and requested interval.',
             'Eligible entries for the same freed interval are considered in order of joinedAt, with entry UUID as the tie-breaker.',
             'A waiting-list offer temporarily blocks the offered unit until acceptance or offer expiry.',
             'A borrower may have only one active waiting-list entry for the same model, lab, and interval.',
             'A waiting-list offer expires 20 minutes after it is created.'
         ],
         wf=[
             'When cancellation frees an interval, the worker checks training and suspension before creating an offer.',
             'Accepting a still-valid offer creates a Confirmed reservation and closes the corresponding waiting-list entry.',
             'An expired offer releases the temporary hold and processing continues with the next eligible entry.',
             'Priority treatment for accessibility accommodations has been requested but neither the priority rule nor its authorizer is agreed.'
         ],
         api=[
             'POST /v1/waitlist requires modelId, labId, startAt, and endAt; a duplicate active entry returns 409 WAITLIST_DUPLICATE.',
             'POST /v1/waitlist-offers/{id}/accept checks the offer deadline using server time.',
             'Accepting an expired offer returns 409 OFFER_EXPIRED and creates no reservation.',
             'Offer acceptance and expiry use mutually exclusive transactional state transitions.'
         ],
         adr=[
             'The outbox consumer may process the same freed-interval event more than once; a unique offer constraint prevents duplicate active offers.',
             'The waiting list never reserves a different interval from the one accepted by the borrower.',
             'Offer ranking uses stored joinedAt, not email delivery order.'
         ],
         faq=[
             'A waiting-list offer remains available for 30 minutes after creation.',
             'Failure to read an offer notification does not automatically accept the reservation.',
             'A training-ineligible entry is skipped for that offer without being silently deleted from the waiting list.'
         ],
         cases=[
             R('Keep offer order stable when timestamps match', 'Two students joined a camera waiting list at the same instant and their ordering changes between worker runs.', 'BR2 ADR3', 'Order by joinedAt and then entry UUID; notification order must not decide priority.'),
             R('Prevent accepting an expired offer', 'A borrower clicked an old offer link after its deadline and still got a confirmed reservation. Enforce the validity check.', 'API2 API3', 'Use server time to reject expired acceptance with OFFER_EXPIRED and create no reservation.'),
             R('Skip ineligible borrowers without deleting entries', 'The first waiting student lost training eligibility. The offer worker should move on without erasing the entry.', 'WF1 FAQ3', 'Check training and suspension before offering, skip the ineligible entry for that offer, and retain the entry.'),
             U('Prioritize accessibility accommodation requests', 'Student support wants approved accommodation requests to receive earlier waiting-list offers.', 'WF4', 'What priority ordering applies to accommodation requests, and who authorizes that status?', True),
             U('Let borrowers pause waiting-list offers', 'Students away for a week want to pause offers without losing their place.', 'BR2 BR4', 'Does a paused entry retain its original joinedAt, and how is a pause started and ended?'),
             U('Offer a different interval to waiting borrowers', 'If the exact interval never opens, offer a nearby time instead.', 'BR1 ADR2', 'What time flexibility may borrowers specify and how should alternative intervals be ranked?'),
             P('Show waiting-list position estimates', 'Use the stored ordering to show a student their likely waiting position and expected wait.', 'BR2', 'The queue order has a documented tie-breaker; an expected-wait calculation is not defined.', 'How should expected waiting time account for eligibility changes and future cancellations?'),
             P('Retry undelivered offer notifications', 'Keep the temporary unit hold while retrying an offer notification that could not be delivered.', 'BR3 FAQ2', 'A hold belongs to the offer and reading a notification does not accept it; retries must not invent a new acceptance.', 'May a notification failure extend the offer deadline, and if so by how much?'),
             C('Release an unanswered waiting-list offer', 'When an offered slot has not been accepted by the deadline, release its temporary hold so the next eligible borrower can receive an offer.', 'BR5 FAQ1', 'The active waiting-list rules specify 20 minutes while the FAQ specifies 30 minutes.', 'Should an offer expire after 20 or 30 minutes from creation?'),
             A('Show a clear waiting-list leave action', 'For an active waiting-list entry, change the action label from "Remove" to "Leave waiting list". Preserve the existing confirmation and endpoint. Do not show the action on closed entries. Verify both states.')
         ]),
    dict(code='NOS', name='Pickup deadlines and no-shows', component='Pickup Expiry',
         context='Uncollected reservations need a defined lifecycle after the start time. No-show processing releases a booked slot and may supply operational data, but it must never race with a successful physical handover.',
         br=[
             'Only Confirmed reservations that have no completed checkout are eligible for no-show expiry.',
             'No-show expiry changes the reservation to ExpiredNoShow, releases the interval, and records one expiry event.',
             'A successful checkout prevents later no-show expiry of the same reservation.',
             'A borrower can see their own no-show entries; staff views require access to the reservation\'s lab.',
             'The normal pickup deadline is 30 elapsed minutes after reservation startAt.'
         ],
         wf=[
             'The pickup screen shows the scheduled start and current pickup deadline in the owning lab time zone.',
             'The expiry worker rechecks reservation state under the same lock used for checkout.',
             'The no-show event can trigger waiting-list processing after the expiry transaction commits.',
             'Excused no-shows and their effect on future borrowing are not yet governed by an approved policy.'
         ],
         api=[
             'GET /v1/reservations/{id} returns pickupDeadlineAt as a UTC instant alongside the reservation state.',
             'The internal no-show worker ignores Draft, AwaitingApproval, Cancelled, and Collected reservations.',
             'Reprocessing an expired reservation does not append a second expiry event.',
             'A request that loses a race to a completed checkout returns the current Collected state without releasing the loan\'s occupancy.'
         ],
         adr=[
             'The pickup deadline uses elapsed time rather than a count of business opening minutes.',
             'No-show expiry and checkout serialize on the reservation row.',
             'The worker records its actual execution time separately from the scheduled pickup deadline.'
         ],
         faq=[
             'Reservations are held for 45 elapsed minutes after the scheduled start before being treated as no-shows.',
             'A slow expiry worker does not change the scheduled pickup deadline displayed on the reservation.',
             'A no-show is not a cancelled loan; no loan exists until checkout succeeds.'
         ],
         cases=[
             R('Stop no-show expiry after a completed checkout', 'A student collected a laptop while the expiry worker was running. The booking then became ExpiredNoShow and the slot reopened.', 'BR3 WF2 ADR2', 'Serialize checkout and expiry; once checkout succeeds, expiry must not release the occupied unit.'),
             R('Do not expire requests awaiting approval', 'The no-show worker is treating unapproved reservations as missed pickups. Limit the worker to the correct state.', 'BR1 API2', 'Only Confirmed uncollected reservations may expire as no-shows; skip AwaitingApproval.'),
             R('Avoid duplicate no-show events on retries', 'A retried worker run added several no-show entries for one reservation. Make expiry idempotent.', 'BR2 API3', 'Write one expiry transition and event; later processing must not append another.'),
             U('Allow staff to excuse a no-show', 'A student missed pickup because a lecture ran late. Staff want to mark the absence as excused.', 'WF4', 'Who may excuse a no-show, what evidence is required, and how does that affect borrowing restrictions?', True),
             U('Let borrowers report a late arrival', 'Add an "I am on my way" action when the borrower cannot reach the desk by the deadline.', 'WF1 ADR1', 'Does reporting a late arrival extend the pickup hold, and what limits or staff approval apply?'),
             U('Cancel all future bookings after repeated no-shows', 'The lab wants stronger action when someone repeatedly reserves equipment without collecting it.', 'BR4 WF4', 'How many no-shows trigger action, over which period, and should existing future reservations be cancelled?'),
             P('Show pickup deadlines on calendar cards', 'Display the server pickup deadline and warn the borrower before it passes.', 'API1 WF1', 'Use pickupDeadlineAt and the owning lab time zone; the warning lead time is unspecified.', 'How long before the pickup deadline should the warning appear?'),
             P('Recover availability after a worker outage', 'When the no-show worker catches up after an outage, release expired slots and give staff a summary of affected bookings.', 'BR2 ADR3', 'Record actual processing time separately and release intervals through expiry; summary grouping is not specified.', 'Should the catch-up summary be grouped by lab, worker run, or calendar day, and who receives it?'),
             C('Calculate the pickup deadline for uncollected reservations', 'Populate the reservation pickup deadline from startAt using the normal no-show grace period. The desk should display that deadline to the borrower.', 'BR5 FAQ1', 'The active expiry rule uses 30 elapsed minutes and the FAQ promises 45 elapsed minutes.', 'Should normal pickup expire 30 or 45 elapsed minutes after startAt?'),
             A('Clarify the expired booking badge', 'For state=ExpiredNoShow, replace the badge text "Expired" with "Pickup missed". Keep the state code, color, and sorting unchanged. Verify that Cancelled and Collected badges keep their existing text.')
         ]),
    dict(code='OVD', name='Overdue loans and account restrictions', component='Overdue Processing',
         context='ToolNest v1.1 tracks late loans and borrowing restrictions without collecting money. Overdue state follows the physical receipt time; a delayed staff inspection must not make the borrower appear to keep equipment longer.',
         br=[
             'An Open loan becomes overdue when server time is later than dueAt and no receipt has been recorded.',
             'Recording receipt stops overdue duration at receivedAt, even while condition inspection is pending.',
             'A borrower with an overdue loan cannot create a new reservation or check out another unit.',
             'Returning the last overdue unit clears the overdue-based restriction; an independent manual suspension still applies.',
             'The first overdue email is scheduled 2 elapsed hours after dueAt if the loan is still unreceived.'
         ],
         wf=[
             'The borrower dashboard lists the due time and overdue duration for each outstanding loan.',
             'The staff overdue queue is scoped to the labs for which the actor has a staff grant.',
             'ToolNest v1.1 records no monetary fines; a future charging policy requires a separate product decision.',
             'An overdue job rechecks receipt state before publishing a reminder intent.'
         ],
         api=[
             'Reservation creation and checkout return 403 OVERDUE_RESTRICTION when the borrower has an unreceived overdue loan.',
             'GET /v1/me/loans computes overdue duration from dueAt to receivedAt or current server time.',
             'The restriction service distinguishes overdue_loan from manual_suspension in its machine-readable reasons.',
             'The overdue processor uses a loan-and-reminder-stage uniqueness key to avoid duplicate reminder intents.'
         ],
         adr=[
             'Overdue duration is derived from timestamps rather than incremented by a scheduled counter.',
             'Overdue restrictions are derived from current loan state and are not permanent account flags.',
             'The first reminder schedule uses elapsed UTC time and does not pause while the desk is closed.'
         ],
         faq=[
             'The first overdue email is sent 4 elapsed hours after the due time if the unit has not been received.',
             'A pending return inspection does not keep an overdue restriction active after receipt.',
             'Settling all overdue loans does not lift an unrelated manual suspension.'
         ],
         cases=[
             R('Stop overdue time when equipment reaches the desk', 'The return was received yesterday but still awaits inspection. The borrower dashboard is continuing to add overdue hours.', 'BR2 API2 FAQ2', 'Stop the overdue interval at receivedAt regardless of inspection completion.'),
             R('Keep a manual suspension after an overdue return', 'Returning a late laptop currently clears every restriction on the account, including a separate staff suspension.', 'BR4 API3 FAQ3', 'Clear the overdue-derived restriction when appropriate while preserving the independent manual suspension.'),
             R('Block borrowing while another loan is overdue', 'A borrower with an unreturned overdue camera managed to reserve and collect a second unit.', 'BR3 API1', 'Check outstanding overdue loans during both reservation creation and checkout and return OVERDUE_RESTRICTION.'),
             U('Introduce daily late fees', 'The department wants to charge a daily fee for overdue equipment.', 'WF3', 'What rates, grace periods, caps, and collection process should the new late-fee policy use?', True),
             U('Escalate long-overdue equipment to security', 'Loans overdue for a long time should be reported to campus security.', 'WF2', 'What overdue duration triggers security escalation and what borrower information may be shared?'),
             U('Waive restrictions during campus disruption', 'A campus closure prevented several returns. Let staff waive overdue restrictions for affected loans.', 'BR3 BR4', 'Who may authorize a closure-related waiver, which loans qualify, and how long does it apply?'),
             P('Display an overdue appeal action', 'Keep showing the overdue duration but let students appeal an overdue restriction from their loan page.', 'WF1 API3', 'Retain the recorded overdue duration and distinguish the restriction reason; appeal handling is not specified.', 'Who reviews an appeal, and does submitting one pause the overdue restriction?'),
             P('Send repeated reminders for late equipment', 'Keep reminders deduplicated and continue contacting borrowers until equipment is received.', 'API4 WF4', 'Use unique reminder stages and recheck receipt before publishing; repeat cadence is undefined.', 'What is the repeat reminder cadence and maximum number of reminders?'),
             C('Schedule the first overdue email', 'Send the first overdue email after the normal delay for an unreceived loan. Check again that the unit is still outstanding before scheduling the message.', 'BR5 FAQ1', 'The overdue rules specify 2 elapsed hours and the FAQ specifies 4 elapsed hours after dueAt.', 'Should the first overdue email be scheduled 2 or 4 elapsed hours after dueAt?'),
             A('Correct the overdue duration unit label', 'In the staff overdue table, replace the column heading "Days late" with "Hours overdue". The existing value is already elapsed hours; do not alter its calculation. Verify the heading and one row containing 2.5 hours.')
         ]),
    dict(code='DAM', name='Damage and missing-accessory incidents', component='Incidents',
         context='An incident is an evidence record, not a finding of borrower liability. Technicians document what they observed and managers classify the incident before repair or financial questions are handled outside the v1.1 product.',
         br=[
             'A damage or missing-accessory incident links to the asset, loan, reporting staff member, and observation time.',
             'Opening an incident does not automatically assign financial liability to the borrower.',
             'An unresolved safety-related incident makes the affected unit unavailable until a lab manager records a safety disposition.',
             'Incident photographs may be viewed only by staff with an incident_reader grant for the owning lab.',
             'A new incident must be triaged by a lab manager within 1 business day.'
         ],
         wf=[
             'The incident form separates observed condition, checkout condition reference, missing accessories, and staff notes.',
             'A safety disposition either keeps the unit blocked for maintenance or releases that safety block with a recorded reason.',
             'The incident timeline retains original evidence; later corrections are appended as separate entries.',
             'Borrower replacement-cost assessment and liability appeals have no approved workflow in v1.1.'
         ],
         api=[
             'POST /v1/incidents requires assetId, loanId, observedAt, incidentType, and a nonempty observation.',
             'POST /v1/incidents/{id}/dispositions requires lab_manager and a reason; safety blocks change transactionally with the disposition.',
             'GET /v1/incidents/{id}/photos enforces incident_reader on each request and returns private download links.',
             'PUT /v1/incidents/{id}/evidence is not supported; use POST /v1/incidents/{id}/corrections to append a correction.'
         ],
         adr=[
             'Incident evidence is append-only so a corrected note does not destroy the original observation.',
             'Borrower-facing loan status contains an incident reference but does not embed private staff notes or photographs.',
             'A safety block has its own reason and cannot be cleared merely by closing the associated loan.'
         ],
         faq=[
             'Managers have 2 business days to triage a new damage or missing-accessory incident.',
             'A loan can show an incident without establishing that the borrower caused the damage.',
             'Closing a loan does not by itself authorize release of a safety-related equipment block.'
         ],
         cases=[
             R('Do not label reported damage as borrower liability', 'The borrower page says "You owe for damage" as soon as staff open an incident. Use the supported incident meaning.', 'BR2 FAQ2', 'Show an incident reference without asserting liability; an observation alone is not a liability finding.'),
             R('Retain original incident observations after a correction', 'A technician corrected a mistaken damage note and the old text disappeared. Preserve the evidence trail.', 'WF3 API4 ADR1', 'Append a correction entry instead of replacing or deleting the original evidence.'),
             R('Keep unsafe equipment blocked after closing its loan', 'Closing the returned loan made a unit with an unresolved electrical-safety incident available again.', 'BR3 ADR3 FAQ3', 'Retain the safety block until a lab manager records an explicit safety disposition.'),
             U('Charge for a missing charger', 'When staff report a missing laptop charger, let the system assess the replacement cost to the borrower.', 'WF4 BR2', 'Who decides liability and replacement value, and what appeal process applies before a charge is assessed?', True),
             U('Send damage evidence to insurers', 'The lab wants to submit equipment damage incidents directly to an insurer.', 'BR4 ADR2', 'Which insurer interface and evidence-sharing permissions should the submission use?'),
             U('Let borrowers upload counter-evidence', 'Students should be able to provide photographs that challenge a staff damage report.', 'WF3 WF4', 'Who can view borrower counter-evidence, when can it be submitted, and who adjudicates a disputed incident?'),
             P('Prioritize the incident queue', 'Keep safety-related equipment blocked and sort the manager queue so the most urgent incidents appear first.', 'BR3', 'Preserve safety blocks; the queue urgency scale is not defined by the safety disposition rule.', 'Which severity levels and tie-breakers determine incident queue priority?'),
             P('Export incident records for an internal committee', 'Include original observations and appended corrections in a committee export while respecting private evidence access.', 'ADR1 BR4 ADR2', 'Keep the append-only evidence history and enforce incident-reader access; committee export content needs definition.', 'Which committee roles may export incidents and which borrower fields must be omitted or pseudonymized?'),
             C('Add a triage due date to new incidents', 'Show lab managers when each new damage or missing-accessory incident must be triaged. Calculate the due date using the standard business-day allowance.', 'BR5 FAQ1', 'The active rule requires 1 business day and the FAQ allows 2 business days for triage.', 'Should new incidents be triaged within 1 or 2 business days?'),
             A('Clarify the correction entry heading', 'For timeline entries with type=correction, display "Correction to observation" above the note. Keep original observation entries unchanged. Render the text with the existing plain-text component and verify both entry types.')
         ]),
    dict(code='MNT', name='Maintenance and service blocks', component='Maintenance',
         context='Maintenance blocks protect equipment that is being inspected or repaired. Closing a work order is distinct from certifying a unit safe for use, and future reservations must be treated explicitly rather than disappearing from the system.',
         br=[
             'A Scheduled or InProgress maintenance job blocks new reservations for its asset during the maintenance interval.',
             'Creating maintenance that overlaps a confirmed reservation returns a conflict and requires staff to resolve the booking separately.',
             'A maintenance job cannot be completed until its service checklist is recorded and an authorized technician signs the result.',
             'Completing maintenance clears only that job\'s block; independent safety incidents and retirement still prevent availability.',
             'A preventive maintenance task becomes due every 90 calendar days after the previous completed preventive service.'
         ],
         wf=[
             'The service planner shows overlapping bookings before a technician commits a maintenance interval.',
             'The maintenance record includes reported symptom, assigned technician, planned interval, checklist, and service outcome.',
             'A repair requiring an outside supplier remains InProgress until staff record the service outcome.',
             'Usage-based preventive service thresholds are not agreed; no checkout-count trigger has been approved.'
         ],
         api=[
             'POST /v1/maintenance-jobs requires assetId, startAt, endAt, and reason; overlap returns 409 MAINTENANCE_BOOKING_CONFLICT.',
             'POST /v1/maintenance-jobs/{id}/complete requires checklistResults, outcome, and technician attestation.',
             'Completion records completedAt using server time and does not modify unrelated block records.',
             'A job with missing required checklist results returns 422 SERVICE_CHECKLIST_INCOMPLETE.'
         ],
         adr=[
             'Availability combines independent reservation, maintenance, and safety-block records rather than a single editable available flag.',
             'Maintenance state transitions and their availability blocks commit in one transaction.',
             'Preventive due dates use the owning lab calendar date, not an assumed fixed number of UTC hours.'
         ],
         faq=[
             'Preventive maintenance is due every 120 calendar days after the last completed preventive service.',
             'An equipment repair does not automatically cancel an existing confirmed reservation.',
             'Completing a service job cannot reactivate a Retired asset.'
         ],
         cases=[
             R('Warn about confirmed bookings before scheduling repair', 'A technician scheduled a repair over a camera booking and the borrower\'s reservation vanished.', 'BR2 API1 WF1', 'Show the overlap and reject with MAINTENANCE_BOOKING_CONFLICT; staff must resolve the booking separately.'),
             R('Require a completed service checklist', 'Technicians can complete maintenance without recording any inspection results. Enforce the service completion requirements.', 'BR3 API2 API4', 'Require checklist results, outcome, and technician attestation; reject incomplete checklists without completion.'),
             R('Preserve independent safety blocks after repair', 'Completing one maintenance job cleared an electrical incident block belonging to another workflow.', 'BR4 API3 ADR1', 'Remove only the completed job\'s block and continue to respect independent safety and lifecycle restrictions.'),
             U('Schedule servicing by checkout count', 'Frequently borrowed equipment should enter preventive maintenance after enough uses, even before its calendar service date.', 'WF4', 'What checkout-count threshold triggers service and does it supplement or replace the calendar schedule?', True),
             U('Record warranty repair claims', 'Help technicians submit repairs under the manufacturer warranty.', 'WF2 WF3', 'Which warranty eligibility fields and supplier claim process should ToolNest support?'),
             U('Reschedule service automatically for urgent teaching use', 'If teaching demand is urgent, move planned preventive maintenance to another slot.', 'BR1 BR2', 'Which maintenance can be postponed, who authorizes it, and how far may the service be deferred?'),
             P('Show estimated repair completion to borrowers', 'Keep units unavailable during repair, but show borrowers an expected return-to-service estimate.', 'BR1 WF3', 'Continue enforcing service blocks; estimate source, confidence, and borrower presentation need a decision.', 'Who supplies repair estimates and how should unknown or missed estimates be displayed?'),
             P('Add supplier service attachments', 'Keep the required service checklist and allow staff to attach a supplier report when completing a repair.', 'BR3 API2', 'A supplier report cannot replace the checklist and attestation; its permitted file types and size are undecided.', 'Which file types and maximum size are allowed for supplier service reports?'),
             C('Calculate the next preventive service date', 'After a preventive maintenance job completes, calculate when the unit next needs preventive service. Use the normal calendar-day interval from the completed service.', 'BR5 FAQ1', 'The maintenance rules specify 90 calendar days while the FAQ specifies 120 calendar days.', 'Should preventive service be due after 90 or 120 calendar days?'),
             A('Rename maintenance completion action', 'Change the button text "Done" to "Complete service" on the maintenance job screen. Keep the current checklist validation and completion endpoint. Verify the button is disabled while the completion request is pending.')
         ]),
    dict(code='XFR', name='Movement between university labs', component='Lab Transfers',
         context='The multi-lab release tracks physical custody separately from ownership. Moving an asset between labs must not lose the source and destination acknowledgements or silently move a borrower\'s confirmed pickup location.',
         br=[
             'A lab transfer requires an asset with no Open loan and no confirmed reservation overlapping the planned transfer interval.',
             'Dispatch marks the asset InTransit and removes it from bookable pickup inventory until destination receipt.',
             'Destination receipt records the receiving staff member and changes the asset\'s current lab; the owning department remains unchanged.',
             'A confirmed reservation retains its pickup lab unless that reservation is explicitly changed through its normal edit workflow.',
             'A destination technician must acknowledge arrival within 4 staffed operating hours after recorded physical delivery.'
         ],
         wf=[
             'The source lab records dispatch with an asset scan and the destination lab records receipt with another scan.',
             'Transfer details show source lab, destination lab, dispatch time, delivery time, and receipt acknowledgement time separately.',
             'Only staff authorized for the source lab can dispatch; only staff authorized for the destination lab can receive.',
             'Cross-lab borrower returns are under review; responsibility for receipt and return inspection has not been assigned.'
         ],
         api=[
             'POST /v1/transfers requires assetId, sourceLabId, destinationLabId, startAt, and endAt.',
             'POST /v1/transfers/{id}/dispatch rejects an asset with an Open loan using 409 ASSET_ON_LOAN.',
             'POST /v1/transfers/{id}/receive requires a destination-lab grant and the scanned asset UUID.',
             'A repeated receive request returns the completed transfer without duplicating custody history.'
         ],
         adr=[
             'Current location, owning department, and reservation pickup lab are distinct fields.',
             'Transfer custody events are append-only and reference immutable asset UUIDs.',
             'A transfer is not treated as a borrower loan and creates no borrower overdue record.'
         ],
         faq=[
             'Destination staff have 8 staffed operating hours after delivery to acknowledge a transferred unit.',
             'Equipment travelling between labs cannot be collected until destination receipt is recorded.',
             'A transfer does not rewrite the pickup lab on an existing confirmed reservation.'
         ],
         cases=[
             R('Hide in-transit units from pickup availability', 'A camera dispatched to another lab is appearing as available at both desks while the van is still travelling.', 'BR2 FAQ2', 'Mark dispatched units InTransit and exclude them from pickup inventory until destination receipt.'),
             R('Do not move a reservation pickup lab during transfer', 'Moving equipment to another lab changed a borrower\'s confirmed pickup location without an explicit booking edit.', 'BR4 ADR1 FAQ3', 'Keep the confirmed reservation\'s pickup lab unchanged unless its normal edit workflow changes it.'),
             R('Require destination authorization when receiving', 'A source-lab technician can acknowledge destination receipt without any access to that lab.', 'WF3 API3', 'Require the receiving actor to hold a destination-lab staff grant and scan the expected asset UUID.'),
             U('Allow borrowers to return to a different lab', 'Students would like to return equipment to whichever university lab is closest.', 'WF4', 'Which lab records receipt and performs inspection for a cross-lab return, and how is custody transferred?', True),
             U('Use an external courier between labs', 'Schedule asset transfers with a commercial courier instead of the internal university van.', 'WF1 ADR2', 'What courier integration and custody evidence are required, and who handles loss in transit?'),
             U('Reserve a unit before its transfer arrives', 'Students want to book incoming equipment for collection as soon as the receiving lab expects delivery.', 'BR2 FAQ2', 'Can an incoming unit be booked before receipt, and how should a late or failed delivery affect those reservations?'),
             P('Add a transfer delay alert', 'Keep dispatched units unavailable and notify receiving staff when a transfer is late.', 'BR2 WF2', 'InTransit units remain unavailable and transfer timestamps are distinct; the lateness rule needs definition.', 'What planned-versus-actual timestamp and tolerance determine that a transfer is late?'),
             P('Track temperature during sensitive equipment movement', 'Preserve the custody timeline and add temperature monitoring for sensitive electronics.', 'ADR2 WF2', 'Retain append-only custody events; environmental measurement thresholds and sensor integration are undecided.', 'Which sensor source, sampling interval, and temperature thresholds apply to sensitive transfers?'),
             C('Flag transfer deliveries awaiting acknowledgement', 'In the receiving-lab transfer queue, show when destination acknowledgement is due after physical delivery. Count only staffed operating hours.', 'BR5 FAQ1', 'The rule specifies 4 staffed operating hours and the FAQ allows 8 staffed operating hours.', 'Should destination acknowledgement be due within 4 or 8 staffed operating hours after delivery?'),
             A('Distinguish transfer timestamps in details', 'In transfer details, label deliveredAt as "Physical delivery" and receivedAt as "Receipt acknowledged". Show "Not recorded" for a null value. Preserve the timestamp formatting helper and verify both null and populated fields.')
         ]),
    dict(code='KIT', name='Equipment kits and bundled items', component='Equipment Kits',
         context='Some borrowable equipment is assembled from several tracked units. A field-recording kit has one reservation and one borrower-facing loan but its component units still need individual availability and condition tracking.',
         br=[
             'A kit definition lists required component asset UUIDs and optional accessory descriptions.',
             'Confirming a kit reservation atomically reserves every required component for the requested interval.',
             'A kit reservation fails if any required component is unavailable; no subset is silently confirmed.',
             'The loan stores a snapshot of the kit composition at checkout so later definition edits do not change return obligations.',
             'A kit may contain at most 12 required tracked component units.'
         ],
         wf=[
             'The kit calendar shows availability only when all required components can satisfy the interval.',
             'The checkout screen requires staff to scan each tracked component and complete the optional accessory checklist.',
             'Return inspection records the condition and presence of every component in the checkout snapshot.',
             'Partial kit returns have no approved loan-state or due-time policy; the initial workflow assumes one complete receipt.'
         ],
         api=[
             'POST /v1/kit-reservations requires kitId, startAt, endAt, and purpose.',
             'An unavailable component returns 409 KIT_COMPONENT_UNAVAILABLE and commits no component reservation.',
             'PATCH /v1/kits/{id} changes future kit definitions without modifying existing loan snapshots.',
             'A kit checkout with a missing or wrong required component returns 422 KIT_SCAN_INCOMPLETE.'
         ],
         adr=[
             'All component interval writes in a kit reservation belong to one PostgreSQL transaction.',
             'A tracked component can belong to a kit definition and also be listed individually, but interval constraints still apply to its single asset UUID.',
             'Kits are logical bundles; their definitions do not replace or merge the identity of component units.'
         ],
         faq=[
             'A kit may include up to 16 required tracked units.',
             'A definition edit applies to future borrowing; an existing loan keeps its original component checklist.',
             'A failed kit booking must not leave temporary reservations on otherwise available components.'
         ],
         cases=[
             R('Roll back kit booking when one component conflicts', 'Booking a recording kit fails on its microphone but still reserves the camera and recorder. Make the operation atomic.', 'BR2 BR3 API2 ADR1', 'Reject the kit with KIT_COMPONENT_UNAVAILABLE and leave no component reservation committed.'),
             R('Keep the borrowed kit checklist after definition edits', 'A manager removed a tripod from a kit definition while the kit was on loan. The borrower\'s return checklist changed.', 'BR4 API3 FAQ2', 'Use the checkout composition snapshot for existing loans and apply definition edits only to future borrowing.'),
             R('Protect individually listed kit components from double booking', 'A camera was booked directly while already reserved as part of a recording kit. Use the same physical-unit availability rule.', 'ADR2 BR2', 'Apply interval constraints to the shared component UUID for both individual and kit reservations.'),
             U('Allow a kit to be returned in pieces', 'A student returned most of a recording kit but will bring the microphone tomorrow. Record the partial return.', 'WF4', 'How should partial return change loan state, component availability, and overdue duration?', True),
             U('Substitute a component in a kit', 'If one kit microphone is broken, let staff use a different model for that loan.', 'BR1 BR4', 'Which substitute components are acceptable, who approves the swap, and how is the loan snapshot updated?'),
             U('Let borrowers build custom bundles', 'Students want to assemble their own bundle from individually listed equipment.', 'ADR3 API1', 'What bundle size, eligibility, and approval rules apply to borrower-created bundles?'),
             P('Explain which kit component is unavailable', 'Keep all-or-nothing kit booking but show the borrower a helpful explanation when one component conflicts.', 'BR3 API2', 'Commit no partial booking and return KIT_COMPONENT_UNAVAILABLE; disclosure detail needs a decision.', 'Should borrowers see the conflicting component identity, just its category, or a generic kit-unavailable message?'),
             P('Version kit definitions in the catalog', 'Preserve existing loan snapshots and let staff compare kit compositions across earlier definition versions.', 'BR4 API3', 'Do not alter existing loan snapshots; historical definition retention and comparison scope are unspecified.', 'How many definition versions should be retained and which fields should the comparison show?'),
             C('Enforce the supported size of a kit', 'Stop managers adding required tracked units after a kit reaches the supported component maximum. Show how many required units are already selected.', 'BR5 FAQ1', 'The kit rule caps required tracked components at 12 while the FAQ allows 16.', 'Should a kit support at most 12 or 16 required tracked units?'),
             A('Use precise kit checklist headings', 'On the kit checkout screen, rename "Items" to "Tracked components" and "Extras" to "Optional accessories". Keep scan validation unchanged. Verify both headings on a kit containing one tracked unit and one optional accessory.')
         ]),
    dict(code='NTF', name='Notifications and delivery', component='Notifications',
         context='Domain events create notification intents after the underlying transaction commits. Delivery is asynchronous, so the equipment workflow must remain correct when an email provider is slow, unavailable, or delivers the same message more than once.',
         br=[
             'Reservation approval, staff cancellation, waiting-list offer, and overdue events create in-app notification intents for the affected borrower.',
             'Borrowers can disable optional email copies; the corresponding in-app transaction notifications remain enabled.',
             'Notification content must not disclose another borrower\'s name, email address, or reservation purpose.',
             'A notification delivery failure does not roll back a committed reservation, loan, or return.',
             'A transient email delivery failure is retried at most 3 times after the initial send attempt.'
         ],
         wf=[
             'The notification inbox lists newest first and marks an item read only after an explicit read action.',
             'A worker records provider message ID, attempt time, and the final delivery outcome for staff troubleshooting.',
             'The delivery worker deduplicates intents using domain event ID, recipient ID, and channel.',
             'Daily digests are proposed; digest cutoff time, lab time zone selection, and included event types are undecided.'
         ],
         api=[
             'GET /v1/me/notifications returns only the authenticated borrower\'s inbox using cursor pagination.',
             'POST /v1/me/notifications/{id}/read is idempotent and cannot mark another borrower\'s item as read.',
             'PATCH /v1/me/notification-preferences accepts optionalEmailEnabled without disabling in-app transaction notifications.',
             'An email attempt with a permanent invalid-recipient response is marked FailedPermanent and is not retried.'
         ],
         adr=[
             'Notification intents are created through a transactional outbox and consumed asynchronously.',
             'Delivery logs contain internal IDs and provider response codes, not full rendered email bodies.',
             'A read receipt is not a domain action: reading an offer notification does not accept the waiting-list offer.'
         ],
         faq=[
             'A temporary email failure receives up to 5 retries after the initial send attempt.',
             'Disabling optional email does not remove in-app records of changes to your borrowing.',
             'A permanent invalid address must be corrected before a new notification can be sent successfully.'
         ],
         cases=[
             R('Keep transactions successful when email delivery fails', 'A student\'s confirmed booking is being undone when the email provider returns an error. Decouple the operations.', 'BR4 ADR1', 'Keep the committed reservation and process notification delivery asynchronously through the outbox.'),
             R('Retain in-app updates when email is disabled', 'Turning off email currently removes approval and cancellation messages from the borrower inbox too.', 'BR2 API3 FAQ2', 'Apply optionalEmailEnabled only to optional email copies and retain in-app transaction notifications.'),
             R('Stop retrying permanently invalid email addresses', 'The email worker repeatedly retries a permanent invalid-recipient response. Handle it using the delivery contract.', 'API4 FAQ3', 'Mark the attempt FailedPermanent and do not retry that permanent failure.'),
             U('Send a daily borrowing digest', 'Borrowers want one daily summary rather than checking the inbox for each change.', 'WF4', 'Which event types belong in the digest, at what cutoff time, and in which time zone?', True),
             U('Deliver reminders through SMS', 'Add text messages for time-sensitive pickup and overdue reminders.', 'BR1 WF2', 'Which SMS provider, consent rules, and event types should the new channel support?'),
             U('Add quiet hours for optional email', 'Students should be able to stop optional borrowing emails arriving overnight.', 'BR2 API3', 'What quiet-hour configuration is supported and should deferred messages be combined or sent individually?'),
             P('Show a notification delivery health panel', 'Use the stored provider outcomes to show staff which delivery problems need attention.', 'WF2 ADR2', 'Use IDs, attempt times, and response codes without exposing rendered email bodies; health thresholds need definition.', 'What failure rate or queue age should mark delivery health as degraded?'),
             P('Add push notifications for existing events', 'Keep the current transaction notification events and add a mobile push copy.', 'BR1 WF3', 'Use the existing event recipients and per-channel deduplication; device and consent behavior is unspecified.', 'How are push devices registered and revoked, and can borrowers disable push independently of email?'),
             C('Stop email retries when the retry budget is exhausted', 'For temporary email delivery failures, apply the normal retry allowance after the initial attempt and then mark the delivery as exhausted.', 'BR5 FAQ1', 'The rule allows 3 retries after the initial attempt and the FAQ allows 5 retries after the initial attempt.', 'Should a transient email failure receive at most 3 or 5 retries after the initial attempt?'),
             A('Make unread notification text accessible', 'For unread notification rows, add the visually hidden text "Unread" before the subject using the existing screen-reader-only utility. Keep the visible subject unchanged. Verify the accessible text disappears after the row is marked read.')
         ]),
    dict(code='SEC', name='Authentication and lab-scoped permissions', component='Identity and Access',
         context='University single sign-on identifies a user, while ToolNest grants authorize actions for particular labs. Being staff in one lab must not grant broad access to borrower information or management actions in another.',
         br=[
             'ToolNest v1.1 requires university single sign-on for application access; an authenticated session alone does not grant staff permissions.',
             'lab_technician and lab_manager grants are scoped to one lab and do not confer access to another lab.',
             'Borrowers may read their own reservations and loans; staff access to another borrower\'s transaction requires the relevant lab grant.',
             'Permission revocation takes effect on the next authorized API request, even if the user keeps the browser open.',
             'A session expires after 30 minutes without an authenticated API request.'
         ],
         wf=[
             'Changing the selected lab updates the interface context but never changes the actor\'s stored grants.',
             'The server checks authorization before returning protected borrower or staff data.',
             'An unauthenticated request returns 401; an authenticated actor lacking a required grant receives 403.',
             'Visiting users without university identities have no agreed account sponsorship, verification, or expiry policy.'
         ],
         api=[
             'GET /v1/me/grants returns the signed-in user\'s current lab-scoped grants.',
             'All mutation endpoints derive actorId from the authenticated session rather than a request body field.',
             'An authorized request must verify the labId of the target resource, not only a labId supplied by the client.',
             'The identity provider subject is the stable external user identifier; an email-address change does not create a new borrower account.'
         ],
         adr=[
             'Authentication uses the fictional university OIDC provider; ToolNest does not store university passwords.',
             'Current grant state is read during authorization rather than trusting a long-lived role claim in the browser.',
             'Authorization decisions use internal user IDs mapped to the identity provider subject.'
         ],
         faq=[
             'An inactive signed-in session remains usable for 45 minutes after its last authenticated API request.',
             'Selecting another lab in the header does not grant access to that lab\'s staff screens.',
             'If a user\'s email changes, their existing loans stay attached to the same university identity.'
         ],
         cases=[
             R('Enforce grants for the asset lab rather than the selected header', 'A manager can edit an asset in another lab by sending their own labId in the request. Fix resource authorization.', 'BR2 API3', 'Read the target resource\'s actual lab and require a matching grant; a client-selected lab cannot confer access.'),
             R('Revoke staff access in an already open tab', 'A technician removed from a lab can still read its staff transactions until signing out.', 'BR4 ADR2', 'Use current server-side grants on the next request so revoked permissions take effect without a new login.'),
             R('Preserve borrower history when university email changes', 'An email update produced a second account and made the student\'s open loan disappear from their profile.', 'API4 ADR3 FAQ3', 'Match the stable identity provider subject to the existing internal user ID instead of creating an account by email.'),
             U('Onboard visiting researchers without university SSO', 'The summer school wants external researchers to borrow equipment without a university account.', 'WF4 BR1', 'Who sponsors and verifies visiting accounts, and when must their access expire?', True),
             U('Require stronger verification for sensitive actions', 'The lab wants an extra identity check before staff release high-value equipment.', 'ADR1 BR1', 'Which actions require step-up verification and what identity-provider assurance level is sufficient?'),
             U('Create emergency staff access', 'When nobody with the right lab grant is available, staff need an emergency way to operate the desk.', 'BR2 WF2', 'Who may activate emergency access, for how long, and which actions are permitted and reviewed?'),
             P('Preview role changes before saving', 'Show the effective lab permissions that will result from a staff grant edit and flag risky combinations.', 'BR2 API1', 'Compute effective permissions from lab-scoped grants; risky combinations are not defined.', 'Which grant combinations should be flagged and should a flagged edit be blocked or merely warned about?'),
             P('Explain access denial in the staff interface', 'Use the existing 401 and 403 distinction to guide staff when a protected screen cannot load.', 'WF3 WF2', 'Distinguish unauthenticated from insufficient permissions without returning protected data; recovery routing needs definition.', 'Should a 403 screen offer a grant request, a lab switch, or contact details, and where should each action lead?'),
             C('Expire staff sessions after inactivity', 'Apply the standard idle timeout to signed-in sessions. Measure inactivity from the last authenticated API request and require sign-in after expiry.', 'BR5 FAQ1', 'The active session rule expires after 30 minutes and the FAQ allows 45 minutes after the same last request.', 'Should inactive sessions expire after 30 or 45 minutes?'),
             A('Remove a misleading permission tooltip', 'On the lab selector, replace "Switching labs changes your permissions" with "Choose a lab to view; your assigned access still applies". Keep selector behavior unchanged. Verify the tooltip is available on focus as well as hover.')
         ]),
    dict(code='AUD', name='Audit records and data retention', component='Audit and Privacy',
         context='The audit trail explains sensitive actions without becoming a second copy of all borrower content. Operational retention and account deletion must preserve required transaction references while limiting unnecessary personal data.',
         br=[
             'Sensitive mutations record an append-only audit event containing eventId, actorId, action, resourceId, labId, and occurredAt.',
             'Staff may query audit entries only with an audit_reader grant for the relevant lab.',
             'Application logs and audit events must not contain authentication tokens, university ID document images, or full borrower free-text purpose fields.',
             'An account deletion request is blocked while the borrower has an Open loan or a pending return inspection.',
             'Ordinary operational audit events are retained for 180 calendar days before scheduled deletion.'
         ],
         wf=[
             'The audit viewer filters by lab, action, resource ID, and UTC time interval.',
             'A correction to a sensitive record produces a new audit event rather than modifying the earlier audit event.',
             'The account deletion screen lists blocking transaction references visible to the requesting borrower.',
             'A legal-hold process is proposed, but who can place a hold and which records it covers are not agreed.'
         ],
         api=[
             'GET /v1/audit-events requires audit_reader for every requested lab and uses cursor pagination.',
             'There is no API for updating the body of an existing audit event.',
             'POST /v1/me/deletion-requests returns 409 ACTIVE_BORROWING_EXISTS when an Open loan or pending inspection blocks deletion.',
             'A retention run records aggregate deletion counts in an operational run summary without copying deleted event bodies.'
         ],
         adr=[
             'Audit event storage is separate from editable application notes and uses append-only writer permissions.',
             'An audit_reader grant does not imply incident_reader access to photographs or private incident notes.',
             'Ordinary audit retention is independent of operational backup rotation.'
         ],
         faq=[
             'Operational audit events remain searchable for 365 calendar days before scheduled deletion.',
             'A request to delete an account cannot finish while a returned unit still awaits condition inspection.',
             'An audit viewer can see that an incident action occurred without gaining permission to view the incident\'s private evidence.'
         ],
         cases=[
             R('Remove purpose text from audit payloads', 'Reservation audit events currently copy the entire borrower purpose field. Minimize the recorded event data.', 'BR1 BR3', 'Keep the defined audit metadata and exclude the full borrower free-text purpose field.'),
             R('Block account deletion during pending return inspection', 'The account deletion action succeeds after receipt even though the loan is still awaiting inspection.', 'BR4 API3 FAQ2', 'Return ACTIVE_BORROWING_EXISTS until pending inspection is completed; receipt alone does not unblock deletion.'),
             R('Do not expose incident evidence through audit access', 'Staff with audit_reader can download private incident photographs from links in audit entries.', 'ADR2 FAQ3', 'Audit access may show the action metadata but must not bypass incident_reader permissions for evidence.'),
             U('Place selected records under legal hold', 'The department needs to stop deletion of records related to an active dispute.', 'WF4', 'Who may place and release a legal hold, and which event and evidence records fall within its scope?', True),
             U('Provide a borrower data portability package', 'Students want to download a machine-readable copy of their personal data.', 'BR3 BR4', 'Which data categories and format belong in the portability package, and how should third-party data be excluded?'),
             U('Pseudonymize completed loan histories', 'After account deletion, preserve anonymous equipment usage history for long-term research.', 'BR4 ADR3', 'Which identifiers should be removed or replaced, and what reidentification risk and retention rules apply to research history?'),
             P('Search audit events by staff display name', 'Keep lab-scoped audit access and let reviewers search by the staff name shown in the directory.', 'BR2 BR1', 'Enforce audit_reader and retain stable actorId references; name-history matching is unspecified.', 'Should name search use current directory names, names at event time, or both?'),
             P('Alert when an audit retention run fails', 'Keep aggregate deletion summaries and notify operations if scheduled audit cleanup is unhealthy.', 'API4', 'Report aggregate counts without duplicating deleted bodies; failure and alert thresholds need definition.', 'How many failed or delayed retention runs trigger an alert, and which operations destination receives it?'),
             C('Delete ordinary audit events after their retention window', 'The scheduled cleanup should remove ordinary operational audit events after the supported calendar-day retention period and record aggregate deletion counts.', 'BR5 FAQ1', 'The ordinary retention rule is 180 calendar days and the FAQ says 365 calendar days.', 'Should ordinary operational audit events be retained for 180 or 365 calendar days?'),
             A('Show audit event identifiers as copyable text', 'In the audit event details drawer, add a "Copy event ID" button that copies the displayed eventId exactly. Show "Copied" for 2 seconds after success. Verify that keyboard activation copies the same value as mouse activation.')
         ]),
    dict(code='INT', name='External API and webhook delivery', component='Integrations',
         context='A course scheduler integrates with ToolNest through a versioned REST API and event subscriptions. Integrations receive lab-scoped service credentials and must tolerate retries, duplicate webhook deliveries, and stale updates.',
         br=[
             'A service credential is scoped to explicit labs and API operations; it never inherits the grants of the staff member who created it.',
             'Webhook payloads contain eventId, eventType, occurredAt, resourceId, and labId, without borrower names or email addresses.',
             'Webhook delivery is at least once; consumers must deduplicate using eventId.',
             'Requests that reuse an Idempotency-Key with a different payload in the same actor-and-route scope return 409 IDEMPOTENCY_MISMATCH.',
             'REST idempotency records are retained for 24 elapsed hours after the original request completes.'
         ],
         wf=[
             'Staff registering a webhook choose allowed event types and labs within their integration_admin grants.',
             'A failed webhook delivery appears in the integration delivery log with an attempt timestamp and response status.',
             'Webhook signatures use HMAC-SHA256 over the timestamp header, a period, and the raw request body; receivers must preserve the raw bytes.',
             'Webhook replay authorization and the maximum historical replay range remain undecided.'
         ],
         api=[
             'Webhook requests include X-ToolNest-Event-Id, X-ToolNest-Timestamp, and X-ToolNest-Signature headers.',
             'A versioned mutation with a stale If-Match returns 412 VERSION_MISMATCH rather than overwriting a newer resource.',
             'A successful idempotent retry within the retention window returns the original response status and body.',
             'Revoking a service credential rejects subsequent requests using that credential without waiting for an application restart.'
         ],
         adr=[
             'The public integration API uses the /v1 prefix; internal database tables are not an integration contract.',
             'Domain events are published from an outbox after the corresponding database transaction commits.',
             'Idempotency scope includes authenticated actor and route so two different integrations cannot read each other\'s stored responses by choosing the same key.'
         ],
         faq=[
             'A REST Idempotency-Key can be retried for 48 elapsed hours after the original request completes.',
             'A consumer may receive the same webhook event more than once and should use eventId to deduplicate.',
             'A service token remains restricted to its configured labs even if its creator later receives access to more labs.'
         ],
         cases=[
             R('Scope service access independently from its creator', 'A course scheduler token gained another lab automatically when its creator became a manager there.', 'BR1 FAQ3', 'Authorize the service credential using its explicit lab and operation scopes, not the creator\'s current grants.'),
             R('Handle duplicate webhook events safely', 'The course scheduler created duplicate calendar entries because it received the same reservation event twice.', 'BR2 BR3 FAQ2', 'Treat delivery as at least once and deduplicate by eventId without requiring borrower personal data.'),
             R('Reject stale integration updates', 'An integration overwrote a newer reservation edit using an old resource version. Apply the versioned mutation contract.', 'API2', 'Return 412 VERSION_MISMATCH for a stale If-Match rather than overwriting current state.'),
             U('Replay historical webhook events', 'An integration was unavailable and needs staff to replay old reservation events.', 'WF4', 'Who may authorize replay and what maximum historical range and event filters are supported?', True),
             U('Define external API request quotas', 'A scheduler integration polls too often. Add service-token request limits.', 'BR1 ADR1', 'What per-token and per-lab quotas, burst allowances, and retry guidance should the rate limit use?'),
             U('Rotate webhook signing secrets without downtime', 'A course integration needs to replace its signing secret while deliveries continue.', 'WF3 API1', 'How long should old and new signing secrets overlap, and how will receivers identify the active secret?'),
             P('Add a webhook failure escalation', 'Keep delivery attempt logs and notify integration owners when an endpoint remains unhealthy.', 'WF2', 'Retain attempt timestamps and response status; escalation cadence and ownership are not defined.', 'What consecutive-failure threshold triggers escalation and how is the integration owner selected?'),
             P('Expose an event preview when creating subscriptions', 'Show the existing webhook envelope before a manager saves a subscription and provide representative sample events.', 'BR2 WF1', 'The preview must use the documented envelope and omit borrower names and emails; sample coverage is unspecified.', 'Which event types require sample payloads and should samples be synthetic or derived from redacted live events?'),
             C('Expire completed REST idempotency records', 'Add cleanup for completed idempotency records after the supported retry window. Measure retention from original request completion rather than the last retry.', 'BR5 FAQ1', 'The REST rule retains idempotency records for 24 hours and the FAQ promises 48 hours.', 'Should REST idempotency records be retained for 24 or 48 elapsed hours?'),
             A('Document the existing webhook header names', 'In the integration quick-start code sample, replace X-Event-ID with X-ToolNest-Event-Id and X-Signature with X-ToolNest-Signature. Preserve the example body and HMAC algorithm. Verify both obsolete header names are absent from that sample.')
         ]),
    dict(code='RPT', name='Reports, calendars, and exports', component='Reporting',
         context='Managers use operational reports to understand completed loans and missed pickups. Reports preserve the distinction between a UTC event instant and a local calendar date, especially when the university changes daylight-saving offset.',
         br=[
             'The completed-loans report includes loans with a recorded receipt in the selected interval and attributes them to the pickup lab.',
             'Report time filters use half-open UTC intervals: an event at fromAt is included and an event at toAt is excluded.',
             'A manager may report only on labs for which they hold the lab_manager grant.',
             'CSV exports escape spreadsheet formula prefixes =, +, -, and @ in free-text fields by prepending a single quote.',
             'An ordinary report CSV export is limited to 10000 data rows, excluding the header.'
         ],
         wf=[
             'A local date selection is converted to UTC using the selected lab\'s IANA time zone; never assume every day has 24 hours.',
             'Export jobs recheck the requester\'s current lab access before making a result available for download.',
             'The report footer shows the selected lab, local date range, generatedAt instant, and whether a row limit was reached.',
             'An equipment utilization percentage is requested, but its numerator, denominator, and treatment of maintenance time are undecided.'
         ],
         api=[
             'POST /v1/report-exports accepts reportType=completed_loans, labIds, fromAt, and toAt and returns 202 with a job ID.',
             'GET /v1/report-exports/{id}/download requires the original requester and current manager grants for the exported labs.',
             'An export that reaches its row cap returns truncated=true with the applied cap in result metadata.',
             'POST /v1/report-exports rejects a requested lab outside the actor\'s grants with 403 LAB_ACCESS_REQUIRED.'
         ],
         adr=[
             'Completed-loan reporting uses receivedAt rather than inspection completion time.',
             'Report workers operate on committed source records; a cached chart is not an authoritative loan record.',
             'Each report job stores the normalized UTC boundaries and the input lab time zone for reproducibility.'
         ],
         faq=[
             'An ordinary CSV report can contain up to 25000 data rows, excluding its header.',
             'A completed-loan report can include a loan whose return inspection is still pending because receipt already occurred.',
             'The same local date range can span a different number of UTC hours when daylight-saving time changes.'
         ],
         cases=[
             R('Count received equipment before inspection finishes', 'The completed-loans report excludes units that reached the desk but have not yet been inspected. Use the defined completion measure.', 'BR1 ADR1 FAQ2', 'Include loans by recorded receipt time, even when inspection remains pending, and attribute them to the pickup lab.'),
             R('Use local dates correctly across daylight-saving changes', 'The daily lab report always queries a 24-hour UTC window and misses records on the autumn clock-change date.', 'WF1 BR2 ADR3', 'Convert local date boundaries with the lab\'s IANA time zone and query the resulting half-open UTC interval.'),
             R('Protect CSV exports from formula execution', 'A borrower purpose beginning with an equals sign is interpreted as a spreadsheet formula when a manager opens the export.', 'BR4', 'Prepend a single quote to free-text values beginning with the documented formula prefixes before CSV export.'),
             U('Introduce equipment utilization percentages', 'The department wants a utilization chart that compares equipment categories fairly.', 'WF4', 'What numerator, denominator, and maintenance-time treatment define equipment utilization?', True),
             U('Forecast future equipment demand', 'Use booking history to forecast how many cameras each lab will need next semester.', 'ADR2 BR1', 'What forecast horizon, aggregation level, and error measure are required for demand prediction?'),
             U('Rank the best-performing borrowers', 'A manager wants a leaderboard of borrowers based on equipment use and timely returns.', 'BR3', 'Is borrower ranking permitted, who may see it, and which scoring and fairness rules should it use?'),
             P('Schedule the existing completed-loans export', 'Use the current receipt-based report and email managers a recurring export.', 'BR1 WF2', 'Keep receipt-based inclusion and current access checks; scheduling and delivery are not established.', 'What schedule and time zone apply, and should the email contain an attachment or an authorized download link?'),
             P('Compare labs across a shared local date range', 'Keep manager-only reporting and show a comparison of labs that use different time zones.', 'BR3 WF1', 'Respect lab grants and IANA conversions; a shared cross-lab date interpretation needs a decision.', 'Should the comparison use each lab\'s local dates or one chosen reference time zone?'),
             C('Apply the ordinary report export row limit', 'Cap ordinary CSV reports at the supported number of data rows. Exclude the header from the count and return the existing truncation metadata when the cap is reached.', 'BR5 FAQ1', 'The reporting rule caps data rows at 10000 and the FAQ allows 25000, both excluding the header.', 'Should an ordinary CSV report allow at most 10000 or 25000 data rows?'),
             A('Expose the existing report truncation flag', 'When export result metadata has truncated=true, show "Export reached the row limit; narrow the date range for a complete result." above the download button. Hide the message for truncated=false. Do not change the export cap or report query.')
         ]),
]


PROJECT_DOCS = [
    dict(id='TN-OV-01', title='Project overview and product scope', owner='Elena Varga, Product Owner', facts=[
        'ToolNest is a fictional university equipment-lending service for students, researchers, technicians, lab managers, and training officers.',
        'ToolNest tracks individual equipment units, reservations, approvals, physical loans, returns, incidents, maintenance, and inter-lab custody.',
        'The fictional pilot labs are Media Studio (Europe/Bucharest), Electronics Workshop (Europe/Bucharest), and Field Research Hub (Europe/London).',
        'Release 1.1 is the active multi-lab baseline; release 1.2 is in development and unapproved proposals do not change baseline behavior.',
        'ToolNest v1.1 does not collect money, provide external visitor accounts, or implement unattended and offline checkout.',
        'All people, institutional systems, identifiers, policies, project events, and ticket histories in this corpus are synthetic.'
    ]),
    dict(id='TN-OV-02', title='Architecture and repository map', owner='Matei Ionescu, Tech Lead', facts=[
        'The fictional repository toolnest contains web/ for a React TypeScript interface, server/ for a Python FastAPI modular monolith, and workers/ for background jobs.',
        'PostgreSQL 16 is the transactional system of record for asset state, reservation intervals, loans, grants, and outbox events.',
        'Redis is used for expendable cache data and worker coordination; cache contents do not authorize borrowing or override database conflicts.',
        'Private object storage contains catalog photographs, incident evidence, and generated exports; authorization is checked before issuing download links.',
        'Modules use explicit service calls within the application and asynchronous domain events for notifications and integrations.',
        'The project integrates with a fictional university OIDC provider and a fictional mail service; there are no real service credentials or real borrower records in this dataset.'
    ]),
    dict(id='TN-OV-03', title='Release history and source authority', owner='Elena Varga, Product Owner', facts=[
        'Release 1.0 launched the Media Studio pilot on 2026-04-06 with reservations, staff checkout, and receipt-based returns.',
        'Release 1.1 became active on 2026-08-28, adding lab-scoped permissions, multi-lab transfers, kits, and versioned integration access.',
        'The active documentation snapshot was published on 2026-08-28; each indexed topic document in this snapshot applies to release 1.1.',
        'Active business rules, workflows, API contracts, architecture decisions, and staff FAQs in this snapshot all require consideration; document family alone does not establish precedence.',
        'When active sources specify incompatible behavior for the same scope, implementers must request an authoritative product decision rather than silently choosing one.',
        'Historical tickets describe the outcome of their recorded release and scope; a past implementation detail does not override the active release documentation.',
        'Release 1.2 work is being explored during September through November 2026; proposals in backlog tickets are requests rather than approved product rules.'
    ]),
    dict(id='TN-OV-04', title='Lab calendars and timestamp conventions', owner='Iris Popa, Operations Lead', facts=[
        'Normal staffed operating hours are Monday through Friday, 09:00 to 17:00 in the relevant lab\'s IANA time zone, excluding closures recorded in that lab\'s calendar.',
        'A staffed operating hour counts only time within staffed opening intervals; elapsed-hour deadlines continue through closures and weekends.',
        'A business-day deadline advances through open local working dates and retains the original local wall-clock time on the resulting date; closed dates are skipped.',
        'Timestamps crossing system boundaries use ISO 8601 with an explicit UTC offset; stored event instants use UTC.',
        'Calendar-day intervals follow local dates and may span fewer or more than 24 elapsed hours at daylight-saving boundaries.',
        'Client clocks are presentation inputs only and cannot establish authoritative checkout, receipt, expiry, or authorization times.'
    ]),
    dict(id='TN-OV-05', title='Implementation readiness and definition of done', owner='Nadia Marin, QA Lead', facts=[
        'A ticket is implementation-ready when its requested scope has testable behavior and its material decisions are explicit in the ticket or resolved by applicable sources.',
        'A missing sentence in a ticket is not automatically a clarification request when an applicable active source supplies the decision.',
        'A new exception or feature with an undecided policy requires a focused question; implementers must not invent thresholds, role grants, or liability rules.',
        'A narrow text, presentation, or regression-test task can be complete without restating the whole product workflow.',
        'Definition of done requires the relevant acceptance checks, authorization checks for changed protected actions, and a review of changed state transitions and error behavior.',
        'Jira workflow status describes delivery progress and is not a requirements-quality label; a completed ticket can have had an incomplete original request.'
    ])
]
