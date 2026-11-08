# TeamFlow — Knowledge Registry

**Dataset:** TeamFlow fictional project, documentation corpus v1.0 (English).
**Purpose:** A review-only index of source references and intentionally conflicting requirements. Do not index this registry for retrieval or include it in agent input.
**Canonical source:** [TeamFlow documentation](teamflow-docs/TeamFlow_Project_Documentation_100_pages.md), containing the 100 source sections used for retrieval.

## Source structure

| Documentation family | Sections / corpus pages |
|---|---:|
| Business rules / Product requirements (`BR`) | 35 |
| Functional specifications / User flows (`FS`) | 25 |
| API contracts / Integration specifications (`API`) | 15 |
| Architecture decisions (`ADR`) | 10 |
| Guidelines / Conventions (`GL`) | 10 |
| FAQ / Troubleshooting (`FAQ`) | 5 |
| **Total** | **100** |

## Source registry

The `Corpus page` shown for each section is its 1-based position in the 100-page document. To retrieve exact normative statements, search for their IDs (e.g. `BR-03-R06`) in the canonical Markdown source.

| Corpus page | Section ID | Topic |
|---:|---|---|
| 1 | `BR-01` | Workspace isolation |
| 2 | `BR-02` | Account registration and invitation |
| 3 | `BR-03` | Authentication and sessions |
| 4 | `BR-04` | Workspace roles and grants |
| 5 | `BR-05` | Project setup and lifecycle |
| 6 | `BR-06` | Project membership and visibility |
| 7 | `BR-07` | Task identity and fields |
| 8 | `BR-08` | Task states and transitions |
| 9 | `BR-09` | Task assignment and ownership |
| 10 | `BR-10` | Priority and severity |
| 11 | `BR-11` | Dependencies between tasks |
| 12 | `BR-12` | Due dates and estimates |
| 13 | `BR-13` | Subtasks and task grouping |
| 14 | `BR-14` | Labels and custom fields |
| 15 | `BR-15` | Comments, edits and mentions |
| 16 | `BR-16` | Attachments and downloads |
| 17 | `BR-17` | Sprint creation and capacity |
| 18 | `BR-18` | Sprint execution and completion |
| 19 | `BR-19` | Backlog and ordering |
| 20 | `BR-20` | Boards and saved views |
| 21 | `BR-21` | Notifications and delivery |
| 22 | `BR-22` | Activity history and audit |
| 23 | `BR-23` | Search and query semantics |
| 24 | `BR-24` | Reports and computed metrics |
| 25 | `BR-25` | Time tracking |
| 26 | `BR-26` | Milestones and releases |
| 27 | `BR-27` | External guests and sharing |
| 28 | `BR-28` | Templates and automated actions |
| 29 | `BR-29` | Archiving and exports |
| 30 | `BR-30` | Webhooks and integrations |
| 31 | `BR-31` | Retention and account deletion |
| 32 | `BR-32` | Security and trust boundaries |
| 33 | `BR-33` | Imports and external migrations |
| 34 | `BR-34` | Accessibility and localization |
| 35 | `BR-35` | Plans, quotas and usage |
| 36 | `FS-01` | Create and verify an account |
| 37 | `FS-02` | Sign in, refresh and revoke sessions |
| 38 | `FS-03` | Invite a workspace member |
| 39 | `FS-04` | Create and activate a project |
| 40 | `FS-05` | Manage project membership |
| 41 | `FS-06` | Create a task from scratch or template |
| 42 | `FS-07` | Advance task through review |
| 43 | `FS-08` | Assign or claim a task |
| 44 | `FS-09` | Create and resolve a blocking link |
| 45 | `FS-10` | Plan an upcoming sprint |
| 46 | `FS-11` | Activate a sprint and freeze commitment |
| 47 | `FS-12` | Complete a sprint with unfinished tasks |
| 48 | `FS-13` | Post a comment and mention colleagues |
| 49 | `FS-14` | Upload and inspect an attachment |
| 50 | `FS-15` | Filter and personalize board view |
| 51 | `FS-16` | Search workspace tasks safely |
| 52 | `FS-17` | Configure notification preferences |
| 53 | `FS-18` | Log actual time against a task |
| 54 | `FS-19` | Publish a release and inspect milestones |
| 55 | `FS-20` | Inspect reports and historical metrics |
| 56 | `FS-21` | Archive a project and request restoration |
| 57 | `FS-22` | Subscribe and deliver a webhook |
| 58 | `FS-23` | Preview and commit an import |
| 59 | `FS-24` | Export project data with permissions |
| 60 | `FS-25` | Handle permission loss while interacting |
| 61 | `API-01` | Authentication and credentials |
| 62 | `API-02` | Workspace details and switching |
| 63 | `API-03` | Projects and lifecycle |
| 64 | `API-04` | Invitations and membership |
| 65 | `API-05` | Project reads and member search |
| 66 | `API-06` | Task create and update |
| 67 | `API-07` | Task transitions and reopen |
| 68 | `API-08` | Task assignment and claim |
| 69 | `API-09` | Dependencies and subtasks |
| 70 | `API-10` | Sprint planning and activation |
| 71 | `API-11` | Sprint tasks and completion |
| 72 | `API-12` | Comments and file attachments |
| 73 | `API-13` | Notifications and preferences |
| 74 | `API-14` | Search and reports |
| 75 | `API-15` | Exports, imports and integration hooks |
| 76 | `ADR-01` | Modular monolith for initial release |
| 77 | `ADR-02` | PostgreSQL as transactional system of record |
| 78 | `ADR-03` | Tenant separation through workspace IDs |
| 79 | `ADR-04` | Event-driven notifications and webhooks |
| 80 | `ADR-05` | Short-lived access tokens and rotating sessions |
| 81 | `ADR-06` | Object storage with quarantine scanning |
| 82 | `ADR-07` | Versioned REST API contracts |
| 83 | `ADR-08` | Search index derived from source records |
| 84 | `ADR-09` | Append-only audit trail for sensitive mutations |
| 85 | `ADR-10` | Operational backup and recovery |
| 86 | `GL-01` | Naming, IDs and schema conventions |
| 87 | `GL-02` | Error envelopes and client feedback |
| 88 | `GL-03` | Time zones, dates and numeric units |
| 89 | `GL-04` | Pagination, filtering and sorting |
| 90 | `GL-05` | Idempotency, concurrency and retries |
| 91 | `GL-06` | Security, role checks and session handling |
| 92 | `GL-07` | Test cases and acceptance-criteria mapping |
| 93 | `GL-08` | Logs, tracing and observability |
| 94 | `GL-09` | Accessibility and user-facing language |
| 95 | `GL-10` | Documentation governance and references |
| 96 | `FAQ-01` | Accounts, invitations and workspace access |
| 97 | `FAQ-02` | Tasks, subtasks and comments |
| 98 | `FAQ-03` | Notifications, preferences and audit |
| 99 | `FAQ-04` | Projects, sprints and exports |
| 100 | `FAQ-05` | Files, search, reports and limits |

