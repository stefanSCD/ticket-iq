# Authentication and lab-scoped permissions — Architecture decision

Document ID: `TN-SEC-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

University single sign-on identifies a user, while ToolNest grants authorize actions for particular labs. Being staff in one lab must not grant broad access to borrower information or management actions in another.

## Requirements and guidance

### TN-SEC-ADR-01

Authentication uses the fictional university OIDC provider; ToolNest does not store university passwords.

### TN-SEC-ADR-02

Current grant state is read during authorization rather than trusting a long-lived role claim in the browser.

### TN-SEC-ADR-03

Authorization decisions use internal user IDs mapped to the identity provider subject.
