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

# Electric Mobility — Agent

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


# 43. Universal Electric Mobility Skill Specification

## 43.1. Domain Architecture & Protocol Coverage

This is example of how to codifies end-to-end standards across the three core tiers of EV charging software:

* **Protocol Engine (Domain Core)**: OCPP 1.6-J, 2.0.1, 2.1 JSON RPC over WebSockets, OCPI 2.2.1 / 3.0 eMSP/CPO roaming REST modules, and ISO 15118-2/-20 Plug & Charge PKI protocols.
* **Backend Platform (C# / .NET 9+)**: High-throughput ASP.NET Core CSMS connection pool, background WebSocket dispatchers, and zero-allocation JSON DTOs (`System.Text.Json`).
* **Mobile Platforms (Android & iOS)**: Reactive charging dashboards, live energy delivery telemetry, marker clustering, and background session tracking via Jetpack Compose and SwiftUI + ActivityKit.

---

## 43.2. Cross-Protocol State Machine Matrix

All backend engines and client UIs MUST resolve charger states using this deterministic state mapping:

| Target Standard State | OCPP 1.6-J | OCPP 2.0.1 / 2.1 | OCPI 2.2.1 | Mobile UI Mapping & Accent Token |
| :--- | :--- | :--- | :--- | :--- |
| **Available** | `Available` | `Available` | `AVAILABLE` | Green (`#00C853`) / Ready for Tap |
| **Preparing** | `Preparing` | `Occupied` | `OCCUPIED` | Amber (`#FFB300`) / Cable Plugged |
| **Charging** | `Charging` | `Occupied` | `CHARGING` | Primary Blue (`#007AFF`) / Pulse Gauge |
| **Suspended EV/EVSE** | `SuspendedEV` | `Occupied` | `SUSPENDED_EV` | Warning Orange (`#FF6D00`) / Check Car |
| **Finishing** | `Finishing` | `Occupied` | `FINISHING` | Slate Gray (`#78909C`) / Session Ending |
| **Faulted / Inoperative**| `Faulted` | `Faulted` | `INOPERATIVE` | Red (`#D32F2F`) / Alert Badge |

---

## 43.3. Platform Blueprints & Implementation Patterns

### 43.3.A. C# ASP.NET Core CSMS Engine (`platform-csharp`)
* **Rule 1**: WebSockets must stream frame arrays `[MessageTypeId, MessageId, Action, Payload]`.
* **Rule 2**: Enforce UTC millisecond precision for all telemetry (`YYYY-MM-DDTHH:mm:ss.sssZ`).
* **Rule 3**: Use `System.Text.Json` Source Generators for low-allocation RPC frame dispatch.

```csharp
using System.Net.WebSockets;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.AspNetCore.Http;

namespace Mobility.CSMS.Core;

public record OcppCall(int MessageType, string MessageId, string Action, JsonElement Payload);

public class OcppWebSocketDispatcher
{
    public async Task ProcessConnectionAsync(string stationId, WebSocket socket, CancellationToken ct)
    {
        var buffer = new byte[1024 * 8];
        
        while (socket.State == WebSocketState.Open && !ct.IsCancellationRequested)
        {
            var result = await socket.ReceiveAsync(new ArraySegment<byte>(buffer), ct);
            if (result.MessageType == WebSocketMessageType.Close) break;

            var rawJson = Encoding.UTF8.GetString(buffer, 0, result.Count);
            byte[] responseFrame = DispatchFrame(rawJson);
            
            if (responseFrame.Length > 0)
            {
                await socket.SendAsync(responseFrame, WebSocketMessageType.Text, true, ct);
            }
        }
    }

    private byte[] DispatchFrame(string rawJson)
    {
        using var doc = JsonDocument.Parse(rawJson);
        var root = doc.RootElement;
        
        int msgType = root[0].GetInt32();
        string msgId = root[1].GetString()!;

        if (msgType == 2) // CALL
        {
            string action = root[2].GetString()!;
            var payload = root[3];

            object responsePayload = action switch
            {
                "BootNotification" => new { status = "Accepted", currentTime = DateTime.UtcNow.ToString("o"), interval = 300 },
                "Heartbeat" => new { currentTime = DateTime.UtcNow.ToString("o") },
                "StatusNotification" => new { },
                "TransactionEvent" => new { totalCost = 0.00 },
                _ => new { errorCode = "NotSupported" }
            };

            var rpcResponse = new object[] { 3, msgId, responsePayload };
            return JsonSerializer.SerializeToUtf8Bytes(rpcResponse, OcppJsonContext.Default.ObjectArray);
        }
        return Array.Empty<byte>();
    }
}

[JsonSerializable(typeof(object[]))]
public partial class OcppJsonContext : JsonSerializerContext { }

```

### 43.3.B. Android Jetpack Compose EV Client (`platform-android`)

* **Rule 1**: UI states must be exposed via `StateFlow` inside ViewModel with Unidirectional Data Flow (UDF).
* **Rule 2**: Charge rate (kW) and battery state-of-charge (SoC %) must render with animated gauges.

```kotlin
package com.mobility.charging.ui

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

data class SessionState(
    val stationName: String = "FastCharge Point #01",
    val powerKw: Double = 0.0,
    val socPercent: Int = 0,
    val isCharging: Boolean = false
)

class ChargingViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(SessionState())
    val uiState: StateFlow<SessionState> = _uiState

    fun updateTelemetry(power: Double, soc: Int) {
        _uiState.value = _uiState.value.copy(powerKw = power, socPercent = soc, isCharging = true)
    }
}

@Composable
fun ChargingDashboard(viewModel: ChargingViewModel) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    
    Column(
        modifier = Modifier.fillMaxSize().padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.SpaceBetween
    ) {
        Text(text = state.stationName, style = MaterialTheme.typography.titleLarge)
        
        Box(contentAlignment = Alignment.Center, modifier = Modifier.size(220.dp)) {
            val animProgress by animateFloatAsState(
                targetValue = state.socPercent / 100f,
                animationSpec = tween(600), label = "soc"
            )
            Canvas(modifier = Modifier.fillMaxSize()) {
                drawArc(Color.LightGray.copy(alpha = 0.3f), 135f, 270f, false, style = Stroke(18.dp.toPx(), cap = StrokeCap.Round))
                drawArc(Color(0xFF00C853), 135f, 270f * animProgress, false, style = Stroke(18.dp.toPx(), cap = StrokeCap.Round))
            }
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text(text = "${state.socPercent}%", style = MaterialTheme.typography.headlineLarge)
                Text(text = "${state.powerKw} kW", style = MaterialTheme.typography.bodyLarge, color = Color.Gray)
            }
        }
        
        Button(
            onClick = { /* Stop Charging */ },
            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error),
            modifier = Modifier.fillMaxWidth().height(52.dp)
        ) {
            Text("Stop Session")
        }
    }
}

```

### 43.3.C. iOS SwiftUI & ActivityKit Client (`platform-ios`)

* **Rule 1**: State objects must leverage Swift 6 `@Observable` macro architecture.
* **Rule 2**: Support Live Activities via `ActivityKit` for Dynamic Island session updates during app backgrounding.

```swift
import SwiftUI
import ActivityKit

@Observable
@MainActor
public final class EVSessionModel {
    public private(set) var powerKw: Double = 0.0
    public private(set) var socPercent: Int = 0
    public private(set) var activeSessionId: String? = nil
    
    public init() {}
    
    public func update(power: Double, soc: Int, sessionId: String) {
        self.powerKw = power
        self.socPercent = soc
        self.activeSessionId = sessionId
    }
}

public struct EVChargingView: View {
    @State private var model = EVSessionModel()
    
    public init() {}
    
    public var body: some View {
        VStack(spacing: 28) {
            Text("DC Fast Charger - Bay A")
                .font(.headline)
                .foregroundStyle(.secondary)
            
            Gauge(value: Double(model.socPercent), in: 0...100) {
                Text("Battery Level")
            } currentValueLabel: {
                Text("\(model.socPercent)%")
                    .font(.title)
                    .bold()
            }
            .gaugeStyle(.accessoryCircular)
            .tint(.green)
            .scaleEffect(1.6)
            .padding(.vertical, 24)
            
            Text(String(format: "%.1f kW", model.powerKw))
                .font(.system(.title, design: .monospaced))
                .bold()
            
            Button(role: .destructive) {
                // Terminate session
            } label: {
                Text("End Session")
                    .frame(maxWidth: .infinity)
                    .padding()
            }
            .buttonStyle(.borderedProminent)
        }
        .padding(24)
        .onAppear {
            model.update(power: 120.0, soc: 58, sessionId: "SESS-789")
        }
    }
}

```

---

## 43.4. Decision Matrix & Error Handling Rules

1. **Protocol Mismatch Rules**:
* If an incoming OCPP message violates schema format, return `FormationViolation` (Error Code `4`).
* If an OCPI token authorization fails, respond with OCPI status code `2001` (`Invalid Token`) with HTTP `200 OK`.


2. **Reconnection Strategy**:
* Client applications (Compose / SwiftUI) must implement exponential backoff reconnection for WebSockets: initial delay $1.0\,s$, backoff multiplier $2.0$, maximum delay $60.0\,s$.


3. **Data Precision**:
* Store all billing energy metrics in Watt-Hours ($Wh$) internally. Convert to kilowatt-hours ($kWh$) rounded to 2 decimal places strictly for UI display.

# 44. RFID Card Authorization & Consolidated Billing Skill

This is only if the project does required a single invoice for the whole system. It's an example of how to handle one single rfid card to authenticate in a platform of an IoT ecosystem.

## 44.1. Architecture & Unified Billing Domain Model

To ensure a user receives **one single invoice** regardless of which physical RFID card, key fob, or vehicle-linked tag they tap, the system maps multiple hardware RFID UIDs to a single internal `UserAccount` entity.


```

+-------------------------------------------------------+
|                 User Account (User ID)                |
|  - Unified Wallet Balance                             |
|  - Single Monthly Invoice / Ledger                    |
+-------------------------------------------------------+
|
+---------------+---------------+
| 1:N                           | 1:N
+--------------------+           +--------------------+
|  RFID Token #1     |           |  RFID Token #2     |
|  UID: "A1B2C3D4"   |           |  UID: "E5F67890"   |
|  Type: ISO14443    |           |  Type: MifareDes   |
+--------------------+           +--------------------+
|                               |
+---------------+---------------+
|
v
+-------------------------------------+
|  OCPP / OCPI Authorization Engine   |
|  - Resolves UID -> Token -> User    |
|  - Checks Status (Accepted/Blocked) |
|  - Routes CDR to User Account       |
+-------------------------------------+

```

---

## 44.2. Hardware UID Normalization Protocol

RFID readers (e.g., ISO 14443 Type A/B, Mifare Classic, DESFire, Legic) report byte sequences differently depending on endianness. The CSMS and charging station MUST normalize all RFID bytes before database lookup or OCPP dispatch.

### UID Format Standards Matrix
| RFID Card Type | Raw Byte Length | Hardware Reader Output Format | Standardized OCPP `idToken` |
| :--- | :--- | :--- | :--- |
| **Mifare Classic 1K/4K** | 4 Bytes (32-bit UID) | Hex String (Big Endian) | `A1B2C3D4` |
| **Mifare DESFire / EV1** | 7 Bytes (56-bit UID) | Hex String Uppercase | `04A1B2C3D4E5F6` |
| **ISO 15693 / Vicinity** | 8 Bytes (64-bit UID) | Reversed Hex / Swapped Bytes | Normalized Big Endian Hex |
| **OCPI Token Visual ID** | Printed Text | Alphanumeric (Formatted) | `FR-CPO-c12345` |

---

## 44.3. OCPP 1.6-J & 2.0.1 Authorization Handshakes

### Flow: Station RFID Tap to Unified Session


```

[EV Driver]            [EVSE / Charger]               [CSMS Core System]             [Billing Ledger]
|                        |                                |                            |
|-- Tap RFID Card ------>|                                |                            |
|                        |-- Authorize.req(idToken) ----->|                            |
|                        |   Type: ISO14443               |                            |
|                        |                                |-- Resolve UID to User ---->|
|                        |                                |   Check Balance / Status   |
|                        |<-- Authorize.conf(Accepted) ---|<-- Return User Account OK -|
|                        |                                |                            |
|-- Connect Cable ------>|                                |                            |
|                        |-- TransactionEvent(Started) -->|                            |
|                        |                                |-- Attach Tx to User Account|
|                        |                                |                            |
|-- Tap RFID Card Stop ->|                                |                            |
|                        |-- TransactionEvent(Ended) ---->|                            |
|                        |                                |-- Create CDR ------------->|
|                        |                                |   Add to Monthly Invoice   |

```

---

## 44.4. Backend Implementation Patterns (C# ASP.NET Core)

### 44.4.A. RFID Authorization & Billing Resolver Service

```csharp
namespace Mobility.Domain.Services;

public record RfidAuthRequest(string RawUid, string StationId, int EvseId, string TokenType = "ISO14443");
public record RfidAuthResponse(bool IsAuthorized, string IdTokenStatus, Guid? UserAccountId, string? FailureReason);

public interface IRfidAuthorizationService
{
    Task<RfidAuthResponse> AuthorizeTapAsync(RfidAuthRequest request, CancellationToken ct);
}

public class RfidAuthorizationService : IRfidAuthorizationService
{
    private readonly ITokenRepository _tokenRepository;
    private readonly IUserAccountRepository _userRepository;

    public RfidAuthorizationService(ITokenRepository tokenRepository, IUserAccountRepository userRepository)
    {
        _tokenRepository = tokenRepository;
        _userRepository = userRepository;
    }

    public async Task<RfidAuthResponse> AuthorizeTapAsync(RfidAuthRequest request, CancellationToken ct)
    {
        // 1. Normalize UID Format (Uppercase Hex String without delimiters)
        string normalizedUid = NormalizeRfidUid(request.RawUid);

        // 2. Fetch Token Entity
        var token = await _tokenRepository.FindByUidAsync(normalizedUid, ct);
        if (token == null)
        {
            return new RfidAuthResponse(false, "Unknown", null, "RFID card not registered in system");
        }

        if (!token.IsActive || token.IsBlocked)
        {
            return new RfidAuthResponse(false, "Blocked", token.UserAccountId, "RFID card has been deactivated");
        }

        // 3. Resolve User Account
        var userAccount = await _userRepository.GetByIdAsync(token.UserAccountId, ct);
        if (userAccount == null || !userAccount.CanStartSession(out var reason))
        {
            return new RfidAuthResponse(false, "Invalid", token.UserAccountId, reason ?? "User account suspended");
        }

        // 4. Return Authorized Response linked to single User Account
        return new RfidAuthResponse(true, "Accepted", userAccount.Id, null);
    }

    private static string NormalizeRfidUid(string rawUid)
    {
        return rawUid.Replace(":", "").Replace("-", "").Replace(" ", "").Trim().ToUpperInvariant();
    }
}

```

### 44.4.B. Single Ledger CDR Routing Engine

```csharp
namespace Mobility.Domain.Billing;

public class ChargingTransactionBillingEngine
{
    private readonly IBillingLedgerRepository _ledgerRepository;

    public ChargingTransactionBillingEngine(IBillingLedgerRepository ledgerRepository)
    {
        _ledgerRepository = ledgerRepository;
    }

    public async Task ProcessCompletedTransactionAsync(Guid userAccountId, string rfidUid, double totalKwh, decimal cost, CancellationToken ct)
    {
        // All transactions, regardless of RFID UID, route directly to the single user ledger
        var ledgerEntry = new LedgerEntry
        {
            Id = Guid.NewGuid(),
            UserAccountId = userAccountId,
            UsedRfidUid = rfidUid,
            EnergyDeliveredKwh = totalKwh,
            AmountDecimal = cost,
            Timestamp = DateTime.UtcNow,
            EntryType = LedgerEntryType.SessionCharge
        };

        await _ledgerRepository.AddEntryAsync(ledgerEntry, ct);
    }
}

```

---

## 44.5. Mobile UI Component Patterns (Managing Linked RFID Cards)

Users must be able to add, manage, and assign custom nicknames to multiple RFID cards under their single account.

### Android Jetpack Compose RFID Card Management

```kotlin
package com.mobility.charging.ui.rfid

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

data class RfidCardUiModel(
    val id: String,
    val uidMasked: String, // e.g., "**** A1B2"
    val cardNickname: String,
    val isActive: Boolean
)

@Composable
fun UserRfidCardsScreen(
    cards: List<RfidCardUiModel>,
    onToggleCardStatus: (String, Boolean) -> Unit
) {
    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Text("My Charging Badges & Cards", style = MaterialTheme.typography.titleLarge)
        Text("All cards are billed to your primary monthly invoice.", style = MaterialTheme.typography.bodyMedium)
        
        Spacer(modifier = Modifier.height(16.dp))
        
        LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            items(cards) { card ->
                Card(modifier = Modifier.fillMaxWidth()) {
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(16.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Text(text = card.cardNickname, style = MaterialTheme.typography.titleMedium)
                            Text(text = "UID: ${card.uidMasked}", style = MaterialTheme.typography.bodySmall)
                        }
                        Switch(
                            checked = card.isActive,
                            onCheckedChange = { isChecked -> onToggleCardStatus(card.id, isChecked) }
                        )
                    }
                }
            }
        }
    }
}

```

### iOS SwiftUI Linked RFID Badges View

```swift
import SwiftUI

public struct RfidBadgeViewModel: Identifiable {
    public let id: String
    public let nickname: String
    public let maskedUid: String
    public var isActive: Bool
}

public struct UserRfidBadgesView: View {
    @State private var badges: [RfidBadgeViewModel] = [
        RfidBadgeViewModel(id: "1", nickname: "Primary Key Fob", maskedUid: "•••• A1B2", isActive: true),
        RfidBadgeViewModel(id: "2", nickname: "Work Car Badge", maskedUid: "•••• E5F6", isActive: false)
    ]
    
    public var body: some View {
        List {
            Section(header: Text("Linked RFID Badges"), footer: Text("Sessions started with any enabled badge will automatically combine into your primary account invoice.")) {
                ForEach($badges) {$badge in
                    HStack {
                        VStack(alignment: .leading, spacing: 4) {
                            Text(badge.nickname)
                                .font(.headline)
                            Text(badge.maskedUid)
                                .font(.subheadline)
                                .foregroundStyle(.secondary)
                        }
                        Spacer()
                        Toggle("", isOn: $badge.isActive)
                    }
                }
            }
        }
        .navigationTitle("RFID Badges")
    }
}

```

---

## 44.6. OCPI 2.2.1 Tokens Module Mapping Engine

When roaming between CPO and eMSP systems, RFID authorization tokens are synchronized via the OCPI `Tokens` module.

```json
{
  "country_code": "FR",
  "party_id": "CPO",
  "uid": "A1B2C3D4",
  "type": "RFID",
  "contract_id": "FR-CPO-C12345678",
  "visual_number": "NL-TNM-000123-X",
  "issuer": "Electric Mobility Solutions",
  "valid": true,
  "whitelist": "ALWAYS",
  "last_updated": "2026-08-26T12:00:00Z"
}

```

### Authorization Rules & Fallbacks

1. **Local Auth List (Offline Cache)**: Download OCPI Token lists to charger memory via OCPP `SendLocalList` for fast local RFID validation when offline.
2. **Real-time Authorization**: If UID is not in Local Auth List, send OCPP `Authorize.req` to CSMS to resolve token online.
3. **Roaming Authorization**: If CSMS does not recognize local UID, forward `POST /ocpi/receiver/2.2.1/tokens/A1B2C3D4/authorize` to connected eMSP partners.

# 45. OCPP 2.0.1 SendLocalList Authorization Cache Synchronization Skill

## 45.1. Domain Overview & Protocol Mechanics

The `SendLocalList` command allows a CSMS (Charging Station Management System) to push a local authorization list to an EVSE (Charger). This enables stations to validate RFID cards (`IdToken`) locally when internet or CSMS connectivity is lost.

### Key Concepts & Enums

* **`UpdateType`**:
  * `Full`: Replaces the entire local authorization list on the charger. Resets `versionNumber`.
  * `Differential`: Applies delta changes (additions, updates, deletions) to the existing list on the charger.
* **`SendLocalListStatus`**:
  * `Accepted`: The charger successfully applied the update list.
  * `Failed`: The charger failed to process the update list.
  * `VersionMismatch`: The charger's current list version number does not match the expected base version for a differential update.
  * `UpdateNotSupported`: The charger does not support local authorization lists.
* **`AuthorizationData`**:
  * `idToken`: Contains the identifier (`idToken.id` string and `idToken.type` e.g., `ISO14443`, `MacAddress`, `eMAID`).
  * `idTokenInfo`: Status (`Accepted`, `Blocked`, `Expired`, `Invalid`, `ConcurrentTx`), optional `groupIdToken`, `cacheExpiryDateTime`, and `personalMessage`.

---

## 45.2. Synchronization Flow & Versioning State Machine


```

CSMS Database                          Charging Station (EVSE)
[Version: 104]                              [Version: 103]
|                                           |
|--- 1. Calculate Differential Delta ------>|
|    (Version 104, Differential)            |
|                                           |
|--- 2. SendLocalList.req(104, Diff) ------>|
|                                           |-- Validate Version --+
|                                           |   Current (103) + 1  |
|                                           |   == Incoming (104)  |
|                                           |<---------------------+
|<-- 3. SendLocalList.conf(Accepted) -------| Updates Local DB
|                                           | New Version: 104
|                                           |
====================== VERSION MISMATCH RECOVERY ======================
|                                           |
[Version: 108]                              [Version: 102]
|                                           |
|--- SendLocalList.req(108, Diff) --------->|
|                                           |-- Check Version: Mismatch!
|<-- SendLocalList.conf(VersionMismatch) ---| Returns VersionMismatch
|                                           |
|--- 4. Trigger Full Sync ----------------->|
|    SendLocalList.req(108, Full)           | Replaces complete
|<-- SendLocalList.conf(Accepted) ----------| local authorization list

```

---

## 45.3. JSON RPC 2.0 Frame Schemas

### 45.3.A. Request Payload (`SendLocalListRequest`)

```json
[
  2,
  "msg-sync-89021",
  "SendLocalList",
  {
    "versionNumber": 104,
    "updateType": "Differential",
    "localAuthorizationList": [
      {
        "idToken": {
          "id": "04A1B2C3D4E5F6",
          "type": "ISO14443"
        },
        "idTokenInfo": {
          "status": "Accepted",
          "cacheExpiryDateTime": "2026-12-31T23:59:59.000Z",
          "groupIdToken": {
            "id": "FLEET-VIP-01",
            "type": "Central"
          }
        }
      },
      {
        "idToken": {
          "id": "A1B2C3D4",
          "type": "ISO14443"
        },
        "idTokenInfo": {
          "status": "Blocked"
        }
      }
    ]
  }
]

```

### 45.3.B. Response Payload (`SendLocalListResponse`)

```json
[
  3,
  "msg-sync-89021",
  {
    "status": "Accepted"
  }
]

```

---

## 45.4. C# ASP.NET Core Server-Side Sync Engine

### 45.4.A. Local List Domain Models (`Ocpp201LocalList.cs`)

```csharp
using System.Text.Json.Serialization;

namespace Mobility.CSMS.Ocpp201;

public enum UpdateType
{
    Full,
    Differential
}

public enum SendLocalListStatus
{
    Accepted,
    Failed,
    VersionMismatch,
    UpdateNotSupported
}

public enum IdTokenStatus
{
    Accepted,
    Blocked,
    Expired,
    Invalid,
    ConcurrentTx
}

public record IdTokenDto(
    [property: JsonPropertyName("id")] string Id,
    [property: JsonPropertyName("type")] string Type = "ISO14443"
);

public record IdTokenInfoDto(
    [property: JsonPropertyName("status")] string Status,
    [property: JsonPropertyName("cacheExpiryDateTime")] string? CacheExpiryDateTime = null,
    [property: JsonPropertyName("groupIdToken")] IdTokenDto? GroupIdToken = null
);

public record AuthorizationDataDto(
    [property: JsonPropertyName("idToken")] IdTokenDto IdToken,
    [property: JsonPropertyName("idTokenInfo")] IdTokenInfoDto? IdTokenInfo = null
);

public record SendLocalListRequestDto(
    [property: JsonPropertyName("versionNumber")] int VersionNumber,
    [property: JsonPropertyName("updateType")] string UpdateType,
    [property: JsonPropertyName("localAuthorizationList")] List<AuthorizationDataDto>? LocalAuthorizationList
);

public record SendLocalListResponseDto(
    [property: JsonPropertyName("status")] string Status
);

```

### B. Synchronization Service Manager (`LocalListSyncService.cs`)

```csharp
using System.Text.Json;

namespace Mobility.CSMS.Services;

public interface ILocalListSyncService
{
    Task PushFullListAsync(string stationId, CancellationToken ct);
    Task PushDifferentialUpdateAsync(string stationId, List<AuthorizationDataDto> changedTokens, CancellationToken ct);
}

public class LocalListSyncService : ILocalListSyncService
{
    private readonly IStationRepository _stationRepository;
    private readonly ITokenRepository _tokenRepository;
    private readonly IWebSocketConnectionPool _connectionPool;

    public LocalListSyncService(
        IStationRepository stationRepository,
        ITokenRepository tokenRepository,
        IWebSocketConnectionPool connectionPool)
    {
        _stationRepository = stationRepository;
        _tokenRepository = tokenRepository;
        _connectionPool = connectionPool;
    }

    public async Task PushFullListAsync(string stationId, CancellationToken ct)
    {
        var station = await _stationRepository.GetStationAsync(stationId, ct);
        var allTokens = await _tokenRepository.GetAllActiveTokensAsync(ct);

        int newVersion = station.LocalListVersion + 1;

        var authList = allTokens.Select(t => new AuthorizationDataDto(
            IdToken: new IdTokenDto(t.Uid, t.TokenType),
            IdTokenInfo: new IdTokenInfoDto(
                Status: t.IsBlocked ? IdTokenStatus.Blocked.ToString() : IdTokenStatus.Accepted.ToString(),
                CacheExpiryDateTime: t.ExpiresAtUtc?.ToString("o")
            )
        )).ToList();

        var payload = new SendLocalListRequestDto(
            VersionNumber: newVersion,
            UpdateType: UpdateType.Full.ToString(),
            LocalAuthorizationList: authList
        );

        var status = await SendLocalListCallAsync(stationId, payload, ct);
        if (status == SendLocalListStatus.Accepted)
        {
            await _stationRepository.UpdateLocalListVersionAsync(stationId, newVersion, ct);
        }
    }

    public async Task PushDifferentialUpdateAsync(string stationId, List<AuthorizationDataDto> changedTokens, CancellationToken ct)
    {
        var station = await _stationRepository.GetStationAsync(stationId, ct);
        int targetVersion = station.LocalListVersion + 1;

        var payload = new SendLocalListRequestDto(
            VersionNumber: targetVersion,
            UpdateType: UpdateType.Differential.ToString(),
            LocalAuthorizationList: changedTokens
        );

        var status = await SendLocalListCallAsync(stationId, payload, ct);

        switch (status)
        {
            case SendLocalListStatus.Accepted:
                await _stationRepository.UpdateLocalListVersionAsync(stationId, targetVersion, ct);
                break;

            case SendLocalListStatus.VersionMismatch:
                // Recovery strategy: Mismatch detected, trigger full resynchronization
                await PushFullListAsync(stationId, ct);
                break;

            case SendLocalListStatus.Failed:
            case SendLocalListStatus.UpdateNotSupported:
                // Log failure or raise operational alert
                break;
        }
    }

    private async Task<SendLocalListStatus> SendLocalListCallAsync(string stationId, SendLocalListRequestDto request, CancellationToken ct)
    {
        string messageId = Guid.NewGuid().ToString("N");
        var rpcCall = new object[] { 2, messageId, "SendLocalList", request };
        byte[] buffer = JsonSerializer.SerializeToUtf8Bytes(rpcCall);

        var responseJson = await _connectionPool.SendAndAwaitResponseAsync(stationId, messageId, buffer, TimeSpan.FromSeconds(30), ct);
        
        using var doc = JsonDocument.Parse(responseJson);
        var root = doc.RootElement;
        
        // Unpack CallResult: [3, messageId, payload]
        var responsePayload = root[2];
        string statusStr = responsePayload.GetProperty("status").GetString()!;

        return Enum.Parse<SendLocalListStatus>(statusStr, ignoreCase: true);
    }
}

```

---

## 45.5.5. Offline Validation Logic & Edge Cases

When an RFID card is tapped at an offline EVSE:

1. **Check Local Auth List**: Query the internal local database for the matching `idToken.id` and `idToken.type`.

2. **Evaluate Expiry & Status**:

* If `status == "Accepted"` AND `cacheExpiryDateTime` > Current Time $\rightarrow$ **Authorize Charging**.
* If `status == "Blocked"` OR `status == "Expired"` $\rightarrow$ **Reject Charging**.
* If `idToken` is **Not Found**:
* Check `LocalAuthListWithoutAuth` configuration variable:
* If `true` $\rightarrow$ Allow emergency/fallback charge up to maximum allowed energy limit.
* If `false` $\rightarrow$ Reject charging.

3. **Queue Offline Transactions**: Store transactions locally with an `OfflineCreated` flag until reconnection, then batch push via OCPP `TransactionEvent` messages.


# 46. Quality Gate

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

# 45. Final Principle

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