## Known documented conflicts (intentional)

These references express incompatible requirements in the v1.0 corpus. Do not silently pick one as ground truth; the expected agent behavior for affected tickets is to surface the conflict and ask for an authoritative decision.

| Evidence source A | Evidence source B | Issue |
|---|---|---|
| `BR-03-R06` | `GL-06-R05` | Session inactivity timeout: 30 vs 45 minutes |
| `BR-15-R03` | `FAQ-02-Q4` | Comment edit limit: 30 vs 60 minutes |
| `BR-21-R04` | `FAQ-03-Q2` | Notification digest: documented values disagree |
| `BR-29-R03` | `FAQ-04-Q3` | Archived project restoration window: 14 vs 30 days |
| `BR-10-R02` | `BR-28-R03` | Priority default behavior differs between sources |

## Ticket/knowledge linkage

- Input-only tickets: `teamflow-tickets/tickets.jsonl` (no golden information).
- Golden labels: `teamflow-tickets/ticket_labels.jsonl` (category + L1/L2/L3 difficulty).
- Full expected answers with evidence: `teamflow-tickets/golden_answers.jsonl` or `teamflow-tickets/TeamFlow_200_tickets_with_golden.json`.
- Fields `evidence[].source_id` point to exact passage IDs in the Markdown documentation.
- For `unresolved` tickets, an empty evidence list does not by itself prove that a requirement is absent: manually verify absence across the source corpus.
- Keep the golden files outside the RAG prompt and evaluation input.

## Quality / validation notes

- 200 tickets; category distribution: resolved 60, unresolved 60, partially resolved 40, conflicting 20, already clear 20.
- Difficulty levels: L1, L2, L3; independent from golden categories.
- The 20 conflicting tickets reuse five underlying source conflicts in different scenarios; consider this when splitting train/validation/test.
- Automatically generated and structurally checked; human semantic review is still required before using it as a trusted benchmark.

## Files in part3-dataset

- `knowledge-registry.md` — this review-only registry.
- `teamflow-docs/` — extracted documentation with 100 logical sections (Markdown, PDF, DOCX).
- `teamflow-tickets/` — extracted tickets, golden answers, Jira CSV, and review files.

**Normalization:** The original files retain their source format. The shared converter, `scripts/normalize_datasets.py` at the repository root, exports TeamFlow alongside the other datasets into [the normalized collection](../normalized/README.md), with common fields and categories and separate agent inputs and reference answers.
