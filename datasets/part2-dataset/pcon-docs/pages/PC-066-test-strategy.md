# Test Strategy

| Field | Value |
|---|---|
| Page ID | PC-066 |
| Owner | Sofia Brandt |
| Last updated | 2026-07-06 |

## Test levels

| Level | Environment | Purpose |
|---|---|---|
| Unit tests | Developer PC / CI | Logic of individual components |
| Component integration | SiL | Interaction of PCON components with simulated stack and vehicle |
| System tests | HiL | Real head unit, real Bluetooth radio, reference phones |
| Vehicle tests | Prototype vehicles | Real vehicle network, real environment |
| Field tests | Test fleet | Long-term behavior, real usage |

## Principles

- Every approved requirement is verified on at least one level above unit tests.
- Timing requirements (REQ-002) must be verified in HiL **and** Vehicle, because SiL does not reproduce radio timing.
- Defects are reproduced on the lowest level possible.
- All HiL and vehicle executions produce traces in the TraceRepository.

## Evidence for release

The release evidence consists of HiL and vehicle executions for all approved requirements. For requirements that do not depend on radio behavior (e.g. REQ-006 diagnostics, parts of REQ-003), the team discussed whether SiL executions alone could be accepted as verification evidence. Quality Management has not yet confirmed this; currently there is **no agreed rule**.

## Test automation

- SiL: fully automated, nightly.
- HiL: automated with robot-controlled phones (button presses via phone automation frameworks); weekly full regression and on-demand runs.
- Vehicle: manual execution following test procedures; results entered in the TestManagementSystem.

## Roles

Test Lead: Sofia Brandt. HiL: Daniel Szabo. Vehicle: Lukas Becker.
