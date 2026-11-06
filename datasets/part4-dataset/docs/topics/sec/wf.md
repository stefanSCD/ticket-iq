# Authentication and lab-scoped permissions — Workflow

Document ID: `TN-SEC-WF`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

University single sign-on identifies a user, while ToolNest grants authorize actions for particular labs. Being staff in one lab must not grant broad access to borrower information or management actions in another.

## Requirements and guidance

### TN-SEC-WF-01

Changing the selected lab updates the interface context but never changes the actor's stored grants.

### TN-SEC-WF-02

The server checks authorization before returning protected borrower or staff data.

### TN-SEC-WF-03

An unauthenticated request returns 401; an authenticated actor lacking a required grant receives 403.

### TN-SEC-WF-04

Visiting users without university identities have no agreed account sponsorship, verification, or expiry policy.
