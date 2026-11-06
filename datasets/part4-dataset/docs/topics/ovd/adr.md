# Overdue loans and account restrictions — Architecture decision

Document ID: `TN-OVD-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

ToolNest v1.1 tracks late loans and borrowing restrictions without collecting money. Overdue state follows the physical receipt time; a delayed staff inspection must not make the borrower appear to keep equipment longer.

## Requirements and guidance

### TN-OVD-ADR-01

Overdue duration is derived from timestamps rather than incremented by a scheduled counter.

### TN-OVD-ADR-02

Overdue restrictions are derived from current loan state and are not permanent account flags.

### TN-OVD-ADR-03

The first reminder schedule uses elapsed UTC time and does not pause while the desk is closed.
