# FAQ and Support — Invoice issuance

**Project:** LedgerCloud  
**Feature:** invoice-issue  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible finance clerk to issue a validated customer invoice. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: PDF rendering failures may be retried without changing the issued invoice number. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Operational event records for Invoice issuance must be retained for 90 days after closure.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the invoice-issue feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.
