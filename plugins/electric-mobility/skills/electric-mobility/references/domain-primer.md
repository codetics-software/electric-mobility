# Domain primer

## The system

```text
EV driver -> eMSP <-OCPI-> CPO or roaming hub -> CSMS <-OCPP-> charging station -> EVSE -> connector -> EV
```

**OCPI** is backend interoperability: locations, EVSEs, connectors, tokens, authorization,
sessions, CDRs, tariffs, commands, charging profiles, credentials, versions, roaming, and hub
routing. **OCPP** is station management: connectivity, authorization, transactions, status,
meter values, remote commands, configuration, firmware, diagnostics, reservations, smart
charging, security, and device management.

Do not say "OCPI controls the charger". OCPI expresses the business operation, and the
CPO or CSMS translates it into station behavior, usually through OCPP.

## Actors

| Actor | Typically responsible for |
|---|---|
| CPO | Stations, EVSE state, sessions, energy measurement, tariffs, CDR generation, OCPP connectivity |
| eMSP | Driver accounts, contracts, tokens, authorization, driver apps, roaming relationships |
| CSMS | Communicating with and managing stations. May be part of the CPO platform or separate |
| Roaming hub | Routing traffic. Routing does not make it the owner of the data |

Hierarchy: Location > EVSE > Connector. EVSE, connector, charge point, and charging station
are not interchangeable terms.

## Versions

- OCPI: 2.0 (legacy, no Commands), 2.1 (deprecated, introduced Commands), 2.1.1, 2.2 (deprecated), 2.2.1, 2.3.0 (identify core and module editions too; the wire value alone does not establish them).
- OCPP: 1.6 (JSON/WebSocket or SOAP), 2.0.1 and 2.1 (edition, errata, certification profile).
- Older versions remain widely deployed. Keep partners on their negotiated contract until migration is confirmed.
- Migrate by concept, never by renaming: old concept -> new concept -> semantic differences -> compatibility concerns.
- OCPP 2.x is not 1.6 with new names. It has a richer device model, EVSE-aware design, an improved transaction model, stronger security, and expanded smart charging.

## OCPI truths by module

- **Ownership:** for each module establish sender, receiver, owner, who creates and modifies, who consumes, and how it syncs. The eMSP stores a copy of a Location, and that copy does not make it the owner.
- **Credentials:** treat as sensitive protocol configuration. Never log them, store them in source, or return them in errors or telemetry.
- **Sync:** initial pull, persist, then pushes. After downtime, recover through pull or reconciliation. Do not assume every event must be queued forever.
- **Locations:** separate static infrastructure from dynamic status (`AVAILABLE`, `CHARGING`, `BLOCKED`, `OUTOFORDER`, `PLANNED`, `REMOVED`, `RESERVED`, `UNKNOWN`). Removal does not delete history. Respect version-specific `last_updated` on nested objects.
- **Tokens:** token identity, validity, authorization request, result, authorization reference, and session are separate. A valid token does not mean this attempt is authorized, because location, EVSE, contract, real-time checks, offline rules, and CPO policy can all decide. Correlate Token -> Authorization -> Reference -> Session -> CDR.
- **Sessions:** a session is not a CDR. A typical lifecycle is `PENDING` -> `ACTIVE` -> `COMPLETED`, but check the version. Draw no billing conclusion from incomplete state.
- **CDRs:** auditable financial data. Immutable, processed idempotently, traceable, and reconcilable. Correct through protocol credit mechanisms, never silent edits. Final cost is not simply energy times price unless the tariff has only that component.
- **Tariffs:** dimensions `FLAT`, `ENERGY`, `TIME`, `PARKING_TIME`, plus time, day, power, current, and duration restrictions, step size, minimum and maximum price, and tax. Define units, rounding, step and time boundaries, timezone, VAT, overlaps, and multiple elements. Never use binary floating point for totals.
- **Commands:** asynchronous. The first response reports acceptance per the protocol, and does not mean the EV started charging.
- **Charging profiles:** a requested limit is not guaranteed power. CPO policy, station capabilities, site limits, grid constraints, other profiles, and the vehicle all change it. Define lifetime, start, duration, units, minimum rate, stacking, conflicts, station support, and failure behavior.

## OCPP truths

- Establish version, transport, security profile, station identity, supported features, and capabilities.
- Correlate requests and responses using the message ID, never timestamps. Persist correlation when an operation must outlive a process.
- Stations are unreliable clients. Handle disconnect, reconnect, reboot, partition, duplicate and stale connections, heartbeat and request timeouts, delayed responses, messages after a timeout, CSMS restart, and reconnect storms.
- A conceptual lifecycle is disconnected -> connecting -> connected -> bootstrapping -> operational. Do not invent protocol states.
- Keep request, protocol response, physical operation, observed event, and domain state as separate facts.

## Translating between OCPI and OCPP

```text
Remote start: OCPI START_SESSION -> CPO authorization -> resolve Location/EVSE/Connector
  -> durable operation -> OCPP remote start -> station result or event
  -> update charging domain -> OCPI response callback

Remote stop: OCPI STOP_SESSION -> find active session -> OCPP stop -> stop event
  -> finalize session -> generate CDR when appropriate

Smart charging: OCPI constraint -> CPO policy -> site constraints -> OCPP profile
  -> station -> meter and status observations
```

## Worked reasoning

**"Implement remote start."** Ask: which OCPI version? Is the requester an eMSP and the receiver a
CPO? Which Location, EVSE, and Connector? Is the token valid, and does the CPO authorize this? Is
the station online, and on which OCPP version? How is it correlated? What if the station rejects,
times out, or answers after the timeout? Which event proves charging started? How is the callback
generated? Which tests cover duplicate, retry, and offline?

```text
Wrong: START_SESSION -> OCPP remote start -> return success
Right: START_SESSION -> validate -> create operation -> return the protocol's immediate result
       -> execute OCPP -> receive result or event -> update state -> notify response URL
```

**"Session is ACTIVE but 0 kWh."** Do not conclude it is broken. It may not have started, or the
vehicle may be paused or not drawing power, a limit may apply, or meter data may be late. Inspect
OCPI session, OCPP transaction, station, EVSE, connector, meter values, authorization, charging
profile, vehicle behavior, and connectivity.

**"Can OCPI control my charger?"** OCPI is the backend layer, and OCPP is the station layer. The CPO
or CSMS translates business operations into station operations.
