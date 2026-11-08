# Phone Connectivity (PCON) – Project Overview

| Field | Value |
|---|---|
| Page ID | PC-001 |
| Space | Phone Connectivity |
| Owner | Mara Lindqvist (Product Owner) |
| Last updated | 2026-09-02 |
| Status | Approved |

## Purpose

The Phone Connectivity project (Jira key **PCON**) delivers the Bluetooth phone connectivity services of the **HU4** infotainment head unit for the vehicle program **Meridian**. The project is responsible for everything that happens between a paired phone and the head unit after pairing has been completed: automatic reconnection, profile restoration, multi-phone handling, phonebook synchronization, diagnostics, and the status information shown to the driver.

The flagship feature of Release 1 (R1) is **FEAT-001 – Bluetooth Phone Automatic Reconnection**: a phone that was previously paired with the vehicle shall reconnect automatically after the vehicle ignition is switched on, without any interaction from the driver.

## Why this project exists

Customer clinics on the predecessor platform (HU3) showed that "my phone does not connect when I start the car" was the most frequent connectivity complaint. Field data from HU3 showed a median reconnection time of 14 seconds, with a long tail above 30 seconds. Meridian targets a reconnection that the driver perceives as immediate: the phone should be connected before the driver leaves the parking space.

## Main deliverables

1. Automatic reconnection after ignition (REQ-001 … REQ-007, see PC-011).
2. Multi-phone priority handling for up to two simultaneously connected phones (PC-019).
3. Link-loss reconnection while driving (PC-020).
4. Phonebook and call-history synchronization via PBAP (PC-022).
5. Diagnostic events and diagnostic trouble codes for connectivity (PC-017, PC-089).
6. HMI status information delivered to the HMI Platform team through the HMI Connectivity Presenter (PC-039).

## Team

The PCON team is a single cross-functional Scrum team of nine people plus a part-time HiL bench engineer. Roles and responsibilities are listed in PC-004. The team works in two-week sprints; sprint boundaries are on Wednesdays.

## System context

The connectivity software runs on the application processor of HU4 and is composed of ten software components (COMP-001 … COMP-010, see PC-031). It sits between:

- the **vehicle network**, from which it receives ignition and power-mode information through the Vehicle State Adapter;
- the **Bluetooth stack** (Nimbus BT Stack 5.2, supplied by Sylvan Wireless), accessed only through the BT Stack Adapter;
- the **HMI Platform**, which renders the status icons, toasts and settings screens;
- the **Diagnostics Platform**, which stores diagnostic trouble codes and makes them available to workshop testers.

## How to navigate this space

| Area | Pages |
|---|---|
| Governance and process | PC-001 – PC-010 |
| Requirements | PC-011 – PC-030 |
| Architecture and components | PC-031 – PC-050 |
| Decisions and meeting notes | PC-051 – PC-065 |
| Testing | PC-066 – PC-082 |
| Defects, diagnostics, build and release | PC-083 – PC-092 |
| Supplier, compliance, onboarding, roadmap | PC-093 – PC-100 |

New team members should start with the onboarding guide (PC-097) and the glossary (PC-003).

## Current status (September 2026)

- Requirements REQ-001 … REQ-006 are approved; REQ-007 is still in draft.
- Connectivity SW release 2.3.0 has been tested in SiL, HiL and Vehicle. 16 executions were run; 7 failed. The dominant failure is delayed reconnection, tracked as DEF-001.
- The B-Sample software freeze has been reached on 2026-09-30.
- The team is preparing the C-Sample release (see PC-005).
