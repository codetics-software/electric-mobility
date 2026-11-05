# OCPP-J WebSocket implementation

Read this when building a charging station client, CSMS server, local controller, gateway, or simulator. It summarizes OCA OCPP-J 1.6, 2.0.1, and 2.1 transport behavior in a self-contained reference. Use the matching [message cards](messages/) for payloads. For a certification claim or disputed newer-edition behavior, check OCA's current Part 4, errata, and selected security profile. OCPP 1.6 also has SOAP; this guide covers JSON over WebSocket.

## Handshake and authenticated connection

1. The station forms the endpoint by appending its percent-encoded unique identity to the configured OCPP-J URL path. Bind that path identity to the authenticated credential/certificate and provisioned station record; do not trust the path alone.
2. The station offers supported subprotocols in `Sec-WebSocket-Protocol` in preference order, for example `ocpp2.1`, `ocpp2.0.1`, `ocpp1.6`. The CSMS selects one offered value. A version-like URL path does **not** select the OCPP version. Reject/close connections where no common subprotocol is negotiated according to the selected Part 4.
3. Authenticate during the HTTP upgrade using the chosen OCPP security profile. Validate TLS and certificate chain where applicable; bind the Basic-auth username/credential or client certificate to the station identity. Redact handshake credentials.
4. Create one connection epoch for the authenticated station and atomically replace or reject a stale socket. Route commands only to the owner of the current epoch. Reconnection does not erase persisted operations or transaction evidence.

OCPP 2.0.1 Part 4 requires CSMS and local-controller support for RFC 7692 WebSocket compression; the station's support is optional. Negotiate it instead of assuming compressed frames. Set decompressed payload limits to protect the server. OCPP 1.6 has no SOAP semantics on a WebSocket connection.

## Frame codec

| Type | Versions | Shape | Meaning |
|---|---|---|---|
| CALL `2` | 1.6, 2.0.1, 2.1 | `[2, id, action, payload]` | Version-specific action request; payload is an object. |
| CALLRESULT `3` | 1.6, 2.0.1, 2.1 | `[3, id, payload]` | Response to a CALL; action comes from the pending request, not the frame. |
| CALLERROR `4` | 1.6, 2.0.1, 2.1 | `[4, id, code, description, details]` | RPC/format/processing error for a CALL; details is an object. |
| CALLRESULTERROR `5` | 2.1 | `[5, id, code, description, details]` | Error on a received CALLRESULT, with the response's ID. |
| SEND `6` | 2.1 | `[6, id, action, payload]` | Unconfirmed message; receiver sends no CALLRESULT/CALLERROR. |

Use UTF-8 JSON; enforce array arity, element types, message ID length and uniqueness, known action, and request/response schema. Use `{}` for an empty payload. The station identity belongs to the authenticated connection, not each frame. Preserve exact case for action and enum strings. A regular business rejection is normally a valid CALLRESULT with a defined status; reserve CALLERROR for conditions specified by the RPC rules.

The selected Part 4 sets message-ID uniqueness rules. In 1.6, a sender's CALL IDs must be unique on the WebSocket connection. In 2.0.1 and 2.1, IDs are unique across connections using the same station identity; a retry may reuse its original ID. Store a bounded deduplication record that survives reconnect when the operation matters. A CALLRESULT or CALLERROR copies the pending CALL ID. A 2.1 CALLRESULTERROR copies the CALLRESULT ID. Do not correlate by action name or timestamp.

## Duplex scheduling and pending calls

The inspected Part 4 documents say a station or CSMS does not send another CALL on the **same OCPP-J connection** until its previous outbound CALL receives a result/error or times out. This is per direction and per connection. Both peers may have an outbound CALL in flight at once, so the read loop must continue accepting and answering incoming CALLs while waiting for its own response. OCPP 2.1 SEND can be sent without waiting, but it shares the socket and can delay CALL traffic.

Use one serialized writer per socket, an inbound parser/dispatcher, a pending-CALL table, and a bounded outbound queue with priority for responses and critical control traffic. Do not hold the writer or read loop while waiting on storage, payment, firmware transfer, or another network service. Define deadlines for upgrade, request handling, pending CALL, idle socket, and reconnect. On timeout, complete the caller with an *unknown outcome* when the station may have acted; reconcile before issuing a non-idempotent retry. Limit queue size and memory under reconnect storms.

WebSocket Ping/Pong checks the transport; OCPP `Heartbeat` has protocol clock/liveness meaning. A Ping does not prove the charger is operational, and a missed Heartbeat does not by itself end a transaction. Preserve independent transport, registration, availability, and transaction states.

## Dispatch and failure handling

```text
authenticated socket + negotiated version
  → parse frame shape and ID
  → match CALLRESULT/ERROR to pending call, or validate incoming action and direction
  → decode with exact version schema
  → authorize against station/tenant and current capability/state
  → persist accepted evidence / operation intent
  → execute handler without blocking the read loop
  → serialize matching result/error through the one writer
  → await and reconcile later physical/transaction evidence
```

Handle malformed JSON, unknown frame type, unknown action, unsupported feature, schema failure, handler exception, duplicate ID, late response, socket close, and server restart distinctly. Part 4 allows specific choices for malformed/invalid messages; follow its exact error/drop behavior instead of reflexively sending CALLERROR for every invalid byte sequence. Never reflect untrusted raw payload text into error descriptions or logs.

For 2.0.1 edition 4 and 2.1 edition 2 with the June 2026 errata, silently ignore an unknown message-type number. `MessageTypeNotSupported` is deprecated. This is distinct from a known CALL action that the receiver does not implement. See [errata-2026-06.md](errata-2026-06.md).

## Security and interoperability checks

- Security profile and OCA security extensions vary by version and station firmware. Document the agreed profile and test credential rotation, certificate expiry/revocation, clock skew, and reconnect after renewal.
- Authorize outbound control actions (`Reset`, start/stop, unlock, configuration, firmware, certificate, smart charging, DER) per tenant/operator and station capability. Audit request, response, and observed outcome.
- Limit frame size, nesting, decompression ratio, queue depth, and concurrent sockets. Validate URLs used by firmware/log actions against allowed destinations and prevent SSRF.
- Test subprotocol mismatch, wrong identity, duplicate connections, partial writes, ping/pong loss, crossed CALLs, timed-out CALL followed by late result, duplicate CALL after reconnect, and 2.1 SEND backpressure.
- Run the matching Part 5 profile and Part 6/OCTT cases for conformance claims; use real station interoperability tests for vendor deviations.
