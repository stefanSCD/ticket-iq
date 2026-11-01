# CareQueue — Project overview and glossary

**Status:** Active

## About

CareQueue: Outpatient appointment and administration platform. The page is authoritative only in the synthetic project context.

## Scope

CareQueue handles non-clinical scheduling and administrative workflows for outpatient practices. This project is fictional. It has 10 independent feature areas and a set of shared cross-cutting constraints.

## Terms

A request is a user-intended operation. An event records an observed transition. A policy is an approved product decision. A ticket describes work; it does not override a policy unless approved.

## Roles

patient, clinic receptionist, clinician, clinic administrator. Each role is limited to the records and tenants it is authorized to act upon.

## Interpretation

Product policy lives in business rules; functional specifications define user flows; API contracts define network semantics; ADRs explain engineering choices; FAQ is support-facing context. Similarity to a feature does not automatically answer a ticket question.
