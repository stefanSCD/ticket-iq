# PCON Documentation – Hidden Knowledge Registry

**NOT part of the documentation corpus.** Do not index this file for retrieval. It is the answer key used to generate and label tickets (Resolved / Unresolved / Partially resolved / Conflicting / Already clear).

Project: Phone Connectivity (Jira key `PCON`), infotainment head unit platform **HU4**, vehicle program **Meridian**. 100 pages, IDs `PC-001` … `PC-100`. Built on the Bluetooth Reconnection KG PoC data (FEAT-001, REQ-001…007, COMP-001…005, TEST-001…010, EXEC-001…016, TRACE-001…010, DEF-001…003); everything else is an extension.

## Cast (fictional)

| Person | Role |
|---|---|
| Mara Lindqvist | Product Owner, Phone Connectivity |
| Tobias Kern | System Architect, Connectivity domain |
| Andrei Popescu | Tech Lead, Connectivity |
| Sofia Brandt | Test Lead |
| Jonas Weber | HMI Lead |
| Elena Rusu | Diagnostics owner (COMP-005) |
| Karim Haddad | Cybersecurity Manager |
| Petra Novak | Release Manager |
| Radu Ionescu | Developer, COMP-002 Bluetooth Connection Manager |
| Nina Hoffmann | Developer, COMP-004 Bluetooth Profile Service |
| Felix Wagner | Developer, COMP-003 Pairing Data Store |
| Ioana Marin | Developer, COMP-007 Phonebook Sync Service |
| Daniel Szabo | HiL bench engineer |
| Lukas Becker | Vehicle test engineer |
| Liam O'Connor | Supplier contact, Sylvan Wireless (Nimbus BT Stack) |

---

## 1. Resolved facts (clearly answered, single source of truth, no contradiction)

