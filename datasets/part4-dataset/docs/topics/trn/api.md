# Training and borrower eligibility — API contract

Document ID: `TN-TRN-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Some tools require a current training certificate. Eligibility is evaluated for the borrower, equipment category, and intended checkout instant rather than being a permanent flag on the account.

## Requirements and guidance

### TN-TRN-API-01

GET /v1/eligibility requires borrowerId, assetId, and checkoutAt and returns eligible plus machine-readable blocking reasons.

### TN-TRN-API-02

POST /v1/training-certificates requires the training_officer grant and records the acting staff ID.

### TN-TRN-API-03

Checkout fails with 403 TRAINING_REQUIRED when a required certificate is missing or expired.

### TN-TRN-API-04

GET /v1/me/eligibility exposes the signed-in borrower's own reasons; other borrowers require the training_officer grant.
