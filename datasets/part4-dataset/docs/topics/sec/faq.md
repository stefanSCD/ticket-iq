# Authentication and lab-scoped permissions — Staff FAQ

Document ID: `TN-SEC-FAQ`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

University single sign-on identifies a user, while ToolNest grants authorize actions for particular labs. Being staff in one lab must not grant broad access to borrower information or management actions in another.

## Requirements and guidance

### TN-SEC-FAQ-01

An inactive signed-in session remains usable for 45 minutes after its last authenticated API request.

### TN-SEC-FAQ-02

Selecting another lab in the header does not grant access to that lab's staff screens.

### TN-SEC-FAQ-03

If a user's email changes, their existing loans stay attached to the same university identity.