| ID | Fact | Page(s) |
|---|---|---|
| R-01 | Jira project key is PCON; issue types Story, Bug, Task, Spike, Decision | PC-007 |
| R-02 | Feature FEAT-001 = Bluetooth Phone Automatic Reconnection, owned by Mara Lindqvist | PC-001, PC-004 |
| R-03 | R1 boundary: one or more previously paired phones, reconnection after ignition and link loss; first-time pairing UX is owned by HMI Platform team, not PCON | PC-002 |
| R-04 | Wi-Fi, Android Auto and Apple CarPlay projection are out of scope for PCON (owned by Projection team) | PC-002, PC-028 |
| R-05 | REQ-001: auto-reconnect previously paired phone after ignition ON, no user interaction | PC-012 |
| R-06 | REQ-003: stored pairing info reused; no new pairing confirmation | PC-014 |
| R-07 | REQ-005 profiles restored: HFP (phone audio) and A2DP (media audio); AVRCP restored together with A2DP | PC-016 |
| R-08 | REQ-006 diagnostic events: RECONNECT_START, RECONNECT_COMPLETE, RECONNECT_FAIL, RECONNECT_DURATION | PC-017, PC-055 |
| R-09 | REQ-007 status is Draft, priority Low | PC-018 |
| R-10 | Max simultaneously connected phones = 2 (one primary for HFP+A2DP, one secondary HFP only) | PC-019, PC-052 |
| R-11 | Multi-phone priority rule = Most-Recently-Used (MRU) by last successful connection timestamp | PC-052 |
| R-12 | Link keys are stored encrypted, keys wrapped by HSM (AES-256-GCM) | PC-025, PC-053 |
| R-13 | Pairing method: Secure Simple Pairing with Numeric Comparison; legacy PIN pairing not supported | PC-025 |
| R-14 | Phonebook and call history of a phone are deleted when the phone is unpaired | PC-026 |
| R-15 | Factory reset deletes all pairing data, phonebooks, and connectivity settings | PC-026, PC-034 |
| R-16 | Pairing list eviction when full = Least-Recently-Used device removed | PC-034 |
| R-17 | Persistence location: encrypted partition `/persist/bt/` | PC-047 |
| R-18 | Per-profile restoration timeout = 5 s | PC-035, PC-046 |
| R-19 | Reconnection retry delay = 2 s (ADR-001) | PC-051, PC-046 |
| R-20 | Reconnection state machine states: IDLE, WAIT_BT_READY, CONNECTING, RETRY_WAIT, PROFILE_RESTORE, CONNECTED, FAILED, SUSPENDED | PC-042 |
| R-21 | Vehicle State Adapter consumes signal `KL15_Status` and `PowerMode` via SOME/IP service `VehicleStateSrv` | PC-032, PC-045 |
| R-22 | BT stack = Nimbus BT Stack 5.2 by Sylvan Wireless, wrapped by COMP-009 BT Stack Adapter | PC-040, PC-093 |
| R-23 | Supplier bug-report response SLA = 10 business days via Sylvan support portal | PC-093 |
| R-24 | Diagnostics event schema fields: eventType, timestamp, deviceIdHash, attemptId, durationMs, resultCode, swVersion | PC-055 |
| R-25 | DTC B1A10 = BT module not responding; B1A11 = pairing storage corrupted; B1A12 = repeated reconnection failure | PC-089 |
| R-26 | Test environments SiL, HiL, Vehicle; HiL benches HIL-BT-01 and HIL-BT-02 | PC-067, PC-068 |
| R-27 | HiL uses shielded RF box with programmable attenuator (0–90 dB) | PC-068 |
| R-28 | Reference phone list has 12 phones (6 iOS, 6 Android) | PC-069 |
| R-29 | TEST-001…TEST-010 map to requirements as in PoC (e.g. TEST-002 → REQ-002) | PC-070 |
| R-30 | Each single execution verifying REQ-002 is FAIL when reconnection > 10 s | PC-070, PC-074 |
| R-31 | Nightly SiL regression starts 02:00 CET in GitLab CI | PC-076, PC-090 |
| R-32 | R1 test results: 16 executions on SW 2.3.0, 9 PASS / 7 FAIL | PC-078 |
| R-33 | EXEC-010 failed with 18.0 s in Vehicle; linked to DEF-001 | PC-078, PC-084 |
| R-34 | DEF-001 root cause: reconnection request queued behind PBAP/inquiry operations in BT Stack Adapter queue; fix = priority queue, target COMP-002 2.3.1 | PC-084 |
| R-35 | DEF-003 root cause: A2DP connect attempted while HFP SLC still in setup; fixed in COMP-004 3.1.1, status Resolved | PC-086 |
| R-36 | DEF-002: completion event lost when shutdown occurs within 200 ms of completion; In Progress | PC-085 |
| R-37 | Severity definitions Critical/High/Medium/Low | PC-083 |
| R-38 | Critical defects triaged within 1 working day | PC-083 |
| R-39 | Branching: trunk-based, release branches `release/r1.x` | PC-092 |
| R-40 | Component versioning: semantic versioning per component | PC-092 |
| R-41 | Functional safety classification: QM | PC-096 |
| R-42 | SOP = 2027-06-01; C-Sample release = 2026-12-15; B-Sample SW freeze = 2026-09-30 | PC-005 |
| R-43 | Definition of Done includes passing HiL regression for changed requirements | PC-006 |
| R-44 | HiL bench booking via BenchBooker tool | PC-068, PC-099 |
| R-45 | Memory budget for connectivity domain ≤ 12 MB RSS; COMP-002 CPU ≤ 5% average during startup | PC-029 |
| R-46 | HMI states: Disconnected, Connecting, Connected, Partially connected (one profile missing) | PC-027 |
| R-47 | Success toast "Connected to <name>" shown 3 s | PC-027 |
| R-48 | Phonebook sync uses PBAP 1.2 vCard 3.0 | PC-022 |
| R-49 | Repository name `pcon-connectivity` in GitLab; components in `/components/<name>` | PC-090, PC-097 |
| R-50 | Field test fleet: 6 prototype vehicles, 3 routes (urban, highway, underground garage) | PC-080 |
| R-51 | Weak-signal test (TEST-008) uses attenuation step to −80 dBm at phone RSSI | PC-070, PC-068 |
| R-52 | Cybersecurity concept: TARA performed, BT attack surface rated "medium" | PC-095 |
| R-53 | Bluetooth SIG qualification required before SOP; owner Tobias Kern | PC-094 |
| R-54 | Trace format: `<ISO timestamp> <LEVEL> <component> <attemptId> <message>` | PC-049 |
| R-55 | Connectivity SW release 2.3.0 release notes contents | PC-091 |

