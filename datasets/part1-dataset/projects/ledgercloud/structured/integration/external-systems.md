# LedgerCloud — Integration catalogue

**Status:** Active

## About

LedgerCloud: Small-business invoicing and expense administration. The page is authoritative only in the synthetic project context.

## Dependencies

bank statement import, email provider, tax reporting portal, object storage. Each provider may fail, delay, duplicate or time out. A timeout does not prove the provider failed to accept an operation.

## Reconciliation

A stable operation ID links local changes to provider acknowledgements. Failed side effects can be reconciled without silently overwriting authoritative data.

## Product choices

A provider offering an API does not make that option a default business requirement. The product owner must explicitly approve user-visible behavior.
