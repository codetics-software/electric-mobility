# ⚡ Electric Mobility Skill — Codetics

An AI agent skill for building complete electric-mobility products—from CPO/eMSP/CSMS backends and interoperability to web supervision, native iOS, and native Android applications. Covers OCPI, OCPP, Gireve integration, C#/.NET, Kotlin, Swift, and full charging-to-settlement lifecycles.

**Publisher:** [Codetics](https://codetics.fr)

---

## What this skill covers

| Domain | Content |
|---|---|
| **Ecosystem** | Actor roles (CPO, eMSP, Hub, SCSP, NSP, NAP), physical hierarchy (Location → EVSE → Connector) |
| **Domain modeling** | Provider/Account/User boundaries, cards vs tokens, ownership, cardinality, identity scopes, snapshots, state vectors, policy groups |
| **Lifecycles** | RFID and remote charging, metering, stop/finalization, late settlement, corrections, payment terminals, reconciliation |
| **OCPI** | Authentication/registration, all 10 modules (Locations, Sessions, CDRs, Tokens, Tariffs, Commands, ChargingProfiles, Credentials, Versions, HubClientInfo), transport conventions, pagination, Push/Pull patterns |
| **OCPP 1.6** | All CP↔CS messages, smart charging profiles, reservation, configuration management |
| **OCPP 2.0.1 / 2.1** | TransactionEvent model, Device Model, ISO 15118 Plug & Charge, V2G |
| **Full platform** | Complete CPO/eMSP/CSMS capability map, modular architecture, delivery slices, security, observability, C#/.NET and Kotlin backends |
| **Applications** | Web supervision and portals, Blazor/.NET MAUI, iOS/SwiftUI, Android/Kotlin/Compose, maps, real-time state, offline recovery, accessibility |
| **Interoperability** | Direct OCPI and Gireve hub profiles, conformance matrices, onboarding, synchronization, certification, reconciliation |
| **Architecture** | CSMS design, OCPI service patterns, multi-party platforms, common pitfalls |
| **French market** | AFIREV IDs, IRVE decree, national NAP, key roaming hubs |

## Files

```
SKILL.md                              ← Main skill and progressive loading rules
references/
  domain-relationships.md             ← Vendor-neutral domain graph and schema rules
  charging-lifecycles.md              ← End-to-end lifecycle and failure playbooks
  full-platform-blueprint.md          ← Full eMSP/CPO/CSMS and C#/.NET/Kotlin architecture
  supervision-and-client-apps.md      ← Web, iOS, and Android product guidance
  gireve-interoperability.md          ← Gireve profile, operations, and conformance playbook
  ocpi/                               ← Module-specific OCPI implementation references
examples/
  ocpi-examples.md                    ← Canonical OCPI JSON examples from spec
  ocpp-examples.md                    ← Canonical OCPP 1.6 wire-format examples
README.md                             ← This file
```

## When to use

Trigger this skill whenever working on:
- OCPI integration (CPO ↔ eMSP, roaming hubs like Gireve / EVRoaming)
- Complete eMSP, CPO, or combined platform development
- CSMS (Central System / Charge Management System) development
- C#/.NET or Kotlin backend implementation
- Web-based EV network supervision and operator portals, including Blazor
- Cross-platform C# applications with .NET MAUI
- Native iOS driver/operator apps with Swift and SwiftUI
- Native Android apps with Kotlin and Jetpack Compose
- Charge point firmware or OCPP client implementation
- EV driver, fleet, installer, support, finance, and site-host experiences
- Gireve onboarding, OCPI conformance, certification, and production operations
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

Org:      Provider/Tenant → Account → Membership/User
Physical: Location → Station → EVSE → Connector
Auth:     Credential → Authorization decision → Charging attempt
Runtime:  Command ≠ Transaction ≠ Energy delivery ≠ Session
Billing:  Session → CDR/settlement version → Invoice/adjustment
Remote:   eMSP Command → CPO → OCPP → Station → observed async result
Product:  Web + iOS + Android → product APIs → CPO/eMSP/CSMS modules
Roaming:  direct OCPI or hub profile (for example Gireve) → reconciliation
```



## License

Based on publicly available OCPI and OCPP specifications. Skill content © Codetics. Specifications © EVRoaming Foundation / Open Charge Alliance.
