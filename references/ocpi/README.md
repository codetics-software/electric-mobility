# OCPI Protocol Reference

## Select the exact source first

The [official OCPI repository](https://github.com/ocpi/ocpi) is the authority for protocol details. Read [versions.md](versions.md) to select among all six numbered repository versions: 2.0, 2.1, 2.1.1, 2.2, 2.2.1, and 2.3.0. Pin the negotiated version, documentation revision, core edition, optional module edition, hub profile, and actual tag or commit before implementing a field or endpoint. For 2.3.0, select the [core](https://github.com/ocpi/ocpi/tree/2.3.0/release/core), [Payments](https://github.com/ocpi/ocpi/tree/2.3.0/release/payments), or [Bookings](https://github.com/ocpi/ocpi/tree/2.3.0/release/bookings) lineage according to the feature.

Use the module references below for engineering context, then verify exact fields, endpoints, status codes, and obligations against the pinned upstream source. Partner or hub profiles may narrow the supported modules and change operational expectations; label those deviations.

## What Is OCPI?

The **Open Charge Point Interface (OCPI)** is the backend-to-backend protocol for EV charging interoperability. It lets a Charge Point Operator (CPO) and an e-Mobility Service Provider (eMSP) exchange structured data over HTTPS so that a driver registered with one network can charge on another network's chargers — without either side exposing its internal systems.

> **OCPI ≠ OCPP.** OCPP is "south-bound" (charger ↔ CSMS/CPMS). OCPI is "east-west" (CPO backend ↔ eMSP backend or hub). A full EV operator stack runs both.

---

## Architectural Fundamentals

### Transport and Auth

- All exchanges are **HTTPS + JSON** (REST, stateless HTTP — no WebSocket)
- Every request carries a **credentials token** in the `Authorization: Token <base64>` header under the current specification. The [official transport guide](https://github.com/ocpi/ocpi/blob/2.3.0/release/core/transport_and_format.asciidoc) notes that some older 2.1.1/2.2 implementations used unencoded tokens; handle such partners with an explicit compatibility setting.
- Tokens are scoped per-partner and rotated through the Credentials handshake (see `credentials.md`)
- OCPI response envelopes include a protocol `status_code` and `timestamp`; `data` and its shape depend on the endpoint and outcome. Check HTTP status and OCPI status separately.

### Push vs Pull

OCPI supports both models per module. The data **owner** is the Sender; the receiver can either:

- **Pull**: `GET` a paginated list (required for applicable list interfaces so receivers can re-sync)
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

### OCPI 2.0–2.1.1 — CPO/eMSP model

| Role | Owns |
|---|---|
| **CPO** (Charge Point Operator) | Locations, EVSEs, Sessions, CDRs, Tariffs |
| **eMSP** (e-Mobility Service Provider) | Tokens, driver accounts |

### OCPI 2.2 / 2.2.1 / 2.3.0 — Multi-Role Platform Model

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

### Hub-Based (2.2+)
CPO and eMSP both connect to a roaming hub (GIREVE). The hub routes messages. One integration unlocks the full hub network.

Hub routing headers in the 2.2+ line:
- `OCPI-from-country-code` / `OCPI-from-party-id`
- `OCPI-to-country-code` / `OCPI-to-party-id`

---

## Module Map

### Baseline modules (verify exact version and endpoint discovery)

| Module | File | Data Owner | Direction |
|---|---|---|---|
| Credentials | `credentials.md` | Both | Mutual handshake |
| Versions | _(inline in credentials)_ | Both | Discovery |
| Locations | `locations.md` | CPO | CPO → eMSP/NSP/NAP |
| Sessions | `sessions.md` | CPO | CPO → eMSP |
| CDRs | `cdrs.md` | CPO | CPO → eMSP |
| Tariffs | `tariffs.md` | CPO | CPO → eMSP/NSP |
| Tokens | `tokens.md` | eMSP | eMSP → CPO |
| Commands | `commands.md` | eMSP | eMSP → CPO (async); introduced in 2.1, absent from 2.0 |

### Added in the 2.2 line

| Module | File | Data Owner |
|---|---|---|
| ChargingProfiles | `charging-profiles.md` | SCSP / CPO |
| HubClientInfo | `hub-client-info.md` | Hub |

### 2.3.0 core and separately packaged modules

| Module | File | Notes |
|---|---|---|
| Payments | `direct-payment.md` | Wire ModuleID `payments`; separately packaged Payments branch |
| Booking | `booking.md` | Separately packaged Bookings branch; verify module and core edition pairing |
| InvoiceReconciliation | `invoice-reconciliation.md` | In 2.3.0 core edition 2; verify the tag and partner capability |

---

## Version Evolution

| Version line | Integration decision |
|---|---|
| 2.0 / 2.1 / 2.1.1 | Confirm legacy version and revision; 2.1 adds Commands, 2.1.1 fixes 2.1. |
| 2.2 / 2.2.1 | Confirm multi-role/hub topology, routing headers, and the partner's supported modules. |
| 2.3.0 core | Pin the core edition/tag; check revised types and Invoice Reconciliation availability. |
| 2.3.0 Payments or Bookings | Pin the separate module branch and edition together with the compatible core edition; do not infer support from `2.3.0` alone. |

---

## Module Reference Files

- [`versions.md`](versions.md)
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
