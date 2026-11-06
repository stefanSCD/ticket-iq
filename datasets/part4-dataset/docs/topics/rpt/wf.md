# Reports, calendars, and exports — Workflow

Document ID: `TN-RPT-WF`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Managers use operational reports to understand completed loans and missed pickups. Reports preserve the distinction between a UTC event instant and a local calendar date, especially when the university changes daylight-saving offset.

## Requirements and guidance

### TN-RPT-WF-01

A local date selection is converted to UTC using the selected lab's IANA time zone; never assume every day has 24 hours.

### TN-RPT-WF-02

Export jobs recheck the requester's current lab access before making a result available for download.

### TN-RPT-WF-03

The report footer shows the selected lab, local date range, generatedAt instant, and whether a row limit was reached.

### TN-RPT-WF-04

An equipment utilization percentage is requested, but its numerator, denominator, and treatment of maintenance time are undecided.
