# OCPI — Sessions Module

## Purpose

The Sessions module provides **real-time visibility of active and completed charging sessions**. The CPO owns and pushes Session objects so that the eMSP can show live charging status to the driver and track energy consumption.

**Data owner**: CPO  
**Direction**: CPO (Sender) → eMSP (Receiver)

---

## Version Availability

| Version | Mandatory |
|---|---|
| 2.1.1 | Optional |
| 2.2.1 | Optional |
| 2.3.0 | Optional |

---

## Session Lifecycle

```
Driver taps RFID / app initiates session
      ↓
CPO creates Session (status: ACTIVE)
CPO → POST/PUT to eMSP /sessions
      ↓
Session ongoing — CPO sends periodic updates
  (energy consumed, charging periods accumulate)
CPO → PATCH to eMSP /sessions/{session_id}
      ↓
Charging stops
CPO marks Session (status: COMPLETED)
CPO → PATCH to eMSP /sessions/{session_id}
      ↓
CPO creates CDR (billing record, separate module)
```

> A Session and a CDR are **different objects**. The Session is live; the CDR is final and immutable for billing.

---

## Key Data Models

### `Session`

| Field | Type | Description |
|---|---|---|
| `country_code` | string(2) | ISO country code of CPO |
| `party_id` | string(3) | CPO's party ID |
| `id` | string(36) | CPO-assigned session ID |
| `start_date_time` | DateTime | When charging began |
| `end_date_time` | DateTime? | When charging ended (null while active) |
| `kwh` | number | Total energy delivered so far (kWh) |
| `cdr_token` | CdrToken | Which token authorized this session |
| `auth_method` | AuthMethod | How authorization happened |
| `authorization_reference` | string? | Reference from real-time auth |
| `location_id` | string | Location where session occurs |
| `evse_uid` | string | EVSE where session occurs |
| `connector_id` | string | Connector used |
| `meter_id` | string? | Physical meter serial number |
| `currency` | string | ISO 4217 currency code |
| `charging_periods` | ChargingPeriod[] | Time-sliced cost breakdown |
| `total_cost` | Price? | Running total (may be null until complete) |
| `status` | SessionStatus | `ACTIVE`, `COMPLETED`, `INVALID`, `PENDING`, `RESERVATION` |
| `last_updated` | DateTime | |

### `SessionStatus` Enum

| Value | Meaning |
|---|---|
| `ACTIVE` | Charging is ongoing |
| `COMPLETED` | Session finished normally |
| `INVALID` | Session was invalid (e.g., token rejected mid-session) |
| `PENDING` | Session reserved but charging not started |
| `RESERVATION` | Slot is reserved, driver not yet connected (2.2.1+) |

### `ChargingPeriod`

Represents one pricing slice of the session:

```json
{
  "start_date_time": "2025-06-01T14:00:00Z",
  "dimensions": [
    { "type": "ENERGY", "volume": 5.2 },
    { "type": "TIME", "volume": 30.0 }
  ],
  "tariff_id": "TARIFF_PEAK"
}
```

`DimensionType` values: `ENERGY` (kWh), `FLAT` (session fee), `MAX_CURRENT` (A), `MIN_CURRENT` (A), `PARKING_TIME` (hours), `TIME` (hours)

### `CdrToken` (2.2.1+)

Embedded token snapshot used for authorization:

```json
{
  "uid": "RFID123",
  "type": "RFID",
  "contract_id": "FR*MCP*C12345*6"
}
```

In 2.1.1, this was just `auth_id` (string) + `auth_method`.

---

## HTTP Endpoints

### Sender Interface (CPO exposes this — for eMSP to pull)

| Method | Path | Description |
|---|---|---|
| `GET` | `/ocpi/cpo/2.x/sessions` | Get sessions (paginated, filterable by date) |
| `GET` | `/ocpi/cpo/2.x/sessions/{session_id}` | Get single session |

### Receiver Interface (eMSP exposes this — for CPO to push)

