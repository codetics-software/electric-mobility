# OCPP source and version guide

Use this index for station or CSMS work. Establish the negotiated OCPP subprotocol, transport, station identity, security profile, supported functional blocks, specification edition, errata, and vendor firmware before deciding what behavior is required. A message name alone does not establish support.

## Source hierarchy

1. The exact OCA version, edition, and errata agreed for the integration.
2. The matching Part 2 use case and requirements, Part 3 JSON schema, and Part 4 OCPP-J transport rules. For 1.6, use the 1.6 specification and the appropriate JSON or SOAP supplement.
3. Part 5 certification profiles and Part 6 test cases where conformance is claimed. A supported protocol version does not imply every optional profile.
4. A documented vendor compatibility profile, kept separate from standard behavior.

The bundled [message cards](messages/) are the working field references: 28 OCPP 1.6 actions, 64 OCPP 2.0.1 actions, and 90 OCPP 2.1 CALL actions plus its SEND action. Each card lists request/response fields, required status, constraints, enums, and nested object shapes. Use the version and runtime guides for state and transport behavior. No local PDF, ZIP, iCloud folder, or download is required to use the skill. For a conformance claim or a disputed interpretation, check the applicable OCA edition and errata through the [official OCPP page](https://openchargealliance.org/protocols/open-charge-point-protocol/).

The field cards were derived from the locally available OCA 1.6 JSON schema set and OCA Part 3 ZIPs for 2.0.1 and 2.1. The 2.x schema packages can predate the newest prose editions (2.0.1 edition 4 and 2.1 edition 2). Treat the cards as precise schema summaries for those packages, and check later errata before asserting edition-specific conformance. For OCPP 1.6 SOAP, use the separate SOAP binding; these cards describe OCPP-J payloads.

## Choose the version reference

| Version | Read | Distinct engineering concern |
|---|---|---|
| 1.6 | [ocpp-1.6.md](ocpp-1.6.md) | SOAP versus JSON transport, connector-based transactions, security extension support |
| 2.0.1 | [ocpp-2.0.1.md](ocpp-2.0.1.md) | Device Model, EVSE model, TransactionEvent, security and ISO 15118 support |
| 2.1 | [ocpp-2.1.md](ocpp-2.1.md) | 2.0.1 application logic plus V2X, DER, ISO 15118-20, payments, tariffs, and transaction options |

For implementation, read [message-catalog.md](message-catalog.md) to find the action, then load **only its card** in `messages/<version>/<Action>.md`. Read [websocket-and-runtime.md](websocket-and-runtime.md) for handshake, frame codec, concurrency, and security; [charge-point-management.md](charge-point-management.md) for station/CSMS lifecycles; and the [June 2026 errata digest](errata-2026-06.md) for 2.x behavior corrections. Pair these with [the language guide](../implementation-and-debugging.md) for the target stack.

OCA states that 1.6 and 2.0.1 are not compatible. Its 2.1 introduction says 2.0.1 application logic remains valid but needs extensions for new features. Treat this as an application-level migration statement, not proof that every station supports every 2.1 action. Verify negotiated subprotocol, schema, and capability for each operation.

## Shared engineering rules

- Parse the version-specific OCPP-J frame type and unique ID before dispatch. Match CALLRESULT or CALLERROR to a pending CALL by unique ID; handle late and duplicate responses without executing the business operation twice. OCPP 2.1 also defines CALLRESULTERROR and unconfirmed SEND; do not wait for a CALLRESULT where the selected Part 4/use case specifies SEND.
- Authenticate the station identity before assigning it to a tenant. Bind the WebSocket path, negotiated subprotocol, credentials/certificate, and station record; reject mismatches.
- Distinguish a transport acknowledgment, an accepted command, a reported transaction, and observed energy. Persist the operation and its correlation so a restart or reconnect does not erase the outcome.
- Reconcile after reconnect using version-specific transaction evidence, meter readings, and station status. Never turn a missed heartbeat alone into a completed transaction or a billing fact.
- Validate message direction, required fields, enums, cardinality, timestamps, and units with the matching schema and use case. Preserve unknown vendor diagnostics without accepting them as standard fields.
- Keep station connection ownership explicit in a scaled CSMS; route outbound calls to the instance holding the authenticated socket and invalidate stale ownership on reconnect.
- Test online, offline, duplicate, reordered, delayed, rejected, and timeout paths with a simulator plus a real station where available. Link each failure to a message ID and domain operation ID.

OCA version overview: <https://openchargealliance.org/protocols/open-charge-point-protocol/>.
