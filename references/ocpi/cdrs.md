# OCPI — CDRs (Charge Detail Records) Module

## Purpose

The CDR module delivers the **final, immutable billing record** for a completed charging session. It is the only object in OCPI that is authoritative for invoicing. A CDR is a snapshot — it captures the exact state of the Location, Token, and Tariff as they were at session start, so the bill can never be contested by later changes.

**Data owner**: CPO  
**Direction**: CPO (Sender) → eMSP (Receiver)

---

## Version Availability

| Version | Mandatory |
|---|---|
| 2.1.1 | Optional (but required for billing) |
| 2.2.1 | Optional (but required for billing) |
| 2.3.0 | Optional (but required for billing) |

---

## CDR vs Session

| Attribute | Session | CDR |
|---|---|---|
| Mutable | Yes — updates while active | No — immutable once sent |
| Purpose | Real-time visibility | Billing and settlement |
| Sent | Continuously during session | Once, after session ends |
| `total_cost` | Estimate | Final, authoritative |
| Snapshot | No | Yes — embeds full Location, Token, Tariff state |

---

## Key Data Models

### `CDR`

| Field | Type | Description |
|---|---|---|
| `country_code` | string(2) | CPO's country |
| `party_id` | string(3) | CPO's party ID |
| `id` | string(36) | Unique CDR ID (stable, max 36 chars for non-credit CDRs) |
| `start_date_time` | DateTime | Session start |
| `end_date_time` | DateTime | Session end |
| `session_id` | string? | References the Session (may be omitted if Sessions module not implemented) |
| `cdr_token` | CdrToken | Token used (snapshot at session start) |
| `auth_method` | AuthMethod | How authorized |
| `authorization_reference` | string? | Real-time auth reference |
| `cdr_location` | CdrLocation | Location snapshot at session start |
| `meter_id` | string? | Physical meter serial |
| `currency` | string | ISO 4217 |
| `tariffs` | Tariff[] | Tariff snapshot at session start (full object, not just ID) |
| `charging_periods` | ChargingPeriod[] | Time-sliced billing breakdown |
| `signed_data` | SignedData? | Calibration law / Eichrecht signed meter values (2.2.1+) |
| `total_cost` | Price | Final cost |
| `total_fixed_cost` | Price? | Session/flat fees |
| `total_energy` | number | kWh delivered |
| `total_energy_cost` | Price? | Energy portion of total |
| `total_time` | number | Hours connected |
| `total_time_cost` | Price? | Time portion of total |
| `total_parking_time` | number? | Hours parked (not charging) |
| `total_parking_cost` | Price? | Parking fee portion |
| `total_reservation_cost` | Price? (2.2.1+) | Reservation fee |
| `remark` | string? | Billing note |
| `invoice_reference_id` | string? | Link to external invoice |
| `credit` | boolean? (2.2.1+) | True = credit CDR (correction) |
| `credit_reference_id` | string? (2.2.1+) | References the original CDR being corrected |
| `last_updated` | DateTime | |

### `CdrLocation`

A snapshot of the Location at the time of session start (not a live reference):

```json
{
  "id": "LOC001",
  "name": "My Charging Hub",
  "address": "12 rue de la Paix",
  "city": "Paris",
  "country": "FRA",
  "coordinates": { "latitude": "48.8698", "longitude": "2.3312" },
  "evse_uid": "EV001",
  "evse_id": "FR*CPO*E001",
  "connector_id": "1",
  "connector_standard": "IEC_62196_T2_COMBO",
  "connector_format": "CABLE",
  "connector_power_type": "DC"
}
```

### `AuthMethod` Enum

| Value | Meaning |
|---|---|
| `AUTH_REQUEST` | Real-time authorization (eMSP queried at session start) |
| `COMMAND` | Authorized via Commands module (remote start) |
| `WHITELIST` | Pre-authorized via cached Token whitelist |

### `SignedData` (2.2.1+)

Required in Germany (Eichrecht/Calibration Law). Contains cryptographically signed meter values from the physical meter:

```json
{
  "encoding_method": "OCMF",
  "encoding_method_version": "1.0",
  "public_key": "...",
  "signed_values": [
    { "nature": "BEGIN", "plain_data": "...", "signed_data": "..." },
    { "nature": "END", "plain_data": "...", "signed_data": "..." }
  ]
}
```

---

## HTTP Endpoints

### Sender Interface (CPO exposes this — eMSP pulls)

| Method | Path | Description |
|---|---|---|
| `GET` | `/ocpi/cpo/2.x/cdrs` | Get all CDRs (paginated) |
| `GET` | `/ocpi/cpo/2.x/cdrs/{cdr_id}` | Get single CDR |

### Receiver Interface (eMSP exposes this — CPO pushes to)