## 2. Unresolved decisions (topic appears in docs, but no decision exists)

Representation: **E** = explicitly marked open/TBD somewhere; **S** = silent (topic touched, decision never made).

| ID | Missing decision | Where the topic is touched | Repr. |
|---|---|---|---|
| U-01 | Does auto-reconnect trigger on Comfort Mode wake-up (infotainment on without ignition)? | PC-024, PC-041, PC-059 | E |
| U-02 | Favourite phone vs MRU precedence | PC-052, PC-100 | E |
| U-03 | Upload of reconnection diagnostics to telematics backend | PC-036, PC-055, PC-063 | E |
| U-04 | Upgrade to Nimbus BT Stack 5.3 within R1? | PC-062, PC-093 | E |
| U-05 | Active call on phone at ignition ON: auto-transfer audio to car? | PC-012, PC-098 | S |
| U-06 | Link-loss reconnection: number of attempts / total timeout | PC-020 | E |
| U-07 | Manual reconnect of phone B while auto-reconnect of phone A is running: cancel A or queue? | PC-021, PC-033 | S |
| U-08 | Guest / valet mode: block auto-reconnect? | PC-002, PC-100 | S |
| U-09 | Pseudonymize phone names in traces? | PC-049, PC-095 | E |
| U-10 | Can the driver disable call-history download separately from contacts? | PC-026, PC-014 | S |
| U-11 | REQ-007 detection method and whether in R1 | PC-018, PC-059 | E |
| U-12 | Two connected phones requesting A2DP: which plays? | PC-019 | S |
| U-13 | PBAP phonebook download timeout | PC-022, PC-038 | S |
| U-14 | Set DTC B1A12 after how many consecutive failed cycles (N)? | PC-089 | E |
| U-15 | Reconnection allowed during OTA installation? | PC-024, PC-100 | S |
| U-16 | Fallback when HSM unavailable at startup | PC-053, PC-095 | E |
| U-17 | DEF-002 fix in R1 or R2? | PC-085, PC-063 | E |
| U-18 | Is AVRCP browsing (folder navigation) required? | PC-016 | S |
| U-19 | Show HFP indicators (phone battery, signal) in HMI? | PC-027 | S |
| U-20 | Owner of field test data analysis | PC-080 | E |
| U-21 | Phone deleted the vehicle (auth failure): keep trying it on subsequent ignition cycles, or exclude it from auto-reconnect? | PC-014, PC-033, PC-088 | S |
| U-22 | Active call when the run-on phase ends: hand the call back to the phone or drop it? (run-on behavior itself is documented) | PC-024 | S |
| U-23 | Accept SiL-only evidence for requirement verification? | PC-066, PC-082 | E |
| U-24 | Procure third HiL bench (HIL-BT-03)? | PC-068, PC-064 | E |
| U-25 | Device names with emoji / unsupported characters in HMI | PC-027, PC-039 | S |
| U-26 | Sync pairing list with user profile / cloud | PC-034, PC-100 | S |
| U-27 | Auto-reconnect in transport mode | PC-024 | S |
| U-28 | Does a phone-initiated connection count as a successful REQ-002 reconnection? | PC-013, PC-019 | S |
| U-29 | Number of vehicle cycles for multi-phone sign-off | PC-071, PC-077 | E |
| U-30 | Pairing data handling on vehicle owner change | PC-026, PC-034 | E |

## 3. Partially resolved topics (part documented, part missing)

