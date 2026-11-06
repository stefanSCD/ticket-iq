# Pickup deadlines and no-shows — Staff FAQ

Document ID: `TN-NOS-FAQ`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Uncollected reservations need a defined lifecycle after the start time. No-show processing releases a booked slot and may supply operational data, but it must never race with a successful physical handover.

## Requirements and guidance

### TN-NOS-FAQ-01

Reservations are held for 45 elapsed minutes after the scheduled start before being treated as no-shows.

### TN-NOS-FAQ-02

A slow expiry worker does not change the scheduled pickup deadline displayed on the reservation.

### TN-NOS-FAQ-03

A no-show is not a cancelled loan; no loan exists until checkout succeeds.
