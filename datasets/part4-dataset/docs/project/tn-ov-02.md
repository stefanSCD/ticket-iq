# Architecture and repository map

Document ID: `TN-OV-02`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Shared project context for the active ToolNest baseline.

## Requirements and guidance

### TN-OV-02-01

The fictional repository toolnest contains web/ for a React TypeScript interface, server/ for a Python FastAPI modular monolith, and workers/ for background jobs.

### TN-OV-02-02

PostgreSQL 16 is the transactional system of record for asset state, reservation intervals, loans, grants, and outbox events.

### TN-OV-02-03

Redis is used for expendable cache data and worker coordination; cache contents do not authorize borrowing or override database conflicts.

### TN-OV-02-04

Private object storage contains catalog photographs, incident evidence, and generated exports; authorization is checked before issuing download links.

### TN-OV-02-05

Modules use explicit service calls within the application and asynchronous domain events for notifications and integrations.

### TN-OV-02-06

The project integrates with a fictional university OIDC provider and a fictional mail service; there are no real service credentials or real borrower records in this dataset.
