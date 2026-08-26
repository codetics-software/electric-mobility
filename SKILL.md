---
name: electric-mobility
description: >
  Electric mobility software engineering skill covering OCPI, OCPP,
  EV charging infrastructure, CPO/eMSP systems, roaming, CSMS,
  charging sessions, CDRs, tariffs, smart charging, and IRVE.
license: MIT
metadata:
  author: Codetics
  repository: https://github.com/codetics-software/electric-mobility
  topics: ocpi, ocpp, electric-mobility, ev-charging, cpo, emsp, csms
---

# Electric Mobility Skill — Codetics

> **Trigger this skill** whenever a task involves OCPI, OCPP, EV charging infrastructure, CPO/eMSP systems, roaming, charge sessions, CDRs, tariffs, smart charging, or any electric mobility protocol.

---

## 1. Ecosystem Overview

Electric mobility software sits at the intersection of three protocol layers:

```
EV Driver  ←→  eMSP (app/card)  ←→  [OCPI]  ←→  CPO backend  ←→  [OCPP]  ←→  Charge Point
```

### Actors & Roles

| Abbreviation | Full name | What they do |
|---|---|---|
| **CPO** | Charge Point Operator | Owns and operates charge points. Sends Locations, Sessions, CDRs. Receives Tokens and Commands. |
| **eMSP** | e-Mobility Service Provider | Issues credentials (RFID/app) to EV drivers. Receives Locations, Sessions, CDRs. Sends Tokens. |
| **Hub** | Roaming Hub | Routes OCPI messages between multiple CPOs and eMSPs (e.g. Gireve, Hubject, EVRoaming). |
| **NSP** | Navigation Service Provider | Consumes Location data only (maps, route planners). |
| **NAP** | National Access Point | National database of public charge points (e.g. France's national registry). |
| **SCSP** | Smart Charging Service Provider | Sends ChargingProfiles to CPOs to shape load. Aggregator / energy broker. |
| **EVSE** | Electric Vehicle Supply Equipment | One charging outlet. Can charge one EV at a time. Has one or more connectors. |

### Physical Hierarchy

```
Location (site, address)
  └─ EVSE (one power supply unit, one session at a time)
       └─ Connector (socket or cable, e.g. CCS, CHAdeMO, Type 2)
```

**OCPI** models this hierarchy directly. **OCPP** models it as ChargePoint → Connector (OCPP 1.x) or ChargingStation → EVSE → Connector (OCPP 2.x).

---

## 2. OCPI — Open Charge Point Interface

**Purpose:** Backend-to-backend roaming between CPO systems and eMSP systems.  
**Transport:** HTTPS REST, JSON, token-based auth (Bearer token in Authorization header, Base64-encoded since 2.2).  
**Current versions:** 2.1.1 (widely deployed), 2.2.1 (standard), 2.2.1-d2 (clarified docs, same protocol).

### 2.1 Architecture Topologies

**Peer-to-peer (bilateral):** CPO platform connects directly to eMSP platform.

**Hub topology:** All platforms connect to a Hub; Hub routes messages. Introduced in OCPI 2.2. Hub uses `OCPI-to-party-id` / `OCPI-from-party-id` routing headers.

**Platform model:** A single OCPI platform may serve multiple CPO or eMSP roles (multi-tenant). Each role is identified by `country_code` + `party_id`.

### 2.2 Authentication & Registration

Every OCPI request carries:
```
Authorization: Token <base64-encoded-credentials-token>
```

**Registration sequence (3-token handshake):**
1. Out-of-band: Receiver creates `CREDENTIALS_TOKEN_A` and shares it with Sender.
2. Sender GETs `/ocpi/versions` and `/ocpi/2.2.1/` (version details) using `TOKEN_A`.
3. Sender POSTs to `/ocpi/2.2.1/credentials` with `TOKEN_B` (its new token for receiver to use).
4. Receiver stores `TOKEN_B`, generates `TOKEN_C`, returns it in the POST response.
5. Sender now uses `TOKEN_C` for all future requests. `TOKEN_A` is discarded.

**Update credentials:** PUT to credentials endpoint (same version or new version).  
**Unregister:** DELETE to credentials endpoint.

### 2.3 Transport Conventions

**Response envelope:**
```json
{
  "data": { ... },
  "status_code": 1000,
  "status_message": "Success",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Status code ranges:**
- `1xxx` Success (1000 = generic success)
- `2xxx` Client error (2001 = invalid params, 2003 = unknown Location, 2004 = unknown Token)
- `3xxx` Server error (3001 = cannot reach client API, 3002 = unsupported version, 3003 = required endpoints unavailable)

**Pagination:** All list GETs support `date_from`, `date_to`, `offset`, `limit`. Response headers: `X-Total-Count`, `X-Limit`, `Link` (next page URL).

**Push vs Pull:**
- **Push** (preferred): Data owner proactively PUTs/PATCHes to receiver. Low latency.
- **Pull** (required): Receiver GETs from sender. Used for initial sync / recovery after downtime.

**Client Owned Objects:** In most OCPI modules, the **sender** is the data owner and controls the object's identity (URL). The receiver stores it at the URL dictated by the sender.

**DateTime format:** ISO 8601 / RFC 3339 in UTC. `2024-01-15T10:30:00Z`. No timezone offset — always UTC.

**snake_case everywhere.** All JSON field names are lowercase snake_case.

### 2.4 OCPI Modules

#### Credentials (Configuration)
Both sides implement. Required. See §2.2 above.

#### Versions (Configuration)
```
GET /ocpi/versions           → list of supported versions + URL per version
GET /ocpi/2.2.1/             → list of endpoints for this version
```

#### Locations (Functional — CPO is Sender, eMSP/NSP/NAP receive)

**Hierarchy:** Location → EVSE[] → Connector[]

**Key fields:**
- `id` (CiString 36) — Location identifier within the CPO
- `evse_id` — eMI3 format: `{country}{CPO_ID}*E{local_id}` e.g. `FR*GFX*E12345`
- `status`: AVAILABLE, CHARGING, BLOCKED, OUTOFORDER, PLANNED, REMOVED, RESERVED, UNKNOWN
- `capabilities`: CHARGING_PREFERENCES_CAPABLE, REMOTE_START_STOP_CAPABLE, RESERVABLE, etc.
- Connectors: `standard` (IEC_62196_T2, CHADEMO, IEC_62196_T2_COMBO…), `format` (CABLE/SOCKET), `power_type` (AC_1_PHASE, AC_3_PHASE, DC), `max_voltage`, `max_amperage`, `max_electric_power`

**Delete EVSE:** Set `status: REMOVED` and PUT/PATCH. Locations cannot be fully deleted (Sessions/CDRs reference them).

**Push:** CPO PUTs full object, or PATCHes partial changes. Updating a Connector must also bump `last_updated` on its EVSE and Location (cascade).

#### Sessions (Functional — CPO is Sender)

**Lifecycle states:** PENDING → ACTIVE → COMPLETED (no deletion).

**Key fields:**
- `id` — CPO-assigned, unique per CPO
- `start_date_time`, `end_date_time` (set when COMPLETED)
- `kwh` — energy delivered so far
- `cdr_token` — identifies the charging driver (RFID uid, APP_USER uid, etc.)
- `auth_method`: WHITELIST, OCPI, COMMAND, APP_IDENTIFIER
- `location_id`, `evse_uid`, `connector_id`
- `currency`, `total_cost` (updates during session)
- `charging_periods[]` — time-sliced billing periods, each with `dimensions[]`
- `status`: PENDING, ACTIVE, COMPLETED

**Reservation:** Session starts with `status: RESERVED` when a RESERVE_NOW command is executed.

**Charging Preferences (smart charging input from driver):**
```
PUT {sessions_url}/{session_id}/charging_preferences
```
Body: `ChargingPreferences { profile_type, departure_time, energy_need, discharge_allowed }`

#### CDRs — Charge Detail Records (Functional — CPO is Sender)

The **only billing-relevant object**. Sent after session ends.

**Key rules:**
- Cannot be modified once sent.
- **Credit CDR**: To correct an error, send a new CDR with `credit: true` and `credit_reference_id` pointing to original CDR id. Values in `total_cost` are negative.
- CDRs may reference Locations not published via OCPI (e.g. home chargers).

**Key fields:**
- `cdr_token` — who charged
- `cdr_location` — snapshot of location at time of session (Location, EVSE, Connector identifiers + connector specs)
- `auth_method`, `authorization_reference`
- `tariffs[]` — snapshot of tariff(s) applied
- `charging_periods[]` — dimension-based billing breakdown
- `total_cost` (excl_vat + incl_vat), `total_energy` (kWh), `total_time` (hours)
- `total_fixed_cost`, `total_energy_cost`, `total_time_cost`, `total_parking_time`, `total_parking_cost`
- `signed_data` — Eichrecht / calibration law support

#### Tokens (Functional — eMSP is Sender, CPO receives)

**Types:** RFID, APP_USER, OTHER, AD_HOC_USER.

**Whitelist modes:**
- `ALWAYS` — CPO authorizes from local cache, no real-time call to eMSP
- `ALLOWED` — CPO may authorize from cache or real-time
- `ALLOWED_OFFLINE` — use cache when offline, real-time when online
- `NEVER` — CPO must call eMSP real-time for every authorization

**Real-time authorization:**
```
POST {emsp_tokens_url}/{country_code}/{party_id}/{token_uid}/authorize
```
Optional body: `LocationReferences` (specific Location/EVSE). Response: `AuthorizationInfo { allowed, location, authorization_reference, info }`.

**Invalidate (not delete):** Send Token with `valid: false`.

#### Tariffs (Functional — CPO is Sender)

Tariffs are attached to Connectors. One Connector can have multiple Tariffs (one per ProfileType for smart charging).

**Tariff structure:**
```json
{
  "elements": [
    {
      "price_components": [
        { "type": "FLAT", "price": 0.50, "vat": 20, "step_size": 1 },
        { "type": "ENERGY", "price": 0.25, "vat": 20, "step_size": 1 },
        { "type": "TIME", "price": 2.00, "vat": 20, "step_size": 300 },
        { "type": "PARKING_TIME", "price": 5.00, "vat": 10, "step_size": 300 }
      ],
      "restrictions": {
        "start_time": "08:00",
        "end_time": "18:00",
        "day_of_week": ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY"],
        "min_current": 32.0,
        "max_current": 32.0,
        "min_power": 0,
        "max_power": 22000,
        "min_duration": 0,
        "max_duration": 3600
      }
    }
  ],
  "min_price": { "excl_vat": 0.50 },
  "max_price": { "excl_vat": 25.00 }
}
```

**Price component types:** FLAT (session start fee), ENERGY (per kWh), TIME (per hour while charging), PARKING_TIME (per hour after charging ends, cable still connected).

**`step_size`:** Billing granularity in Wh (ENERGY), seconds (TIME/PARKING_TIME), or 1 (FLAT).

**Tariff types (OCPI 2.2+):** AD_HOC_PAYMENT, PROFILE_CHEAP, PROFILE_FAST, PROFILE_GREEN, REGULAR.

#### Commands (Functional — eMSP is Sender, CPO receives)

**Asynchronous two-step flow:**
1. eMSP POSTs command to CPO → CPO responds immediately with `CommandResponse { result, timeout, message }` (ACCEPTED/NOT_SUPPORTED/REJECTED/UNKNOWN_SESSION etc.)
2. CPO sends command via OCPP to Charge Point, then POSTs result back to eMSP's `response_url`.

**Command types:**

| Command | Purpose |
|---|---|
| `CANCEL_RESERVATION` | Cancel a previously made reservation |
| `RESERVE_NOW` | Reserve an EVSE for a Token before arriving |
| `START_SESSION` | Remotely start a charging session |
| `STOP_SESSION` | Remotely stop an ongoing session |
| `UNLOCK_CONNECTOR` | Unlock connector (use with caution) |

**StartSession body:**
```json
{
  "response_url": "https://emsp.example.com/commands/result/abc123",
  "token": { ... },
  "location_id": "LOC1",
  "evse_uid": "3256",
  "connector_id": "1",
  "authorization_reference": "optional-ref"
}
```

**CPO-initiated cancel:** For RESERVE_NOW, CPO can call Sender (eMSP) with a CANCEL_RESERVATION at the URL given in the original command.

#### ChargingProfiles (Functional — SCSP/eMSP is Sender, CPO receives)

Used by eMSPs or SCSPs (aggregators) to shape charging speed for an ongoing session.

**Asynchronous flow** (same pattern as Commands):
1. Sender PUTs ChargingProfile to CPO for a `session_id`.
2. CPO forwards to Charge Point via OCPP.
3. CPO POSTs result to `response_url`.
4. CPO continues to update Sender via PUT when ActiveChargingProfile changes.

**ChargingProfile object:**
```json
{
  "start_date_time": "2024-01-15T10:00:00Z",
  "duration": 3600,
  "charging_rate_unit": "W",
  "charging_profile_period": [
    { "start_period": 0, "limit": 11000 },
    { "start_period": 1800, "limit": 7400 }
  ],
  "min_charging_rate": 1400
}
```

**Topologies:**
- eMSP generates profiles directly → sends to CPO
- eMSP delegates to SCSP → SCSP sends via eMSP to CPO
- CPO delegates to SCSP → SCSP sends directly to CPO (eMSP unaware)

#### Hub Client Info (Configuration — Hub is Sender)

Only relevant when connecting via a Hub. Informs connected parties of other parties' connection status: CONNECTED, OFFLINE, PLANNED, SUSPENDED.

**Key rule:** When another party goes OFFLINE, do NOT queue Push messages. The other party must GET to re-sync when it comes back online.

### 2.5 OCPI Message Routing (Hub scenarios)

When using a Hub, functional module requests include routing headers:
```
OCPI-to-country-code: NL
OCPI-to-party-id: TNM
OCPI-from-country-code: BE
OCPI-from-party-id: BEC
OCPI-correlation-id: unique-id-123
```

**Broadcast Push:** CPO sends one PUT to Hub with `X-Request-ID`; Hub fans out to all connected eMSPs. Hub responds immediately, delivers asynchronously.

**Open Routing Request:** Sender asks Hub to route GET to the correct owner without specifying `to` party — Hub resolves.

---

## 3. OCPP — Open Charge Point Protocol

**Purpose:** Communication between a Charge Point (hardware) and a CSMS (Central System / Management System).  
**Transport:** WebSocket (OCPP-J / JSON) or SOAP (OCPP-S, legacy 1.6).  
**Versions:** 1.6 (widely deployed), 2.0.1 (modern, current standard), 2.1 (newest, adds V2G/bidirectional).

### 3.1 Connection Model

```
Charge Point ←─── WebSocket ───→ CSMS (Central System)
```

- Charge Point initiates WebSocket connection to CSMS.
- Both directions: Charge Point sends requests; CSMS also sends requests (commands).
- Message format: JSON array `[MessageTypeId, UniqueId, Action, Payload]`
  - `2` = Request, `3` = Response, `4` = Error

```json
// Request (Charge Point → CSMS)
[2, "19223201", "BootNotification", {
  "chargePointVendor": "VendorX",
  "chargePointModel": "ModelY"
}]

// Response (CSMS → Charge Point)
[3, "19223201", {
  "currentTime": "2024-01-15T10:00:00Z",
  "interval": 300,
  "status": "Accepted"
}]
```

### 3.2 OCPP 1.6 — Core Messages

#### Charge Point → CSMS (Initiated by Charge Point)

| Action | When | Key fields |
|---|---|---|
| `BootNotification` | On startup/reboot | `chargePointVendor`, `chargePointModel`, `firmwareVersion`, `iccid`, `imsi` |
| `Heartbeat` | Periodic keep-alive | _(no body)_ |
| `StatusNotification` | Connector state changes | `connectorId`, `status`, `errorCode`, `timestamp` |
| `Authorize` | RFID presented | `idTag` → response: `idTagInfo { status, expiryDate, parentIdTag }` |
| `StartTransaction` | Session starts | `connectorId`, `idTag`, `meterStart` (Wh), `timestamp`, `reservationId?` |
| `StopTransaction` | Session ends | `transactionId`, `meterStop` (Wh), `timestamp`, `reason`, `transactionData[]` |
| `MeterValues` | Periodic meter readings | `connectorId`, `transactionId`, `meterValue[{ timestamp, sampledValue[] }]` |
| `FirmwareStatusNotification` | OTA update progress | `status` (Downloading, Downloaded, Installing, Installed, Failed) |
| `DiagnosticsStatusNotification` | Diagnostics upload | `status` |

**StatusNotification connector states (OCPP 1.6):**  
Available, Preparing, Charging, SuspendedEVSE, SuspendedEV, Finishing, Reserved, Unavailable, Faulted

**Measurands (MeterValues):** `Energy.Active.Import.Register` (primary kWh), `Power.Active.Import` (W), `Current.Import` (A), `Voltage` (V), `SoC` (%), `Temperature`.

#### CSMS → Charge Point (Commands)

| Action | Purpose | Key fields |
|---|---|---|
| `RemoteStartTransaction` | Start session remotely | `idTag`, `connectorId?`, `chargingProfile?` |
| `RemoteStopTransaction` | Stop ongoing session | `transactionId` |
| `ReserveNow` | Reserve a connector | `connectorId`, `expiryDate`, `idTag`, `reservationId` |
| `CancelReservation` | Cancel reservation | `reservationId` |
| `ChangeAvailability` | Take connector in/out of service | `connectorId`, `type` (Operative/Inoperative) |
| `ChangeConfiguration` | Set a config key | `key`, `value` |
| `GetConfiguration` | Read config keys | `key[]?` |
| `ClearCache` | Clear authorization cache | _(no body)_ |
| `Reset` | Reboot charge point | `type` (Hard/Soft) |
| `UnlockConnector` | Unlock connector | `connectorId` |
| `SetChargingProfile` | Apply smart charging schedule | `connectorId`, `csChargingProfiles` |
| `ClearChargingProfile` | Remove charging profile | `id?`, `connectorId?`, `chargingProfilePurpose?`, `stackLevel?` |
| `GetCompositeSchedule` | Get effective schedule | `connectorId`, `duration`, `chargingRateUnit?` |
| `TriggerMessage` | Request a notification | `requestedMessage` (BootNotification, Heartbeat, MeterValues, etc.) |
| `SendLocalList` | Update authorization cache | `listVersion`, `updateType` (Full/Differential), `localAuthorizationList[]` |
| `DataTransfer` | Vendor-specific data | `vendorId`, `messageId?`, `data?` |
| `UpdateFirmware` | Trigger OTA update | `location` (URL), `retrieveDate` |
| `GetDiagnostics` | Upload logs | `location` (URL), `startTime?`, `stopTime?` |

### 3.3 OCPP 1.6 — Smart Charging

**ChargingProfile structure:**
```json
{
  "chargingProfileId": 1,
  "stackLevel": 0,
  "chargingProfilePurpose": "TxProfile",
  "chargingProfileKind": "Absolute",
  "chargingSchedule": {
    "chargingRateUnit": "W",
    "chargingSchedulePeriod": [
      { "startPeriod": 0, "limit": 11000 },
      { "startPeriod": 3600, "limit": 7400 }
    ],
    "duration": 7200
  }
}
```

**Profile purposes:**
- `ChargePointMaxProfile` — overall site limit (stackLevel 0)
- `TxDefaultProfile` — default per transaction
- `TxProfile` — for a specific `transactionId`

**Profile kinds:** `Absolute` (fixed times), `Recurring` (Daily/Weekly), `Relative` (seconds since session start).

**Resolution:** EVSE applies the minimum of all active profiles for each time period.

### 3.4 OCPP 2.0.1 — Improvements over 1.6

OCPP 2.0.1 introduces significant changes:

**Device Model:** Variables instead of raw config keys. Structure: `Component { name, instance?, evse? } → Variable { name, instance? } → Attribute { type: Actual/Target/MinSet/MaxSet }`.

**Transaction lifecycle changes:**
- `TransactionEvent` replaces `StartTransaction`, `StopTransaction`, `MeterValues`
- `eventType`: `Started`, `Updated`, `Ended`
- `triggerReason`: `Authorized`, `CablePluggedIn`, `ChargingRateChanged`, `EVConnectTimeout`, `MeterValueClock`, `StopAuthorized`, etc.

**Authorization improvements:**
- `RequestStartTransaction` replaces `RemoteStartTransaction`
- `IdToken` replaces `idTag`: `{ idToken, type: Central/eMAID/ISO14443/ISO15693/KeyCode/Local/MacAddress/NoAuthorization }`
- `EMAID` (Electric Mobility Account ID) — ISO 15118 / Plug & Charge

**Security:** Certificate-based security profiles, TLS client certificates, signed firmware.

**ISO 15118 (PnC):** Plug & Charge via ISO 15118. EVSE reads vehicle certificate, no RFID needed. `AuthorizeRequest` can carry `15118CertificateHashData`.

**OCPP 2.1 additions:** V2G (Vehicle-to-Grid), bidirectional charging (BPT), Dynamic Smart Charging (replaces static profiles), AFC (Automated Frequency Control), better PnC support.

### 3.5 OCPP Architecture (2.0.1+)

```
ChargingStation (hardware unit)
  └─ EVSE 1..n (independently operated supply)
       └─ Connector 1..n (socket/cable)
```

A ChargingStation has one WebSocket connection to the CSMS. The CSMS identifies individual EVSEs and Connectors via `evse.id` and `evse.connectorId` in messages.

---

## 4. Protocol Interaction Patterns

### 4.1 Full Roaming Charge Session Flow

```
1. Sync: eMSP pushes Token to CPO (OCPI Tokens PUT)
2. Driver arrives: presents RFID card
3. CPO Authorize: check local token cache → hit → Accepted
   (or: OCPI real-time Authorize POST to eMSP)
4. OCPP StartTransaction: Charge Point → CSMS
5. CSMS creates OCPI Session (status: ACTIVE), pushes to eMSP
6. Charging: OCPP MeterValues flow, CSMS patches Session (kwh update)
7. Driver stops: OCPP StopTransaction → CSMS
8. CSMS finalizes OCPI Session (status: COMPLETED)
9. CSMS creates and pushes OCPI CDR to eMSP
10. eMSP bills the driver
```

### 4.2 Remote Start Flow (App-initiated)

```
1. Driver taps "Start" in eMSP app
2. eMSP POSTs OCPI Commands/START_SESSION to CPO
3. CPO responds: CommandResponse { result: ACCEPTED }
4. CPO sends OCPP RemoteStartTransaction to Charge Point
5. Charge Point responds OCPP: Accepted
6. Driver plugs in (if not already)
7. OCPP StartTransaction sent → CSMS
8. CSMS creates OCPI Session, pushes to eMSP
9. OCPP ChargingProfile result POSTed to eMSP response_url
```

### 4.3 Reservation Flow

```
1. eMSP POSTs OCPI RESERVE_NOW command to CPO
2. CPO sends OCPP ReserveNow to Charge Point
3. Charge Point: StatusNotification (status: Reserved)
4. CPO creates OCPI Session (status: RESERVED), pushes to eMSP
5. Driver arrives within timeout, authorizes → session becomes ACTIVE
   (or timeout elapses → CancelReservation, Session COMPLETED with no energy)
```

### 4.4 Smart Charging Flow (SCSP via eMSP)

```
1. Session starts → CPO pushes Session to eMSP
2. eMSP forwards Session to SCSP
3. SCSP calculates profile (grid signal, tariff, driver preference, departure time)
4. SCSP PUTs ChargingProfile via eMSP to CPO
5. CPO sends OCPP SetChargingProfile to Charge Point
6. Charge Point ACKs → result POSTed to response_url
7. Charge Point changes rate → StatusNotification / TransactionEvent → CSMS notifies SCSP of ActiveChargingProfile update
```

---

## 5. Data Model Reference

### 5.1 OCPI Core Objects

**Location (CPO-owned):**
```json
{
  "country_code": "FR", "party_id": "GFX",
  "id": "LOC1", "publish": true,
  "name": "Parking Gare du Nord",
  "address": "18 Rue de Dunkerque", "city": "Paris",
  "postal_code": "75010", "country": "FRA",
  "coordinates": { "latitude": "48.881065", "longitude": "2.355108" },
  "parking_type": "PARKING_GARAGE",
  "evses": [ ... ],
  "time_zone": "Europe/Paris",
  "last_updated": "2024-01-15T10:00:00Z"
}
```

**Session (CPO-owned):**
```json
{
  "country_code": "FR", "party_id": "GFX",
  "id": "SES-001",
  "start_date_time": "2024-01-15T10:17:09Z",
  "kwh": 12.5,
  "cdr_token": {
    "country_code": "DE", "party_id": "TNM",
    "uid": "012345678", "type": "RFID",
    "contract_id": "DE8ACC12E46L89"
  },
  "auth_method": "WHITELIST",
  "location_id": "LOC1", "evse_uid": "EVSE-01", "connector_id": "1",
  "currency": "EUR",
  "total_cost": { "excl_vat": 3.125, "incl_vat": 3.75 },
  "status": "ACTIVE",
  "last_updated": "2024-01-15T11:00:00Z"
}
```

**CDR (CPO-owned, immutable after POST):**
```json
{
  "country_code": "FR", "party_id": "GFX",
  "id": "CDR-001",
  "start_date_time": "2024-01-15T10:17:09Z",
  "end_date_time": "2024-01-15T12:05:22Z",
  "cdr_token": { ... },
  "auth_method": "WHITELIST",
  "cdr_location": {
    "id": "LOC1", "evse_uid": "EVSE-01", "evse_id": "FR*GFX*E001",
    "connector_id": "1",
    "connector_standard": "IEC_62196_T2",
    "connector_format": "SOCKET",
    "connector_power_type": "AC_3_PHASE"
  },
  "currency": "EUR",
  "tariffs": [ { ... tariff snapshot ... } ],
  "charging_periods": [
    {
      "start_date_time": "2024-01-15T10:17:09Z",
      "dimensions": [
        { "type": "ENERGY", "volume": 12.5 },
        { "type": "TIME", "volume": 1.804 }
      ],
      "tariff_id": "TARIFF-01"
    }
  ],
  "total_cost": { "excl_vat": 3.25, "incl_vat": 3.90 },
  "total_energy": 12.5,
  "total_time": 1.804,
  "last_updated": "2024-01-15T12:10:00Z"
}
```

**Token (eMSP-owned):**
```json
{
  "country_code": "DE", "party_id": "TNM",
  "uid": "bdf21bce-fc97-11e8-8eb2-f2801f1b9fd1",
  "type": "APP_USER",
  "contract_id": "DE8ACC12E46L89",
  "issuer": "TheNewMotion",
  "valid": true,
  "whitelist": "ALLOWED",
  "last_updated": "2024-01-15T09:00:00Z"
}
```

### 5.2 Identifiers

**EVSE ID (eMI3):** `{country}{CPO_ID}*E{local_id}` e.g. `FR*GFX*E041503001`  
**Contract ID (eMAID):** `{country}{eMSP_ID}{customer_id}` e.g. `DE8ACC12E46L89`  
**Location ID:** CPO-local string (max 36 chars). Unique within a CPO's `country_code + party_id`.

### 5.3 Connector Standards

| Standard | Description | Typical use |
|---|---|---|
| `IEC_62196_T2` | Type 2 / Mennekes | AC Europe standard |
| `IEC_62196_T2_COMBO` | CCS2 (CCS Combo 2) | DC fast charging Europe |
| `CHADEMO` | CHAdeMO | DC, Japanese vehicles |
| `IEC_62196_T1` | Type 1 / J1772 | AC, US/Japan |
| `IEC_62196_T1_COMBO` | CCS1 | DC fast, US |
| `TESLA_S` | Tesla proprietary | Tesla Supercharger (legacy) |
| `GBT_AC` / `GBT_DC` | GB/T | China standard |

---

## 6. Architecture Decisions for EV Software

### 6.1 CSMS Architecture Patterns

**Event-driven CSMS:**
- Each Charge Point = one WebSocket connection = one actor/coroutine
- OCPP messages are events; process them asynchronously
- State machine per connector (Available → Preparing → Charging → Finishing → Available)
- Idempotent handling: replay-safe on reconnect

**Scaling:**
- Sticky sessions: a Charge Point must reconnect to the same CSMS node (or use distributed session state)
- Message broker (Kafka, Pub/Sub) for fan-out: one OCPP event → multiple consumers (billing, monitoring, OCPI bridge)
- Separate read/write paths: OCPP write path (low latency), reporting read path (analytics)

### 6.2 OCPI Service Patterns

**Push with pull fallback:**
- Always implement push for production; implement pull (GET with `date_from`) for recovery
- Sync window: `date_to` of period N = `date_from` of period N+1 (no overlap, no gap)

**Token cache strategy:**
- Keep a local token cache; refresh via full pull on startup
- Listen for push updates during operation
- Real-time authorize when `whitelist = NEVER` or for new/unknown tokens

**CDR pipeline:**
- OCPP StopTransaction → build CDR → POST to eMSP → store response URL for verification
- Retry with exponential backoff
- Credit CDR workflow: create negative CDR, reference original, then create corrected CDR

**Multi-party platform:**
- Each CPO/eMSP role gets its own `country_code + party_id` tuple
- Credentials stored per counterparty connection (many-to-many)
- Token DB keyed by `(country_code, party_id, uid, type)`

### 6.3 Common Pitfalls

**OCPI:**
- `last_updated` must cascade: Connector update → EVSE update → Location update. Failure causes sync issues.
- `date_from` is inclusive, `date_to` is exclusive. Off-by-one in sync windows causes duplicates or gaps.
- Base64-encode the credentials token in the `Authorization` header (required since 2.2, often missed in 2.1.1 interop).
- Never send Push to a party that is OFFLINE via Hub — they will miss it. They GET on reconnect.
- CDRs are immutable — never PUT to update; issue a Credit CDR pair instead.
- Pagination: always follow `Link: next` header until exhausted.

**OCPP:**
- Charge Points are often behind NAT/firewalls with unreliable connectivity. Design for reconnects.
- `heartbeatInterval` in BootNotification response controls frequency — tune per network condition.
- `connectorId: 0` in OCPP 1.6 refers to the entire Charge Point (e.g., for `ChangeAvailability` of all connectors).
- MeterValues `Energy.Active.Import.Register` is cumulative (Wh total) — compute delta for kWh per session.
- OCPP 1.x has no EVSE concept: map one "virtual EVSE" per connector for OCPI compatibility.
- `TxProfile` in smart charging is tied to `transactionId`. Profile expires when transaction ends.
- Firmware updates: schedule off-peak. `UpdateFirmware` only triggers download; actual install requires Reset.

### 6.4 Security Considerations

- Use TLS 1.2+ for all WebSocket connections (OCPP) and HTTPS (OCPI).
- OCPP Security Profile 3: client-side TLS certificates for mutual authentication (OCPP 2.0.1+).
- Rotate OCPI credentials tokens regularly (recommended monthly minimum).
- Validate `idTag` / `idToken` before allowing session start — don't trust the Charge Point's local cache without verification policies.
- ISO 15118 / Plug & Charge: requires PKI infrastructure (V2G Root CA, contract certificates, provisioning certificates).
- Rate-limit OCPI endpoints to prevent abuse; document limits in `ChargingProfiles` (`TOO_OFTEN` response).

---

## 7. French Market Specifics

- **AFIREV** issues CPO and eMSP operator IDs for France (prefix `FR`). Required for eMI3-compliant EVSE IDs and Contract IDs.
- French EVSE IDs: `FR*{CPO_ID}*E{local}` (e.g. `FR*GFX*E041503001`)
- **IRVE Decree**: Public charging stations in France must publish data to the national NAP (data.gouv.fr). Data format: schema IRVE (based on OCPI Location structure).
- **Calibration law / Eichrecht**: Not legally required in France (unlike Germany), but `signed_data` in CDRs is good practice for dispute resolution.
- **Belib' / Gireve / Freshmile** are major French roaming hubs connecting CPOs and eMSPs via OCPI.
- **TRV (Tarif Réglementé de Vente)**: EDF regulated tariff — some MSPs tie night-rate charging to this.

---

## 8. Quick Reference

### OCPI Module Summary

| Module | Data Owner | CPO role | eMSP role | Key operations |
|---|---|---|---|---|
| Credentials | Both | Both | Both | GET, POST, PUT, DELETE |
| Versions | Both | Both | Both | GET |
| Locations | CPO | Sender | Receiver | Push PUT/PATCH, Pull GET |
| Sessions | CPO | Sender | Receiver | Push PUT/PATCH, PUT ChargingPreferences |
| CDRs | CPO | Sender | Receiver | Push POST, Pull GET |
| Tokens | eMSP | Receiver | Sender | Push PUT/PATCH, POST Authorize |
| Tariffs | CPO | Sender | Receiver | Push PUT/DELETE, Pull GET |
| Commands | — | Receiver | Sender | POST (async), callback POST |
| ChargingProfiles | — | Receiver | Sender (or SCSP) | PUT (async), callback POST |
| HubClientInfo | Hub | Receiver | Receiver | Push PUT, Pull GET |

### OCPP 1.6 Message Quick Reference

| Direction | Message | Trigger |
|---|---|---|
| CP→CS | BootNotification | Startup / reset |
| CP→CS | Heartbeat | Timer (per BootNotification interval) |
| CP→CS | StatusNotification | State change |
| CP→CS | Authorize | RFID tap (when not whitelisted) |
| CP→CS | StartTransaction | Session start |
| CP→CS | MeterValues | Periodic / transaction begin/end |
| CP→CS | StopTransaction | Session end |
| CS→CP | RemoteStartTransaction | App start |
| CS→CP | RemoteStopTransaction | App stop |
| CS→CP | SetChargingProfile | Smart charging |
| CS→CP | ChangeAvailability | Maintenance |
| CS→CP | Reset | Reboot |
| CS→CP | UpdateFirmware | OTA |

### Key URL Patterns (OCPI 2.2.1)

```
GET  /ocpi/versions
GET  /ocpi/2.2.1/
GET  /ocpi/2.2.1/credentials
POST /ocpi/2.2.1/credentials          (register)
PUT  /ocpi/2.2.1/credentials          (update)
GET  /ocpi/cpo/2.2.1/locations
GET  /ocpi/cpo/2.2.1/locations/{location_id}
GET  /ocpi/cpo/2.2.1/locations/{location_id}/{evse_uid}
PUT  /ocpi/emsp/2.2.1/locations/{country_code}/{party_id}/{location_id}/{evse_uid}
GET  /ocpi/cpo/2.2.1/sessions?date_from=...
PUT  /ocpi/emsp/2.2.1/sessions/{country_code}/{party_id}/{session_id}
PUT  /ocpi/cpo/2.2.1/sessions/{session_id}/charging_preferences
GET  /ocpi/cpo/2.2.1/cdrs
POST /ocpi/emsp/2.2.1/cdrs
GET  /ocpi/cpo/2.2.1/tokens
PUT  /ocpi/cpo/2.2.1/tokens/{country_code}/{party_id}/{token_uid}
POST /ocpi/emsp/2.2.1/tokens/{country_code}/{party_id}/{token_uid}/authorize
GET  /ocpi/cpo/2.2.1/tariffs
PUT  /ocpi/emsp/2.2.1/tariffs/{country_code}/{party_id}/{tariff_id}
POST /ocpi/cpo/2.2.1/commands/{command_type}
PUT  /ocpi/cpo/2.2.1/chargingprofiles/{session_id}
```
