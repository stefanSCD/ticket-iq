# Equipment kits and bundled items — Architecture decision

Document ID: `TN-KIT-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Some borrowable equipment is assembled from several tracked units. A field-recording kit has one reservation and one borrower-facing loan but its component units still need individual availability and condition tracking.

## Requirements and guidance

### TN-KIT-ADR-01

All component interval writes in a kit reservation belong to one PostgreSQL transaction.

### TN-KIT-ADR-02

A tracked component can belong to a kit definition and also be listed individually, but interval constraints still apply to its single asset UUID.

### TN-KIT-ADR-03

Kits are logical bundles; their definitions do not replace or merge the identity of component units.
