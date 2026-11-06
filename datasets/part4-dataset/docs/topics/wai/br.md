# Waiting lists and offers — Business rules

Document ID: `TN-WAI-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

The waiting list offers a newly freed interval to an eligible borrower. An offer is a temporary hold rather than an automatic reservation; the borrower still has to accept before its deadline.

## Requirements and guidance

### TN-WAI-BR-01

Waiting-list entries are scoped to an equipment model, pickup lab, and requested interval.

### TN-WAI-BR-02

Eligible entries for the same freed interval are considered in order of joinedAt, with entry UUID as the tie-breaker.

### TN-WAI-BR-03

A waiting-list offer temporarily blocks the offered unit until acceptance or offer expiry.

### TN-WAI-BR-04

A borrower may have only one active waiting-list entry for the same model, lab, and interval.

### TN-WAI-BR-05

A waiting-list offer expires 20 minutes after it is created.
