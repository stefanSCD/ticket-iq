# Equipment kits and bundled items — API contract

Document ID: `TN-KIT-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Some borrowable equipment is assembled from several tracked units. A field-recording kit has one reservation and one borrower-facing loan but its component units still need individual availability and condition tracking.

## Requirements and guidance

### TN-KIT-API-01

POST /v1/kit-reservations requires kitId, startAt, endAt, and purpose.

### TN-KIT-API-02

An unavailable component returns 409 KIT_COMPONENT_UNAVAILABLE and commits no component reservation.

### TN-KIT-API-03

PATCH /v1/kits/{id} changes future kit definitions without modifying existing loan snapshots.

### TN-KIT-API-04

A kit checkout with a missing or wrong required component returns 422 KIT_SCAN_INCOMPLETE.
