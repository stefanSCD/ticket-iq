# Notifications and delivery — Workflow

Document ID: `TN-NTF-WF`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Domain events create notification intents after the underlying transaction commits. Delivery is asynchronous, so the equipment workflow must remain correct when an email provider is slow, unavailable, or delivers the same message more than once.

## Requirements and guidance

### TN-NTF-WF-01

The notification inbox lists newest first and marks an item read only after an explicit read action.

### TN-NTF-WF-02

A worker records provider message ID, attempt time, and the final delivery outcome for staff troubleshooting.

### TN-NTF-WF-03

The delivery worker deduplicates intents using domain event ID, recipient ID, and channel.

### TN-NTF-WF-04

Daily digests are proposed; digest cutoff time, lab time zone selection, and included event types are undecided.
