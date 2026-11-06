# Damage and missing-accessory incidents — API contract

Document ID: `TN-DAM-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

An incident is an evidence record, not a finding of borrower liability. Technicians document what they observed and managers classify the incident before repair or financial questions are handled outside the v1.1 product.

## Requirements and guidance

### TN-DAM-API-01

POST /v1/incidents requires assetId, loanId, observedAt, incidentType, and a nonempty observation.

### TN-DAM-API-02

POST /v1/incidents/{id}/dispositions requires lab_manager and a reason; safety blocks change transactionally with the disposition.

### TN-DAM-API-03

GET /v1/incidents/{id}/photos enforces incident_reader on each request and returns private download links.

### TN-DAM-API-04

PUT /v1/incidents/{id}/evidence is not supported; use POST /v1/incidents/{id}/corrections to append a correction.
