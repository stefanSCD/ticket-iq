# Lab calendars and timestamp conventions

Document ID: `TN-OV-04`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Shared project context for the active ToolNest baseline.

## Requirements and guidance

### TN-OV-04-01

Normal staffed operating hours are Monday through Friday, 09:00 to 17:00 in the relevant lab's IANA time zone, excluding closures recorded in that lab's calendar.

### TN-OV-04-02

A staffed operating hour counts only time within staffed opening intervals; elapsed-hour deadlines continue through closures and weekends.

### TN-OV-04-03

A business-day deadline advances through open local working dates and retains the original local wall-clock time on the resulting date; closed dates are skipped.

### TN-OV-04-04

Timestamps crossing system boundaries use ISO 8601 with an explicit UTC offset; stored event instants use UTC.

### TN-OV-04-05

Calendar-day intervals follow local dates and may span fewer or more than 24 elapsed hours at daylight-saving boundaries.

### TN-OV-04-06

Client clocks are presentation inputs only and cannot establish authoritative checkout, receipt, expiry, or authorization times.
