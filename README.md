# ⚡ Electric Mobility Skill — Codetics

An AI agent skill for building electric mobility software. Covers OCPI (backend roaming) and OCPP (charge point protocol) from first principles, based directly on the official specifications.

**Publisher:** [Codetics](https://codetics.fr)

---

## What this skill covers

| Domain | Content |
|---|---|
| **Ecosystem** | Actor roles (CPO, eMSP, Hub, SCSP, NSP, NAP), physical hierarchy (Location → EVSE → Connector) |
| **OCPI** | Authentication/registration, all 10 modules (Locations, Sessions, CDRs, Tokens, Tariffs, Commands, ChargingProfiles, Credentials, Versions, HubClientInfo), transport conventions, pagination, Push/Pull patterns |
| **OCPP 1.6** | All CP↔CS messages, smart charging profiles, reservation, configuration management |
| **OCPP 2.0.1 / 2.1** | TransactionEvent model, Device Model, ISO 15118 Plug & Charge, V2G |
| **Architecture** | CSMS design, OCPI service patterns, multi-party platforms, common pitfalls |
| **French market** | AFIREV IDs, IRVE decree, national NAP, key roaming hubs |

## Files

```
SKILL.md                    ← Main skill document (read this first)
examples/
  ocpi-examples.md          ← Canonical OCPI JSON examples from spec
  ocpp-examples.md          ← Canonical OCPP 1.6 wire-format examples
README.md                   ← This file
```

## When to use

Trigger this skill whenever working on:
- OCPI integration (CPO ↔ eMSP, roaming hubs like Gireve / EVRoaming)
- CSMS (Central System / Charge Management System) development
- Charge point firmware or OCPP client implementation
- EV driver apps consuming charging data
- Smart charging / load management systems
- NAP / IRVE compliance in France
- Tariff modeling and billing pipelines for EV charging

## Installation

Install this skill with:

```bash
npx skills add https://github.com/codetics-software/electric-mobility
```
Or 
```bash
npx skills add codetics-software/electric-mobility
```

## Key concepts at a glance

```
OCPP: Charge Point ←→ CSMS   (WebSocket, JSON-RPC style)
OCPI: CPO backend  ←→ eMSP   (HTTPS REST, JSON)

Physical: Location → EVSE → Connector
Billing:  Session → CDR (immutable, credit CDR for corrections)
Auth:     Token (RFID/APP_USER) → Authorize → StartTransaction
Remote:   eMSP Command → CPO → OCPP → Charge Point → async result
```

## License

Based on publicly available OCPI and OCPP specifications. Skill content © Codetics. Specifications © EVRoaming Foundation / Open Charge Alliance.
