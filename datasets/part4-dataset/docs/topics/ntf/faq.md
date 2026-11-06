# Notifications and delivery — Staff FAQ

Document ID: `TN-NTF-FAQ`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Domain events create notification intents after the underlying transaction commits. Delivery is asynchronous, so the equipment workflow must remain correct when an email provider is slow, unavailable, or delivers the same message more than once.

## Requirements and guidance

### TN-NTF-FAQ-01

A temporary email failure receives up to 5 retries after the initial send attempt.

### TN-NTF-FAQ-02

Disabling optional email does not remove in-app records of changes to your borrowing.

### TN-NTF-FAQ-03

A permanent invalid address must be corrected before a new notification can be sent successfully.
