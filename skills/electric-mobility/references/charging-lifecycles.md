# Charging Lifecycle Playbooks

Use this reference for end-to-end flows, state machines, API design, events, debugging, and tests.

The state names below are conceptual unless explicitly tied to a selected protocol or vendor API. Never expose them as normative OCPI/OCPP values without verification.

## Lifecycle Mapping Method

Describe every flow in parallel lanes:

| Lane | Question |
|---|---|
| Human / physical | What did the driver, vehicle, cable, and station actually do? |
| Business | What authorization, pricing, contract, or billing decision happened? |
| Platform domain | Which internal operation and state transition occurred? |
| Protocol | Which version-specific message or endpoint carried the fact? |
| Evidence | What proves the transition happened? |
| Failure / recovery | What if the next participant is offline or replies late? |

Do not say only “the user started the session.” Specify whether the user requested a start, the command was accepted, the station reported a transaction, or energy was observed.

For each transition record:

```text
initiator
recipient
protocol/version
correlation identity
idempotency identity
timeout
retry authority
source of truth
evidence of success
```

## Evidence Ladder

```text
credential read               -> credential was presented
Authorize accepted            -> charging attempt was permitted
start command accepted        -> station accepted a request
transaction-start event       -> station reports transaction began
meter values increasing       -> energy delivery observed
transaction-stop event        -> station reports transaction ended
final CDR / settlement        -> commercial values reported as final
invoice / ledger posting      -> accounting consequence recorded
```

One level does not prove the next.

## RFID Charging Through Roaming

```text
Account / contract created
  -> credential issued and assigned
  -> token shared or made authorizable through roaming
  -> driver presents RFID
  -> station asks CSMS to authorize
  -> CPO resolves local/offline/roaming authorization
  -> authorization decision returned
  -> station starts transaction
  -> CPO creates/updates operational session
  -> meter and status evidence arrives
  -> session updates propagate to interested parties
  -> station transaction stops
  -> CPO finalizes operational facts
  -> CDR / settlement is generated or received
  -> eMSP creates customer-facing session/billing allocation
  -> invoices and reimbursements are produced
```

Required failure questions:

```text
Was the token known locally, cached, or authorized in real time?
What if the roaming party is offline?
What if authorization is accepted but no transaction starts?
What if a transaction starts before its authorization response is persisted?
What if meter values are missing or reset?
What if the CDR arrives twice, late, or corrected?
```

## Remote Start

```text
Driver taps Start
  -> eMSP validates account, credential, and selected EVSE
  -> eMSP creates durable StartOperation
  -> OCPI/vendor command sent to CPO
  -> CPO validates and acknowledges according to its contract
  -> CPO resolves station and connector
  -> CSMS sends version-specific OCPP operation
  -> station accepts or rejects
  -> station emits transaction/event evidence
  -> CPO correlates operational session
  -> CPO sends callback/update
  -> eMSP updates StartOperation and user-visible session
```

Suggested internal operation states:

```text
REQUESTED
VALIDATING
DISPATCHED
ACKNOWLEDGED
STATION_ACCEPTED
START_OBSERVED
REJECTED
TIMED_OUT
EXPIRED
CANCELLED
```

These are implementation states, not protocol enums.

### Immediate API response

Return an operation resource, not a false success claim:

```json
{
  "operationId": "...",
  "status": "DISPATCHED",
  "sessionId": "...",
  "pollAfterSeconds": 2
}
```

The exact HTTP status and shape are application choices. Communicate “accepted for processing,” not “vehicle is charging,” until operational evidence exists.

### Edge cases

```text
duplicate mobile request
same credential used concurrently
EVSE status stale
station disconnect after command acceptance
late station response after timeout
transaction starts without expected callback
callback delivered twice
callback and polling update race
wrong connector starts
start succeeds but meter remains zero
CPO accepts while downstream station rejects
```

## Remote Stop

```text
Stop requested
  -> resolve authoritative active transaction
  -> create durable StopOperation
  -> send interoperability/business command
  -> translate to station-level operation
  -> station acknowledges or rejects
  -> observe transaction-ended evidence
  -> mark operational session stopped
  -> wait for final meter/commercial data
  -> settle and bill later
```

Do not mark a session financially complete when stop is accepted.

Model uncertain outcomes explicitly:

```text
STOP_REQUESTED
STATION_ACKNOWLEDGED
STOP_OBSERVED
STOP_REJECTED
STOP_TIMED_OUT
OUTCOME_UNKNOWN
```

If retries are exhausted while the station is unreachable, “outcome unknown” can be more truthful than “failed.” Final data may still arrive later.

## Local Start Versus Remote Start

Local authorization can originate through RFID, Plug & Charge, a local list, payment terminal, or another mechanism. Remote start originates through a backend command path.

Both may converge on the same operational session, but preserve:

```text
initiation_channel
presented_credential_type
authorization_source
remote_operation_id (nullable)
station transaction identity
```

Do not require a remote command ID for every session.

## Active Charging and Metering

