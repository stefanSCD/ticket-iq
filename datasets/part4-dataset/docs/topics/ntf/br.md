# Notifications and delivery — Business rules

Document ID: `TN-NTF-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Domain events create notification intents after the underlying transaction commits. Delivery is asynchronous, so the equipment workflow must remain correct when an email provider is slow, unavailable, or delivers the same message more than once.

## Requirements and guidance

### TN-NTF-BR-01

Reservation approval, staff cancellation, waiting-list offer, and overdue events create in-app notification intents for the affected borrower.

### TN-NTF-BR-02

Borrowers can disable optional email copies; the corresponding in-app transaction notifications remain enabled.

### TN-NTF-BR-03

Notification content must not disclose another borrower's name, email address, or reservation purpose.

### TN-NTF-BR-04

A notification delivery failure does not roll back a committed reservation, loan, or return.

### TN-NTF-BR-05

A transient email delivery failure is retried at most 3 times after the initial send attempt.
