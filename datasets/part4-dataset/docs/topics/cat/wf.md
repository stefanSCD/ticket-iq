# Catalog and asset lifecycle — Workflow

Document ID: `TN-CAT-WF`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

A department can own several physical units of the same equipment model. The catalog must distinguish a model description from a uniquely tracked unit; changing a display label must never change a reservation reference.

## Requirements and guidance

### TN-CAT-WF-01

The asset creation form requires model, owning lab, asset tag, serial number, and initial condition; serial number may be explicitly recorded as unknown.

### TN-CAT-WF-02

Catalog filters combine lab, equipment category, and lifecycle state using AND semantics; the default lifecycle filter is Active.

### TN-CAT-WF-03

A retirement attempt displays the blocking loan, reservation, or maintenance reference to an authorized lab manager.

### TN-CAT-WF-04

Reactivation of a retired unit is an open product decision; no reactivation workflow is approved.
