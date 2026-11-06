# Damage and missing-accessory incidents — Architecture decision

Document ID: `TN-DAM-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

An incident is an evidence record, not a finding of borrower liability. Technicians document what they observed and managers classify the incident before repair or financial questions are handled outside the v1.1 product.

## Requirements and guidance

### TN-DAM-ADR-01

Incident evidence is append-only so a corrected note does not destroy the original observation.

### TN-DAM-ADR-02

Borrower-facing loan status contains an incident reference but does not embed private staff notes or photographs.

### TN-DAM-ADR-03

A safety block has its own reason and cannot be cleared merely by closing the associated loan.
