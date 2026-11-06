# Overdue loans and account restrictions — Business rules

Document ID: `TN-OVD-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

ToolNest v1.1 tracks late loans and borrowing restrictions without collecting money. Overdue state follows the physical receipt time; a delayed staff inspection must not make the borrower appear to keep equipment longer.

## Requirements and guidance

### TN-OVD-BR-01

An Open loan becomes overdue when server time is later than dueAt and no receipt has been recorded.

### TN-OVD-BR-02

Recording receipt stops overdue duration at receivedAt, even while condition inspection is pending.

### TN-OVD-BR-03

A borrower with an overdue loan cannot create a new reservation or check out another unit.

### TN-OVD-BR-04

Returning the last overdue unit clears the overdue-based restriction; an independent manual suspension still applies.

### TN-OVD-BR-05

The first overdue email is scheduled 2 elapsed hours after dueAt if the loan is still unreceived.
