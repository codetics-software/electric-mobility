# Full Electric-Mobility Platform Blueprint

Use this reference when building or reviewing a complete eMSP, CPO, CSMS, supervision platform, or a product combining several roles.

The goal is a full lifecycle, not a collection of CRUD endpoints.

## 1. Establish the Product Roles

One organization or deployment may perform several roles. Keep role boundaries explicit even when code is deployed together.

```text
Driver / fleet user
  -> eMSP product
       -> direct OCPI connection or roaming hub
            -> CPO platform
                 -> CSMS
                      -> charging station via OCPP
                           -> EVSE / Connector / EV

CPO/eMSP commercial records
  -> CDR / settlement / reconciliation
       -> invoicing, payments, reimbursements, reporting
```

For each role identify:

```text
customers and users
owned data
synchronized data
protocol interfaces
commands initiated and received
operational state authority
commercial obligations
security boundary
support responsibilities
```

Do not erase boundaries merely because the initial product is a modular monolith.

## 2. Complete Capability Map

### Shared platform foundation

- tenants/providers, accounts, memberships, roles, grants, and audit;
- organizations, legal entities, contacts, contracts, and feature entitlements;
- identity federation, MFA, service credentials, API keys, and secret rotation;
- localization, currencies, tax configuration, time zones, and notification preferences;
- immutable audit events and operator activity history;
- webhooks, API clients, idempotency, rate limits, and integration health;
- files, exports, privacy retention, pseudonymization, and deletion workflows.

### CPO capabilities

- locations, stations, EVSEs, connectors, publication, and ownership;
- commissioning, installer workflows, configuration, firmware, diagnostics, and maintenance;
- OCPP connection registry, bootstrapping, heartbeats, status, transactions, and meter values;
- remote start/stop, unlock, reset, reservation, availability, and configuration commands;
- incidents, alarms, reliability, issue resolution, and maintenance tickets;
- tariffs, charging groups, customer/access groups, policies, and ad-hoc pricing;
- CPO sessions, CDR generation, roaming exports, corrections, and reconciliation;
- payment-terminal, QR/ad-hoc payment, refunds, and chargebacks where applicable;
- site-host revenue, reimbursements, energy cost, and operational reports;
- smart charging, site limits, load balancing, EMS integration, and profile observability.

### eMSP capabilities

- customer accounts, users, fleets, vehicles, drivers, and cost centers;
- physical and virtual cards, tokens/credentials, assignment, fulfillment, activation, blocking, and expiry;
- roaming coverage, location search, map, favorites, availability, tariff display, and routing;
- authorization, remote start/stop, command status, active sessions, receipts, and support;
- MSP sessions, incoming CDR validation, duplicate detection, disputes, and corrections;
- plans, subscriptions, markups, taxes, budgets, spending controls, and customer invoices;
- fleet allocation, employee/home-charging reimbursement, exports, and integrations;
- driver notifications, session updates, payment failures, card status, and invoice availability.

### CSMS capabilities

- secure WebSocket endpoint and station identity;
- connection ownership, duplicate connections, routing, timeout, and correlation;
- OCPP version negotiation and version-specific message handlers;
- command queue/operation model without blocking connection event loops;
- station/EVSE/connector projections and freshness;
- transaction/event ingestion, raw evidence, deduplication, ordering, and reconciliation;
- meter normalization, signed meter data where applicable, and anomaly handling;
- configuration/device model, firmware, diagnostics, certificates, and security events;
- reservations, local authorization lists, smart charging, monitoring, and availability;
- simulator/test harness, vendor compatibility profiles, and certification support.

### Roaming and interoperability

- OCPI credentials and version discovery;
- sender/receiver interfaces by role and module;
- party, country, tenant, and external identity scoping;
- pull, push, pagination, incremental synchronization, retry, and reconciliation;
- Locations, Tokens, Tariffs, Sessions, CDRs, Commands, Charging Profiles, and applicable extensions;
- direct partners and hub connections as separately configured relationships;
- partner capability matrix, certification evidence, mapping rules, and operational dashboards;
- B2B tariff, CDR, invoice, settlement, and dispute reconciliation.

## 3. Recommended Architecture

Start with a modular monolith unless scale, team topology, availability, or regulatory boundaries justify distribution.

```text
Web / iOS / Android / Partner API
                 |
          API/BFF boundary
                 |
  +--------------+--------------+
  | Identity & tenancy           |
  | Accounts & contracts         |
  | Infrastructure               |
  | Credentials & authorization  |
  | Charging operations          |
  | Sessions & metering          |
  | Tariffs & policy             |
  | CDR & settlement             |
  | Billing & reimbursement      |
  | OCPI interoperability        |
  | OCPP CSMS                    |
  | Notifications & support      |
  +--------------+--------------+
                 |
    database + outbox + workers
                 |
       OCPI / OCPP / payments
```