Facts can change independently:

```text
station connected / disconnected
connector occupied
transaction active
energy flowing / paused
charging profile applied
meter data fresh / stale
session update delivered / pending
cost estimated / unknown
```

A cached status or meter value is not current without its observation time.

Meter ingestion pipeline:

```text
raw protocol message
  -> authenticated source
  -> deduplication and ordering checks
  -> raw evidence retention where required
  -> unit normalization
  -> validation / anomaly detection
  -> transaction attribution
  -> aggregates and session projection
  -> outbound session update
```

Never discard source unit, timestamp, measurand, phase/context, or provenance when needed for audit.

## Stop, Finalization, and Settlement

```text
Transaction ended
  -> final meter evidence may still arrive
  -> CPO operational session finalized
  -> CDR generated or awaited
  -> eMSP validates and ingests CDR
  -> settlement becomes billable
  -> invoice allocation occurs
  -> payment/reimbursement settles later
```

Use independent state dimensions:

```text
operation = STOPPED
metering = FINAL_OR_PROVISIONAL
cdr = NOT_RECEIVED / RECEIVED / REJECTED / CORRECTED
settlement = PENDING / CONFIRMED / DISPUTED
billing = UNBILLED / INVOICED / ADJUSTED
payout = NOT_APPLICABLE / PENDING / PAID / REVERSED
```

## Corrections and Late Arrivals

```text
Session stopped at T0
  -> provisional display
  -> settlement v1 at T1
  -> invoice or ledger posting
  -> correction v2 at T2
  -> delta/reversal/new posting
  -> downstream notifications and audit
```

Rules:

- Operational completion does not imply financial finality.
- Store the settlement/CDR identity and version or supersession chain.
- Apply only newer authoritative corrections.
- Make correction handling idempotent.
- Re-run affected downstream calculations deterministically.
- Never mutate an issued invoice silently.
- Define a dispute/manual-review path for impossible or stale corrections.
- Treat any fixed settlement window as vendor/contract-specific.

## Payment-Terminal and Ad-Hoc Charging

A payment-terminal session can be related to, but is not identical to, the charging session.

```text
Payment intent / pre-authorization
  -> payment credential accepted
  -> charging authorization
  -> station transaction
  -> charging session
  -> final amount
  -> capture / adjustment / release / refund
```

Preserve separate identities and states for payment and charging. A successful card tap does not prove charging started; a completed charge does not prove capture succeeded.

Check:

```text
pre-authorization amount and expiry
partial/final capture
incremental authorization
currency
failed capture after charging
refund and correction behavior
chargeback evidence
privacy boundary for payment data
RFID presented to a multi-purpose terminal
```

## Roaming Synchronization Lifecycle

```text
credentials and version negotiation
  -> initial paginated pull
  -> local source-attributed projection
  -> incremental pushes
  -> deduplication / last-updated checks
  -> outage
  -> reconciliation pull
  -> conflict handling
```

A local copy does not become authoritative merely because it is persisted. Preserve owner, source party, protocol version, external identity, and last synchronization evidence.

## Smart-Charging Lifecycle

```text
driver / EMS / grid constraint
  -> business charging objective
  -> site capacity and policy resolution
  -> station-capability translation
  -> version-specific OCPP profile/limit
  -> station response
  -> observed power and energy
  -> feedback/recalculation
```

Requested power is not delivered power. Store request, accepted/applied representation, effective interval, limiting source, station capability, and observed outcome separately.

## Lifecycle Review Format

When explaining or reviewing a flow, output in this order:

1. **Assumptions** — protocol versions, actors, topology.
2. **Relationship slice** — only relevant entities and ownership.
3. **Sequence** — physical, business, domain, and protocol facts.
4. **State vector** — independent operational and financial states.
5. **Evidence** — what proves each important transition.
6. **Failure matrix** — timeout, duplicate, late, out-of-order, offline.
7. **Persistence and correlation** — durable IDs and snapshots.
8. **Tests** — happy path plus adversarial cases.

A useful failure matrix:

| Boundary | Failure | Durable state | Retry owner | Reconciliation |
|---|---|---|---|---|
| app → eMSP | duplicate start tap | one operation by idempotency key | client/eMSP contract | return existing operation |
| eMSP → CPO | timeout | outcome unknown | defined command owner | poll/callback/reconcile |
| CSMS → station | disconnect | pending or unknown | CSMS policy | reconnect and observe events |
| CPO → eMSP | duplicate callback | already-applied version | CPO delivery | idempotent consumer |
| CDR → billing | correction | supersession chain | source party | adjustment ledger |

## Lifecycle Test Pack

For every implemented lifecycle include:

```text
happy path
rejection at each boundary
timeout before and after remote acceptance
duplicate request and duplicate event
out-of-order event
late success after local timeout
restart during pending operation
station disconnect/reconnect
missing or stale meter data
wrong tenant/account/resource correlation
late CDR
corrected settlement
currency/unit mismatch
historical data after infrastructure removal
```
