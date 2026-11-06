"""Fictional completed work. Unlike answer keys, exported history is valid retrieval context."""

# Per area: summary, original request, accepted completion note, supporting source refs.
HISTORY = {
    'CAT': [
        ('Separate equipment models from physical units',
         'Make the inventory work when we buy another camera of the same model.',
         'Delivered a model page with separate UUID-backed physical units. Model names can repeat; asset tags remain university-wide unique. Acceptance checked two cameras with the same display name and different tags.', 'BR1 FAQ2'),
        ('Default the inventory screen to active units',
         'Show Active units by default. Staff can explicitly include Retired units; keep lab and category filters combined with the lifecycle filter.',
         'The Active filter is applied on first load. Staff can include Retired records without losing the selected lab and category filters.', 'WF2 API4')
    ],
    'RSV': [
        ('Reject a booking whose end precedes its start',
         'Some odd date selections are getting through the booking screen. Make them sensible.',
         'The server now validates endAt later than startAt before conflict checking. The UI retains invalid values for correction instead of creating a reservation.', 'WF3'),
        ('Use the lab time zone on booking details',
         'Persist reservation instants in UTC and render booking details using the owning lab IANA time zone. Verify the same UTC instant in Bucharest and London.',
         'Booking details use the owning lab zone; the stored reservation timestamps remain UTC.', 'BR4')
    ],
    'TRN': [
        ('Explain why a restricted tool cannot be borrowed',
         'Students do not understand the training error. Improve it.',
         'The eligibility panel identifies the missing training category and directs the borrower to a training officer. It does not claim the lab manager can issue the certificate.', 'WF1 BR5'),
        ('Keep suspension checks alongside certificate checks',
         'A valid training certificate must not permit a suspended borrower to reserve or collect equipment. Test the valid-certificate plus suspended-account combination.',
         'Suspension blocks both actions even when a matching training certificate is current.', 'BR4 ADR3')
    ],
    'APR': [
        ('Retain the manager decision in history',
         'We need to know who decided a request after it leaves the inbox.',
         'Approval and rejection now append actor and request-version audit events. Reviewing a decided request shows the decision maker.', 'WF3 ADR1'),
        ('Release a rejected approval hold',
         'When a manager rejects an AwaitingApproval request with a reason, transition to Rejected and release its interval in the same transaction.',
         'The rejected request retains its reason. Its slot becomes available atomically with the state transition.', 'BR3 ADR2')
    ],
    'OUT': [
        ('Keep personal data out of printed equipment QR labels',
         'Make the QR stickers safe to put on public equipment shelves.',
         'Labels encode only the opaque asset UUID. They contain no borrower ID, reservation secret, or authorization token.', 'ADR1'),
        ('Record pre-existing accessory exceptions at pickup',
         'Staff must confirm required accessories before handover or record an existing exception. Show the checklist beside the borrower and asset tag.',
         'The pickup checklist records present accessories and pre-existing exceptions as part of handover.', 'WF1 WF2')
    ],
    'RET': [
        ('Separate physical receipt from condition inspection',
         'The return desk needs to scan things in quickly and inspect them afterwards.',
         'Receipt records server receivedAt and puts the loan in ReturnedPendingInspection. A later condition inspection is a separate action; the unit remains unavailable in between.', 'BR1 BR2 WF1'),
        ('Record a missing accessory during inspection',
         'For each required accessory, require present or missing. Missing must open a linked incident and cannot produce a clean inspection result.',
         'Incomplete checklists are rejected and missing accessories route to an incident linked to the loan.', 'BR3 WF2 API4')
    ],
    'EXT': [
        ('Explain extension failures without identifying another student',
         'The extension error leaks the next borrower. Clean it up.',
         'The borrower sees the extension conflict reason without another borrower\'s identity. A rejected extension preserves dueAt.', 'WF2'),
        ('Track the ordinary extension count on each loan',
         'Only one approved ordinary extension is allowed per loan. A different loan must not inherit the old loan\'s extension counter.',
         'Extension count is stored per loan; the ordinary action rejects a second approved extension on that loan.', 'BR2 ADR2')
    ],
    'CAN': [
        ('Retain cancelled reservation history',
         'Cancelled bookings should not just disappear from our records.',
         'Cancellation keeps the reservation row, cancellation actor, time, and reason. Cancelled intervals no longer block availability.', 'WF3 ADR1 ADR3'),
        ('Send the staff cancellation reason to the borrower inbox',
         'A manager cancellation requires a borrower-visible reason. Include the same reason in the in-app notification after commitment.',
         'The borrower receives the recorded manager cancellation reason through the transaction notification.', 'BR4 WF2')
    ],
    'WAI': [
        ('Stop duplicate waiting-list entries',
         'People can join the same waiting list several times. Prevent that.',
         'A borrower can keep one active entry for the same model, lab, and requested interval. The API returns WAITLIST_DUPLICATE for the duplicate tuple.', 'BR4 API1'),
        ('Reserve an offered unit until offer resolution',
         'An active waiting-list offer should temporarily block its assigned unit. Acceptance and expiry must use mutually exclusive transitions.',
         'The offer owns a temporary availability hold. Only one of acceptance or expiry can commit.', 'BR3 API4')
    ],
    'NOS': [
        ('Expose the pickup deadline on reservation details',
         'Students need to see when their pickup hold ends.',
         'Reservation details include pickupDeadlineAt in UTC and render the start and deadline in the owning lab time zone. This task did not choose or change the grace-period duration.', 'API1 WF1'),
        ('Separate worker run time from scheduled pickup deadline',
         'When expiry runs late, retain the scheduled deadline and record actual processing time separately. Do not move the displayed deadline to worker execution time.',
         'The expiry event and reservation deadline remain distinct, making delayed worker runs visible without altering the schedule.', 'ADR3 FAQ2')
    ],
    'OVD': [
        ('Compute overdue hours from loan timestamps',
         'The overdue counter drifts when the worker misses a run. Make it reliable.',
         'Overdue duration is derived from dueAt and receipt or current server time rather than accumulated worker increments.', 'API2 ADR1'),
        ('Separate automatic and manual restriction reasons',
         'Return distinct machine reasons for overdue_loan and manual_suspension. Do not represent all restrictions as one permanent account boolean.',
         'The restriction service exposes separate reasons and derives overdue restriction state from current loans.', 'API3 ADR2')
    ],
    'DAM': [
        ('Link incident reports to the affected borrowing record',
         'We cannot tell which loan a damage note belongs to. Fix incident traceability.',
         'New incident reports require asset, loan, reporting actor, observation time, type, and observation text.', 'BR1 API1'),
        ('Guard private incident photograph downloads',
         'Check incident_reader for the incident\'s owning lab on every photo request. Return private authorized links only after this check.',
         'Private photograph access requires a matching incident_reader grant rather than general borrower or audit access.', 'BR4 API3')
    ],
    'MNT': [
        ('Show repair progress while a supplier has the unit',
         'A repair should not look completed just because we shipped it to a supplier.',
         'Supplier repairs remain InProgress until staff record the service outcome. The maintenance block stays in force.', 'WF3 BR1'),
        ('Record technician and service outcome at completion',
         'Service completion must record the required checklist, outcome, and technician attestation, with server completedAt.',
         'The completed job includes the checklist results, outcome, attesting technician, and authoritative completion instant.', 'API2 API3')
    ],
    'XFR': [
        ('Keep transfer custody separate from student borrowing',
         'Moving an asset on the university van should not create an overdue student loan.',
         'Transfers have separate custody events and do not create a borrower loan or overdue borrower record.', 'ADR2 ADR3'),
        ('Prevent dispatching equipment still on loan',
         'Reject transfer dispatch if the asset has an Open loan. Return ASSET_ON_LOAN without recording dispatch.',
         'Dispatch checks outstanding borrowing and returns 409 ASSET_ON_LOAN without changing custody.', 'BR1 API2')
    ],
    'KIT': [
        ('Keep physical unit identities inside kits',
         'Bundle the field recorder equipment without losing track of the individual serialled units.',
         'The kit definition references component asset UUIDs. Kit membership neither merges identities nor replaces physical unit records.', 'BR1 ADR3'),
        ('Require scans for each tracked kit component',
         'Checkout must scan every required tracked component and reject a missing or wrong unit with KIT_SCAN_INCOMPLETE.',
         'The kit handover screen validates each tracked component scan before checkout can commit.', 'WF2 API4')
    ],
    'NTF': [
        ('Deduplicate notification intents after worker retries',
         'Worker redelivery sends multiple copies of one change. Make notification creation safe.',
         'Intent uniqueness uses domain event ID, recipient ID, and channel. Redelivering one outbox event does not create a second identical intent.', 'WF3 ADR1'),
        ('Do not accept offers when their messages are read',
         'Marking a waiting-list notification read must not create a reservation. Only the explicit offer acceptance action may do so.',
         'Read receipts change inbox state only and never perform offer acceptance.', 'ADR3 API2')
    ],
    'SEC': [
        ('Keep selected lab separate from permission grants',
         'Changing the header lab should not let students open staff screens.',
         'The lab selector changes interface context only. All protected data still requires server authorization from stored grants.', 'WF1 WF2'),
        ('Ignore actor IDs supplied by API clients',
         'Derive mutation actorId exclusively from the authenticated session. A request body field cannot impersonate a different staff member.',
         'Mutation audit attribution uses the session actor even when a malicious request supplies another actorId.', 'API2')
    ],
    'AUD': [
        ('Make sensitive-action history append only',
         'An edited record needs to leave its previous history intact.',
         'Corrections generate new audit events. No API can rewrite an existing event body, and writer permissions enforce append-only storage.', 'WF2 API2 ADR1'),
        ('Summarize audit cleanup without duplicating deleted records',
         'Each retention run should retain aggregate deletion counts but must not copy deleted event bodies into its own run log.',
         'Operational summaries contain aggregate counts only; the cleanup job does not create a second copy of removed events.', 'API4')
    ],
    'INT': [
        ('Publish integration events only after commitment',
         'The scheduler sometimes sees a booking event for a booking that never committed. Fix publication ordering.',
         'Integration events come from the transactional outbox after their domain transaction commits.', 'ADR2'),
        ('Stop revoked service credentials immediately',
         'A revoked service credential must fail subsequent API requests without an application restart. Verify another active credential remains usable.',
         'Credential revocation affects the next request; it does not depend on worker or API process restarts.', 'API4')
    ],
    'RPT': [
        ('Show report provenance in the footer',
         'Managers cannot tell what period a downloaded report covers. Include its context.',
         'The footer shows lab, local date range, generatedAt, and row-limit status. The job stores normalized UTC bounds and input time zone.', 'WF3 ADR3'),
        ('Recheck access before an export download',
         'A completed export can be downloaded only by its original requester while they still hold manager grants for the exported labs.',
         'Download checks both requester identity and current grants; revoking access blocks a previously generated result.', 'WF2 API2')
    ]
}
