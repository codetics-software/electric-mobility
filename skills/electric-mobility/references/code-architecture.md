# How to architect the code

Engineering policy for every language, not a protocol requirement. In an existing project, follow its
sound conventions and move toward this gradually. Do not rewrite a working system unless asked. For
data rules, client structure, scaling, tests by layer, decision records, and anti-patterns, see
[details](code-architecture-details.md).

## Start with a modular monolith

Build one deployable application with strict internal modules. A charging platform has many
operations that must commit together, such as a session, its payment, and its outgoing
command. Splitting those across services early replaces a simple transaction with distributed
failure handling.

Split a module out only when you can name the need:

| Good reason to split | Example |
|---|---|
| Very different scaling | The station connection tier holds many long-lived sockets |
| Different failure isolation | A dashboard deployment must not disconnect the fleet |
| Security or compliance isolation | A signing service holds the CA key |
| Separate team ownership with a stable contract | A dedicated billing team |

"It feels cleaner", or a technology being popular, is not a reason. Add a broker, cache, or
service only when you can state the measured problem it solves.

## Modules

Organize by business capability, not by technical type. Each module owns its data, and others
reach it only through its public interface.

| Module | Owns | Does not own |
|---|---|---|
| `identity` | Accounts, sessions, roles, tenants | Charging decisions |
| `assets` | Sites, zones, stations, EVSEs, connectors, static data | Live connection state |
| `connectivity` | Station sockets, handshake, presence | Business rules |
| `commands` | Durable station commands, deadlines, results | Why a command was requested |
| `authorization` | Tokens, access decisions, offline lists | Payment |
| `charging` | Sessions, transactions, state, meter evidence | Prices |
| `pricing` | Tariffs, scope resolution, calculations | Collecting money |
| `billing` | Orders, invoices, refunds, settlement, payment provider adapter | Energy measurement |
| `roaming` | OCPI connections, partners, synced copies, CDR exchange | Local station control |
| `smart-charging` | Site limits, allocation, profiles to apply | Sending frames |
| `notifications` | Delivery of email and push | Deciding that something happened |
| `audit` | Append-only records of actions | Business state |

Dependencies between modules run in one direction and contain no cycles. A common order is:

```text
roaming, billing, smart-charging, notifications
              |
              v
     charging, pricing, authorization
              |
              v
     commands, assets, connectivity
              |
              v
      identity, audit, shared kernel
```

When a lower module needs to inform a higher one, it publishes an event. For example, `charging`
publishes `SessionCompleted`, and `billing` and `roaming` react. `charging` never imports `billing`.

Keep the shared kernel tiny: IDs, money, energy, time, and tenant types. Anything larger becomes a
place where every module is coupled to every other.

## Layers inside a module

```text
adapters  ->  application  ->  domain
    |              |
    v              v
infrastructure implements ports defined by application/domain
```

| Layer | Contains | Must never |
|---|---|---|
| **Adapters (inbound)** | HTTP routes, WebSocket handlers, OCPP and OCPI endpoints, webhooks, jobs | Hold business rules or query a database |
| **Application** | Use cases: load, authorize, call the domain, save, emit | Know about HTTP, JSON, or a specific database |
| **Domain** | State machines, invariants, calculations, value types | Do I/O, read a clock, or import a framework |
| **Infrastructure** | Repositories, partner clients, provider SDKs, station sender | Decide business outcomes |

**The test:** you should be able to run all domain logic with no database, no network, and no framework.

## Standard layout

Adapt names to the language and framework:

```text
src/
  modules/
    charging/
      domain/            Session state machine, meter rules, value types
      application/       StartSession, RecordMeterValue, ports
      adapters/          Internal API routes, event handlers
      infrastructure/    Repositories
      api                The module's public interface, the only thing others import
    commands/  billing/  pricing/  ...
  protocols/
    ocpp/
      transport/         Handshake, frames, correlation, limits
      v1_6/              Wire DTOs and mapping
      v2_0_1/
      v2_1/
      vendors/           Vendor deviations, each one labeled
    ocpi/
      transport/         Token auth, envelope, outbound client
      v2_1_1/
      v2_2_1/
      v2_3_0/
  shared/                Money, energy, IDs, clock, tenant
  composition/           Wiring and configuration; the only place that sees everything
tests/
  architecture/          Rules enforcing this structure
  simulators/            Fake station, fake partner, fake payment provider
```

## Enforce boundaries in each language

A boundary that only exists in a document will erode. Use the language's real mechanism, and fail CI
when it is crossed.

| Language | Express modules with | Enforce with (verify for your version) |
|---|---|---|
| Java | Maven or Gradle modules, package-private classes, the module system | ArchUnit |
| Kotlin | Gradle modules, `internal` visibility | ArchUnit on the JVM, Gradle dependency rules; for KMP, keep common code platform-free |
| C#/.NET | Separate projects, `internal` | Project references, NetArchTest or similar |
| Go | Packages, `internal/` directories | Compiler for `internal/`; narrow interfaces at the consumer |
| Rust | Workspace crates, `pub(crate)` | Crate dependency graph |
| Python | Packages, with `__all__` | import-linter, type checking |
| TypeScript | Workspaces, `exports` in package.json | dependency-cruiser or ESLint boundary rules |
| Swift | Swift Package Manager targets, `internal` and `package` access | Target dependency graph |
| Other | The language's module and visibility tools | An import check in CI |

