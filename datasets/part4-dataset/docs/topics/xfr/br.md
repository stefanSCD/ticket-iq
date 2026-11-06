# Movement between university labs — Business rules

Document ID: `TN-XFR-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

The multi-lab release tracks physical custody separately from ownership. Moving an asset between labs must not lose the source and destination acknowledgements or silently move a borrower's confirmed pickup location.

## Requirements and guidance

### TN-XFR-BR-01

A lab transfer requires an asset with no Open loan and no confirmed reservation overlapping the planned transfer interval.

### TN-XFR-BR-02

Dispatch marks the asset InTransit and removes it from bookable pickup inventory until destination receipt.

### TN-XFR-BR-03

Destination receipt records the receiving staff member and changes the asset's current lab; the owning department remains unchanged.

### TN-XFR-BR-04

A confirmed reservation retains its pickup lab unless that reservation is explicitly changed through its normal edit workflow.

### TN-XFR-BR-05

A destination technician must acknowledge arrival within 4 staffed operating hours after recorded physical delivery.
