# Working Agreements – Definition of Ready and Done

| Field | Value |
|---|---|
| Page ID | PC-006 |
| Owner | Andrei Popescu |
| Last updated | 2026-06-20 |

## Definition of Ready (Story)

A story can be pulled into a sprint when:

- the user value or technical goal is described in one or two sentences;
- the affected requirement(s) are linked (REQ-xxx);
- acceptance criteria are written and testable;
- the affected components are known;
- open questions are either answered or explicitly accepted as risk by the Product Owner;
- the story is estimated by the team.

## Definition of Done (Story)

A story is done when:

- code is merged to `main` after review by at least one other developer;
- unit tests are written and the component coverage does not decrease;
- the SiL regression suite passes;
- **the HiL regression passes for all requirements touched by the change**;
- diagnostic events are emitted where the requirement asks for them;
- the component page in this space is updated if interfaces or parameters changed;
- the Product Owner has accepted the story in the sprint review.

## Code review rules

- Every merge request needs one approval; changes in COMP-003 (pairing data) additionally need the approval of Karim Haddad or his delegate.
- Merge requests should stay below 400 changed lines.
- The author resolves all review threads before merging.

## Meetings

| Meeting | When |
|---|---|
| Daily | Every working day, 09:30, 15 minutes |
| Refinement | Monday, 60 minutes |
| Sprint review and planning | Every second Wednesday |
| Retrospective | Every second Wednesday, after review |
| Defect triage | Tuesday and Thursday, 30 minutes |
