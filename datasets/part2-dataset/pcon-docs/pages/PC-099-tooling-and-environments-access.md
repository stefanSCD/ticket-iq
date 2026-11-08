# Tooling and Environments

| Field | Value |
|---|---|
| Page ID | PC-099 |
| Owner | Andrei Popescu |
| Last updated | 2026-08-30 |

| Tool | Purpose | URL / Location |
|---|---|---|
| GitLab | Source code, CI | gitlab.meridian.internal/pcon/pcon-connectivity |
| Jira | Backlog (project PCON) | jira.meridian.internal/browse/PCON |
| Confluence | This documentation | Space "Phone Connectivity" |
| TestManagementSystem | Test cases, executions | tms.meridian.internal |
| TraceRepository | Traces of HiL/vehicle | traces.meridian.internal |
| DefectTrackingSystem export | DEF records for traceability graph | nightly export from Jira |
| BenchBooker | HiL bench booking | benchbooker.meridian.internal |
| Neo4j traceability graph | Requirement–test–defect graph | Local PoC instance (see knowledge graph PoC) |
| Sylvan support portal | Stack defects | support.sylvan-wireless.example |

## Development environment

- Ubuntu 24.04, Docker, Yocto SDK for HU4 (version in `/tools/sdk-version.txt`).
- IDE: free choice; a VS Code dev container is provided.

## Traceability graph

The traceability graph (Neo4j) is rebuilt from validated CSV exports of requirements, components, tests, executions, traces and defects. It is used for investigation questions such as "why did EXEC-010 fail?" and coverage analysis.
