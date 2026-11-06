# Equipment kits and bundled items — Business rules

Document ID: `TN-KIT-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Some borrowable equipment is assembled from several tracked units. A field-recording kit has one reservation and one borrower-facing loan but its component units still need individual availability and condition tracking.

## Requirements and guidance

### TN-KIT-BR-01

A kit definition lists required component asset UUIDs and optional accessory descriptions.

### TN-KIT-BR-02

Confirming a kit reservation atomically reserves every required component for the requested interval.

### TN-KIT-BR-03

A kit reservation fails if any required component is unavailable; no subset is silently confirmed.

### TN-KIT-BR-04

The loan stores a snapshot of the kit composition at checkout so later definition edits do not change return obligations.

### TN-KIT-BR-05

A kit may contain at most 12 required tracked component units.
