# Catalog and asset lifecycle — API contract

Document ID: `TN-CAT-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

A department can own several physical units of the same equipment model. The catalog must distinguish a model description from a uniquely tracked unit; changing a display label must never change a reservation reference.

## Requirements and guidance

### TN-CAT-API-01

POST /v1/assets assigns the UUID server-side and returns 409 ASSET_TAG_EXISTS when the asset tag is already used.

### TN-CAT-API-02

PATCH /v1/assets/{id} accepts displayName and conditionNote; assetId and assetTag are immutable after creation.

### TN-CAT-API-03

POST /v1/assets/{id}/retire returns 409 ASSET_IN_USE when any retirement precondition fails.

### TN-CAT-API-04

GET /v1/assets excludes Retired units unless lifecycle=all is explicitly requested by an authorized staff member.
