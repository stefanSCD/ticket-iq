# CareQueue — Security and privacy boundaries

**Status:** Active

## About

CareQueue: Outpatient appointment and administration platform. The page is authoritative only in the synthetic project context.

## Identity

Bearer tokens identify principals. Services validate token status, tenant scope and record ownership before responding with sensitive state.

## Minimization

Requests and logs should contain stable references rather than passwords, personal attachments or credentials. Synthetic examples in this dataset do not represent real users.

## Audit

Mutations require event correlation and actor attribution. Auditability does not specify a feature-specific retention duration.

## Controls

Duplicate operations must be idempotent, and cross-tenant record access must be rejected before reading protected data.
