# Cancellations and booking edits — API contract

Document ID: `TN-CAN-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Cancelling a booking is a reservation operation and is distinct from returning borrowed equipment. The system must release inventory promptly while retaining enough history to explain who cancelled the request and why.

## Requirements and guidance

### TN-CAN-API-01

POST /v1/reservations/{id}/cancel requires the current reservation version.

### TN-CAN-API-02

Cancelling an already Cancelled reservation returns its existing state and does not append another cancellation event.

### TN-CAN-API-03

Cancelling a Collected reservation returns 409 USE_RETURN_WORKFLOW.

### TN-CAN-API-04

A failed cancellation leaves both the reservation state and the availability interval unchanged.
