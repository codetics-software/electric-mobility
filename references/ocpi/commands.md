# OCPI — Commands Module

## Purpose

The Commands module enables the **eMSP to send remote actions to the CPO** — start a session, stop a session, reserve a connector, cancel a reservation, or unlock a connector. It is the only OCPI module with **asynchronous two-step responses**.

**Data owner**: eMSP (initiates commands)  
**Direction**: eMSP (Sender) → CPO (Receiver) → Charge Point → CPO → eMSP (async callback)

---

## Version Availability

| Version | Mandatory |
|---|---|
| 2.1.1 | Optional |
| 2.2.1 | Optional |
| 2.3.0 | Optional |

---

## Why Two-Step Async?

The CPO cannot immediately confirm whether a command succeeded — it must relay the command to the physical charger (via OCPP) and wait for the charger's response. This can take seconds.

```
Step 1 — Synchronous acknowledgment:
  eMSP → POST to CPO's Commands endpoint
  CPO → 200 + CommandResponse
    { "result": "ACCEPTED" }    ← CPO says "I can try this"
  (not "it worked" — just "I accepted the request")

Step 2 — Asynchronous result (callback):
  Charger executes command (or fails)
  CPO → POST to eMSP's response_url
    { "result": "ACCEPTED" }    ← This means the charger actually did it
```

The `response_url` in the command body is a URL **on the eMSP's side** that the CPO calls back when the charger responds. The eMSP controls this URL and can embed a correlation ID in it.

---

## Command Types

### `START_SESSION`

Remote start a charging session for a specific token:

```json
{
  "response_url": "https://emsp.example.com/commands/callback/START/12345",
  "token": {
    "uid": "RFID123",
    "type": "RFID",
    "contract_id": "FR*MCP*C12345*6"
  },
  "location_id": "LOC001",
  "evse_uid": "EV001",
  "connector_id": "1",
  "authorization_reference": "AUTH-ABC-789"
}
```

### `STOP_SESSION`

Stop an ongoing session:

```json
{
  "response_url": "https://emsp.example.com/commands/callback/STOP/12345",
  "session_id": "SES001"
}
```

### `RESERVE_NOW`

Reserve a connector for a specific token until a given expiry:

```json
{
  "response_url": "https://emsp.example.com/commands/callback/RESERVE/12345",
  "token": { ... },
  "expiry_date": "2025-06-01T16:00:00Z",
  "reservation_id": "RES001",
  "location_id": "LOC001",
  "evse_uid": "EV001",
  "connector_id": "1"
}
```

### `CANCEL_RESERVATION`

Cancel a reservation before expiry:

```json
{
  "response_url": "https://emsp.example.com/commands/callback/CANCEL/12345",
  "reservation_id": "RES001"
}
```

### `UNLOCK_CONNECTOR`

Unlock a stuck connector:

```json
{
  "response_url": "https://emsp.example.com/commands/callback/UNLOCK/12345",
  "location_id": "LOC001",
  "evse_uid": "EV001",
  "connector_id": "1"
}
```

---

## HTTP Endpoints

### Receiver Interface (CPO exposes this — eMSP sends to)

| Method | Path | Description |
|---|---|---|
| `POST` | `/ocpi/cpo/2.x/commands/START_SESSION` | Initiate remote start |
| `POST` | `/ocpi/cpo/2.x/commands/STOP_SESSION` | Initiate remote stop |
| `POST` | `/ocpi/cpo/2.x/commands/RESERVE_NOW` | Reserve connector |
| `POST` | `/ocpi/cpo/2.x/commands/CANCEL_RESERVATION` | Cancel reservation |
| `POST` | `/ocpi/cpo/2.x/commands/UNLOCK_CONNECTOR` | Unlock connector |

### Sender Interface (eMSP exposes this — CPO calls back to)

This is **not a fixed endpoint** — the eMSP provides the callback URL per command in `response_url`. The CPO POSTs the `CommandResult` to that URL when the charger responds.

---

## Response Objects

### `CommandResponse` (Step 1 — synchronous)

```json
{
  "result": "ACCEPTED",
  "timeout": 30,
  "message": []
}
```

| `result` Value | Meaning |
|---|---|
| `ACCEPTED` | CPO accepted the command and will relay to charger |
| `CANCELED_RESERVATION` | Reservation was already cancelled |
| `EVSE_OCCUPIED` | EVSE is occupied — cannot start |
| `EVSE_INOPERATIVE` | EVSE is inoperative |
| `FAILED` | CPO cannot process the command |
| `NOT_SUPPORTED` | Command not supported by this CPO |
| `REJECTED` | Command rejected (authorization failure) |
| `TIMEOUT` | CPO timed out waiting for charger |
| `UNKNOWN_RESERVATION` | Reservation ID not found |
| `UNKNOWN_SESSION` | Session ID not found |