Module rules:

- one module owns each write model;
- cross-module access uses application contracts, not arbitrary table joins;
- protocol DTOs stay in adapters;
- domain events describe committed facts;
- external publication uses an outbox or equivalent durable handoff;
- commands and synchronization have durable operation records;
- read models may denormalize for supervision and mobile performance;
- never distribute a system just to imitate a large platform.

## 4. Core Domain Modules

| Module | Owns | Must not own |
|---|---|---|
| Identity/Tenancy | users, memberships, roles, grants, tenant boundary | charging authorization decisions |
| Infrastructure | locations, stations, EVSEs, connectors, capabilities | live WebSocket connections |
| CSMS Connection | sockets, station routing, protocol correlation | customer billing |
| Credentials | cards, tokens, contracts, assignments, lifecycle | station transaction state |
| Authorization | decision requests/results, policy evidence | mutable card fulfillment state |
| Operations | remote commands, timeout, callback, correlation | final settlement amount |
| Sessions | operational charging view, periods, aggregates | invoice lifecycle |
| Metering | raw/normalized observations and provenance | tariff configuration |
| Tariffs/Policy | groups, rules, tariff definitions | immutable historical CDR facts |
| CDR/Settlement | commercial charging records, corrections | current infrastructure topology |
| Billing | ledger, invoices, payments, reimbursements | protocol message handling |
| Interoperability | OCPI connections, partner projections, sync state | core domain authority |

Read `domain-relationships.md` before turning this table into entities.

## 5. Write and Read Paths

### Command path

```text
client request
  -> authenticate and authorize tenant/account
  -> validate current projection
  -> create idempotent operation
  -> commit operation
  -> dispatch asynchronously
  -> map to OCPI/OCPP/payment provider
  -> ingest result/event
  -> update domain facts and projections
  -> notify clients
```

### Telemetry path

```text
station message
  -> authenticate connection
  -> validate protocol/version
  -> retain correlation/raw evidence as required
  -> deduplicate/order
  -> normalize units
  -> apply transaction/session projection
  -> publish supervision update
  -> synchronize roaming state where appropriate
```

### Financial path

```text
operational session
  -> final/provisional metering
  -> CDR issued or received
  -> validate and deduplicate
  -> settlement/correction chain
  -> accounting ledger
  -> invoice/reimbursement/payment
  -> reconciliation and disputes
```

## 6. Backend in C# / .NET

Use current project conventions. A suitable modern baseline is ASP.NET Core with explicit application/domain/infrastructure boundaries.

```text
Api
Application
Domain
Infrastructure
Protocol.Ocpi
Protocol.Ocpp
Workers
Tests.Unit
Tests.Integration
Tests.Contract
```

Recommended practices:

- use ASP.NET Core authentication/authorization policies for tenant and account scope;
- use `decimal` for money and explicit types/value objects for units;
- use `DateTimeOffset` or `Instant`-style abstractions for protocol instants;
- use nullable reference types and explicit wire validation;
- use `System.Text.Json` converters for exact protocol enums and timestamps;
- use `HttpClientFactory` with named/typed clients, timeouts, resilience, and redacted logging;
- use hosted services or workers for outbox, reconciliation, and async operations;
- use cancellation tokens through I/O paths;
- use bounded channels/queues only where their durability semantics are understood;
- keep WebSocket/OCPP connection ownership outside controllers;
- use EF Core persistence models separately from OCPI/OCPP DTOs when responsibilities differ;
- test JSON contracts and avoid relying on CLR enum names as wire values.

Do not introduce MediatR, MassTransit, Orleans, Kafka, or another framework unless it solves a demonstrated problem and fits the existing codebase.

## 7. Backend in Kotlin

Use current project conventions. For Spring-based systems, use Spring Boot with Kotlin and clear boundaries.

```text
api
application
domain
infrastructure
protocol.ocpi
protocol.ocpp
worker
test
```

Recommended practices:

- model value objects and sealed outcomes explicitly;
- use `BigDecimal` for money with defined scale/rounding;
- use `Instant`/`OffsetDateTime` for protocol timestamps;
- use explicit Jackson wire mappings and validate nullability at boundaries;
- do not apply JPA entity classes directly as API/OCPI DTOs;
- avoid data classes for mutable JPA entities without understanding equality/proxy behavior;
- place transaction boundaries in application services;
- use coroutines only with libraries and execution models that support them correctly;
- use WebClient or the project's HTTP client with timeouts, redaction, and response-envelope validation;
- keep OCPP WebSocket handling non-blocking and isolate blocking persistence work;
- use scheduled/worker processing for outbox, retries, and reconciliation;
- test serialization, persistence identity, tenant isolation, and duplicate delivery.

