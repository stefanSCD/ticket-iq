# Notifications and delivery — Architecture decision

Document ID: `TN-NTF-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Domain events create notification intents after the underlying transaction commits. Delivery is asynchronous, so the equipment workflow must remain correct when an email provider is slow, unavailable, or delivers the same message more than once.

## Requirements and guidance

### TN-NTF-ADR-01

Notification intents are created through a transactional outbox and consumed asynchronously.

### TN-NTF-ADR-02

Delivery logs contain internal IDs and provider response codes, not full rendered email bodies.

### TN-NTF-ADR-03

A read receipt is not a domain action: reading an offer notification does not accept the waiting-list offer.
