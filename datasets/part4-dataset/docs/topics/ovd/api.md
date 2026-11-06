# Overdue loans and account restrictions — API contract

Document ID: `TN-OVD-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

ToolNest v1.1 tracks late loans and borrowing restrictions without collecting money. Overdue state follows the physical receipt time; a delayed staff inspection must not make the borrower appear to keep equipment longer.

## Requirements and guidance

### TN-OVD-API-01

Reservation creation and checkout return 403 OVERDUE_RESTRICTION when the borrower has an unreceived overdue loan.

### TN-OVD-API-02

GET /v1/me/loans computes overdue duration from dueAt to receivedAt or current server time.

### TN-OVD-API-03

The restriction service distinguishes overdue_loan from manual_suspension in its machine-readable reasons.

### TN-OVD-API-04

The overdue processor uses a loan-and-reminder-stage uniqueness key to avoid duplicate reminder intents.
