# Training and borrower eligibility — Business rules

Document ID: `TN-TRN-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Some tools require a current training certificate. Eligibility is evaluated for the borrower, equipment category, and intended checkout instant rather than being a permanent flag on the account.

## Requirements and guidance

### TN-TRN-BR-01

A restricted equipment category requires a certificate whose category matches the unit and whose validUntil is later than the checkout instant.

### TN-TRN-BR-02

A certificate expiring exactly at checkout time is invalid.

### TN-TRN-BR-03

Creating a reservation checks current eligibility; checkout checks eligibility again using the actual checkout instant.

### TN-TRN-BR-04

A suspended borrower cannot create reservations or check out equipment even when their training certificate is valid.

### TN-TRN-BR-05

Only a training officer can record or revoke a training certificate; a lab manager role alone does not grant that permission.