For non-Spring Kotlin, preserve the same domain and adapter boundaries rather than forcing Spring patterns.

## 8. API Design for First-Party Clients

Do not expose raw OCPI or OCPP DTOs directly to web/mobile clients.

Create product APIs shaped around user intent:

```text
GET  /locations/map
GET  /locations/{id}
POST /charging-operations/start
GET  /charging-operations/{id}
POST /sessions/{id}/stop
GET  /sessions/active
GET  /sessions/history
GET  /stations/{id}/supervision
POST /stations/{id}/commands
GET  /incidents
GET  /invoices
```

These paths are illustrative implementation choices, not protocol endpoints.

First-party APIs should expose:

- stable internal IDs plus safe external references where needed;
- operation resources for asynchronous actions;
- state, evidence time, and freshness;
- localized/display-ready amounts alongside precise structured values;
- capability flags rather than client guesses;
- cursor pagination for changing datasets;
- consistent problem details and correlation IDs;
- optimistic-concurrency or version fields for destructive administration.

## 9. Events and Real-Time Updates

Use WebSocket, Server-Sent Events, push notifications, polling, or a combination according to client needs.

```text
Domain fact
  -> committed transaction
  -> durable event/outbox
  -> projection
  -> real-time gateway
  -> subscribed clients
```

Clients must reconnect and recover from missed events by refetching a versioned projection. Real-time delivery is an optimization, not the sole source of truth.

Candidate client events:

```text
station.connection.changed
evse.status.changed
operation.updated
session.updated
metering.summary.updated
incident.opened
incident.resolved
settlement.updated
invoice.available
```

Event names are application choices.

## 10. Security Baseline

- tenant/account authorization on every resource traversal;
- separate human sessions, mobile tokens, station credentials, and partner credentials;
- MFA and step-up authorization for sensitive operator commands;
- station certificate/security profile appropriate to OCPP version and deployment;
- secrets in managed secret storage with rotation;
- PII and payment data minimization;
- redaction of authorization headers, OCPI tokens, RFID identifiers where sensitive, and certificates;
- signed/authenticated webhooks with replay controls;
- audit actor, reason, target, command, result, and correlation;
- rate limits and abuse prevention on start/stop/unlock and authorization paths;
- privacy retention and lawful deletion without destroying required financial evidence.

## 11. Observability and Operations

A supervision platform must answer:

```text
Is the station connected now, and how fresh is that fact?
What is each EVSE/connector doing?
Which command was sent, by whom, and what followed?
Which sessions are active, stuck, or financially incomplete?
Which OCPI partners are synchronized or failing?
Which CDRs are late, duplicate, rejected, or corrected?
Which invoices and reimbursements do not reconcile?
```

Track metrics by tenant, role, partner, station vendor/model, protocol/version, and failure class without leaking secrets or creating unbounded-cardinality labels.

## 12. Delivery Slices

Build vertical, testable slices rather than all schemas first.

1. tenancy, accounts, users, audit;
2. station onboarding and OCPP connectivity;
3. topology/status supervision;
4. local authorization and transaction lifecycle;
5. metering and operational sessions;
6. remote commands with operation tracking;
7. tariffs and deterministic pricing;
8. CDR generation/ingestion and corrections;
9. OCPI direct/hub interoperability;
10. eMSP cards, map, remote charging, and history;
11. invoicing, settlement, and reimbursements;
12. incidents, firmware, smart charging, and advanced operations.

Each slice includes backend, client experience, authorization, audit, observability, failure handling, migrations, and tests.

## 13. Full-Platform Quality Gate

```text
[ ] Product roles and tenant boundaries explicit
[ ] CPO, eMSP, CSMS, and roaming capabilities mapped
[ ] Web, iOS, and Android use product APIs, not raw protocol DTOs
[ ] C# or Kotlin backend follows existing stack conventions
[ ] OCPP station lifecycle works through restart/reconnect
[ ] OCPI initial sync, push, retry, and reconciliation implemented
[ ] Remote operations are asynchronous and observable
[ ] Meter values retain unit/time/source provenance
[ ] Sessions, CDRs, settlement, invoices, and payouts are distinct
[ ] Tariff calculation is deterministic and auditable
[ ] Corrections create traceable adjustments
[ ] Tenant isolation and command authorization tested
[ ] Real-time clients recover missed events
[ ] Partner/vendor behavior isolated from standards
[ ] Simulators and contract tests cover full charging cycles
[ ] Operational dashboards expose freshness and failure state
```
