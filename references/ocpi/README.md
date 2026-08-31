# OCPI Protocol Reference

## What Is OCPI?

The **Open Charge Point Interface (OCPI)** is the backend-to-backend protocol for EV charging interoperability. It lets a Charge Point Operator (CPO) and an e-Mobility Service Provider (eMSP) exchange structured data over HTTPS so that a driver registered with one network can charge on another network's chargers — without either side exposing its internal systems.

> **OCPI ≠ OCPP.** OCPP is "south-bound" (charger ↔ CSMS/CPMS). OCPI is "east-west" (CPO backend ↔ eMSP backend or hub). A full EV operator stack runs both.

---

## Architectural Fundamentals

### Transport and Auth

- All exchanges are **HTTPS + JSON** (REST, stateless HTTP — no WebSocket)
- Every request carries a **credentials token** in the `Authorization: Token <base64>` header
- Tokens are scoped per-partner and rotated through the Credentials handshake (see `credentials.md`)
- Responses always wrap data in `{"status_code": 1000, "data": {...}, "timestamp": "..."}` envelope

### Push vs Pull

OCPI supports both models per module. The data **owner** is the Sender; the receiver can either:

- **Pull**: `GET` a paginated list (required by spec — every receiver must be able to re-sync)
- **Push**: receive `PUT`/`PATCH`/`DELETE` calls when the sender detects a change (optional but expected in production)

### Client-Owned Objects

Unlike standard REST, in most OCPI modules **the client owns and controls the URL path** of the objects it pushes. For example, a CPO pushes `PUT /ocpi/emsp/2.2.1/locations/FR/CPO/LOC123` — the CPO constructs that URL, not the eMSP server. This "client-owned objects" pattern is fundamental to understanding OCPI routing.

### Sender / Receiver Terminology

Each module defines:
- **Sender** — the party that originates or owns the data (typically CPO for Locations/Sessions/CDRs/Tariffs; eMSP for Tokens/Commands)
- **Receiver** — the party that stores and uses the data
- Each side of the module exposes its own **interface** (set of HTTP endpoints)

---

## Roles

### OCPI 2.1.1 — Two Roles Only

| Role | Owns |
|---|---|
| **CPO** (Charge Point Operator) | Locations, EVSEs, Sessions, CDRs, Tariffs |
| **eMSP** (e-Mobility Service Provider) | Tokens, driver accounts |

### OCPI 2.2.1 / 2.3.0 — Multi-Role Platform Model

A **Platform** can host multiple roles simultaneously. New roles added:

| Role | Purpose |
|---|---|
| **CPO** | Operates physical chargers |
| **eMSP** | Manages driver accounts and roaming |
| **Hub** | Routes OCPI messages between multiple platforms |
| **NSP** (Navigation Service Provider) | Receives Location data for map/navigation apps |
| **NAP** (National Access Point) | National data aggregator (EU AFIR); can push and receive |
| **SCSP** (Smart Charging Service Provider) | Sends ChargingProfiles to CPOs for grid optimization |

---

## Connection Topology

### Peer-to-Peer (Bilateral)
CPO ↔ eMSP connect directly. Simple, low-latency, but requires one integration per partner pair.

### Hub-Based (2.2.1+)
CPO and eMSP both connect to a roaming hub (GIREVE). The hub routes messages. One integration unlocks the full hub network.

Hub-specific headers added in 2.2.1:
- `OCPI-from-country-code` / `OCPI-from-party-id`
- `OCPI-to-country-code` / `OCPI-to-party-id`

---

## Module Map

### Core Modules (All Versions)

| Module | File | Data Owner | Direction |
|---|---|---|---|
| Credentials | `credentials.md` | Both | Mutual handshake |
| Versions | _(inline in credentials)_ | Both | Discovery |
| Locations | `locations.md` | CPO | CPO → eMSP/NSP/NAP |
| Sessions | `sessions.md` | CPO | CPO → eMSP |
| CDRs | `cdrs.md` | CPO | CPO → eMSP |
| Tariffs | `tariffs.md` | CPO | CPO → eMSP/NSP |
| Tokens | `tokens.md` | eMSP | eMSP → CPO |
| Commands | `commands.md` | eMSP | eMSP → CPO (async) |

### Added in 2.2.1

| Module | File | Data Owner |
|---|---|---|
| ChargingProfiles | `charging-profiles.md` | SCSP / CPO |
| HubClientInfo | `hub-client-info.md` | Hub |

### Added / Formalized in 2.3.0

| Module | File | Notes |
|---|---|---|
| DirectPayment | `direct-payment.md` | Ad-hoc payment terminal flows (AFIR) |
| Booking | `booking.md` | Optional; separate branch `2.3.0/release/bookings` |
| InvoiceReconciliation | `invoice-reconciliation.md` | Optional; 2.3.0 edition 2 only |

---

## Version Evolution

```
2.1.1  →  2.2.1  →  2.3.0
  │           │          │
  │         Hubs       AFIR/NAP
  │         Multi-     DirectPayment
  │         role       Booking
  │         ChgProf    Invoice Reconciliation
  │         HubCI      North American taxes
  │                    vehicle_type on Location
  │                    stronger CDR pricing model
Strict
CPO/eMSP
only
```

---

## Module Reference Files

- [`credentials.md`](credentials.md)
- [`locations.md`](locations.md)
- [`sessions.md`](sessions.md)
- [`cdrs.md`](cdrs.md)
- [`tariffs.md`](tariffs.md)
- [`tokens.md`](tokens.md)
- [`commands.md`](commands.md)
- [`charging-profiles.md`](charging-profiles.md)
- [`hub-client-info.md`](hub-client-info.md)
- [`direct-payment.md`](direct-payment.md)
- [`booking.md`](booking.md)
- [`invoice-reconciliation.md`](invoice-reconciliation.md)
