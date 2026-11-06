# Authentication and lab-scoped permissions — Business rules

Document ID: `TN-SEC-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

University single sign-on identifies a user, while ToolNest grants authorize actions for particular labs. Being staff in one lab must not grant broad access to borrower information or management actions in another.

## Requirements and guidance

### TN-SEC-BR-01

ToolNest v1.1 requires university single sign-on for application access; an authenticated session alone does not grant staff permissions.

### TN-SEC-BR-02

lab_technician and lab_manager grants are scoped to one lab and do not confer access to another lab.

### TN-SEC-BR-03

Borrowers may read their own reservations and loans; staff access to another borrower's transaction requires the relevant lab grant.

### TN-SEC-BR-04

Permission revocation takes effect on the next authorized API request, even if the user keeps the browser open.

### TN-SEC-BR-05

A session expires after 30 minutes without an authenticated API request.
