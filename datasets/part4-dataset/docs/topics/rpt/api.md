# Reports, calendars, and exports — API contract

Document ID: `TN-RPT-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Managers use operational reports to understand completed loans and missed pickups. Reports preserve the distinction between a UTC event instant and a local calendar date, especially when the university changes daylight-saving offset.

## Requirements and guidance

### TN-RPT-API-01

POST /v1/report-exports accepts reportType=completed_loans, labIds, fromAt, and toAt and returns 202 with a job ID.

### TN-RPT-API-02

GET /v1/report-exports/{id}/download requires the original requester and current manager grants for the exported labs.

### TN-RPT-API-03

An export that reaches its row cap returns truncated=true with the applied cap in result metadata.

### TN-RPT-API-04

POST /v1/report-exports rejects a requested lab outside the actor's grants with 403 LAB_ACCESS_REQUIRED.
