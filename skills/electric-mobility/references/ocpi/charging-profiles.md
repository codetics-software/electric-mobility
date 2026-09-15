# OCPI — ChargingProfiles Module

## Purpose

The ChargingProfiles module enables **smart charging** — the SCSP (Smart Charging Service Provider) or eMSP sends a dynamic energy delivery schedule to the CPO, which forwards it to the physical charger. This allows grid-aware charging, solar optimization, and load balancing.

**Data owner**: SCSP (or eMSP acting as SCSP)  
**Direction**: SCSP → CPO → Charger (via OCPP)

---

## Version Availability

| Version | Available |
|---|---|
| 2.1.1 | No — not in 2.1.1 |
| 2.2.1 | Yes (new in 2.2.1) |
| 2.3.0 | Yes |

---

## Relationship to Session Charging Preferences

This module is different from the `ChargingPreferences` in the Sessions module:

| | Sessions ChargingPreferences | ChargingProfiles Module |
|---|---|---|
| Initiator | eMSP (driver preference) | SCSP / eMSP (grid signal) |
| Granularity | High-level preference (`GREEN`, `FAST`) | Precise power schedule (watts per time slot) |
| Mechanism | PUT on session endpoint | Dedicated module with async callback |
| Typical actor | Consumer-facing apps | Grid operators, energy managers |

---

## Key Data Models

### `SetChargingProfile`

Request sent by SCSP to CPO:

```json
{
  "charging_profile": {
    "start_date_time": "2025-06-01T14:00:00Z",
    "duration": 3600,
    "charging_rate_unit": "W",
    "min_charging_rate": 1400.0,
    "charging_profile_period": [
      { "start_period": 0, "limit": 11000.0 },
      { "start_period": 900, "limit": 7400.0 },
      { "start_period": 1800, "limit": 3700.0 }
    ]
  },
  "response_url": "https://scsp.example.com/profiles/callback/REQ-001"
}
```

### `ChargingProfile`

| Field | Type | Description |
|---|---|---|
| `start_date_time` | DateTime? | When profile starts (null = now) |
| `duration` | int? | Duration in seconds (null = indefinite) |
| `charging_rate_unit` | ChargingRateUnit | `W` (watts) or `A` (amps) |
| `min_charging_rate` | number? | Minimum charge rate |
| `charging_profile_period` | ChargingProfilePeriod[] | Time-sliced limits |

### `ChargingProfilePeriod`

| Field | Type | Description |
|---|---|---|
| `start_period` | int | Seconds since `start_date_time` |
| `limit` | number | Maximum charge rate for this period (W or A) |

### `ActiveChargingProfile`

Current profile active on the charger (retrieved via GET):

```json
{
  "start_date_time": "2025-06-01T14:00:00Z",
  "charging_profile": { ... }
}
```

---

## HTTP Endpoints

### Sender Interface (SCSP/eMSP exposes this — CPO calls back)

| Method | Path | Description |
|---|---|---|
| `POST` | `{response_url}` | CPO sends result of profile request back to SCSP |

> The URL is SCSP-controlled and provided per-request in the body (same async pattern as Commands).

### Receiver Interface (CPO exposes this — SCSP calls)

| Method | Path | Description |
|---|---|---|
| `GET` | `/ocpi/cpo/2.x/chargingprofiles/{session_id}` | Get active charging profile for a session |
| `PUT` | `/ocpi/cpo/2.x/chargingprofiles/{session_id}` | Set new charging profile |
| `DELETE` | `/ocpi/cpo/2.x/chargingprofiles/{session_id}` | Clear active charging profile |

---

## Async Flow

```
SCSP → PUT /ocpi/cpo/2.x/chargingprofiles/{session_id}
  Body: { charging_profile: {...}, response_url: "https://..." }
  ← 200 { "result": "ACCEPTED", "timeout": 120 }
    (CPO accepted — will relay to charger)

[CPO → charger via OCPP SetChargingProfile]
[Charger confirms or rejects]

CPO → POST {response_url}
  Body: ChargingProfileResult { "result": "ACCEPTED" }
  ← SCSP responds 200
```

### `ChargingProfileResultType`

| Value | Meaning |
|---|---|
| `ACCEPTED` | Profile set successfully on charger |
| `REJECTED` | Charger rejected the profile |
| `UNKNOWN_SESSION` | Session ID not found |
| `TIMEOUT` | Charger did not respond in time |

---

## GET Active Profile Flow

```
SCSP → GET /ocpi/cpo/2.x/chargingprofiles/{session_id}?response_url=...
  ← 200 { "result": "ACCEPTED", "timeout": 30 }

[CPO fetches current profile from charger via OCPP GetCompositeSchedule]

CPO → POST {response_url}
  Body: ActiveChargingProfileResult {
    "result": "ACCEPTED",
    "profile": { "start_date_time": ..., "charging_profile": {...} }
  }
```

---

## Version Differences

### 2.2.1
- Full module introduced (not in 2.1.1)
- `W` and `A` unit support
- GET, PUT, DELETE on sessions
- Async callback pattern

### 2.3.0
- Aligned with AFIR smart charging requirements
- Improved documentation on SCSP role vs eMSP acting as SCSP
- Clearer rules on profile priority when multiple profiles conflict (charger, SCSP, local OCPP config)

---

## Implementation Notes

### OCPP Translation
The CPO translates OCPI ChargingProfile to an OCPP 1.6 `SetChargingProfile` or OCPP 2.0.1 `SetChargingProfileRequest`. The OCPI profile period structure maps directly to OCPP's `chargingSchedulePeriod`.

### Profile Priority
Multiple profiles can coexist on a charger (local limit, SCSP-set, CPO-set). OCPI does not specify priority — that is handled at the OCPP/charger level. Coordinate with the charger vendor.

### Session Validity
The `session_id` referenced must be an active Session known to the CPO. Attempting to set a profile on a non-existent or completed session returns `UNKNOWN_SESSION`.

---

## Spec References

- 2.2.1: `mod_charging_profiles.asciidoc` — `release-2.2.1-bugfixes`
- 2.3.0: `mod_charging_profiles.asciidoc` — `2.3.0/release/core`
