# Supporting OCPP 1.6 and 2.0.1 on one CSMS

Read this when one backend must manage stations on several OCPP versions. Rules marked
`STANDARD` come from OCPP-J; the rest are `IMPLEMENTATION CHOICE`s that held up on a mixed
fleet. Check the [message cards](messages/) for exact fields.

## Choose the version per station

- Store a per-station setting: `AUTO`, `1.6`, or `2.0.1`. In `AUTO`, select the first
  offered subprotocol the server supports. Record the negotiated version on every
  connection; firmware updates change it.
- Serve all versions on the same path, for example `/ocpp/{tenant}/{station}`. The path
  never selects the version; `Sec-WebSocket-Protocol` does (`STANDARD`).
- Migrate legacy stations to a fixed `1.6` so their behavior does not change on upgrade.
- Order at the upgrade: authenticate first (bad credentials get HTTP 401, before any
  parsing), then negotiate. If an authenticated station offers no acceptable version,
  complete the handshake without a subprotocol header and close at once (`STANDARD` in
  2.0.1 Part 4; a 1002 close code worked). A station that sends no header at all gets
  its fixed version, or 1.6.

## One business core, thin version adapters

```text
socket ─▶ frame codec ─▶ version decoder (strict) ─▶ normalized event ─▶ business core
business core ─▶ canonical command ─▶ version encoder ─▶ queue ─▶ socket
```

- Keep authorization, sessions, meter values, payments, reservations, and events in one
  core. Each version only decodes, encodes, and maps.
- Write the canonical command model once. Mapping 1.6-shaped commands to 2.0.1 worked well
  because most product features predate 2.0.1:

| Canonical (1.6 form) | 2.0.1 message |
|---|---|
| `RemoteStartTransaction` / `RemoteStopTransaction` | `RequestStartTransaction` / `RequestStopTransaction` |
| `ChangeConfiguration` | `SetVariables` |
| `GetConfiguration` | `GetVariables`, or `GetBaseReport` for all keys |
| `Reset` `Hard` / `Soft` | `Reset` `Immediate` / `OnIdle` |
| `GetDiagnostics` | `GetLog` |
| `SignedUpdateFirmware`, `UpdateFirmware` | `UpdateFirmware` |
| `ExtendedTriggerMessage`, `TriggerMessage` | `TriggerMessage` |
| `ChangeAvailability`, `UnlockConnector`, `ReserveNow`, `SetChargingProfile`, `SendLocalList`… | Same name, 2.0.1 payload |

- Map the response back to the canonical shape, so screens and automations behave the same.
- When the station's version is known, refuse a command with no equivalent **at request
  time**, with a clear message. Do not queue something that can never be sent.
- Let administrators send native 2.0.1 commands too, validated against the 2.0.1 schema,
  but route certificate and network-profile commands through dedicated, audited flows.

## Normalizing what stations send

- **EVSE versus connector.** Map a 2.0.1 EVSE to your connector concept, and derive the
  EVSE status from its connectors by taking the most active one.
- **Occupied.** 2.0.1 `Occupied` is coarse. Refine it from `TransactionEvent.chargingState`
  to recover `Preparing`, `Charging`, `SuspendedEV`, `SuspendedEVSE`, and `Finishing`.
- **Transactions.** The station chooses the 2.0.1 `transactionId` (a string). Keep it beside
  your own numeric session ID. Support authorize-first (no EVSE yet), plug-first (no token
  yet), and free-vend (`NoAuthorization`) flows.
- **Inconsistent events.** Log a `TransactionEvent` that contradicts stored state instead of
  rejecting it; a rejection makes stations drop data. Reconcile later.
- **Meter values.** Convert 2.0.1 samples (numeric value, unit multiplier, separate signed
  data) to one internal shape before storage. Keep signed data byte-for-byte.
- **Device model.** Store `NotifyReport` results as parameters named
  `Component[:instance][@evse[.connector]]/Variable[:instance]`. Results of `GetVariables`
  and `SetVariables` update the same store. Trigger `GetBaseReport` on first boot.

## Strict decoding, version-correct errors

- Decode strictly: unknown properties, types, required fields, enums, lengths,
  cardinality, and dates. Tolerate known vendor deviations only in a named adapter (see
  [field lessons](../field-lessons.md)), never in identity or authorization.
- Answer with the error codes of the connection's version (`STANDARD`). 1.6 uses its own
  spellings `FormationViolation` and `OccurenceConstraintViolation`; 2.0.1 uses
  `FormatViolation` and `OccurrenceConstraintViolation`.
- Broken frame or bad message ID: `RpcFrameworkError`. Unknown action: `NotImplemented`.
  An action only the CSMS may send: `NotSupported`. For unknown message types, follow the
  errata of your edition ([errata](errata-2026-06.md)).
- Never answer a malformed CALLRESULT or CALLERROR with an error. Log it and let the pending
  command time out.
- Send UTC timestamps with at most three decimal places.

## Commands: one at a time, deadline from the send

- One outstanding server CALL per station (`STANDARD`). The next command waits for the
  response, the deadline, or a reconnect.
- Start the response deadline when the command is **sent**, not when it is queued.
- On reconnect, close the pending command as timed out with an unknown outcome.
- Ping each socket about every 30 s. Close only a connection that answered pings before and
  then stayed silent for about three intervals; some stacks never answer pings at all.

## Registration states gate everything

Give each station a boot response setting: `Accepted`, `Pending`, or `Rejected`.

| State | Server may send | Station messages |
|---|---|---|
| `Pending` | Provisioning only: variables, reports, trigger, reset, network profile, certificates, monitoring | Charging messages (`Authorize`, transactions, meter values, `DataTransfer`, reservations, ISO 15118) get `SecurityError` |
| `Rejected` | Nothing | Everything except `BootNotification` gets `SecurityError` |

The boot `interval` is the retry delay. Switching to `Accepted` sends
`TriggerMessage(BootNotification)`; queued remote starts stay queued until then.

## Security operations differ per version

| Operation | 1.6 (security whitepaper) | 2.0.1 |
|---|---|---|
| Raise security profile | `ChangeConfiguration SecurityProfile` | Use case A05: `SetNetworkProfile` into a free slot, `SetVariables` to put it first in `NetworkConfigurationPriority`, then `Reset OnIdle` |
| Rotate Basic password | `ChangeConfiguration AuthorizationKey` | `SetVariables SecurityCtrlr.BasicAuthPassword` |

For both: keep accepting the old profile or password until the station connects with the
new one, then commit. Any refusal or missing response cancels the change. Show a new
password once, never store it in command history or parameters, and block these keys from
generic commands and configuration templates. See
[securing stations](../security/ocpp-stations.md).

## Tests that caught real regressions

Subprotocol refusal and missing header, 401 before parsing, codec round trips for every
action, translation both ways, untranslatable command refused, Pending and Rejected gating,
authorize-first and plug-first flows, inconsistent `TransactionEvent`, ping liveness, late
response after timeout, and the profile upgrade cancelled on refusal.
