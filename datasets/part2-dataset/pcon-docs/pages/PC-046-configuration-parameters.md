# Configuration Parameters

| Field | Value |
|---|---|
| Page ID | PC-046 |
| Owner | Andrei Popescu |
| Last updated | 2026-08-18 |

Parameters are stored in the variant coding file `pcon_config.json` and can be changed by coding in development builds. Production values are frozen with the release.

| Parameter | Default | Unit | Used by | Description |
|---|---|---|---|---|
| BT_RECONNECT_ENABLED | true | – | COMP-002 | Master switch for automatic reconnection |
| BT_RECONNECT_MAX_RETRIES | 3 | count | COMP-002 | Number of retries after a transient failure |
| BT_RECONNECT_RETRY_DELAY_MS | 2000 | ms | COMP-002 | Delay before a retry |
| BT_RECONNECT_GIVEUP_S | 60 | s | COMP-002 | Give-up timer for automatic reconnection |
| BT_MAX_CONNECTED | 2 | count | COMP-006 | Max simultaneously connected phones |
| BT_MAX_PAIRED | 10 | count | COMP-003 | Max paired devices |
| BT_PROFILE_TIMEOUT_MS | 5000 | ms | COMP-004 | Timeout per profile |
| BT_INQUIRY_BLOCK_S | 20 | s | COMP-009 | No inquiry after BT_READY |
| PB_BATCH_SIZE | 100 | count | COMP-007 | Contacts per write batch |
| PB_PHOTOS_ENABLED | true | – | COMP-007 | Download contact photos |
| DIAG_EVENTS_ENABLED | true | – | COMP-005 | Record diagnostic events |

## Change process

Changes to default values require a merge request touching `pcon_config.json` and an update of this page. Values that affect requirements (e.g. timing) need approval by the Product Owner.
