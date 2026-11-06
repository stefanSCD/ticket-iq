# Movement between university labs — API contract

Document ID: `TN-XFR-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

The multi-lab release tracks physical custody separately from ownership. Moving an asset between labs must not lose the source and destination acknowledgements or silently move a borrower's confirmed pickup location.

## Requirements and guidance

### TN-XFR-API-01

POST /v1/transfers requires assetId, sourceLabId, destinationLabId, startAt, and endAt.

### TN-XFR-API-02

POST /v1/transfers/{id}/dispatch rejects an asset with an Open loan using 409 ASSET_ON_LOAN.

### TN-XFR-API-03

POST /v1/transfers/{id}/receive requires a destination-lab grant and the scanned asset UUID.

### TN-XFR-API-04

A repeated receive request returns the completed transfer without duplicating custody history.