| ID | Documented | Missing | Pages |
|---|---|---|---|
| P-01 | Transient errors: page timeout (0x04), LMP response timeout (0x22), connection timeout (0x08) | Classification of 0x0B (ACL already exists) and 0x0C (Command disallowed) | PC-048 |
| P-02 | Suspend reconnection below low-voltage threshold | Resume threshold / hysteresis | PC-024, PC-041 |
| P-03 | Factory reset deletes all pairing data | Owner change behavior | PC-026, PC-034 |
| P-04 | Per-profile timeout 5 s | Overall profile-restoration budget | PC-035, PC-046 |
| P-05 | HiL bench setup and booking tool | Rules for unattended night runs | PC-068 |
| P-06 | Phonebook delta sync method | Max number of contacts | PC-054 |
| P-07 | MRU priority | Tie-break when timestamps equal / missing | PC-052 |
| P-08 | HMI states (EN labels) | Localized labels for "Partially connected" | PC-027 |
| P-09 | DTC catalog codes and set conditions | Healing / clearing conditions of the DTCs | PC-089 |
| P-10 | Release milestones | Whether MAP is in R1 scope | PC-005, PC-023 |
| P-11 | Reference phone list | Inclusion of OS beta versions | PC-069 |
| P-12 | Trace format | Log level in production builds | PC-049 |
| P-13 | SSP numeric comparison; pre-2.1 phones cannot pair | What the HMI shows to users of legacy phones | PC-025 |
| P-14 | Severity definitions + Critical SLA | SLA for Low (and Medium) | PC-083 |
| P-15 | Field fleet and routes | Data upload method from vehicles | PC-080 |
| P-16 | Retry count/delay for connection | Retry on profile-level failure | PC-015, PC-035 |
| P-17 | CI pipeline stages | Signing of release artifacts | PC-090 |
| P-18 | Supplier SLA 10 business days | Escalation path for Critical stack bugs | PC-093 |
| P-19 | CarPlay phones: BT HFP stays connected | Which component owns the handover | PC-028 |
| P-20 | Diagnostics schema fields | Schema versioning strategy | PC-055 |
| P-21 | Endurance setup | Duration of R1 soak test | PC-081 |
| P-22 | Onboarding access steps | Whether HiL safety training is required | PC-097 |

## 4. Conflicting documentation (two pages disagree)

| ID | Topic | Page A says | Page B says |
|---|---|---|---|
| C-01 | REQ-002 timing start (t0) | PC-013: BT subsystem available (BT_READY) | PC-074: ignition ON (KL15) |
| C-02 | Max reconnection retries | PC-015 / PC-051: 1 | PC-046: default 3 |
| C-03 | Max paired devices | PC-034 / PC-046: 10 | PC-039: 8 |
| C-04 | Profile restoration order | PC-035: HFP then A2DP | PC-043: A2DP then HFP |
| C-05 | Diagnostic ring buffer size | PC-036: 500 events | PC-049: 1000 events |
| C-06 | Give-up timer | PC-042 / PC-046: 60 s | PC-033: 30 s |
| C-07 | Failure notification | PC-027 (REQ-027): no popup, icon only | PC-039: popup after give-up |
| C-08 | R1 timing KPI | PC-077: ≥98% cycles ≤10 s | PC-063: ≥95% |
| C-09 | R1 code freeze | PC-005: 2026-11-20 | PC-063: 2026-11-27 |
| C-10 | Who closes defects | PC-007: developer after SiL verification | PC-083: tester only after HiL/vehicle verification |
| C-11 | Phonebook sync | PC-054 (ADR-004): delta | PC-038: full sync on each connection |
| C-12 | Low-voltage threshold | PC-024: 9.0 V | PC-041: 8.5 V |
| C-13 | Retry delay | PC-051 / PC-046: 2 s | PC-033: 1.5 s |
| C-14 | DEF-001 severity | PC-084: Critical | PC-061: downgraded to High |
| C-15 | HFP version | PC-016: HFP 1.8 | PC-094: HFP 1.7 |

## 5. Notes for ticket generation

- Unresolved tickets should ask about the U-items; retrieval will return related pages that do **not** contain the decision.
- Partially-resolved tickets should combine one documented aspect with one missing aspect of the same P-item, so the correct behavior is to ask only about the missing part.
- Conflicting tickets should touch a C-item; the correct behavior is to name both pages and the contradiction.
- Several items are deliberately only one page deep (e.g. PC-039 vs PC-034); others need two hops (e.g. REQ page → ADR → config).

## 6. Already-clear tickets

Tickets that are self-contained (typo fixes, rename a log string, bump a test-bench firmware with given version, add a given phone to a list, etc.) do not need documentation. No planted content required.
