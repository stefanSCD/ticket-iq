# Waiting lists and offers — Architecture decision

Document ID: `TN-WAI-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

The waiting list offers a newly freed interval to an eligible borrower. An offer is a temporary hold rather than an automatic reservation; the borrower still has to accept before its deadline.

## Requirements and guidance

### TN-WAI-ADR-01

The outbox consumer may process the same freed-interval event more than once; a unique offer constraint prevents duplicate active offers.

### TN-WAI-ADR-02

The waiting list never reserves a different interval from the one accepted by the borrower.

### TN-WAI-ADR-03

Offer ranking uses stored joinedAt, not email delivery order.
