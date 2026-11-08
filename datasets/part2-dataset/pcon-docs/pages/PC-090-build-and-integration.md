# Build and Integration Process

| Field | Value |
|---|---|
| Page ID | PC-090 |
| Owner | Andrei Popescu |
| Last updated | 2026-08-15 |

## Repository

All PCON components live in the GitLab repository **`pcon-connectivity`**, one folder per component under `/components/<component-name>`. Interfaces are in `/interfaces`, configuration in `/config`.

## Pipeline stages

1. **lint** – clang-tidy, cpplint, proto lint.
2. **build** – Yocto SDK cross build for HU4 (aarch64) and native x86-64 build for SiL.
3. **unit** – unit tests with coverage report.
4. **sil-smoke** – 25 SiL scenarios (merge requests) or full suite (nightly at 02:00 CET).
5. **package** – creation of the PCON layer package `pcon-<version>.ipk` set.
6. **publish** – upload to the internal artifact repository.

## Integration into the HU4 image

The HU4 integration team pulls PCON packages weekly (Wednesday) into the platform image. Hotfixes can be requested via the integration channel.

## Versions

Each component has its own semantic version (PC-092); the PCON release (e.g. "Connectivity SW 2.3.0") is the version of COMP-002 by convention.

## Release artifacts

Release builds are produced from `release/r1.x` branches and published with a release tag. The Platform team's handling of the final HU4 image is described in the platform documentation.
