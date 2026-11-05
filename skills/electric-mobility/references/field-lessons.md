# Field lessons: how charging systems really behave

Read this when designing or debugging charging behavior. The specifications describe
what should happen. This describes what production systems meet on real stations.

These are **implementation choices and observed behavior, not protocol rules**. Label
them that way. Check the selected specification before stating a requirement, and test
against the stations actually deployed.

## Know which fact you hold

Each of these can be true while the next is false:

```text
Socket connected         the station has a network path, nothing more
Boot accepted            the station is provisioned
Connector Available      nothing reported in use; a car may still be parked there
Authorize accepted       this token may charge; nothing started
Remote start Accepted    the station took the request; no car may be plugged in
Transaction started      the session opened; zero energy may flow
Energy rising            the car is charging
Stop requested           nothing has stopped yet
Socket closed            says nothing about the session
Session ended            money is not final yet
Final meter received     the amount can now be computed
CDR accepted             the partner agreed
```

Show the fact you hold in the UI. "Starting" and "charging" are different screens, and
a closed socket must not end a session. Stations commonly keep charging offline and
report later.

## Stations deviate from the specification

Tolerate these without giving up validation. Handle them in one adapter layer, keep the
original value, and label it as vendor behavior.

| Observed on the market | Handling that worked |
|---|---|
| Timestamps with no zone, or a `+0100` offset without a colon | Parse leniently; read a missing zone as UTC |
| Numeric values where the schema says string, or decimal meter indexes | Accept the number, keep precision |
| Vendor or model strings longer than the schema limit | Accept up to a higher bound, truncate for display |
| Missing `Sec-WebSocket-Protocol` header | Accept where the deployment supports one version, and record it |
| Unknown error codes | Store as `OtherError`, keep the original code in the event |
| Message IDs restarting from 1 after a reboot | Scope dedup by connection, except for transaction messages |

**Never tolerate deviations in identity, authorization, or authentication.** Being
lenient on a timestamp format is fine. Being lenient on who is calling is not.

## Retries and duplicates

- Stations retry transaction messages until answered, sometimes across a reconnect and
  sometimes with a new message ID. Identify a repeated `StartTransaction` by connector,
  token, timestamp, and meter start, then return the session already open.
- On one connection, an identical repeated message receives the stored response, and a
  reused ID with different content is a protocol error.
- After a reconnect, replay only `StartTransaction`, `StopTransaction`, and `MeterValues`.
  Treat everything else as new, or a rebooted station's messages get wrongly dropped.
- Keep the station's own timestamps and raw samples. Receive time and event time are
  different facts, and offline stations deliver hours of history at once.

## Commands

- Every command gets an ID, a deadline, and a persisted result. Its states are queued,
  sent, succeeded, failed, timed out, and cancelled.
- Record "sent" before writing to the socket, and never automatically resend after a
  transport error. The station may have already executed it.
- A late response updates the record as evidence. It does not reopen a finished decision.
- A database-backed queue removes the need for sticky routing or a message broker at
  moderate scale, because any instance holding the socket can claim the station's work.
  Add infrastructure only when a measured limit requires it.
- Applying saved configuration at boot needs care. Stations reboot often, and a template
  must not overwrite protected keys.

## Meters and energy

- Prefer `Energy.Active.Import.Register` from the outlet, and check the unit on every
  sample, since Wh and kWh both occur.
- Use the register's difference, not a sum of intervals. Never let energy go backward,
  and treat a drop as a meter anomaly to investigate.
- Keep signed values exactly as received. When a raw value is available use it for
  calculation. An OCMF value can be a fallback when no raw value was sent.
- Allow for clock skew when a sample's time looks wrong. Ignore samples before the session
  start or too far ahead.
- A long active session with zero energy is often normal, such as a paused car or a
  scheduled departure. Flag it for review rather than ending it.
- Sanity limits catch stuck sessions: maximum duration, implausible energy, a long time
  in `Preparing`, and sessions with no recent data. Tune them per deployment.

## Tariffs and money

- Resolve the most specific tariff scope: connector, then station, zone, site, workspace.
- Snapshot the tariff when the session starts. Later edits must not change that session.
- A session can combine energy, time, parking, and a flat fee. Bill time pro rata by the
  second, and define rounding explicitly.
- Keep the measured facts, tariff snapshot, and computed amount separately, so a dispute
  can be recalculated.
- Prepaid flows need a clear end: credit exhausted, stop requested, stop confirmed or not,
  final reading, settlement, refund. See
  [payments](security/payments-and-public-charging.md).

## Smart charging

- A shared site limit cannot be divided below the minimum current a car will accept. In
  practice that is about 6 A per phase, so past a certain number of cars, some must pause.
  Decide who pauses, such as by arrival order, and show it to the operator.
- Never allocate more than a connector's own maximum, and count other site loads when you
  have equipment measurements.
- A limit is a request. Compare it against observed power, because cars and stations may
  draw less, and profiles do not always survive a reboot. Re-send them after a reconnect.
- Losing connectivity must not cause an overload. Set the station's fallback or default
  profile to a safe value for when the supervision system goes quiet.

## Tokens and identifiers

- RFID UIDs vary in case, byte order, and length between readers. Normalize them
  deliberately, and test both NFC reading directions when matching a printed or scanned
  card.
- A token's owner, status, expiry, and site access are all checked for each decision. A
  site can restrict charging to assigned users, and a blocked user's tokens stop working
  even if the token itself is still enabled.
- Deleting a user anonymizes the account and frees their tokens. It does not rewrite
  history.
- A registered vehicle should stay optional. Many sessions never know which car it was.

## Provisioning and lifecycle

- Treat first contact as a security event. An unknown station gets in only with a valid,
  expiring, revocable registration token, or after an operator creates it.
- Deleting a station is refused while it has an active session. Mark it deleted and keep
  its history, because sessions and CDRs still point to it.
- Offline detection needs its own rule. Missed heartbeats are a signal, and WebSocket
  pings help keep NAT and proxy paths open. Alert on real absence, with a delay that
  tolerates normal reconnects.
- Restarting the server reconnects the whole fleet. Test that the limiter, the hash cost,
  and the database all survive it.
- Clean up on schedule: abandoned sessions, expired commands, and old events, using a
  separate retention period for each kind of data.

## Multi-database and persistence

If you support several databases, operations that rely on transactions and locks must
really have them on each one. For example, MongoDB needs a replica set for transactions,
and "compatible" services may not behave the same. Serialize work per station, payment,
or command with row locks or their equivalent, and run the same test suite on every
supported database.

## Testing what matters

Local tests with an in-memory database prove logic, not deployment. State this clearly
when reporting results. These need a real environment before you claim they work:

- real payment provider test mode, including webhooks;
- actual station models and firmware, not only a simulator;
- the production database engine;
- the real proxy in front of WebSocket connections, including idle timeouts and client
  certificates;
- a partner's or hub's test environment.

Never report something as interoperable or certified on the strength of a simulator.
