# OCPI — Booking Module

## Purpose

The Booking module enables **advance reservation of charging slots** beyond the simple `RESERVE_NOW` command. It is designed for fleet operators (especially HDVs — Heavy Duty Vehicles) who need to guarantee availability, manage complex booking windows, and handle no-show fees.

> This is an **optional module**, shipped as a separate branch from the core 2.3.0 spec.

---

## Version Availability

| Version | Available |
|---|---|
| 2.1.1 | No |
| 2.2.1 | No — `RESERVE_NOW` command exists, but not this module |
| 2.3.0 | Yes — optional; `2.3.0/release/bookings` branch |

---

## Booking vs `RESERVE_NOW`

| Feature | `RESERVE_NOW` (Commands module) | Booking module |
|---|---|---|
| Time horizon | Minutes to hours | Days/weeks ahead |
| No-show fees | No | Yes |
| Booking management | Basic (reserve/cancel) | Full lifecycle (confirm, modify, cancel) |
| Target user | Consumer EV | Fleet / HDV operators |
| State machine | Simple | Multi-step with driver check-in |

---

## Booking Lifecycle

```
eMSP/Fleet → POST booking (PENDING)
              ↓ (CPO accepts)
           RESERVED — slot held
              ↓ (driver arrives)
           CHECKED_IN — driver has checked in
              ↓ (charging starts)
           CHARGING
              ↓ (session ends)
           COMPLETED
              ↓
           CDR generated

Alternatively:
  RESERVED → CANCELED (by eMSP or CPO)
  RESERVED → NO_SHOW (expiry passed, driver didn't arrive)
```

---

## Key Data Models

### `Booking`

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique booking ID |
| `status` | BookingStatus | Current state |
| `location_id` | string | Location |
| `evse_uid` | string? | Specific EVSE (null = any available at location) |
| `connector_id` | string? | Specific connector |
| `token` | Token | Driver token to authorize the reserved session |
| `start_date_time` | DateTime | Requested booking start |
| `end_date_time` | DateTime | Requested booking end |
| `session_id` | string? | Set when session starts |
| `tariff` | Tariff? | Pricing including booking/no-show fees |
| `last_updated` | DateTime | |

### `BookingStatus` Enum

| Value | Meaning |
|---|---|
| `PENDING` | Booking requested, awaiting CPO confirmation |
| `RESERVED` | Slot confirmed and held |
| `CHECKED_IN` | Driver arrived and identified at EVSE |
| `CHARGING` | Session is active |
| `COMPLETED` | Booking and session finished |
| `CANCELED` | Canceled (by eMSP or CPO) |
| `NO_SHOW` | Driver did not arrive by end time |
| `INVALID` | Booking became invalid |

---

## Booking Fees in Tariff

The Booking module extends the Tariff model with booking-specific price components:

```json
{
  "elements": [
    {
      "price_components": [
        { "type": "FLAT", "price": 2.00 }
      ],
      "restrictions": { "reservation": "RESERVATION" }
    },
    {
      "price_components": [
        { "type": "FLAT", "price": 10.00 }
      ],
      "restrictions": { "reservation": "RESERVATION_EXPIRES" }
    }
  ]
}
```

- `RESERVATION` fee: charged when booking is confirmed
- `RESERVATION_EXPIRES` (no-show fee): charged if driver doesn't arrive

---

## HTTP Endpoints

### Receiver Interface (CPO exposes this)

| Method | Path | Description |
|---|---|---|
| `POST` | `/ocpi/cpo/2.x/bookings` | Create a new booking |
| `GET` | `/ocpi/cpo/2.x/bookings/{booking_id}` | Get booking status |
| `PUT` | `/ocpi/cpo/2.x/bookings/{booking_id}` | Modify a booking (time, EVSE) |
| `DELETE` | `/ocpi/cpo/2.x/bookings/{booking_id}` | Cancel a booking |

### Sender Interface (eMSP exposes this — CPO pushes updates)

| Method | Path | Description |
|---|---|---|
| `PUT` | `/ocpi/emsp/2.x/bookings/{country}/{party}/{booking_id}` | CPO pushes status updates |

---

## Branch Note

The Booking module lives in `2.3.0/release/bookings`, which branched from the core before edition 2. As of August 2026, the Booking branch v1.1 was updated to be more aligned with OCPI 3.0's architecture. When implementing:

1. Check whether the booking branch is rebased onto `2.3.0/release/core` edition 2 — it may not be
2. The `InvoiceReconciliation` module (edition 2 only) is not available on the bookings branch unless rebased

---

## Implementation Notes

### HDV Use Case
The primary driver is fleet operators for trucks, buses, and other heavy vehicles that need guaranteed charging windows. Ad-hoc reservation (consumer use) is also supported but `RESERVE_NOW` is simpler for short-term needs.

### Availability Check
Before accepting a booking, the CPO must verify EVSE availability for the requested window. This requires the CPO to maintain a calendar of reserved slots — more complex than simple `RESERVE_NOW`.

### Session Linking
When the driver arrives and charging starts, the CPO creates a regular OCPI Session and links it via `session_id` on the Booking object. The CDR is generated from the Session, not the Booking directly.

---

## Spec References

- 2.3.0: Separate branch `2.3.0/release/bookings` in the OCPI GitHub repository
- Latest Booking module version (v1.1) aligns more closely with OCPI 3.0 patterns
