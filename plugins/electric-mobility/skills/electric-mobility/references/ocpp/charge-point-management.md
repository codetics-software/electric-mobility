# Building accurate charge point management

Use this playbook with the [message catalog](message-catalog.md), [WebSocket runtime](websocket-and-runtime.md), and the chosen version reference. It applies to a CSMS, station client, or simulator. Build both protocol peers in tests even if the product implements only one side.

## Separate the state dimensions

Maintain station transport connection, Boot/provisioning decision, configured security/capabilities, EVSE/connector availability, authorization decision, command attempt, transaction lifecycle, energy transfer, meter evidence, and financial Session/CDR as distinct facts. A WebSocket connection does not mean `BootNotification` was accepted. A valid remote-start response does not mean a transaction started. A transaction start does not mean energy flowed. A closed socket does not prove the session ended.

Use version-specific identities: 1.6 charge point + connector and CSMS-assigned transaction ID; 2.x charging station + EVSE + connector and station-assigned transaction ID. Scope all of them by tenant and station. Keep event time and ingestion time, original meter values/units/context, firmware version, and source message ID. Store immutable history and derived current state separately.

## End-to-end lifecycle checkpoints

| Stage | Protocol evidence and required management action |
|---|---|
| Provision | Authenticate the socket, negotiate version/security, process `BootNotification` according to accepted/pending/rejected response, identify hardware/firmware and capabilities, then permit version-appropriate operations. |
| Availability | Process status/availability events at their proper station/EVSE/connector scope. Reconcile after reconnect; use status age and source before showing a connector as available. |
| Authorization | Handle online and configured offline/local-list/cache paths. Record token type, authority, expiry, and decision source. Never log secrets or treat a token seen in a message as authorized. |
| Start | Persist command or local-start intent. In 1.6 use `StartTransaction`; in 2.x use `TransactionEvent(Started)` under the selected transaction model. Correlate remote request to the observed start. |
| Energy | Ingest meter values with timestamp, measurand, unit, location, phase, transaction context, and import/export direction. Detect resets, rollover, gaps, late data, and implausible deltas. Do not bill on a status enum alone. |
| Stop | Correlate the requested stop with `StopTransaction` in 1.6 or a version-specific `TransactionEvent(Ended)` in 2.x. Recover offline events and decide finality only after expected meter and authorization evidence is reconciled. |
| Settlement | Translate station facts to product Session/CDR using tariff snapshots and decimal-safe calculations. Keep late corrections/audit chains; do not mutate a final CDR because a later OCPP message arrived. |

## Capability areas to implement deliberately

- **Remote operations:** start, stop, availability, reset, unlock, reservation, and trigger. Track protocol result and later observed effect separately. Make retries explicit and safe after timeout or disconnect.
- **Configuration/device management:** 1.6 configuration keys differ from the 2.x Device Model. Discover supported variables and mutability; apply least privilege to writes and keep before/after audit. Do not fabricate a 1.6 key equivalent for every 2.x variable.
- **Smart charging:** calculate schedules with power/current units, validity, EVSE scope, stack/purpose, station limits, and conflicts. Verify installed/composite schedule or resulting behavior; use an explicit fallback when a station rejects or ignores a profile.
- **Firmware and diagnostics:** authorize and validate artifact/log URLs, track asynchronous download/install/status messages, handle reboot and version verification, and avoid treating the initial acceptance as a completed upgrade.
- **Security and certificates:** maintain certificate ownership, enrollment/rotation/expiry, local authorization data, security events, and secure firmware behavior according to version/profile. Alert on rejected credentials and unexpected security events without leaking private material.
- **2.1 extensions:** isolate V2X, DER, tariff/payment, battery swapping, and periodic event streams behind negotiated 2.1 version and tested capabilities. Preserve bidirectional energy and settlement meaning.

## Build order for a complete implementation

1. Implement and test the frame codec, handshake, authentication, one-writer/one-outbound-CALL scheduler, correlation, timeouts, reconnection, and duplicate handling.
2. Create versioned DTOs for **every action in the selected message catalog** from its bundled per-action card, with request/response serialization tests. Register all actions in a version-aware dispatcher; feature-disabled actions return the specified unsupported behavior.
3. Implement a small end-to-end vertical path: Boot, Heartbeat, status, authorization, transaction start/meter/end, and a remote start/stop with observed outcomes. Persist evidence and operation state before adding optional modules.
4. Add the remaining action families—configuration, local lists, smart charging, firmware/logs, reservation, security/certificates, monitoring, display/cost, and 2.1 capabilities—using a capability matrix and the matching Part 2 use cases.
5. Run protocol fixtures, state-machine and reconnect tests, vendor simulator/real station tests, then the matching OCA certification profile/test cases. A schema pass alone does not prove correct physical or financial behavior.

For each implemented action, review: correct initiator/direction; exact schema and version; capability; authentication/authorization; state precondition; persistence/idempotency; timeout/retry; protocol response versus observed completion; metrics/log redaction; and valid, invalid, duplicate, late, offline, and reconnect tests. Coverage means every action is either implemented with those checks or intentionally reported unsupported under the selected profile; it does not mean every optional feature is enabled on every station.

## Language implementation mapping

Use the existing stack, and read [../implementation-and-debugging.md](../implementation-and-debugging.md) for language details. In Java/Kotlin/C#/Go/Rust/Python/TypeScript, keep the socket reader, serialized writer, pending-CALL scheduler, handler executor, and persistence boundary explicit; use bounded queues and nonblocking async I/O. In Swift, use actor-isolated connection state and persisted operation results across app or process lifecycle. Build or generate DTOs from the bundled action cards, then review unknown enum handling, optional versus null fields, decimal values, timestamps, and custom data. Keep protocol DTOs separate from domain and database models in every language.
