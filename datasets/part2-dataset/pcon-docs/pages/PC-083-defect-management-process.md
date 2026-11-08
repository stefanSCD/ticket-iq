# Defect Management Process and Severity Definitions

| Field | Value |
|---|---|
| Page ID | PC-083 |
| Owner | Sofia Brandt |
| Last updated | 2026-08-10 |

## Severity

| Severity | Definition | Example |
|---|---|---|
| Critical | Requirement with priority Critical violated in normal use, or safety/security impact, no workaround | Reconnection regularly above limit |
| High | Main function impaired, workaround exists | Media audio not restored, manual reconnect helps |
| Medium | Secondary function impaired | Diagnostic event missing |
| Low | Cosmetic or minor | Wrong text in a log line |

## Triage SLA

| Severity | Triage within |
|---|---|
| Critical | 1 working day |
| High | 3 working days |

Triage happens in the defect triage meeting (Tuesday and Thursday) or ad hoc for Critical defects.

## Lifecycle

1. Tester creates a Bug with environment, SW version, execution ID, trace.
2. Triage sets severity and assignee.
3. Developer fixes and links the merge request.
4. **Verification and closure are done by the test team only.** A Bug can only be closed by a tester after the fix has been verified on HiL or in the vehicle in the environment where the defect was found. SiL verification alone is not sufficient for closing.
5. Reopened Bugs return to triage.

## Defect data

Defects are exported as DEF-xxx records to the DefectTrackingSystem export used for the traceability graph. Each defect must be linked to at least one failed execution and one affected component.
