# OCPI — Locations Module

## Purpose

The Locations module exchanges **static and dynamic charge point data** — where chargers are, what connectors they have, and their real-time availability. It is the foundation for map apps, roaming authorization, and driver-facing UIs.

**Data owner**: CPO  
**Direction**: CPO (Sender) → eMSP / NSP / NAP (Receiver)

---

## Version Availability

| Version | Mandatory |
|---|---|
| 2.1.1 | Recommended (effectively required for useful roaming) |
| 2.2.1 | Yes (for CPO role) |
| 2.3.0 | Yes (for CPO role) |

---

## Object Hierarchy

```
Location (1)
  └── EVSE (1..N)         — one physical charging point
        └── Connector (1..N)  — one physical socket/plug
```

Each level has its own `last_updated` timestamp. Push operations target the most granular changed object.

---

## Key Data Models

### `Location`

| Field | Type | Description |
|---|---|---|
| `id` | string(36) | CPO-assigned unique ID |
| `publish` | boolean (2.2.1+) | Whether to publish to eMSPs (false = private) |
| `name` | string | Human-readable site name |
| `address` | string | Street address |
| `city` | string | City |
| `country` | string | ISO 3166-1 alpha-2 (2.1.1) or alpha-3 (2.2.1+) |
| `coordinates` | GeoLocation | `{ latitude, longitude }` |
| `evses` | EVSE[] | All EVSEs at this location |
| `opening_times` | Hours | Operating hours |
| `charging_when_closed` | boolean | Can charge outside opening hours |
| `tariffs` | Tariff[] (2.2.1+) | Multiple tariffs per location |
| `energy_mix` | EnergyMix | Renewable energy info |
| `last_updated` | DateTime | RFC3339 UTC — crucial for sync |
| `vehicle_type` | VehicleType[] (2.3.0+) | `CAR`, `MOTORCYCLE`, `TRUCK`, `BICYCLE` |

### `EVSE`

| Field | Type | Description |
|---|---|---|
| `uid` | string(36) | Unique within this Location |
| `evse_id` | string | eMI3 standard ID (e.g. `FR*CPO*E1234`) |
| `status` | Status | `AVAILABLE`, `CHARGING`, `INOPERATIVE`, `OUTOFORDER`, `PLANNED`, `REMOVED`, `RESERVED`, `UNKNOWN` |
| `connectors` | Connector[] | Physical sockets |
| `capabilities` | Capability[] | `RESERVABLE`, `REMOTE_START_STOP_CAPABLE`, `RFID_READER`, `CREDIT_CARD_PAYABLE` (2.2.1+) |
| `parking_restrictions` | ParkingRestriction[] | Who can park here |
| `floor_level` | string | For multi-floor locations |
| `physical_reference` | string | Label visible on the hardware |
| `last_updated` | DateTime | |

### `Connector`

| Field | Type | Description |
|---|---|---|
| `id` | string(36) | Unique within EVSE |
| `standard` | ConnectorType | `IEC_62196_T2`, `CHADEMO`, `DOMESTIC_F`, `IEC_62196_T2_COMBO`, etc. |
| `format` | ConnectorFormat | `SOCKET` or `CABLE` |
| `power_type` | PowerType | `AC_1_PHASE`, `AC_3_PHASE`, `DC` |
| `max_voltage` | int | Volts |
| `max_amperage` | int | Amps |
| `max_electric_power` | int (2.2.1+) | Watts — easier than computing V×A |
| `tariff_ids` | string[] | References to Tariff objects |
| `last_updated` | DateTime | |

---

## HTTP Endpoints

### Sender Interface (CPO exposes this)

| Method | Path | Description |
|---|---|---|
| `GET` | `/ocpi/cpo/2.x/locations` | Get all Locations (paginated) |
| `GET` | `/ocpi/cpo/2.x/locations/{location_id}` | Get single Location |
| `GET` | `/ocpi/cpo/2.x/locations/{location_id}/{evse_uid}` | Get single EVSE |
| `GET` | `/ocpi/cpo/2.x/locations/{location_id}/{evse_uid}/{connector_id}` | Get single Connector |

### Receiver Interface (eMSP exposes this — for CPO to push to)

| Method | Path | Description |
|---|---|---|
| `GET` | `/ocpi/emsp/2.x/locations/{country_code}/{party_id}/{location_id}` | Validate a pushed Location |
| `PUT` | `/ocpi/emsp/2.x/locations/{country_code}/{party_id}/{location_id}` | Push full Location |
| `PUT` | `/ocpi/emsp/2.x/locations/{country_code}/{party_id}/{location_id}/{evse_uid}` | Push full EVSE |
| `PUT` | `/ocpi/emsp/2.x/locations/{country_code}/{party_id}/{location_id}/{evse_uid}/{connector_id}` | Push full Connector |
| `PATCH` | `/ocpi/emsp/2.x/locations/{country_code}/{party_id}/{location_id}` | Partial update (e.g., `last_updated` + changed fields only) |
| `PATCH` | `/ocpi/emsp/2.x/locations/.../{evse_uid}` | Partial EVSE update (e.g., status change) |

