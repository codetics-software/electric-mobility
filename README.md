# Electric Mobility Skill by Codetics

I build electric mobility software across the full charging lifecycle: CPO, eMSP, and CSMS platforms; OCPI roaming; OCPP station management; charging sessions, tariffs, CDRs, billing, and operator and driver applications. This skill records the engineering decisions I expect in production systems: clear protocol boundaries, version-aware implementations, observable asynchronous operations, secure integrations, and correct financial history.

For my complete work and services, visit [codetics.fr](https://codetics.fr).

## What the skill helps with

| Area | Guidance |
|---|---|
| OCPI | Stable 2.3.0 migration guidance, tax/Price contracts, parking, connector capabilities, hub roles, extensibility, editions, and legacy versions from 2.0 |
| OCPP | Self-contained field cards for every JSON action in 1.6 (28), 2.0.1 (64), and 2.1 (90 plus SEND); versioned payloads, WebSocket runtime, station/CSMS lifecycles, security, smart charging, V2X, and debugging |
| Product and domain | CPO/eMSP/CSMS architecture, EVSE relationships, authorization, charging lifecycles, supervision, mobile apps, settlement, and reconciliation |
| Security | Risk-tiered gate before any action; station identity, security profiles, certificates, roaming tokens, request forgery, payments, tenancy, mobile storage, and controls for every language |
| Architecture | Modular monolith, module ownership, layers, protocol adapters, pure state machines, transaction rules, and boundaries enforced in CI, for every language |
| Engineering | Dedicated agent and language rules, Java with Vert.x or pure Jakarta, idiomatic Kotlin/coroutines, current practices for all languages, clean code, versioned APIs, OpenAPI JSON, and Next.js native forms |

The skill separates protocol requirements from implementation choices and vendor behavior. It sends agents to the relevant reference before they generate code or make version-specific claims.

## Security comes first

Charging software moves electricity, unlocks hardware, takes money, and records where people go. Before doing anything, the skill makes an agent run a [security gate](skills/electric-mobility/references/security/README.md) that sets the work by risk:

| Tier | The task touches | The agent must |
|---|---|---|
| S0 | Explanation only | Answer directly |
| S1 | Code behind existing boundaries | Apply the invariants |
| S2 | A trust boundary, such as a station socket, OCPI, a login, a webhook, or a tenant query | Write a preflight, load the guide, and test abuse cases |
| S3 | A physical, financial, or credential effect, such as unlock, firmware, rotation, payment, or a CDR | Also define who may do what, idempotency, audit, and residual risk |

Agents also check dependencies against live sources with [vulnerability management](skills/electric-mobility/references/security/vulnerability-management.md): CVE, CVSS, CISA KEV, EPSS, SBOMs, and station firmware. They never claim a version is clean from memory.

The guides cover [stations and OCPP](skills/electric-mobility/references/security/ocpp-stations.md), [OCPI and roaming](skills/electric-mobility/references/security/ocpi-roaming.md), [payments and public charging](skills/electric-mobility/references/security/payments-and-public-charging.md), and [platform and clients](skills/electric-mobility/references/security/platform-and-clients.md). Every [language file](skills/electric-mobility/references/rules/README.md) has its own Security controls section, and a capability table covers languages not listed. [Field lessons](skills/electric-mobility/references/field-lessons.md) record how real stations behave.

## Built to use little context

`SKILL.md` is a small router, and everything else loads only when a task needs it. Agents go straight to the one OCPP card, OCPI module, or language file in scope. `scripts/verify-skill.py` fails if the description, `SKILL.md`, or any reference grows past its budget.

## Rules for every assistant

The rules work with **Claude, Codex, Grok, v0, and other assistants**. Each supported language has [its own file](skills/electric-mobility/references/rules/README.md), and unlisted languages use [a capability table](skills/electric-mobility/references/rules/security-capabilities.md). Agents verify versions and sources at use time instead of relying on a fixed claim of being "latest". [Answer formats](skills/electric-mobility/references/rules/agents.md) load only for full design requests.

## Contents

Everything an agent needs is in one folder, which is installed as a unit:

```text
skills/electric-mobility/
  SKILL.md                            Entry point, security gate, reference routing
  references/
    security/README.md                Security gate: preflight, stop conditions, exit check
    security/vulnerability-management.md
                                      CVE, CVSS, KEV, EPSS, SBOM, scanners, priorities
    security/vulnerability-program.md Firmware, CWE checks, supply chain, disclosure, legal reporting
    security/ocpp-stations.md         Handshake, security levels, proxies, certificates, commands
    security/ocpi-roaming.md          Token scope, request forgery, ownership, roaming commands
    security/payments-and-public-charging.md
                                      Webhooks, start gate, refunds, meter evidence, QR portals
    security/platform-and-clients.md  Tenancy, accounts, secrets, privacy, mobile, deployment
    code-architecture.md              Modules, layers, transactions, where code goes
    code-architecture-details.md      Data rules, clients, scaling, tests, decisions, anti-patterns
    domain-primer.md                  Actors, OCPI versus OCPP, module truths, worked reasoning
    engineering-principles.md         State, distributed behavior, units, money, tests, debugging
    field-lessons.md                  How real stations, meters, and tariffs behave
    rules/                            Assistant rules, security capabilities, one file per language
    ocpi/                             OCPI versions, roles, module references, build workflow
    ocpp/                             OCPP versions, runtime, management, and per-action message cards
    code-design-and-api.md            Clean code, Next.js forms, API versions, OpenAPI JSON
    implementation-and-debugging.md   Protocol boundaries and server debugging
    domain-relationships.md           Ownership, identity, and data modeling
    charging-lifecycles.md            End-to-end charging and failure flows
    full-platform-blueprint.md        Platform scope and delivery
    supervision-and-client-apps.md    Operator, web, and mobile products
    gireve-interoperability.md        Hub integration and conformance
  examples/                           OCPI and OCPP wire examples

SECURITY.md                           How this skill is secured, and how to report a problem
scripts/verify-skill.py               Checks the skill is self-contained and safe to install
evals/                                Behavior tests for the skill (not installed)
```

## Sources

- [OCPI official specification repository](https://github.com/ocpi/ocpi). Select the negotiated version and the appropriate 2.3.0 core or optional module release branch.
- [Open Charge Alliance OCPP versions](https://openchargealliance.org/protocols/open-charge-point-protocol/). The skill contains field-level JSON message references and implementation guidance, so readers need no local PDFs or downloaded ZIPs. Check the applicable edition, errata, and certification profile when conformance or a disputed detail depends on them.

The references summarize the inspected OCA JSON schema packages and specification behavior; they are not copies of the standards. The 2.x schema packages predate the newest prose editions, so verify later errata for edition-specific conformance.

## Install

```bash
npx skills add codetics-software/electric-mobility
```

The skill follows the [Agent Skills format](https://agentskills.io/specification): `SKILL.md`, `references/`, and `examples/` all sit in one folder, and installers copy that folder whole. To install by hand, copy `skills/electric-mobility/` into your agent's skills directory, and keep the folder name.

To check a clone before installing, or after changing the skill:

```bash
python3 scripts/verify-skill.py
```

Read [SECURITY.md](SECURITY.md) first. A skill is text an agent acts on, so treat it like a dependency.

## License

Skill content © Codetics, MIT license. OCPI specifications © EVRoaming Foundation; OCPP specifications © Open Charge Alliance.
