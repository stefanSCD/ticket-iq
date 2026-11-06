# Catalog and asset lifecycle — Architecture decision

Document ID: `TN-CAT-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

A department can own several physical units of the same equipment model. The catalog must distinguish a model description from a uniquely tracked unit; changing a display label must never change a reservation reference.

## Requirements and guidance

### TN-CAT-ADR-01

Asset UUIDs are foreign keys in reservations and loans so that a renamed model cannot detach its transaction history.

### TN-CAT-ADR-02

Retirement is a lifecycle transition rather than a physical database deletion.

### TN-CAT-ADR-03

Photo objects are stored privately; catalog responses return short-lived authorized download links.
