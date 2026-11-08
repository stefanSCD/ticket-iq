# Known Test Bench Limitations

| Field | Value |
|---|---|
| Page ID | PC-079 |
| Owner | Daniel Szabo |
| Last updated | 2026-08-28 |

| ID | Limitation | Affected | Workaround |
|---|---|---|---|
| LIM-01 | BT Peer Simulator does not model radio timing | SiL timing results | Use HiL/Vehicle for REQ-002 |
| LIM-02 | HIL-BT-02 cannot simulate transport mode | Power mode tests | Use HIL-BT-01 |
| LIM-03 | RF box shielding ~70 dB; above that, leakage from lab phones possible | Link-loss tests | Switch off lab phones nearby |
| LIM-04 | iOS actions need robotic finger, which fails ~2 % of attempts | iOS automation | Automatic re-run once |
| LIM-05 | HiL power supply rise time 5 ms (vehicle faster) | Cranking profiles | Accepted |
| LIM-06 | Phone battery degradation in permanent charging | Long-term HiL | Replace phones yearly |
| LIM-07 | Bench time shared with Audio team on Thu/Fri afternoons | Availability | Book early |

Limitations are reviewed in the test review meeting every month.
