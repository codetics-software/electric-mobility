# Engineering principles

Sharp defaults for charging systems. Small modeling errors surface months later as wrong
authorization, history, or invoices.

```text
relationships before tables         facts before aggregate statuses
evidence before inference           state vectors before overloaded enums
snapshots before mutable joins      operations before success booleans
correction chains before mutation   explicit units before primitives
```

Add an abstraction only when its identity, lifecycle, authority, or historical purpose is clear.

## State

Do not use one status field. Separate connectivity, protocol, station, EVSE, connector,
authorization, transaction, session, billing, synchronization, and command state. These change
independently:

```text
station connected != EVSE available != authorization accepted != charging started
!= energy delivered != session completed != CDR accepted
```

## Distributed behavior

Assume messages duplicate, delay, and reorder; connections vanish; remote systems restart; callbacks
retry; stations reboot; clocks differ; databases briefly disagree. For each integration define timeout,
retry, duplicate, ordering, reconciliation, recovery, idempotency, and expiration.

- **Idempotency:** duplicate delivery must not duplicate a business effect. Keys include protocol object identity, OCPP message ID, external operation ID, source + object ID, or a protocol sequence. HTTP method semantics are not enough.
- **Ordering:** later receipt does not mean later event. Use timestamps, sequence numbers, transaction IDs, counters, persistent event order, or reconciliation. If the protocol gives no ordering, define your own consistency strategy.
- **Offline:** ask what happens at 10 seconds, 10 minutes, and 24 hours offline, and after restart. Which state is authoritative? How is missing data recovered? Prefer protocol sync over building a queue because you can.

## Tenancy and identity

```text
Tenant -> Party (country_code, party_id, role), Connections, Locations, EVSEs, Sessions, CDRs
```

External protocol ID is not your database ID. Store internal UUID, external ID, protocol, version,
party, and tenant. Tenant isolation is a security boundary.

## Units and money

- Name units: kWh or Wh, kW or W, V, A, seconds or hours, price per kWh, price per hour. Never convert silently. 11 kW is not 11 W, and 22 kWh is not 22 kW.
- Money is Decimal, BigDecimal, or minor units, never binary floating point.
- Separate energy measurement, tariff calculation, tax calculation, billing amount, and settlement amount.
- Timestamps are protocol data: timezone-aware, UTC internally, never local server time. For time-based tariffs, sessions, and sync, account for timezone, DST, inclusive or exclusive boundaries, clock skew, and precision.

## Testing

- **Contract:** method, URL, headers, authentication, schema, required and optional fields, enums, envelope, pagination, callbacks, version discovery.
- **State machine:** valid and invalid transitions, duplicates, out-of-order, timeout, retry, reconnect, restart, offline, remote rejection.
- **Integration:** authorization -> start -> charging -> meter -> stop -> completion -> CDR, and OCPI command -> CPO -> OCPP -> station -> result -> OCPI callback.
- **Invariants:**
  - energy >= 0
  - a completed session cannot silently become active
  - a duplicate CDR or callback causes no duplicate effect
  - tenant A cannot access tenant B
  - an unknown station does not become operational because a message arrived
  - an accepted remote start does not imply charging

## Debugging

Collect evidence in this order, redacting secrets: protocol, version, roles, topology, authentication, raw
request, raw response, payload, correlation ID, UTC timestamps, station connectivity, domain state, database
state, sync state, retry history, vendor behavior.

Classify: transport, authentication, authorization, schema, protocol semantics, state machine, business logic,
synchronization, vendor interoperability, or infrastructure. Do not conclude without evidence that HTTP 500
means a protocol problem, a closed WebSocket means an OCPP problem, or an active session means a charging vehicle.

## Observability

Useful fields, never with secrets: `tenant_id`, `party_id`, `protocol`, `protocol_version`, `operation_id`,
`correlation_id`, `message_id`, `station_id`, `evse_id`, `connector_id`, `session_id`, `external_object_id`,
`timestamp`, `attempt`, `duration`, `result`, `error_class`.

For OCPP you must be able to answer: which station was connected, what was sent and when, with which message
ID, did it respond, with what, which event followed, and what domain state changed.

## Fleet scale

One WebSocket does not mean one process. Design station -> owning instance and command -> locate station ->
route to owner. Options are sticky routing, a connection registry, a broker, pub/sub, or partitioning. Introduce
Kafka, Redis, or queues only by stating the problem they solve.

## Vendor behavior

Report differences as standard, vendor behavior, workaround, and risk. Isolate them in a compatibility layer so
they never contaminate the domain, and never encode vendor behavior as standard.

## Verifying external sources

Verify when an exact version, enum, endpoint, or schema matters, when behavior differs by version, for
certification, for recent changes, or for a vendor claim. Trust in this order: official specification,
certification documents, migration guides, vendor documents, interoperability reports, community sources, memory.
A blog post is not authority when the specification is available. Official sites:
[OCPI](https://ocpi-protocol.com/), [Open Charge Alliance](https://openchargealliance.org/).
