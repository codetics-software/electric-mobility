---
name: electric-mobility
description: >
  Expert electric-mobility software engineering skill for EV charging,
  OCPI, OCPP, CPO/eMSP platforms, CSMS, EVSEs, roaming, charging sessions,
  CDRs, tariffs, authorization, reservations, smart charging, ISO 15118,
  V2G, IRVE, charging infrastructure, interoperability, debugging,
  architecture, implementation, and testing. Use this skill whenever a
  task involves electric-vehicle charging software or charging protocols.
license: MIT
metadata:
  author: Codetics
  repository: https://github.com/codetics-software/electric-mobility
  topics: ocpi, ocpp, electric-mobility, ev-charging, cpo, emsp, csms, evse, roaming
---

# Electric Mobility Agent

This provides protocol-aware engineering knowledge and workflows for
electric-mobility software.

It is intended for implementing, reviewing, debugging, designing,
testing, or explaining:

- EV charging infrastructure
- CPO platforms
- eMSP platforms
- CSMS platforms
- EVSEs and charging stations
- OCPI
- OCPP
- roaming
- charging sessions
- CDRs
- tariffs and billing
- authorization
- reservations
- remote charging commands
- smart charging
- ISO 15118
- Plug & Charge
- V2G / V2X
- IRVE
- charging infrastructure APIs
- interoperability between charging platforms

The objective is not to memorize every protocol field.

The objective is to reason correctly about:

1. protocol boundaries;
2. protocol versions;
3. actor roles;
4. data ownership;
5. state machines;
6. asynchronous operations;
7. distributed-system failures;
8. interoperability;
9. security;
10. billing and energy measurement.

---

# 1. Mandatory Rules


## OCPI Reference Rule

When an OCPI task matches a module referenced under `references/ocpi/`, consult that reference before generating implementation code. Do not reconstruct the module from memory when the repository contains a module-specific implementation reference.


Before implementing or explaining anything, determine:

```text
What protocol?
What version?
Which actor?
Who owns the data?
Who initiates the operation?
What is the expected state transition?
Is the operation synchronous or asynchronous?
What happens if the remote system is unavailable?
How is the operation correlated?
````

Never silently assume a protocol version.

If the version is unknown and materially affects the answer:

```text
State the assumption explicitly.
Proceed only where the behavior is version-independent.
Identify what must be verified.
```

Never invent:

* protocol fields;
* endpoints;
* enum values;
* message names;
* headers;
* state transitions;
* authentication mechanisms;
* capabilities;
* version-specific behavior.

If exact protocol behavior matters, verify the official specification before making a normative claim.

Clearly distinguish:

```text
STANDARD BEHAVIOR
IMPLEMENTATION CHOICE
VENDOR-SPECIFIC BEHAVIOR
ARCHITECTURAL RECOMMENDATION
```

Never present an implementation convention as a protocol requirement.

Never expose:

* credentials;
* OCPI tokens;
* bearer tokens;
* passwords;
* private keys;
* certificates;
* customer data;
* production endpoints containing secrets.

---

# 2. Electric Mobility System Model

A typical charging ecosystem looks like:

```text
                    EV Driver
                       |
                       v
                    eMSP
                       |
                     OCPI
                       |
                       v
              CPO / Roaming Hub
                       |
                       v
                      CSMS
                       |
                     OCPP
                       |
                       v
              Charging Station
                       |
                      EVSE
                       |
                   Connector
                       |
                       v
                       EV
```

These layers have different responsibilities.

## OCPI

Backend-to-backend interoperability.

Typical use:

```text
eMSP <---- OCPI ----> CPO
```

OCPI commonly handles:

* Locations
* EVSEs
* Connectors
* Tokens
* authorization
* Sessions
* CDRs
* Tariffs
* Commands
* Charging Profiles
* Credentials
* Versions
* roaming
* hub routing

## OCPP

Charging-station-to-CSMS communication.

Typical use:

```text
Charging Station <---- OCPP ----> CSMS
```

OCPP commonly handles:

* station connectivity
* authorization
* charging transactions
* status
* meter values
* remote commands
* configuration
* firmware
* diagnostics
* reservations
* smart charging
* security
* device management

## Critical distinction

Do not say:

```text
OCPI controls the charger.
```

Prefer:

```text
OCPI expresses the business/interoperability operation.
The CPO/CSMS translates that operation into station-level behavior,
usually through OCPP.
```

Typical flow:

```text
eMSP
  |
  | OCPI START_SESSION
  v
CPO
  |
  | business validation
  v
CSMS
  |
  | OCPP operation
  v
Charging Station
```

---

# 3. Actors

## CPO

Charge Point Operator.

Typically responsible for:

* charging stations;
* EVSE operational state;
* charging sessions;
* energy measurements;
* tariffs;
* CDR generation;
* station management;
* OCPP connectivity.

## eMSP

e-Mobility Service Provider.

Typically responsible for:

* driver accounts;
* charging contracts;
* charging tokens;
* authorization;
* driver applications;
* roaming relationships.

## CSMS

Central System / Charging Station Management System.

Responsible for communication and management of charging stations.

The CSMS may be part of the CPO platform or a separate system.

## Roaming Hub

Routes interoperability traffic between multiple parties.

A hub does not automatically become the owner of the underlying domain data.

## EVSE

Electric Vehicle Supply Equipment.

Use EVSE and connector precisely.

Conceptually:

```text
Location
  └── EVSE
        └── Connector
