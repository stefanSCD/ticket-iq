# Reports, calendars, and exports — Business rules

Document ID: `TN-RPT-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Managers use operational reports to understand completed loans and missed pickups. Reports preserve the distinction between a UTC event instant and a local calendar date, especially when the university changes daylight-saving offset.

## Requirements and guidance

### TN-RPT-BR-01

The completed-loans report includes loans with a recorded receipt in the selected interval and attributes them to the pickup lab.

### TN-RPT-BR-02

Report time filters use half-open UTC intervals: an event at fromAt is included and an event at toAt is excluded.

### TN-RPT-BR-03

A manager may report only on labs for which they hold the lab_manager grant.

### TN-RPT-BR-04

CSV exports escape spreadsheet formula prefixes =, +, -, and @ in free-text fields by prepending a single quote.

### TN-RPT-BR-05

An ordinary report CSV export is limited to 10000 data rows, excluding the header.
