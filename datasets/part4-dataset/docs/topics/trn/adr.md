# Training and borrower eligibility — Architecture decision

Document ID: `TN-TRN-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Some tools require a current training certificate. Eligibility is evaluated for the borrower, equipment category, and intended checkout instant rather than being a permanent flag on the account.

## Requirements and guidance

### TN-TRN-ADR-01

Eligibility reads certificate state from PostgreSQL at the action boundary; it is not copied into a long-lived access token.

### TN-TRN-ADR-02

Training categories are stable IDs shared by equipment models and certificates.

### TN-TRN-ADR-03

Training checks do not bypass account suspension checks.
