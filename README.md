# Electric Mobility Skill by Codetics

I build electric mobility software across the full charging lifecycle: CPO, eMSP, and CSMS platforms; OCPI roaming; OCPP station management; charging sessions, tariffs, CDRs, billing, and operator and driver applications. This skill records the engineering decisions I expect in production systems: clear protocol boundaries, version-aware implementations, observable asynchronous operations, secure integrations, and correct financial history.

For my complete work and services, visit [codetics.fr](https://codetics.fr).

## What the skill helps with

| Area | Guidance |
|---|---|
| OCPI | All six numbered repository versions from 2.0 through 2.3.0; roles, credentials, modules, push/pull, hubs, optional module editions, and interoperability |
| OCPP | Self-contained field cards for every JSON action in 1.6 (28), 2.0.1 (64), and 2.1 (90 plus SEND); versioned payloads, WebSocket runtime, station/CSMS lifecycles, security, smart charging, V2X, and debugging |
| Product and domain | CPO/eMSP/CSMS architecture, EVSE relationships, authorization, charging lifecycles, supervision, mobile apps, settlement, and reconciliation |
| Engineering | Practical coding guidance for Java, Kotlin, Swift, C#, Rust, Go, Python, and TypeScript; server debugging, bug discovery, security reviews, and regression tests |

The skill separates protocol requirements from implementation choices and vendor behavior. It sends agents to the relevant reference before they generate code or make version-specific claims.

## Contents

```text
SKILL.md                              Skill entrypoint and reference routing
references/ocpi/README.md             OCPI version and module index
references/ocpi/versions.md            All repository versions and migration decisions
references/ocpi/*.md                  Module-specific engineering references
references/ocpp/README.md             OCPP source and version index
references/ocpp/ocpp-1.6.md           OCPP 1.6 implementation and diagnosis
references/ocpp/ocpp-2.0.1.md         OCPP 2.0.1 implementation and diagnosis
references/ocpp/ocpp-2.1.md           OCPP 2.1 implementation and diagnosis
references/ocpp/message-catalog.md     Complete OCPP action inventory and DTO workflow
references/ocpp/messages/<version>/    Per-action request, response, nested types, and enums
references/ocpp/websocket-and-runtime.md
                                      WebSocket handshake, RPC frames, concurrency
references/ocpp/charge-point-management.md
                                      End-to-end station and CSMS implementation
references/ocpp/errata-2026-06.md      Actionable 2.x behavior corrections
references/implementation-and-debugging.md
                                      Eight-language, server, and security guidance
references/domain-relationships.md     Ownership, identity, and data modeling
references/charging-lifecycles.md      End-to-end charging and failure flows
references/full-platform-blueprint.md  Platform architecture and delivery
references/supervision-and-client-apps.md
                                      Operator, web, and mobile products
references/gireve-interoperability.md  Hub integration and conformance
examples/                             OCPI and OCPP wire examples
```

## Sources

- [OCPI official specification repository](https://github.com/ocpi/ocpi). Select the negotiated version and the appropriate 2.3.0 core or optional module release branch.
- [Open Charge Alliance OCPP versions](https://openchargealliance.org/protocols/open-charge-point-protocol/). The skill contains field-level JSON message references and implementation guidance, so readers need no local PDFs or downloaded ZIPs. Check the applicable edition, errata, and certification profile when conformance or a disputed detail depends on them.

The references summarize the inspected OCA JSON schema packages and specification behavior; they are not copies of the standards. The 2.x schema packages predate the newest prose editions, so verify later errata for edition-specific conformance.

## Install

```bash
npx skills add codetics-software/electric-mobility
```

## License

Skill content © Codetics, MIT license. OCPI specifications © EVRoaming Foundation; OCPP specifications © Open Charge Alliance.
