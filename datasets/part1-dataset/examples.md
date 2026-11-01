# TicketIQ — annotated example tickets

These are synthetic examples. Keep this file OUT of any retrieval index.

## resolved: SHOP-0001 — Implement web workflow: Order status alerts

**User story:** As a shopper, I want to receive an alert when an order changes state.

**Description:** Add the workflow to the web client. Existing policy and actor eligibility are not repeated in this ticket. The scope is order status alerts in ShopFlow. The ticket does not authorize new choices outside its acceptance criteria.

**Acceptance criteria:**

- The authorized action produces a verifiable result; identical retries have one effect.

- Failed authorization must not mutate another account’s records.

**Ground truth decisions:**

- `resolved` — Which notification channel is required for order status changes?

  - Evidence `shopflow:business_rules:order-alerts`: “Order status alerts are sent by email to the verified address of the order owner.”

- `resolved` — Which actors are authorized to use order status alerts?

  - Evidence `shopflow:business_rules:order-alerts`: “Only authenticated shopper identities with permission on the relevant record may initiate order status alerts operations. Administrative access is logged and does not bypass record ownership checks.”

---

## unresolved: SHOP-0002 — Define operational limits: Order status alerts

**User story:** As a shopper, I want to receive an alert when an order changes state.

**Description:** Support peak use and external delays without violating the product-specific timing boundary. The scope is order status alerts in ShopFlow. The ticket does not authorize new choices outside its acceptance criteria.

**Acceptance criteria:**

- The observable completion time matches an approved, testable boundary.

- Failed authorization must not mutate another account’s records.

**Ground truth decisions:**

- `unresolved` — What is the maximum acceptable delay between the status transition and the outgoing alert?

- `resolved` — Which notification channel is required for order status changes?

  - Evidence `shopflow:business_rules:order-alerts`: “Order status alerts are sent by email to the verified address of the order owner.”

---

## partially_resolved: SHOP-0003 — Make provider recovery reliable: Order status alerts

**User story:** As a shopper, I want to receive an alert when an order changes state.

**Description:** Improve recovery after transient provider errors while preserving the previous successful state. The scope is order status alerts in ShopFlow. The ticket does not authorize new choices outside its acceptance criteria.

**Acceptance criteria:**

- A temporary failure is retried according to an explicit bound and reports a final outcome.

- Failed authorization must not mutate another account’s records.

**Ground truth decisions:**

- `partially_resolved` — What is the maximum number of retries after a temporary email provider error?

  - Evidence `shopflow:faq:order-alerts`: “Temporary provider errors are eligible for an automatic retry.”

- `resolved` — Which notification channel is required for order status changes?

  - Evidence `shopflow:business_rules:order-alerts`: “Order status alerts are sent by email to the verified address of the order owner.”

---

## conflicting: SHOP-0010 — Resolve policy discrepancy: Order status alerts

**User story:** As a shopper, I want auditable operational handling for order status alerts.

**Description:** Apply the agreed lifecycle policy to operational records without relying on provider defaults. The scope is order status alerts in ShopFlow. The ticket does not authorize new choices outside its acceptance criteria.

**Acceptance criteria:**

- The retention or operational cutoff follows one approved, auditable stakeholder decision.

- Failed authorization must not mutate another account’s records.

**Ground truth decisions:**

- `conflicting` — How long must operational event records for Order status alerts be retained?

  - Evidence `shopflow:business_rules:order-alerts`: “Operational event records for Order status alerts must be retained for 30 days after closure.”

  - Evidence `shopflow:faq:order-alerts`: “Operational event records for Order status alerts must be retained for 90 days after closure.”

- `resolved` — Which actors are authorized to use order status alerts?

  - Evidence `shopflow:business_rules:order-alerts`: “Only authenticated shopper identities with permission on the relevant record may initiate order status alerts operations. Administrative access is logged and does not bypass record ownership checks.”

---

## already_clear: SHOP-0004 — Port approved behavior: Order status alerts

**User story:** As a shopper, I want to receive an alert when an order changes state.

**Description:** Port the following approved rule without changing product semantics: Order status alerts are sent by email to the verified address of the order owner. The scope is order status alerts in ShopFlow. The ticket does not authorize new choices outside its acceptance criteria.

**Acceptance criteria:**

- The application implements the rule exactly as stated, applies record-level authorization and introduces no new policy.

- Failed authorization must not mutate another account’s records.

**Ground truth:** No clarification needed for this narrowly scoped ticket.