`timeout`: seconds within which the async callback will arrive. If no callback within timeout, eMSP can assume failure.

### `CommandResult` (Step 2 — async callback)

```json
{
  "result": "ACCEPTED",
  "message": [{ "language": "fr", "text": "Session démarrée" }]
}
```

`result` values: `ACCEPTED`, `CANCELED_RESERVATION`, `EVSE_OCCUPIED`, `EVSE_INOPERATIVE`, `FAILED`, `NOT_SUPPORTED`, `REJECTED`, `TIMEOUT`, `UNKNOWN_RESERVATION`, `UNKNOWN_SESSION`

---

## Full Remote Start Sequence

```
[eMSP side]
1. Driver taps "Start" in app
2. eMSP → POST /ocpi/cpo/2.x/commands/START_SESSION
   Body includes response_url = https://emsp.example.com/commands/result/REQ-001

[CPO side]
3. CPO validates the command
4. CPO → 200 { "result": "ACCEPTED", "timeout": 30 }
   (returned to eMSP synchronously)
5. CPO → sends START_TRANSACTION to charger via OCPP
6. Charger executes and responds to CPO via OCPP

[CPO → eMSP callback]
7. CPO → POST https://emsp.example.com/commands/result/REQ-001
   Body: { "result": "ACCEPTED" }
   ← eMSP responds 200 (acknowledges receipt)

[Session flow continues normally]
8. CPO creates Session, pushes to eMSP via Sessions module
```

---

## Reservation Workflow

```
eMSP → POST RESERVE_NOW (with reservation_id, expiry_date)
  CPO acknowledges
  CPO → reserves EVSE
  Charger responds → CPO calls back eMSP

Later:
  Driver arrives before expiry:
    Driver presents token → CPO matches reservation → starts session
    CPO → POST CANCEL_RESERVATION on existing reservation (auto-consumed)

  Driver doesn't arrive (expiry passes):
    CPO releases the EVSE automatically
    CPO → (optionally) calls eMSP callback with TIMEOUT/EXPIRED

  eMSP cancels proactively:
    eMSP → POST CANCEL_RESERVATION
    CPO acknowledges → charger releases → CPO calls back eMSP
```

---

## Version Differences

### 2.1.1
- All 5 command types present
- `response_url` is per-command in body
- Simpler token representation in `START_SESSION`
- No `connector_id` in `START_SESSION` (EVSE level only)

### 2.2.1
- `connector_id` added to `START_SESSION` and `RESERVE_NOW` — allows targeting a specific socket on multi-connector EVSEs
- `authorization_reference` in `START_SESSION` — links to real-time auth
- Hub routing: commands must include `OCPI-to-country-code` / `OCPI-to-party-id` headers when going through a hub
- Richer `CommandResponse` result codes

### 2.3.0
- Stronger requirements on `evse_uid` presence in `START_SESSION` (previously optional — now mandatory in most implementations)
- Clarified timeout behavior — CPO must call back even on failure
- Improved hub routing documentation for command forwarding
- `connector_id` explicitly optional in `START_SESSION` (CPO selects best available if omitted)

---

## Implementation Notes

### Correlation via `response_url`
Embed a unique request ID in the `response_url` path:
```
https://emsp.example.com/commands/callback/f3a9c2b1-...
```
When the CPO calls this URL, extract the ID from the path to match the callback to the original request. Never rely on request order.

### Timeout Handling
The CPO's `timeout` field tells you the maximum wait. If no callback arrives within `timeout` seconds, treat the command as failed and surface this to the driver. Do not leave pending commands open indefinitely.

### Idempotency
`START_SESSION` is not idempotent — sending it twice starts two sessions. Build a deduplication layer at the eMSP side based on (token, location, EVSE) within a short window.

### OCPP Relay
The CPO translates OCPI Commands to OCPP messages (RemoteStartTransaction, RemoteStopTransaction, ReserveNow, CancelReservation, UnlockConnector). This relay is entirely on the CPO's side — OCPI doesn't specify the OCPP version or commands used.

---

## Common Pitfalls

- **Treating Step 1 `ACCEPTED` as success**: It only means the CPO will try. Wait for the Step 2 callback before confirming to the driver
- **Not handling callback timeout**: If the charger is offline, the callback may never arrive. Always implement a timeout that surfaces an error to the driver
- **Missing hub routing headers (2.2.1+)**: In hub environments, `OCPI-to-country-code` and `OCPI-to-party-id` must be set so the hub routes the command to the correct CPO
- **Ignoring `EVSE_OCCUPIED` in real-time**: If the driver's selected EVSE is already in use, surface this immediately rather than waiting for a timeout

---

## Spec References

- 2.1.1: `mod_commands.md` — `release-2.1.1-bugfixes`
- 2.2.1: `mod_commands.asciidoc` — `release-2.2.1-bugfixes`
- 2.3.0: `mod_commands.asciidoc` — `2.3.0/release/core`
