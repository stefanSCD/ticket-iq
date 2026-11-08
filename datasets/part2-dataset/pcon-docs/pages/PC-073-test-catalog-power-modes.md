# Test Catalog – Power Modes

| Field | Value |
|---|---|
| Page ID | PC-073 |
| Owner | Sofia Brandt |
| Last updated | 2026-08-22 |

| Test | Title | Verifies | Environment | Expected result |
|---|---|---|---|---|
| TEST-025 | Cranking during reconnection | REQ-018 | HiL | Attempt suspended during dip, reconnection afterwards |
| TEST-026 | Orderly disconnect at shutdown | REQ-019 | HiL | All phones disconnected before shutdown confirmation |
| TEST-027 | No attempts before BT_READY | REQ-020 | SiL | No ConnectRequest before BtReady |
| TEST-028 | Low voltage plateau | REQ-018 | HiL | No connection attempts while voltage below threshold |

## Voltage profiles (HiL)

| Profile | Description |
|---|---|
| CRANK-1 | 13.5 V → 6.0 V for 300 ms → 9.5 V for 2 s → 13.5 V |
| LOW-1 | 13.5 V → 8.0 V for 5 s → 13.5 V |
| NORM | 13.5 V constant |

## Not covered

Comfort mode, transport mode and OTA installation mode have no tests in this catalog.
