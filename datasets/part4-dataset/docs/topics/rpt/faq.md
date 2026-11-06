# Reports, calendars, and exports — Staff FAQ

Document ID: `TN-RPT-FAQ`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Managers use operational reports to understand completed loans and missed pickups. Reports preserve the distinction between a UTC event instant and a local calendar date, especially when the university changes daylight-saving offset.

## Requirements and guidance

### TN-RPT-FAQ-01

An ordinary CSV report can contain up to 25000 data rows, excluding its header.

### TN-RPT-FAQ-02

A completed-loan report can include a loan whose return inspection is still pending because receipt already occurred.

### TN-RPT-FAQ-03

The same local date range can span a different number of UTC hours when daylight-saving time changes.