| Method | Path | Description |
|---|---|---|
| `PUT` | `/ocpi/emsp/2.x/sessions/{country_code}/{party_id}/{session_id}` | Full session update |
| `PATCH` | `/ocpi/emsp/2.x/sessions/{country_code}/{party_id}/{session_id}` | Partial update (kwh, status, etc.) |
| `GET` | `/ocpi/emsp/2.x/sessions/{country_code}/{party_id}/{session_id}` | Validate session state |

### Special: Charging Preferences (2.2.1+)

Allows eMSP to send driver preferences to the CPO for smart charging:

| Method | Path | Description |
|---|---|---|
| `PUT` | `/ocpi/cpo/2.x/sessions/{session_id}/charging_preferences` | Set charging preferences for active session |

---

## Push vs Pull

### Pull
Used for initial sync or recovery:
```
GET /ocpi/cpo/2.x/sessions?date_from=2025-06-01T00:00:00Z&limit=50
```

### Push (Real-Time)
CPO PATCHes the session as energy flows:
```
PATCH /ocpi/emsp/2.x/sessions/FR/MCP/SES001
{
  "kwh": 12.4,
  "charging_periods": [...],
  "last_updated": "2025-06-01T14:22:00Z"
}
```

Push frequency is implementation-defined but typically every 30–60 seconds during an active session, and immediately on status change.

---

## Charging Preferences (2.2.1+)

The eMSP can PUT charging preferences to an active session on the CPO side. This is the lightweight smart-charging mechanism (before ChargingProfiles module):

```json
{
  "profile_type": "GREEN",
  "departure_time": "2025-06-01T18:00:00Z",
  "energy_need": 40.0,
  "discharge_allowed": false
}
```

`ProfileType` values: `CHEAP`, `FAST`, `GREEN`, `REGULAR`

The CPO responds with `200` + acceptance or rejection of the preference.

---

## Version Differences

### 2.1.1
- `auth_id` (string) instead of `CdrToken` object
- No `ChargingPreferences`
- No `RESERVATION` or `PENDING` status
- `total_cost` expressed as plain number (no currency breakdown)

### 2.2.1
- `CdrToken` object replaces `auth_id` — richer token info
- `ChargingPreferences` added (PUT to CPO's sessions endpoint)
- `RESERVATION` and `PENDING` status added
- VAT amount separate from total cost
- `authorization_reference` for real-time auth traceability
- Session-level smart charging preferences

### 2.3.0
- Improved event tracking within sessions
- Clearer update mechanisms — CPO must send PATCH immediately on any meaningful state change
- Additional `CdrToken` fields for global unique identification (`country_code`, `party_id`)
- Aligned with AFIR requirements for session transparency

---

## Implementation Notes

### Session ID Stability
The `session_id` is set by the CPO and must be stable from creation through CDR generation. The CDR will reference it. Never reassign an ID.

### Sessions ≠ CDRs
A session becomes a CDR when it ends. The CDR is the billing-authoritative copy. Never use the Session for billing calculations — always wait for the CDR.

### Energy Values
`kwh` is cumulative (not per-period). It monotonically increases until the session ends. Never decreases.

### Partial Updates
Use `PATCH` for real-time updates. Only include fields that changed plus `last_updated`. Never PATCH `id`, `start_date_time`, or `country_code` / `party_id` — those are immutable.

### Session Recovery
If your system restarts, pull the CPO's full session list for the past 24 hours and reconcile against your local state. Match on `id` + `last_updated`.

---

## Common Pitfalls

- **Treating Session cost as final**: Session `total_cost` is an estimate. Only the CDR's `total_cost` is billable
- **Missing PATCH on EVSE status**: When a session becomes ACTIVE, also PATCH the EVSE status to `CHARGING` via the Locations module — these are independent pushes
- **Not handling `INVALID` status**: Sessions can become INVALID if the token is revoked mid-session. Your system must handle this gracefully (flag the session, do not invoice)
- **Duplicate session IDs**: CPO must guarantee uniqueness of `session_id` globally for their `party_id` + `country_code` namespace

---

## Spec References

- 2.1.1: `mod_sessions.md` — `release-2.1.1-bugfixes`
- 2.2.1: `mod_sessions.asciidoc` — `release-2.2.1-bugfixes`
- 2.3.0: `mod_sessions.asciidoc` — `2.3.0/release/core`
