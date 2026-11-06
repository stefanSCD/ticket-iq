# Authentication and lab-scoped permissions — API contract

Document ID: `TN-SEC-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

University single sign-on identifies a user, while ToolNest grants authorize actions for particular labs. Being staff in one lab must not grant broad access to borrower information or management actions in another.

## Requirements and guidance

### TN-SEC-API-01

GET /v1/me/grants returns the signed-in user's current lab-scoped grants.

### TN-SEC-API-02

All mutation endpoints derive actorId from the authenticated session rather than a request body field.

### TN-SEC-API-03

An authorized request must verify the labId of the target resource, not only a labId supplied by the client.

### TN-SEC-API-04

The identity provider subject is the stable external user identifier; an email-address change does not create a new borrower account.