> The URL path embeds `country_code/party_id/location_id` — this is the **client-owned object** pattern. The CPO defines the URL, not the eMSP server.

---

## Push vs Pull Strategy

### Pull (Initial Sync)
On first connection (or after outage), the Receiver `GET`s the full Location list from the Sender:
```
GET /ocpi/cpo/2.x/locations?date_from=2024-01-01T00:00:00Z&limit=100
→ 200, Link: <...>; rel="next"   (pagination header)
```
Walk all pages until no `Link: rel="next"` header.

### Push (Real-Time Updates)
CPO `PATCH`es the EVSE status when a charger's state changes:
```
PATCH /ocpi/emsp/2.x/locations/FR/MCP/LOC001/EV001
{ "status": "CHARGING", "last_updated": "2025-06-01T14:32:00Z" }
```

### Pagination Headers

| Header | Meaning |
|---|---|
| `X-Total-Count` | Total matching objects |
| `X-Limit` | Objects per page |
| `Link: <url>; rel="next"` | URL for next page |

---

## Sync Pattern

```
1. On startup / after long outage:
   Pull full list (GET with date_from far in past or omitted)
   Store each Location with its last_updated

2. On periodic sync (every N minutes):
   Pull with date_from = (last sync time)
   Only changed/new objects returned

3. Real-time:
   Receive PATCH / PUT from CPO
   Apply to local store

4. Validation (optional):
   GET individual Location to confirm your state matches CPO's
```

---

## Version Differences

### 2.1.1
- `country` is ISO 3166-1 **alpha-2** (2-letter code)
- No `publish` field — all locations assumed public
- No `max_electric_power` on Connector — must compute from voltage × amperage
- Single tariff reference per connector (string, not array)
- Simpler `capabilities` set

### 2.2.1
- `country` becomes ISO 3166-1 **alpha-3** (3-letter code) — breaking change
- `publish` field added — CPO can mark a location private
- `max_electric_power` added to Connector
- Multiple tariffs per Location/Connector (`tariff_ids` as array)
- `publish_allowed_to` for selective publishing to specific eMSPs
- `parking_type` field added
- Richer `capabilities` including `CREDIT_CARD_PAYABLE`, `REMOTE_START_STOP_CAPABLE`, `START_SESSION_CONNECTOR_REQUIRED`

### 2.3.0
- `vehicle_type` array on Location and EVSE — `CAR`, `MOTORCYCLE`, `TRUCK`, `BICYCLE`, `SCOOTER`
- **NAP data fields** for EU AFIR compliance — structured accessibility and regulatory data
- `charging_when_closed` clarifications
- Extensibility mechanism (`custom_data` placeholder approach)
- Stronger normalization on `evse_id` format validation

---

## Implementation Notes

### EVSE Status is the Most Frequent Push
Status changes (`AVAILABLE` → `CHARGING` → `AVAILABLE`) happen constantly. Implement a lightweight PATCH pipeline for EVSE status updates that doesn't require re-sending the full Location tree.

### `last_updated` is Critical
- Always update `last_updated` at the granularity of the changed object
- Changing a Connector updates the Connector's `last_updated`, the EVSE's, and the Location's
- Receivers use `last_updated` to detect conflicts and decide which version wins

### ID Stability
- `Location.id`, `EVSE.uid`, and `Connector.id` must be **stable for the lifetime of the physical asset**
- Do not recycle IDs — receivers cache associations between IDs and their internal records
- EVSE `uid` is internal to OCPI; `evse_id` is the eMI3 public identifier

### Private Locations (2.2.1+)
Set `publish: false` for depot chargers not intended for roaming. These SHOULD NOT be sent to eMSPs at all — they are not for public roaming.

---

## Common Pitfalls

- **Sending EVSE `uid` vs `evse_id` confusion**: `uid` is your internal OCPI identifier; `evse_id` is the standardized eMI3 ID visible to drivers. Both must be present and stable
- **Missing `last_updated` on nested objects**: When a Connector changes, update `last_updated` on the Connector, EVSE, and Location — otherwise partial-sync receivers will miss the change
- **Large Location lists without pagination**: Always implement `Link: rel=next` headers — some operators have thousands of locations
- **Country code format mismatch**: 2.1.1 uses alpha-2 (`FR`), 2.2.1+ uses alpha-3 (`FRA`) — sending the wrong format breaks validation on the receiver side

---

## Spec References

- 2.1.1: `mod_locations.md` — `release-2.1.1-bugfixes`
- 2.2.1: `mod_locations.asciidoc` — `release-2.2.1-bugfixes`
- 2.3.0: `mod_locations.asciidoc` — `2.3.0/release/core`
