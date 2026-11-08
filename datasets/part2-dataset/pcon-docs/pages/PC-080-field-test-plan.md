# Field Test Plan – Vehicle Fleet

| Field | Value |
|---|---|
| Page ID | PC-080 |
| Owner | Lukas Becker |
| Last updated | 2026-09-15 |

## Goal

Observe reconnection behavior under real usage over several weeks, with many ignition cycles in varying environments.

## Fleet

- **6 prototype vehicles** (MER-P03 … MER-P08) with HU4 B-Sample and Connectivity SW 2.3.1 (planned).
- Drivers: engineers of the Meridian program who use the vehicles for commuting.
- Each driver uses their own phone plus one reference phone in the glovebox.

## Routes

| Route | Description | Special conditions |
|---|---|---|
| Urban | City commute, many short stops | Many ignition cycles |
| Highway | 150 km round trip | Long connection, link stability |
| Underground garage | Start and stop in garage level −3 | Weak signal, RF reflections |

## Duration

8 weeks, starting after delivery of SW 2.3.1.

## Data collection

- Traces and diagnostic events are recorded on the head unit.
- Drivers report subjective issues via a short form.
- How the trace data is transferred from the vehicles to the TraceRepository has not been defined yet (USB export, workshop readout, or telematics upload).

## Analysis

The analysis of field test data (statistics on reconnection times, correlation with phone models and locations) needs an owner. Sofia (Test Lead) and Elena (Diagnostics) both offered partial support; **ownership is open**.
