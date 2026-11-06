# Pickup deadlines and no-shows — Business rules

Document ID: `TN-NOS-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Uncollected reservations need a defined lifecycle after the start time. No-show processing releases a booked slot and may supply operational data, but it must never race with a successful physical handover.

## Requirements and guidance

### TN-NOS-BR-01

Only Confirmed reservations that have no completed checkout are eligible for no-show expiry.

### TN-NOS-BR-02

No-show expiry changes the reservation to ExpiredNoShow, releases the interval, and records one expiry event.

### TN-NOS-BR-03

A successful checkout prevents later no-show expiry of the same reservation.

### TN-NOS-BR-04

A borrower can see their own no-show entries; staff views require access to the reservation's lab.

### TN-NOS-BR-05

The normal pickup deadline is 30 elapsed minutes after reservation startAt.
