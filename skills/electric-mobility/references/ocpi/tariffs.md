# OCPI — Tariffs Module

## Purpose

The Tariffs module exchanges **pricing structures** so that eMSPs can show drivers the expected cost before they plug in, and so that CDRs can embed a pricing snapshot for billing verification.

**Data owner**: CPO  
**Direction**: CPO (Sender) → eMSP / NSP / NAP (Receiver)

Examples omitting tax_included illustrate 2.2.1. In 2.3.0, tax_included is
required and min_price/max_price use PriceLimit; see the Version Differences
section and [2.3.0 fixtures](../../examples/ocpi-examples.md#ocpi-230-fixtures).

---

## Version Availability

| Version | Mandatory |
|---|---|
| 2.1.1 | Optional |
| 2.2.1 | Optional |
| 2.3.0 | Optional; assess regional transparency duties separately |

---

## Tariff Object Hierarchy

```
Tariff
  └── TariffElement (1..N)         — conditions block
        ├── PriceComponent[] (1..N) — what you pay
        └── TariffRestrictions?     — when this element applies
```

Evaluate elements in order **per tariff dimension**. The first active component
for a given dimension applies; other dimensions can apply from later elements.
Do not stop at the first matching element for the whole tariff.

---

## Key Data Models

### `Tariff`

| Field | Type | Description |
|---|---|---|
| `country_code` | string(2) | CPO's country |
| `party_id` | string(3) | CPO's party ID |
| `id` | string(36) | Unique tariff ID |
| `currency` | string | ISO 4217 |
| `type` | TariffType? (2.2.1+) | `AD_HOC_PAYMENT`, `PROFILE_CHEAP`, `PROFILE_FAST`, `PROFILE_GREEN`, `REGULAR` |
| `tariff_alt_text` | DisplayText[]? | Human-readable description per language |
| `tariff_alt_url` | URL? | Link to full tariff text |
| `min_price` | Price? (2.2.1) / PriceLimit? (2.3.0) | Floor price per session |
| `max_price` | Price? (2.2.1) / PriceLimit? (2.3.0) | Ceiling price per session |
| `tax_included` | TaxIncluded (required in 2.3.0) | YES, NO, or N/A; do not add to a 2.2.1 wire contract |
| `elements` | TariffElement[] | Pricing rules |
| `start_date_time` | DateTime? | When this tariff becomes active |
| `end_date_time` | DateTime? | When this tariff expires |
| `energy_mix` | EnergyMix? | Renewable energy info |
| `last_updated` | DateTime | |

### `TariffElement`

```json
{
  "price_components": [
    { "type": "FLAT", "price": 0.50, "vat": 20.0, "step_size": 1 },
    { "type": "ENERGY", "price": 0.35, "vat": 20.0, "step_size": 1 },
    { "type": "TIME", "price": 3.00, "vat": 20.0, "step_size": 300 }
  ],
  "restrictions": {
    "start_time": "08:00",
    "end_time": "20:00",
    "day_of_week": ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"],
    "min_kwh": 0.0,
    "max_kwh": 50.0
  }
}
```

### `PriceComponent`

| Field | Type | Description |
|---|---|---|
| `type` | TariffDimensionType | What triggers this price |
| `price` | number | 2.2.1: excluding VAT; 2.3.0: tax basis is defined by Tariff.tax_included |
| `vat` | number? | VAT percentage (e.g., `20.0` for 20%) |
| `step_size` | int | Minimum billing unit (see below) |

### `TariffDimensionType` Enum

| Value | Price unit / step multiplier | Meaning |
|---|---|---|
| `ENERGY` | kWh / Wh | Energy price per kWh; step_size in Wh |
| `FLAT` | — | One-time session fee |
| `PARKING_TIME` | hours / seconds | Parking price per hour; apply edition 2's vehicle-demand definition |
| `TIME` | hours / seconds | Charging-time price per hour; distinct from total connection time |

**`step_size` examples**:
- `ENERGY` with `step_size: 1000` → billing rounds up to nearest kWh
- `TIME` with `step_size: 300` → billing rounds up to nearest 5 minutes
- `FLAT` with `step_size: 1` → charged once (always 1 unit)

### `TariffRestrictions`

Conditions that must be met for the element to apply:

| Field | Description |
|---|---|
| `start_time` | Time of day (HH:MM) from which this applies |
| `end_time` | Time of day (HH:MM) until which this applies |
| `start_date` | Calendar date from which this applies |
| `end_date` | Calendar date until which this applies |
| `min_kwh` | Minimum kWh consumed to activate |
| `max_kwh` | Maximum kWh before this stops applying |
| `min_current` | Minimum current (A) for this to apply |
| `max_current` | Maximum current (A) |
| `min_power` | Minimum power (kW) |
| `max_power` | Maximum power (kW) |
| `min_duration` | Minimum session duration (seconds) |
| `max_duration` | Maximum session duration (seconds) |
| `day_of_week` | Days this applies: `MONDAY`…`SUNDAY` |
| `reservation` (2.2.1+) | `RESERVATION` or `RESERVATION_EXPIRES` — applies to reservation cost only |

---

## Tariff Type (2.2.1+)

| Type | Purpose |
|---|---|
| `AD_HOC_PAYMENT` | For drivers without a contract (credit card / ad-hoc) |
| `PROFILE_CHEAP` | Smart charging — cheapest energy (may be slow) |
| `PROFILE_FAST` | Smart charging — fastest charge (may cost more) |
| `PROFILE_GREEN` | Smart charging — renewable energy preference |
| `REGULAR` | Standard contracted roaming tariff |

The CPO publishes multiple tariff types. The eMSP picks the appropriate one based on driver preference or contract.

---

## HTTP Endpoints

### Sender Interface (CPO exposes this)

| Method | Path | Description |
|---|---|---|
| `GET` | `/ocpi/cpo/2.x/tariffs` | Get all tariffs (paginated) |
| `GET` | `/ocpi/cpo/2.x/tariffs/{tariff_id}` | Get single tariff |

### Receiver Interface (eMSP exposes this — for CPO to push to)

| Method | Path | Description |
|---|---|---|
| `GET` | `/ocpi/emsp/2.x/tariffs/{country_code}/{party_id}/{tariff_id}` | Validate tariff |
| `PUT` | `/ocpi/emsp/2.x/tariffs/{country_code}/{party_id}/{tariff_id}` | Push tariff |
| `DELETE` | `/ocpi/emsp/2.x/tariffs/{country_code}/{party_id}/{tariff_id}` | Remove tariff |

---

## Price Calculation Example

**Tariff**: Session fee €0.50 + €0.35/kWh + €3.00/hour after 1 hour

```json
{
  "elements": [
    {
      "price_components": [
        { "type": "FLAT", "price": 0.50, "step_size": 1 },
        { "type": "ENERGY", "price": 0.35, "step_size": 1 }
      ]
    },
    {
      "price_components": [
        { "type": "TIME", "price": 0.05, "step_size": 60 }
      ],
      "restrictions": { "min_duration": 3600 }
    }
  ]
}
```

Driver charges 20 kWh in 90 minutes:
- Flat: €0.50
- Energy: 20 × €0.35 = €7.00
- Time (only last 30 min past 1hr): 30 × €0.05 = €1.50
- **Total: €9.00** (+ VAT)

---

## Version Differences

### 2.1.1
- Simple structure — basic energy/time/flat pricing
- No `TariffType`
- No `min_price` / `max_price`
- No reservation-specific restrictions
- Limited restriction fields
- No per-component VAT — VAT applied globally

### 2.2.1
- **`TariffType` enum** for smart charging tariff classification
- **`min_price` / `max_price`** — price floor/ceiling per session
- **Reservation tariff support** — `restrictions.reservation` for distinguishing reservation fees from charging fees
- Per-component **`vat`** percentage on each `PriceComponent`
- Much richer documentation with many worked examples
- Tariff `start_date_time` / `end_date_time` for time-bounded tariffs

### 2.3.0
- Required `tax_included` indicates `YES`, `NO`, or `N/A`. PriceComponent.price follows that basis rather than always excluding VAT.
- `min_price`/`max_price` use `PriceLimit` with required `before_taxes` and optional `after_taxes`; Session/CDR costs use a different shared Price with `taxes` entries.
- Support multiple taxes without inventing state/province-specific fields. VAT percentage on PriceComponent remains optional.
- Edition 2 fixes a step-size example. Pricing dimensions still require correct ordered selection per dimension, quantity steps, and contractual/currency rounding.
- Read [ocpi-2.3.0.md](ocpi-2.3.0.md) for source pins. Do not claim `AD_HOC_PAYMENT` is universally mandatory or that publishing a tariff proves AFIR compliance.

---

## Implementation Notes

### Tariff Resolution Order
Evaluate elements **top to bottom for each dimension**, using the first active
component for that dimension. ENERGY, TIME, PARKING_TIME, and FLAT can accumulate
independently. Verify the pinned specification's behavior when a dimension has
no active component: in the inspected 2.3.0 source, that dimension has no cost.
A later unrestricted component can supply a defined fallback; never invent one.

### Tariff Snapshot in CDRs
Preserve the tariffs actually used, including any applicable changes during the
session, as immutable billing evidence. When supplied in the CDR, tariffs are
full objects linked by ChargingPeriod.tariff_id. The CDR tariffs field has `*`
cardinality; do not claim every wire CDR must include a tariff snapshot. Make
required audit evidence explicit in the commercial/implementation agreement.

### Tariff Versioning
When a tariff changes (e.g., price increase), do not modify the existing tariff. Instead:
1. Create a new tariff with a new ID
2. Update Location/Connector `tariff_ids` to reference the new one
3. Optionally set `end_date_time` on the old tariff

This preserves historical accuracy for ongoing sessions.

### Display Text
Always provide `tariff_alt_text` in the driver's language. The `DisplayText` object has `language` (ISO 639-1) and `text` fields:
```json
{ "language": "fr", "text": "0,35 €/kWh + 0,50 € de démarrage" }
```

---

## Common Pitfalls

- **Stopping at the first matching element**: Ordered selection is per dimension; later elements can supply other active dimensions.
- **Losing tariff evidence**: An ID resolving only to the current tariff cannot reproduce historical billing. Preserve applicable snapshots; distinguish that audit policy from the wire field's optional cardinality.
- **Ignoring `step_size`**: Round up to the next step. A 4-minute session with 5-minute step_size bills as 5 minutes. This must match between CPO calculation and eMSP verification
- **Tax basis mismatch in 2.3.0**: Missing tax_included or treating all prices as VAT-exclusive can produce incorrect estimates and CDRs.

---

## Spec References

- 2.1.1: `mod_tariffs.md` — `release-2.1.1-bugfixes`
- 2.2.1: `mod_tariffs.asciidoc` — `release-2.2.1-bugfixes`
- 2.3.0: `mod_tariffs.asciidoc` — `2.3.0/release/core`
