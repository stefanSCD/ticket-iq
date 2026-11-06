# Waiting lists and offers — API contract

Document ID: `TN-WAI-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

The waiting list offers a newly freed interval to an eligible borrower. An offer is a temporary hold rather than an automatic reservation; the borrower still has to accept before its deadline.

## Requirements and guidance

### TN-WAI-API-01

POST /v1/waitlist requires modelId, labId, startAt, and endAt; a duplicate active entry returns 409 WAITLIST_DUPLICATE.

### TN-WAI-API-02

POST /v1/waitlist-offers/{id}/accept checks the offer deadline using server time.

### TN-WAI-API-03

Accepting an expired offer returns 409 OFFER_EXPIRED and creates no reservation.

### TN-WAI-API-04

Offer acceptance and expiry use mutually exclusive transactional state transitions.
