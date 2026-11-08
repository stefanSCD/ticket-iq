# Branching and Versioning

| Field | Value |
|---|---|
| Page ID | PC-092 |
| Owner | Andrei Popescu |
| Last updated | 2026-06-30 |

## Branching model

- **Trunk-based development** on `main`.
- Short-lived feature branches `feature/PCON-<id>-<short-name>`, merged within 3 days where possible.
- Release branches `release/r1.x` are created at the B-Sample freeze; fixes are made on `main` first and cherry-picked to the release branch.
- Hotfix branches are not used.

## Versioning

- Each component uses **semantic versioning** (MAJOR.MINOR.PATCH).
- MAJOR: incompatible interface change; MINOR: new functionality; PATCH: bug fix.
- Interface changes in `pcon.proto` follow backward-compatible evolution (PC-044).

## Tags

- Release tags: `pcon-r1.<n>` on the release branch.
- Component tags are not used; component versions are maintained in `component.yaml`.
