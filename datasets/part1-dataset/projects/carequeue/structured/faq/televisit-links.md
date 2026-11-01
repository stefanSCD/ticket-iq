# FAQ and Support — Televisit access links

**Project:** CareQueue  
**Feature:** televisit-links  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible patient to join a remote appointment using a secure link. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Meeting link provisioning may be retried using a stable appointment correlation ID. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

The Televisit access links workflow opens manual review after 5 consecutive processing failures.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the televisit-links feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.
