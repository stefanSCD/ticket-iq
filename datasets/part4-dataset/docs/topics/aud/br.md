# Audit records and data retention — Business rules

Document ID: `TN-AUD-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

The audit trail explains sensitive actions without becoming a second copy of all borrower content. Operational retention and account deletion must preserve required transaction references while limiting unnecessary personal data.

## Requirements and guidance

### TN-AUD-BR-01

Sensitive mutations record an append-only audit event containing eventId, actorId, action, resourceId, labId, and occurredAt.

### TN-AUD-BR-02

Staff may query audit entries only with an audit_reader grant for the relevant lab.

### TN-AUD-BR-03

Application logs and audit events must not contain authentication tokens, university ID document images, or full borrower free-text purpose fields.

### TN-AUD-BR-04

An account deletion request is blocked while the borrower has an Open loan or a pending return inspection.

### TN-AUD-BR-05

Ordinary operational audit events are retained for 180 calendar days before scheduled deletion.