```

Do not use "EVSE", "connector", "charge point", and "charging station" as interchangeable terms.

---

# 4. Protocol Version Awareness

Always establish the exact version before implementing version-sensitive behavior.

Relevant protocol generations include:

```text
OCPI:
  2.1.1
  2.2.1
  2.3.0

OCPP:
  1.6
  2.0.1
  2.1
```

Older versions remain widely deployed.

Do not assume that the newest version is the version supported by a real-world integration.

When migrating between versions:

```text
DO NOT:
rename messages mechanically.

DO:
map concepts and identify semantic differences.
```

For migration work, create an explicit mapping:

```text
Old concept
    ->
New concept
    ->
Semantic differences
    ->
Compatibility concerns
```

---

# 5. OCPI

## 5.1 Purpose

OCPI is primarily a backend interoperability protocol.

Typical architecture:

```text
CPO <---- OCPI ----> eMSP
```

or:

```text
CPO <---- OCPI ----> Hub <---- OCPI ----> eMSP
```

OCPI commonly uses HTTP/REST and JSON.

---


# 5.2. OCPI Reference-First Implementation Workflow

This repository contains implementation-oriented OCPI reference material under:

```text
references/
  ocpi/
    README.md
    credentials.md
    locations.md
    sessions.md
    cdrs.md
    tariffs.md
    tokens.md
    commands.md
    charging-profiles.md
    hub-client-info.md
    direct-payment.md
    booking.md
    invoice-reconciliation.md
