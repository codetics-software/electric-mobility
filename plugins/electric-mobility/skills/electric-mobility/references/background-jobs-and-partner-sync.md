# Background jobs and partner sync

Read this when writing scheduled work in a charging backend: supervision detectors,
cleanup, payment workers, or pushes to roaming partners. These are `IMPLEMENTATION
CHOICE`s that held up in production.

## Rules for every job

- Run each job once per cluster: one replica, a lease, or row claims with locks. See
  [operations](operations-and-deployment.md#scaling).
- Isolate failures: one tenant, partner, or record failing must not stop the rest. Log the
  error class at warn level and details at debug level, and leave the record for the next run.
- Keep money and station state in the database between runs. A job resumes from stored
  state; it never depends on memory surviving a restart.
- Lock the record, re-check its state inside the transaction, then act. Two workers, or a
  worker and a webhook, will touch the same record.
- Never call a network service inside the database transaction. Commit intent, call, then
  record the result in a new transaction.
- Combine event-driven work (mark dirty, process every few seconds) with a slower periodic
  pass that repairs missed events.
- Bound every batch (page size, attempts, age) and every query (time range limits).

## Supervision detectors

| Detector | Signal | Action |
|---|---|---|
| Station offline | Last contact older than a threshold | Notify admins once per outage (dedupe key: station + last-seen time) |
| Authorized, never started | Accepted `Authorize` with no session for that token after N minutes | Notify the token owner once |
| Stuck in `Preparing` | Connector `Preparing` for N minutes with no session | Notify the person who authorized |
| Stale session | Open session with no meter data for N hours, and connector idle or faulted | Close softly at the last reading, settle payment, audit as automatic |
| Expiring certificate | Station or CA certificate within 30 days of expiry | Notify admins |
| Expired commands | Deadline passed while queued or sent | Mark timed out, publish completion |
| Account inactivity | No login for a long period | Notify once, record that notice was sent |

- Give every notification a **dedupe key and window** so a detector that runs every minute
  sends one message per incident.
- A stale-session close uses the last real reading and time, never "now", and is marked as
  automatic so it can be reviewed. Never auto-close a session whose connector still reports
  charging.
- Localize notification text at send time in the recipient's language and the site's zone.

## Retention

Set a separate period per kind of data, and delete in bounded transactions:

| Data | Typical handling |
|---|---|
| Raw OCPP frames, station events | Short (weeks to months) |
| Meter values outside a session | Short |
| Meter values of a session, sessions, CDRs, invoices | Keep: billing and legal evidence |
| Audit log | Per legal and contractual need |
| Notifications, asset measurements | Short |
| Sent partner outbox entries | About 7 days |

## Pushing to roaming partners

Treat each partner as an unreliable, slow, independent consumer.

1. **Build a snapshot** of what the partner should see per module (locations, tariffs,
   tokens), scoped by tenant and by the role the partner holds.
2. **Diff against what was last sent** to that partner, stored per partner, module, and
   object path. Store only changed objects; delete stale ones and send the removal.
3. **Enqueue** each change in an outbox row (partner, module, method, path, body) in the
   same transaction as the business change.
4. **Deliver** in small batches every few seconds. On failure, increment attempts and back
   off exponentially (for example 30 s doubling, capped at one hour), with a maximum attempt
   count. Record the last error on the row and on the partner, truncated, without secrets.
5. **Resolve the endpoint at send time** from the partner's negotiated module list. A
   disabled or unregistered partner, or a missing module, is a recorded failure, not a crash.
6. **Rebuild** periodically (about every 15 minutes) to repair drift.

- Station status and connection changes and session updates trigger targeted pushes;
  the rebuild covers everything else.
- Never push tokens that are not tied to an owner, vehicle identifiers, or internal-only
  badges to partners.
- Show operators per partner: last successful push, last error, queue depth.

## Payment workers

A worker advances each open payment through its states on a short interval:

```text
pending payment ─(expired)─▶ cancelled
start requested ─(rejected or start window passed)─▶ settle at zero, cancel queued start
charging ─(estimate ≥ credit or max duration)─▶ stop requested
settling ─▶ refund unused credit (idempotent) ─▶ completed | refund pending | failed (operator)
```

- Cancel a still-queued start command when the payment is refunded, so it can never start
  later.
- Retrieve an existing refund by its ID before creating a new one.
- A station can open a transaction despite a refusal. Request a real stop and do not bill
  it as a paid session.
- A failed or cancelled refund goes to an operator queue. Never loop on it.

## Tests

Duplicate runs in parallel, a crash between the provider call and the commit, partner down
for hours then back, a deleted object while the partner is offline, notification dedupe,
stale-session close while still charging (must not close), and retention boundaries.