| Method | Path | Description |
|---|---|---|
| `POST` | `/ocpi/emsp/2.x/cdrs` | Push new CDR (CPO-initiated) |
| `GET` | `/ocpi/emsp/2.x/cdrs/{country_code}/{party_id}/{cdr_id}` | CPO validates CDR on eMSP |

> CDRs use `POST` (not `PUT`) because the Receiver assigns the response URL in the `Location` header. This is the exception to the client-owned-object pattern.

---

## Push Flow

```
Session ends
  ↓
CPO computes final CDR
  ↓
CPO → POST /ocpi/emsp/2.x/cdrs
  Body: { ...CDR fields... }
  ← 201 Created
     Location: /ocpi/emsp/2.x/cdrs/FR/CPO/CDR123   ← eMSP-assigned URL
  ↓
CPO stores that URL for future reference / validation
```

The `Location` header from the 201 response is the canonical URL for the CDR on the eMSP's system. The CPO SHOULD store it.

---

## Credit CDRs (2.2.1+)

When a billing error is discovered, the CPO issues a **credit CDR** to correct it:

```json
{
  "id": "CDR456-CREDIT",
  "credit": true,
  "credit_reference_id": "CDR456",
  "total_cost": { "excl_vat": -12.50, "incl_vat": -13.88 },
  ...
}
```

- `credit: true` marks it as a correction
- `credit_reference_id` links it to the original CDR being corrected
- `total_cost` is **negative** (it's a refund)
- Credit CDR IDs can exceed 36 characters (they often include the original ID + suffix)

---

## Tariff Snapshot

The CDR embeds the **full Tariff object** as it existed at session start — not a reference. This ensures the driver sees exactly what they were charged and can verify against the tariff they agreed to.

```json
"tariffs": [
  {
    "id": "TARIFF_PEAK",
    "currency": "EUR",
    "elements": [
      {
        "price_components": [
          { "type": "ENERGY", "price": 0.45, "vat": 20.0, "step_size": 1 }
        ]
      }
    ]
  }
]
```

---

## Version Differences

### 2.1.1
- Simpler cost structure — `total_cost` as single number (excl. VAT)
- `auth_id` string instead of `CdrToken` object
- No credit CDRs
- No signed data (Eichrecht)
- No granular cost breakdown (`total_energy_cost`, `total_time_cost`, etc.)
- Tariff embedded as simplified copy (not full Tariff object)

### 2.2.1
- **Credit CDRs** — `credit: true` + `credit_reference_id`
- **Signed meter values** — `signed_data` for Calibration Law compliance
- `CdrToken` replaces `auth_id` (includes `type`, `contract_id`, `uid`)
- **VAT breakdown** — `excl_vat` and `incl_vat` on all cost fields
- `CdrLocation` formalized as dedicated type (was embedded inline)
- Reservation cost captured
- `session_id` field added — links CDR back to Session
- `authorization_reference` for real-time auth traceability

### 2.3.0
- Additional `CdrToken` fields for global identification
- North American tax fields (US/Canada state/province tax)
- Stronger validation rules on `charging_periods` — periods must be contiguous with no gaps
- Improved AFIR-aligned transparency requirements
- `invoice_reference_id` guidance clarified

---

## Implementation Notes

### CDRs Are Immutable
Once a CDR is pushed to the eMSP, it cannot be changed. To correct it, issue a credit CDR referencing the original, then optionally push a replacement CDR.

### Idempotency
The CDR `POST` endpoint must be idempotent — if the CPO retries the same CDR (network failure), the eMSP must not create a duplicate. Check for existing CDR ID and return the stored URL if it already exists.

### Reconciliation
Implement periodic reconciliation: pull all CPO CDRs from the past N days and compare against your local database. CDRs occasionally arrive late or are re-sent after corrections.

### VAT Handling
Always store both `excl_vat` and `incl_vat`. Tax requirements vary by country and change over time. Never derive one from the other — use what the CPO sends.

### Charging Period Continuity
`ChargingPeriod` entries must be contiguous (each one starts when the previous ends). Validate this on receipt — gaps indicate a data quality issue.

---

## Common Pitfalls

- **Using Session `total_cost` for billing**: Never. Only CDR `total_cost` is authoritative
- **Ignoring credit CDRs**: Must be processed as negative invoices / refunds — easy to accidentally skip when filtering CDR types
- **Not storing the eMSP's `Location` header**: The URL from the 201 response is the only way the CPO can later validate or reference the CDR on the eMSP's system
- **Duplicate CDR processing**: If the CPO retries a push, your endpoint must be idempotent — check by CDR ID before inserting

---

## Spec References

- 2.1.1: `mod_cdrs.md` — `release-2.1.1-bugfixes`
- 2.2.1: `mod_cdrs.asciidoc` — `release-2.2.1-bugfixes`
- 2.3.0: `mod_cdrs.asciidoc` — `2.3.0/release/core`