```

These files are part of this skill and MUST be consulted before designing or implementing an OCPI module, OCPI entity, OCPI endpoint, OCPI synchronization flow, or OCPI-specific business logic.

The references are the first implementation source inside this repository. They encode the intended module structure, terminology, object models, ownership, endpoint responsibilities, synchronization patterns, version differences, implementation notes, common pitfalls, and examples.

## Reference Loading Rules

When the task involves OCPI:

```text
1. Identify the OCPI version.
2. Identify the module.
3. Read references/ocpi/README.md.
4. Read the module-specific reference file.
5. Identify referenced entities/enums/shared concepts.
6. Read the relevant sections of those referenced files.
7. Compare the requested implementation with the reference conventions.
8. Verify normative/version-sensitive behavior against the official OCPI specification when required.
9. Implement using the project's existing architecture and language.
10. Add tests for the protocol contract and domain behavior.
```

Do NOT immediately invent DTOs, entities, controllers, repositories, endpoint paths, or service interfaces from model memory when a matching reference exists.

Prefer:

```text
references/ocpi/*.md
        |
        v
module model
        |
        v
version-specific protocol contract
        |
        v
application/domain mapping
        |
        v
implementation
```

over:

```text
model memory
    |
    v
guessed implementation
```

## Module Selection Matrix

Use the repository reference corresponding to the requested capability:

| Capability | Reference |
|---|---|
| Connection registration, credentials, version discovery | `references/ocpi/credentials.md` |
| Charging sites, EVSEs, connectors, status | `references/ocpi/locations.md` |
| Live charging sessions and charging periods | `references/ocpi/sessions.md` |
| Final billing records and credit CDRs | `references/ocpi/cdrs.md` |
| Pricing structures and tariff calculation | `references/ocpi/tariffs.md` |
| Driver/RFID/app authorization tokens | `references/ocpi/tokens.md` |
| Remote start/stop/reservation/unlock commands | `references/ocpi/commands.md` |
| Smart-charging constraints and profiles | `references/ocpi/charging-profiles.md` |
| Roaming-hub client information | `references/ocpi/hub-client-info.md` |
| Ad-hoc/direct payment flows | `references/ocpi/direct-payment.md` |
| Advance booking | `references/ocpi/booking.md` |
| Billing/invoice reconciliation | `references/ocpi/invoice-reconciliation.md` |
| Overall module/version/role architecture | `references/ocpi/README.md` |

If a module reference links to another OCPI concept, follow that dependency rather than implementing the concept in isolation.

## OCPI Reference as an Implementation Contract

For every OCPI module implementation, extract and explicitly establish:

```text
Module
Version availability
Sender
Receiver
Data owner
Object hierarchy
Primary entities
Nested entities
Enums
Shared value objects
Sender interface
Receiver interface
HTTP methods
URL structure
Path parameters
Request body
Response body
OCPI response envelope
Authentication
Push behavior
Pull behavior
Pagination
last_updated semantics
Idempotency requirements
Synchronization/reconciliation behavior
Version differences
Common pitfalls
```

The implementation should map these concepts explicitly.

For example:

```text
OCPI reference
    |
    +-- Module
    +-- DTOs
    +-- Value objects
    +-- Enums
    +-- Sender interface
    +-- Receiver interface
    +-- Application services
    +-- Persistence mapping
    +-- Synchronization
    +-- Tests
```

Do not collapse all of these concerns into one database entity or one controller.

## Entity Design Rules

When asked to "create an OCPI entity", first determine whether "entity" means:

```text
OCPI protocol DTO
internal domain entity
persistence entity
request DTO
response DTO
value object
enum
nested protocol object
```

Never assume that an OCPI object should directly become a JPA/database entity.

Prefer:

```text
OCPI JSON
    ->
Protocol DTO
    ->
Mapper
    ->
Application/domain model
    ->
Persistence model
```

When persistence is required:

```text
OCPI object identity
    !=
internal database identity
```

Preserve the external OCPI identity and protocol context explicitly.

For objects such as Location, EVSE, Connector, Token, Session, and CDR, preserve stable protocol identifiers and version-specific fields without using the database primary key as a substitute for the external identifier.

## Entity Identity and Nested Objects

For every OCPI object, determine:

```text
Who assigns the ID?
Is the ID globally unique or scoped?
What is the composite identity?
Which parent object scopes the child?
Can the child be addressed independently?
Can the object be updated?
Can it be deleted?
Can historical records still reference it after removal?
```

For nested structures, preserve the protocol hierarchy.

Example:

```text
Location
  └── EVSE[]
        └── Connector[]
```

Do not flatten this hierarchy merely because the relational schema makes flattening convenient.

For synchronization, retain enough information to determine:

```text
external object identity
source party
tenant
protocol version
last_updated
current synchronization state
```

## DTO / Domain / Persistence Separation

Protocol DTOs represent the wire contract.

Domain models represent business meaning.

Persistence entities represent storage.

These are different responsibilities:

```text
OCPI DTO
    |
    | validate / deserialize
    v
Application command
    |
    v
Domain model
    |
    v
Persistence entity
```

For outbound synchronization:

```text
Persistence/domain state
    |
    v
OCPI mapper
    |
    v
OCPI DTO
    |
    v
JSON
```

Do not expose JPA annotations, lazy-loading behavior, database identifiers, internal tenant fields, or implementation-only properties directly through the OCPI API.

## Sender / Receiver Interface Generation

An OCPI module normally has two perspectives:

```text
Sender interface
    -> endpoints used to read the sender's data

Receiver interface
    -> endpoints exposed by the receiver so the sender can push data
```

Before implementing an endpoint, determine which side the application represents.

For example:

```text
CPO
  |
  | Locations
  v
eMSP
```

The CPO needs its Sender interface for Locations.

The eMSP needs its Receiver interface for Locations.

Do not implement an endpoint merely because its path "looks RESTful". Derive it from the module's Sender/Receiver contract.

## Pull, Push, and Reconciliation

For modules supporting synchronization, implement the complete lifecycle rather than only the happy-path POST/PUT endpoint:

```text
Initial synchronization
    ->
Paginated pull
    ->
Persist external state
    ->
Incremental push
    ->
last_updated comparison
    ->
Retry/idempotency
    ->
Reconciliation after outage
```

A receiver must remain capable of reconstructing its state after:

```text
downtime
missed callbacks
duplicate callbacks
out-of-order updates
partial synchronization
application restart
partner retry
```

Do not assume that push delivery alone is sufficient.

## OCPI Response Envelope

OCPI responses are protocol responses, not arbitrary framework responses.

Implement a dedicated protocol response abstraction where appropriate:

```text
{
  "status_code": ...,
  "status_message": ...,
  "timestamp": ...,
  "data": ...
}
```

Use the exact envelope and field requirements of the selected OCPI version/reference.

Do not return a framework-specific response such as:

```json
{
  "success": true,
  "result": {}
}
```

unless the protocol explicitly requires that representation.

## Version-Specific Implementation

The same conceptual entity may differ between OCPI versions.

Never create a single "universal" DTO by blindly unioning every field from every version.

Prefer one of these patterns according to project architecture:

```text
Version-specific DTOs
        |
        v
Common domain model
```

or:

```text
Common DTO
    +
version-aware serialization/validation
```

The choice is an implementation decision, but the wire contract must remain version-correct.

When a field, enum, endpoint, or module exists only in a particular version:

```text
Do not expose it in an older-version contract.
Do not silently reinterpret it.
Do not silently drop it if doing so changes semantics.
```

For version migrations, use:

```text
2.1.1
  ->
semantic mapping
  ->
2.2.1
  ->
semantic mapping
  ->
2.3.0
```

rather than mechanical field/message renaming.

## OCPI HTTP Client Rules

For outbound OCPI integrations, model the remote platform as an unreliable external system.

Every client implementation should explicitly consider:

```text
connection timeout
read timeout
TLS validation
authentication
credential rotation
HTTP status handling
OCPI status_code handling
retry policy
retryable vs non-retryable errors
idempotency
rate limiting
pagination
response validation
malformed payloads
remote 5xx
remote 4xx
partner outage
```

Never treat:

```text
HTTP 200
```

as sufficient evidence that the OCPI business operation succeeded.

Inspect the OCPI response envelope and module-specific result semantics.

## OCPI Controller Rules

Controllers should remain protocol adapters.

Prefer:

```text
HTTP request
    ->
authentication
    ->
deserialization
    ->
protocol validation
    ->
application service
    ->
domain operation
    ->
protocol response
```

Avoid:

```text
HTTP request
    ->
JPA repository
    ->
database entity
    ->
HTTP response
```

Controllers should not contain tariff calculation, charging-session state machines, partner routing, CDR billing logic, or OCPP command orchestration.

## OCPI Persistence Rules

Persist protocol state when it is needed for:

```text
reconciliation
idempotency
retry
audit
history
cross-process asynchronous operations
partner synchronization
```

For important external objects, consider storing:

```text
internal_id
tenant_id
protocol
protocol_version
country_code
party_id
external_id
parent_external_id
last_updated
source/owner
synchronization status
created_at
updated_at
```

Use constraints/indexes appropriate to the protocol identity.

For example, an external object identity may require uniqueness across:

```text
tenant + protocol + version + country_code + party_id + external_id
```

Do not assume that `external_id` alone is globally unique.

## OCPI Enum Rules

Enums are part of the wire contract.

When implementing an enum:

```text
1. Verify the exact OCPI version.
2. Read the module reference.
3. Confirm the official specification when normative accuracy matters.
4. Preserve unknown values safely where interoperability requires forward compatibility.
5. Do not rename wire values merely to match language conventions.
```

For Java, a wire enum should not rely on `Enum.name()` unless that is intentionally identical to the protocol value.

Prefer explicit serialization mapping where needed:

```java
enum TokenType {
    RFID("RFID"),
    APP_USER("APP_USER"),
    OTHER("OTHER");

    private final String wireValue;
}
```

The same principle applies to C#, Kotlin, Swift, and other languages.

## OCPI Date/Time Rules

OCPI timestamps are protocol data.

Use timezone-aware date/time types and preserve the instant accurately.

Prefer:

```text
UTC internally
OffsetDateTime / Instant where appropriate
explicit JSON serialization
```

Do not use local server time as protocol time.

When time-based tariffs, sessions, reservations, or synchronization are involved, explicitly account for:

```text
timezone
DST
start/end boundaries
clock skew
precision
inclusive/exclusive boundaries
```

## OCPI Module Implementation Checklist

Before declaring a module complete, verify:

```text
[ ] Correct OCPI version selected
[ ] README/reference inspected
[ ] Module reference inspected
[ ] Sender/Receiver roles identified
[ ] Data ownership identified
[ ] All protocol entities identified
[ ] Nested entities identified
[ ] Enums identified
[ ] Version-specific fields identified
[ ] Request DTOs implemented
[ ] Response DTOs implemented
[ ] Protocol envelope implemented
[ ] Endpoint paths verified
[ ] HTTP methods verified
[ ] Authentication implemented
[ ] Pagination implemented where required
[ ] Pull synchronization implemented where required
[ ] Push synchronization implemented where required
[ ] last_updated handled correctly
[ ] Idempotency handled
[ ] Retry behavior defined
[ ] Reconciliation/recovery defined
[ ] Domain mapping separated from protocol DTOs
[ ] Persistence identity separated from OCPI identity
[ ] Tenant isolation enforced
[ ] Protocol errors mapped correctly
[ ] Unknown/invalid input handled
[ ] Tests cover serialization
[ ] Tests cover protocol contract
[ ] Tests cover synchronization
[ ] Tests cover duplicates/retries
[ ] Tests cover version-specific behavior
[ ] Official specification checked for normative claims
```

## When the User Gives Existing Code

If the user asks to adapt existing code to OCPI:

```text
1. Inspect the existing package/module structure.
2. Identify the current protocol version.
3. Identify whether existing classes are DTOs, domain objects, or persistence entities.
4. Inspect the matching references/ocpi/*.md file.
5. Reuse existing architecture where it is sound.
6. Change only the layers necessary to satisfy the OCPI contract.
7. Do not duplicate an entity merely because the protocol has a similar name.
8. Explain any required breaking change.
9. Add or update tests around the wire contract.
```

If the existing implementation conflicts with the repository reference, explicitly state:

```text
Current implementation
Reference expectation
Required change
Reason
Compatibility impact
```

Do not silently normalize the code.

## OCPI Reference Priority

Use this priority order:

```text
1. Selected official OCPI specification
2. Repository reference: references/ocpi/*.md
3. Existing project architecture and conventions
4. Official partner/vendor documentation
5. General model knowledge
```

The repository reference is the primary implementation guide for this skill, but it does not override the official specification when the task requires a normative protocol claim or certification-level correctness.

If the repository reference and official specification disagree:

```text
identify the discrepancy
do not silently choose one
prefer the official specification for normative behavior
preserve the repository convention only where it is an implementation choice
```



# 6. OCPI Roles and Ownership

For every OCPI module, determine:

```text
Who is the sender?
Who is the receiver?
Who owns the object?
Who creates it?
Who modifies it?
Who consumes it?
How is it synchronized?
```

Do not infer ownership from the receiving database.

For example:

```text
CPO
 |
 | Locations
 v
eMSP
```

The eMSP stores a copy.

That does not make the eMSP the owner of the Location.

---

# 7. OCPI Credentials and Versions

The connection lifecycle must be treated as protocol configuration.

Conceptually:

```text
Party A
  |
  | credentials token
  v
Party B
  |
  | versions discovery
  v
Version endpoint
  |
  | credentials exchange
  v
Operational connection
```

Credentials are security-sensitive.

Never:

```text
log credentials
store credentials in source code
return credentials in error messages
place credentials in telemetry
```

Use appropriate secret storage.

---

# 8. OCPI Data Synchronization

OCPI integrations must support both initial synchronization and incremental synchronization.

Typical model:

```text
Initial synchronization
        |
        v
Pull existing objects
        |
        v
Persist state
        |
        v
Receive push updates
        |
        v
Maintain synchronized state
```

If the receiver goes offline:

```text
Receiver offline
      |
      v
Missed updates
      |
      v
Connection restored
      |
      v
Pull / reconciliation
      |
      v
Synchronized state
```

Do not assume that a receiver being offline means every event must be queued indefinitely.

The correct recovery mechanism depends on the protocol module and integration architecture.

---

# 9. OCPI Locations

Typical ownership:

```text
CPO -> Locations -> eMSP / NSP / NAP
```

Hierarchy:

```text
Location
  └── EVSE[]
        └── Connector[]
```

A Location represents a physical charging site.

An EVSE represents a charging supply unit.

A Connector represents a physical charging interface.

Dynamic operational state must be distinguished from static infrastructure information.

Examples of dynamic information include:

```text
AVAILABLE
CHARGING
BLOCKED
OUTOFORDER
PLANNED
REMOVED
RESERVED
UNKNOWN
```

Do not treat removal as equivalent to deleting historical data.

Historical Sessions and CDRs may still reference the infrastructure.

When synchronizing nested objects, respect the version-specific `last_updated` semantics.

---

# 10. OCPI Tokens and Authorization

Keep these concepts separate:

```text
Token identity
Token validity
Authorization request
Authorization result
Authorization reference
Charging session
```

A valid token does not necessarily mean:

```text
the charging attempt is authorized.
```

Authorization may depend on:

* roaming;
* location;
* EVSE;
* contract;
* token status;
* real-time authorization;
* offline authorization rules;
* CPO policy.

A robust implementation should be able to correlate:

```text
Token
  |
  v
Authorization
  |
  v
Authorization Reference
  |
  v
Session
  |
  v
CDR
```

---

# 11. OCPI Sessions

A Session represents charging activity.

Typical lifecycle:

```text
PENDING
   |
   v
ACTIVE
   |
   v
COMPLETED
```

The exact lifecycle must always be checked against the selected OCPI version.

A Session is not the same thing as a CDR.

A useful conceptual model is:

```text
Authorization
      |
      v
Charging Session
      |
      +---- meter / energy observations
      |
      +---- charging periods
      |
      v
Completed Session
      |
      v
CDR
```

Do not create billing conclusions from incomplete operational state.

A session may be active while:

```text
energy = 0
```

because:

* charging has not started;
* the vehicle paused charging;
* the station is waiting;
* a power limit is active;
* the vehicle is not drawing power;
* meter data has not yet arrived.

---

# 12. OCPI CDRs

CDRs are billing-oriented records.

Treat them as auditable financial data.

Important properties:

```text
immutable historical record
idempotent processing
traceable origin
reconcilable billing evidence
```

Do not silently mutate an already processed historical CDR.

When the protocol supports correction/credit mechanisms, use them instead.

A CDR can contain:

```text
authorization information
location snapshot
EVSE information
connector information
tariff snapshot
charging periods
energy
duration
parking time
costs
tax/VAT
signed data where applicable
```

Never calculate the final charge using only:

```text
energy × price
```

unless the applicable tariff explicitly has only that component.

---

# 13. OCPI Tariffs

Tariff calculation must consider the complete tariff model.

Potential dimensions include:

```text
FLAT
ENERGY
TIME
PARKING_TIME
```

A tariff may also contain:

```text
time restrictions
day restrictions
power restrictions
current restrictions
duration restrictions
profile/type
step size
minimum price
maximum price
tax/VAT
```

For a tariff engine, explicitly define:

```text
units
rounding
step boundaries
time boundaries
timezone
VAT handling
minimums
maximums
overlapping restrictions
multiple tariff elements
```

Use decimal-safe monetary arithmetic.

Do not use binary floating-point arithmetic for financial totals.

---

# 14. OCPI Commands

Commands are generally asynchronous operations.

Typical architecture:

```text
eMSP
  |
  | OCPI command
  v
CPO
  |
  | immediate protocol response
  v
eMSP

CPO
  |
  | downstream operation
  v
CSMS
  |
  | OCPP
  v
Charging Station
```

The initial response indicates the result of accepting/processing the command according to the protocol.

It does NOT necessarily mean:

```text
the EV started charging.
```

Remote start must be modeled as an operation.

Example:

```text
command received
      |
      v
validated
      |
      v
accepted/rejected
      |
      v
downstream OCPP operation
      |
      v
station result
      |
      v
charging event
      |
      v
session state updated
```

---

# 15. OCPI Charging Profiles

Charging profiles express charging constraints over time.

Do not confuse:

```text
requested charging limit
```

with:

```text
observed electrical power
```

A profile may be transformed by:

* CPO policy;
* station capabilities;
* site power limits;
* grid constraints;
* other active profiles;
* vehicle behavior;
* OCPP capabilities.

Therefore:

```text
Requested limit != guaranteed physical power
```

The implementation should define:

```text
profile lifetime
start time
duration
units
minimum charging rate
replacement/stacking behavior
conflicts
station support
failure behavior
```

---

# 16. OCPP

OCPP is the station-management protocol between charging stations and a CSMS.

Typical architecture:

```text
Charging Station
       |
     OCPP
       |
       v
      CSMS
```

Depending on version and configuration, transport may use WebSocket/JSON or legacy SOAP.

Always establish:

```text
OCPP version
transport
security profile
station identity
supported features
station capabilities
```

---

# 17. OCPP 1.6 vs OCPP 2.x

Do not treat OCPP 2.x as OCPP 1.6 with renamed messages.

OCPP 2.x introduces substantial semantic and architectural changes.

Conceptual differences include:

```text
OCPP 1.6
  transaction-oriented
  simpler connector model
  older configuration model

OCPP 2.x
  richer device model
  EVSE-aware architecture
  improved transaction model
  richer event model
  stronger security
  expanded smart charging
  richer device management
```

For migration work:

```text
OCPP 1.6 concept
      |
      v
OCPP 2.x concept
      |
      v
Semantic differences
      |
      v
Implementation changes
```

Never perform a simple message-name substitution.

---

# 18. OCPP Message Correlation

For JSON OCPP, protocol messages contain a message identifier.

Request/response correlation must use the protocol-defined identifier.

Conceptually:

```text
CSMS
  |
  | request(messageId)
  v
Station
  |
  | response(messageId)
  v
CSMS
```

Never correlate operations using timestamps alone.

Persist correlation state when an operation matters beyond the lifetime of a single process.

---

# 19. OCPP Connection Management

Charging stations are unreliable network clients.

Production systems must handle:

```text
disconnect
reconnect
station reboot
network partition
duplicate connection
stale WebSocket
heartbeat timeout
request timeout
delayed response
messages arriving after timeout
CSMS restart
reconnect storms
```

A conceptual lifecycle:

```text
DISCONNECTED
     |
     v
CONNECTING
     |
     v
CONNECTED
     |
     v
BOOTSTRAPPING
     |
     v
OPERATIONAL
     |
     v
DISCONNECTED
```

The exact protocol behavior depends on the OCPP version.

Do not invent protocol states that do not exist.

---

# 20. OCPP Operations

Separate:

```text
request
protocol response
physical operation
observed event
domain state
```

For example:

```text
CSMS requests remote start
        |
        v
Station accepts request
        |
        v
Charging attempt begins
        |
        v
Station reports transaction/event
        |
        v
Energy is observed
```

These are different facts.

Never interpret:

```text
OCPP request accepted
```

as:

```text
vehicle is charging
```

without the corresponding operational evidence.

---

# 21. OCPI ↔ OCPP Translation

A CPO commonly bridges both protocols.

The agent should reason through the complete chain.

## Remote start

```text
OCPI START_SESSION
        |
        v
CPO authorization
        |
        v
Resolve Location / EVSE / Connector
        |
        v
Create durable operation
        |
        v
OCPP remote-start operation
        |
        v
Charging Station
        |
        v
OCPP result/event
        |
        v
Update charging domain
        |
        v
OCPI response callback
```

## Remote stop

```text
OCPI STOP_SESSION
        |
        v
Find active charging session
        |
        v
OCPP stop operation
        |
        v
Charging Station
        |
        v
Stop event/result
        |
        v
Finalize session
        |
        v
Generate CDR when appropriate
```

## Smart charging

```text
OCPI charging constraint
        |
        v
CPO policy
        |
        v
Site constraints
        |
        v
OCPP charging profile
        |
        v
Charging Station
        |
        v
Meter/status observations
```

---

# 22. State Machines

Charging software is fundamentally stateful.

Do not represent all state with one status field.

Separate at least:

```text
Connectivity state
Protocol state
Station state
EVSE state
Connector state
Authorization state
Charging transaction state
Session state
Billing state
Synchronization state
Command/operation state
```

For example:

```text
Station connected
    !=
EVSE available
    !=
authorization accepted
    !=
charging started
    !=
energy being delivered
    !=
session completed
    !=
CDR accepted
```

These facts may change independently.

---

# 23. Distributed Systems

Treat charging infrastructure as a distributed system.

Assume:

```text
messages can be duplicated
messages can be delayed
messages can arrive out of order
connections can disappear
remote systems can restart
callbacks can be retried
stations can reboot
clocks can differ
databases can temporarily disagree
```

Design for these conditions rather than treating them as exceptional.

Every important integration should consider:

```text
timeout
retry
duplicate
ordering
reconciliation
recovery
idempotency
expiration
```

---

# 24. Idempotency

Assume external systems retry.

Handlers must therefore be designed so that duplicate delivery does not produce duplicate business effects.

Potential idempotency keys include:

```text
protocol object identity
OCPP message ID
external operation ID
source + object ID
protocol-defined sequence/version
```

Do not rely exclusively on HTTP method semantics.

A `POST` can still require application-level idempotency.

---

# 25. Ordering

Network order is not necessarily business-event order.

Do not assume:

```text
message received later
=
event happened later
```

When ordering matters, use the protocol's available:

* timestamps;
* sequence numbers;
* transaction identifiers;
* counters;
* persistent event ordering;
* domain reconciliation.

If the protocol cannot guarantee ordering, the application must define its own consistency strategy.

---

# 26. Offline and Recovery Behavior

For every external connection ask:

```text
What happens if it is offline for 10 seconds?
What happens if it is offline for 10 minutes?
What happens if it is offline for 24 hours?
What happens after restart?
What state is authoritative?
How is missing data recovered?
```

Do not build a queue simply because it is technically possible.

Use protocol-defined synchronization mechanisms where available.

For important domain state, maintain durable reconciliation information.

---

# 27. Multi-Tenant Architecture

Charging platforms are frequently multi-tenant.

Model external protocol identity separately from internal identity.

Conceptually:

```text
Tenant
  |
  +-- Party
  |     |
  |     +-- country_code
  |     +-- party_id
  |     +-- role
  |
  +-- Connections
  |
  +-- Locations
  |
  +-- EVSEs
  |
  +-- Sessions
  |
  +-- CDRs
```

Do not assume:

```text
external protocol ID == internal database ID
```

Prefer:

```text
internal UUID
external ID
protocol
protocol version
party identity
tenant
```

Tenant isolation is a security boundary.

Never allow:

```text
tenant A -> tenant B protocol data
```

through identifiers supplied by the client without authorization checks.

---

# 28. Security

For every charging integration, evaluate:

```text
TLS
certificate validation
authentication
credential rotation
authorization
secret storage
token expiration
request authenticity
replay protection
tenant isolation
rate limiting
input validation
logging
auditability
```

Remote charging commands are security-sensitive.

Authorization must happen before executing operations such as:

```text
remote start
remote stop
unlock connector
reservation
charging-profile modification
station configuration
firmware operations
```

Never recommend:

```text
disable TLS verification
accept every certificate
store secrets in source code
log Authorization headers
```

as a production solution.

---

# 29. Units and Measurements

Electric-mobility software is full of unit-conversion bugs.

Always identify the unit explicitly.

Common dimensions include:

```text
Energy       kWh / Wh
Power        kW / W
Voltage      V
Current      A
Duration     seconds / hours
Energy price €/kWh
Time price   €/hour
```

Never silently convert units.

For example:

```text
11 kW
!=
11 W
```

and:

```text
22 kWh
!=
22 kW
```

For energy and power calculations, make units explicit in variable names, DTOs, or domain types where practical.

---

# 30. Money and Billing

Never use binary floating-point as the authoritative representation of money.

Prefer:

```text
Decimal
BigDecimal
minor currency units
```

depending on the architecture.

Separate:

```text
energy measurement
tariff calculation
tax calculation
billing amount
settlement amount
```

Do not assume that:

```text
CDR total cost
=
energy × tariff
```

because tariffs can contain:

```text
flat fees
energy fees
time fees
parking fees
minimum prices
maximum prices
taxes
restrictions
different billing dimensions
```

---

# 31. Testing

Protocol testing must go beyond serialization tests.

## Contract tests

Verify:

```text
HTTP method
URL
headers
authentication
schema
required fields
optional fields
enum values
response envelope
pagination
callbacks
version discovery
```

## State-machine tests

Test:

```text
valid transition
invalid transition
duplicate event
out-of-order event
timeout
retry
reconnect
restart
offline station
remote rejection
```

## Integration tests

At minimum test realistic flows:

```text
authorization
    ->
start
    ->
charging
    ->
meter updates
    ->
stop
    ->
session completion
    ->
CDR
```

And cross-protocol:

```text
OCPI command
    ->
CPO
    ->
OCPP
    ->
Charging Station
    ->
OCPP event/result
    ->
CPO
    ->
OCPI callback
```

## Invariants

Useful invariants include:

```text
energy >= 0

completed session
cannot silently become active

duplicate CDR
cannot create duplicate billing

duplicate callback
cannot create duplicate business effect

tenant A
cannot access tenant B

unknown station
cannot become operational merely because a message was received

accepted remote-start command
does not imply charging has started
```

---

# 32. Debugging Workflow

When debugging an interoperability problem, collect evidence in this order:

```text
1. Protocol
2. Version
3. Actor roles
4. Connection topology
5. Authentication
6. Raw request
7. Raw response
8. Payload
9. Correlation/message ID
10. UTC timestamps
11. Station connectivity
12. Domain state
13. Database state
14. Synchronization state
15. Retry history
16. Vendor-specific behavior
```

Redact secrets before inspecting or sharing logs.

Classify the problem:

```text
transport
authentication
authorization
schema
protocol semantics
state machine
business logic
synchronization
vendor interoperability
infrastructure
```

Do not conclude:

```text
HTTP 500 = protocol problem
WebSocket disconnected = OCPP problem
session active = vehicle charging
```

without evidence.

---

# 33. Observability

Protocol integrations should expose enough telemetry to reconstruct an operation.

Useful fields:

```text
tenant_id
party_id
protocol
protocol_version
operation_id
correlation_id
message_id
station_id
evse_id
connector_id
session_id
external_object_id
timestamp
attempt
duration
result
error_class
```

Never include secrets.

For OCPP WebSocket systems, make it possible to answer:

```text
Which station was connected?
Which operation was sent?
When was it sent?
What message ID was used?
Did the station respond?
What did it respond?
What event followed?
What domain state changed?
```

---

# 34. Architecture Guidance

Prefer clear boundaries:

```text
Protocol Adapter
      |
      v
Application Service
      |
      v
Domain Model
      |
      v
Persistence
```

Avoid coupling protocol DTOs directly to internal domain entities.

Prefer:

```text
OCPI DTO
    ->
application command
    ->
domain operation
```

rather than:

```text
OCPI JSON
    ->
database entity
```

The same applies to OCPP.

Protocol adapters should handle:

```text
serialization
validation
authentication
protocol-specific errors
transport
correlation
```

Domain services should handle:

```text
business rules
state transitions
authorization decisions
billing
charging operations
```

---

# 35. WebSocket and Fleet Architecture

A CSMS may maintain a large number of simultaneous station connections.

Do not assume:

```text
one WebSocket
=
one server process
```

For horizontally scaled systems, explicitly design:

```text
station -> owning connection instance
```

and:

```text
CSMS command
    ->
locate station connection
    ->
route command to connection owner
```

Possible infrastructure patterns include:

```text
sticky routing
connection registry
distributed session registry
message broker
pub/sub
partitioning
```

Choose according to scale and operational requirements.

Do not introduce Kafka, Redis, queues, or another distributed system merely because it is popular. State the problem the infrastructure solves.

---

# 36. Vendor Interoperability

Real-world charging stations often contain vendor-specific behavior.

When behavior differs from the protocol:

```text
Standard:
  ...

Vendor behavior:
  ...

Required workaround:
  ...

Risk:
  ...
```

Never silently encode vendor behavior as standard behavior.

Prefer isolated compatibility layers:

```text
Standard Protocol
      |
      v
Compatibility Layer
      |
      +---- Vendor A
      +---- Vendor B
      +---- Vendor C
```

This prevents vendor-specific assumptions from contaminating the core domain model.

---

# 37. Implementation Rules

When generating code:

1. Match the user's existing language and framework.
2. Do not introduce a new framework without justification.
3. Keep protocol DTOs separate from domain entities.
4. Validate at protocol boundaries.
5. Use explicit timeouts.
6. Use UTC for protocol timestamps.
7. Preserve correlation IDs.
8. Make external operations observable.
9. Make retry behavior explicit.
10. Make idempotency explicit.
11. Avoid blocking WebSocket event loops.
12. Keep vendor-specific logic isolated.
13. Use decimal-safe money calculations.
14. Use explicit units.
15. Persist important asynchronous operations.
16. Do not hide protocol errors behind generic exceptions.

For Java/Spring:

```text
Controller / WebClient / WebSocket adapter
        |
        v
Protocol DTO
        |
        v
Application service
        |
        v
Domain model
        |
        v
Repository
```

For high-volume OCPP systems, carefully design WebSocket connection ownership and command routing before introducing horizontal scaling.

---

# 38. Agent Response Behavior

## Architecture questions

Answer in this order:

```text
Protocol boundary
Actors
Ownership
Data flow
State
Failure handling
Persistence
Security
Implementation recommendation
```

## Implementation questions

Answer in this order:

```text
Version assumptions
Protocol operation
Message/endpoint mapping
Implementation
Error handling
Timeouts
Idempotency
Tests
Interoperability caveats
```

## Debugging questions

Answer in this order:

```text
Failure classification
Evidence
Concrete checks
Likely causes
Fix
Regression test
```

## Protocol questions

Start with the smallest useful conceptual model.

Then explain:

```text
roles
lifecycle
messages
ownership
state
edge cases
```

Do not overwhelm a simple question with every protocol module.

---

# 39. When to Verify External Documentation

The agent should verify external documentation when:

* the exact protocol version matters;
* an enum value is being implemented;
* an endpoint is being implemented;
* a message schema is being generated;
* behavior differs between versions;
* certification compliance matters;
* a recent specification change may affect the answer;
* a vendor-specific behavior is being asserted.

Preferred source hierarchy:

```text
1. Official protocol specification
2. Official certification/test documentation
3. Official migration guides
4. Official vendor documentation
5. Interoperability reports
6. Community sources
7. Model knowledge
```

Useful official sources:

* OCPI: [https://ocpi-protocol.com/](https://ocpi-protocol.com/)
* Open Charge Alliance: [https://openchargealliance.org/](https://openchargealliance.org/)

Do not use a blog post as the authoritative source for a normative protocol rule when the specification is available.

---

# 40. Example Reasoning: Remote Start

User asks:

> Implement remote start.

The agent should reason:

```text
1. Which OCPI version?
2. Is the requester an eMSP?
3. Is the receiver a CPO?
4. Which Location / EVSE / Connector?
5. Is the Token valid?
6. Does the CPO authorize the operation?
7. Is the station online?
8. Which OCPP version does the station use?
9. What OCPP operation maps to this request?
10. How is the operation correlated?
11. What happens if the station rejects it?
12. What happens if the station times out?
13. What happens if the response arrives after timeout?
14. What event proves charging actually started?
15. How is the OCPI response callback generated?
16. What tests cover duplicate/retry/offline cases?
```

Incorrect implementation:

```text
OCPI START_SESSION
    ->
OCPP remote start
    ->
return success
```

Correct conceptual implementation:

```text
OCPI START_SESSION
    ->
validate
    ->
create operation
    ->
return protocol-defined immediate result
    ->
execute OCPP operation
    ->
receive OCPP result/event
    ->
update domain state
    ->
notify OCPI response URL
```

---

# 41. Example Reasoning: Session ACTIVE but 0 kWh

Do not immediately conclude that the session is broken.

Inspect:

```text
OCPI session state
OCPP transaction state
station state
EVSE state
connector state
meter values
authorization
charging profile
vehicle behavior
station connectivity
```

Possible explanation:

```text
Session active
+
vehicle connected
+
charging paused
+
0 kWh observed
```

This can be valid depending on the system state.

---

# 42. Example Reasoning: OCPI vs OCPP

If asked:

> Can OCPI control my charger?

Answer conceptually:

```text
Driver / eMSP
       |
      OCPI
       |
      CPO
       |
      CSMS
       |
      OCPP
       |
Charging Station
```

OCPI is the backend interoperability layer.

OCPP is the charging-station management layer.

The CPO/CSMS is responsible for translating business-level operations into station-level protocol operations.

---

# 43. Quality Gate

Before finalizing any electric-mobility implementation or technical answer, verify:

```text
[ ] Protocol identified
[ ] Version identified
[ ] Actor roles identified
[ ] Data ownership identified
[ ] OCPI/OCPP boundary correct
[ ] State transitions valid
[ ] Async operations treated as async
[ ] Correlation strategy defined
[ ] Retry behavior considered
[ ] Idempotency considered
[ ] Ordering considered
[ ] Offline/recovery considered
[ ] Security considered
[ ] Secrets protected
[ ] Units explicit
[ ] Monetary precision correct
[ ] Billing semantics correct
[ ] Vendor behavior separated from standard behavior
[ ] Tests defined
[ ] Current specification verified when necessary
```

If one of these items materially affects correctness and cannot be determined, state the uncertainty rather than inventing an answer.

---

# 44. Final Principle

Electric-mobility software is not merely an HTTP API plus a WebSocket.

It is a distributed system connecting:

```text
driver
eMSP
roaming network
CPO
CSMS
charging station
EVSE
connector
vehicle
energy infrastructure
billing systems
```

The protocols describe interoperability between these systems, but production correctness comes from understanding:

```text
ownership
identity
state
time
energy
authorization
billing
asynchrony
failure
security
```

The agent should therefore prefer:

```text
correct reasoning
    >
protocol memorization
```

and:

```text
verified specification
    >
assumption
```

and:

```text
explicit uncertainty
    >
invented protocol behavior
```

The goal is to produce software that interoperates with real charging infrastructure, not merely software that looks correct in a code review.


