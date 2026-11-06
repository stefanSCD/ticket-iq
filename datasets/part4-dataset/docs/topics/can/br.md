# Cancellations and booking edits — Business rules

Document ID: `TN-CAN-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Cancelling a booking is a reservation operation and is distinct from returning borrowed equipment. The system must release inventory promptly while retaining enough history to explain who cancelled the request and why.

## Requirements and guidance

### TN-CAN-BR-01

A borrower can cancel their own Draft, AwaitingApproval, or Confirmed reservation before it becomes Collected.

### TN-CAN-BR-02

Cancellation changes the reservation to Cancelled and releases its interval in one transaction.

### TN-CAN-BR-03

A Collected reservation cannot be cancelled; equipment must be handled through the loan return workflow.

### TN-CAN-BR-04

A lab manager may cancel a reservation in their lab and must provide a reason visible to the borrower.

### TN-CAN-BR-05

A borrower cancellation requires a reason of at least 10 characters.
