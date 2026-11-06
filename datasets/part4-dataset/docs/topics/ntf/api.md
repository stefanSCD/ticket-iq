# Notifications and delivery — API contract

Document ID: `TN-NTF-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Domain events create notification intents after the underlying transaction commits. Delivery is asynchronous, so the equipment workflow must remain correct when an email provider is slow, unavailable, or delivers the same message more than once.

## Requirements and guidance

### TN-NTF-API-01

GET /v1/me/notifications returns only the authenticated borrower's inbox using cursor pagination.

### TN-NTF-API-02

POST /v1/me/notifications/{id}/read is idempotent and cannot mark another borrower's item as read.

### TN-NTF-API-03

PATCH /v1/me/notification-preferences accepts optionalEmailEnabled without disabling in-app transaction notifications.

### TN-NTF-API-04

An email attempt with a permanent invalid-recipient response is marked FailedPermanent and is not retried.