Follow language idioms. Go packages should not imitate Java class hierarchies, and these layers do not
need a class or interface for every function.

## Protocol adapters

A protocol adapter translates. It decides nothing about the business.

Every inbound message follows the same pipeline in the same order, so no route can skip a step:

```text
1. Limit       size, rate
2. Authenticate    verified credential -> identity (station, partner)
3. Parse       frame or envelope
4. Validate    schema, direction, allowed action, version
5. Deduplicate     inbox check by scoped key
6. Map         wire DTO -> application command, with explicit units and UTC time
7. Authorize and execute   the application use case
8. Map back    result -> protocol response
9. Record      redacted evidence and correlation ID
```

- **One DTO set per protocol version.** Never a universal DTO that unions all versions.
- **Keep the domain protocol-free.** The domain says `StartRequested`, never `RemoteStartTransaction`
  or `START_SESSION`. Only the adapter layer translates.
- **Isolate vendor deviations** under a `vendors/` folder, each with a comment naming the device and
  firmware. Never let one leak into the core.
- **Never put wire enums in the domain.** Map them, and keep unknown values safely.

## State machines

Write each state machine as a pure function, which makes it simple to test exhaustively:

```text
decide(state, event, now) -> (new state, effects to perform) or a rejection
```

- `now` is passed in. The function reads no clock.
- Effects are returned as data ("send this command", "publish this event"). The function does not
  perform them.
- Illegal transitions return a rejection. A duplicate event is a no-op.
- Keep dimensions separate, with one machine per fact: connectivity, connector status, authorization,
  transaction, energy, payment, roaming sync. Do not combine them in one `status` column.
- Record evidence with each transition: what proved it, and when.

## Transactions and side effects

This is where most charging-platform bugs live.

1. **Never make a network call inside a database transaction.** A slow partner or station will hold
   locks and bring the whole platform down.
2. **Write intent in the same transaction as the state change.** Use an outbox or a durable command row.
3. **Send after commit.** A worker reads the outbox and delivers.
4. **Station commands are at most once.** Mark as sent, commit, then write to the socket. If the result
   is unknown, surface it for reconciliation rather than resending.
5. **Partner and provider calls are at least once, made safe with idempotency keys.**
6. **Inbound messages go through an inbox.** Store the dedup key in the same transaction as the effect.
7. **Serialize per aggregate.** Lock by station, session, payment, or command, and take locks in one
   documented order to prevent deadlocks.
8. **Run a reconciler for every asynchronous flow.** Something must find commands past their deadline,
   payments stuck between states, and undelivered events.

```text
request -> transaction { validate, change state, write outbox } -> respond with an operation ID
worker  -> read outbox -> send -> record outcome
station -> event -> transaction { dedup, transition, write outbox }
```

## Where security lives

Put each control in exactly one obvious place, so that it cannot be forgotten on a new route.

| Layer | Enforces |
|---|---|
| Edge and proxy | TLS, client certificates, overwriting forwarded headers |
| Inbound adapter | Authentication, limits, schema validation, CSRF and origin checks |
| Application use case | **Permission and tenant checks**, for every caller, including jobs and events |
| Domain | Invariants that hold whoever is calling |
| Repository | Tenant as a required parameter, in every query |
| Outbound adapter | URL validation, timeouts, redirects off, size limits |
| Infrastructure | Secret access, key handling, audit writing |

UI checks are for display only. Authorization belongs in the use case, so that the API, a job, and a
future integration all pass through it.

**Make the insecure path hard to write.** For example:

- a repository method that takes a tenant, so a query without one cannot be written by accident;
- a `Secret` type with a redacted string form;
- a single outbound client for partners, instead of letting any code create one;
- a `Money` type instead of a bare number, and a `WattHours` type instead of a bare decimal.

## Where does this code go?

| I need to... | Put it in |
|---|---|
| Parse a new OCPP message | `protocols/ocpp/<version>/`, then a use case in the owning module |
| Add a rule about when a session may end | `charging/domain` |
| Handle a vendor's odd timestamp | `protocols/ocpp/vendors/`, mapped before the domain |
| Call a partner API | `protocols/ocpi/<version>/` through the shared client, behind a port |
| Check who may unlock a connector | The use case in the owning module |
| Calculate a price | `pricing/domain`, a pure function with a tariff snapshot as input |
| React when a session completes | An event handler in the reacting module |
| Show a session on the dashboard | A read model or query in `charging`, with a view model in the UI |
| Add a scheduled cleanup | `adapters` in the owning module, calling a use case |
| Use a payment provider's SDK | `billing/infrastructure`, behind a port |
| Add a helper used everywhere | Rarely `shared/`. First ask which module actually owns it |

## Review checklist

- [ ] Each change sits in the module that owns the concept.
- [ ] No dependency cycles, and the domain imports no framework, database, or protocol code.
- [ ] Each route runs the full inbound pipeline, with authorization in the use case.
- [ ] Every query is tenant-scoped.
- [ ] No network call inside a transaction, and side effects use an outbox.
- [ ] Commands are at most once, and money operations carry idempotency keys.
- [ ] State machines are pure, with their legal and illegal transitions tested.
- [ ] Money, energy, time, and IDs use explicit types.
- [ ] Protocol versions and vendor deviations stay isolated.
- [ ] Boundaries are enforced in CI, not only described.
- [ ] No infrastructure added without a stated, measured need.
