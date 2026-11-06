# Catalog and asset lifecycle — Business rules

Document ID: `TN-CAT-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

A department can own several physical units of the same equipment model. The catalog must distinguish a model description from a uniquely tracked unit; changing a display label must never change a reservation reference.

## Requirements and guidance

### TN-CAT-BR-01

Each physical unit has an immutable asset UUID and a university-wide unique asset tag; display names are not identifiers.

### TN-CAT-BR-02

Only Active units can enter a new reservation; Retired units remain readable on existing loans and audit entries.

### TN-CAT-BR-03

A lab manager may retire a unit only when it has no open loan, future confirmed reservation, or outstanding maintenance job.

### TN-CAT-BR-04

Model-level specification edits do not overwrite a unit-specific condition note.

### TN-CAT-BR-05

Catalog photographs accept JPEG and PNG only, with a maximum size of 8 MiB per file.
