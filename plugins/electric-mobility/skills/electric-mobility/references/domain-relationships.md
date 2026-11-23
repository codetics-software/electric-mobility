# Electric-Mobility Domain Relationships

Use this reference when designing schemas, APIs, services, event models, permissions, or explaining how charging concepts relate.

This is a vendor-neutral reasoning model, not a protocol specification. Names, cardinalities, and ownership differ by product and protocol version; verify them against the target system.

## Start With Relationships, Not Tables

Before naming entities or fields, write a relationship ledger:

| Subject | Relationship | Object | Cardinality | Owner / authority | Lifecycle coupling | Historical rule |
|---|---|---|---|---|---|---|
| Provider / tenant | contains | Account | 1:N | platform tenant | account cannot cross tenant | retain tenant attribution |
| Account | includes | User membership | 1:N or M:N | account / IAM policy | membership can end independently | retain actor audit trail |
| Location | contains | EVSE | 1:N | CPO | current topology changes | sessions keep snapshots/references |
| EVSE | exposes | Connector | 1:N | CPO / CSMS | connector may be replaced | do not rewrite historical records |
| Credential | identifies | charging contract or principal | context-dependent | issuer | validity changes independently | retain presented identity evidence |
| Authorization | permits or rejects | charging attempt | N:1 attempt | decisioning party | ephemeral decision | persist evidence and reason |
| Session | records | charging activity | 1 per logical charging cycle | operational data owner | mutable while active | freeze/audit final facts |
| CDR / settlement record | settles | session | usually 1:N over corrections | issuing CPO / settlement source | arrives after operation | append/version corrections |

If the ledger is ambiguous, the schema is not ready.

For each relationship establish:

```text
cardinality
ownership
source of truth
scope of identity
creation authority
mutation authority
visibility
lifecycle dependency
historical retention
financial responsibility
protocol representation
```

Never infer ownership from a foreign key. Storage location is not authority.

## Three Graphs, Not One

A charging platform contains at least three overlapping graphs. Do not collapse them.

### Organizational graph

```text
Platform
  └── Provider / Tenant
        └── Account
              ├── User memberships
              ├── roles and grants
              ├── charging credentials
              ├── vehicles
              ├── owned or managed sites
              └── billing arrangements
```

### Physical and operational graph

```text
Location / Site
  └── Charging Station
        └── EVSE
              └── Connector

Charging Station
  └── protocol connection / controller identity
        └── capabilities, configuration, commands, telemetry
```

### Commercial and roaming graph

```text
Driver / contract
  └── credential
        └── authorization
              └── session
                    ├── charging periods and meter evidence
                    ├── applied tariff snapshot
                    └── CDR / settlement versions
                          ├── customer charge
                          ├── CPO receivable
                          ├── platform fee
                          ├── reimbursement
                          └── invoice allocation
```

These graphs intersect, but their edges mean different things. An Account may pay for a session without owning the station. A User may operate a station without being the contractual debtor. A CPO may own Location data while an eMSP stores and displays a synchronized copy.

## Actor, Role, Tenant, Account, and User

Do not use these terms interchangeably.

- **Actor**: a participant in a flow, such as CPO, eMSP, CSMS, hub, driver, station, or payment provider.
- **Role**: behavior in a protocol or business interaction. One company may perform multiple roles.
- **Provider / tenant**: an isolation and configuration boundary in a multi-tenant platform.
- **Account**: a contractual, organizational, or billing unit inside a tenant.
- **User**: a human identity or login.
- **Membership**: the relationship giving a User access to an Account, often with roles or grants.

Prefer a membership model when a person can belong to multiple accounts:

```text
User 1 ── N AccountMembership N ── 1 Account
                    └── roles / grants / status
```

Do not copy account-scoped roles onto the global User unless the product guarantees one account per user.

Ask:

```text
Can one legal organization have several accounts?
Can one user access several accounts?
Is billing account-scoped or user-scoped?
Can resources move between accounts?
What happens to audit history after membership removal?
Which boundary enforces tenant isolation?
```

## Charging Infrastructure

Avoid assuming a universal hardware hierarchy. Product language, OCPI, OCPP 1.6, and OCPP 2.x do not always align perfectly.

Use explicit concepts:

- **Location / Site**: driver-facing geographic place and access context.
- **Charging Station / Charge Point**: deployed equipment or station-level aggregate.
- **Protocol identity / controller**: endpoint connected to the CSMS. It may map 1:1 to a station, but verify it.
- **EVSE**: independently managed electrical charging supply unit in the relevant model.
- **Connector**: physical interface or connector metadata beneath an EVSE.

Model mappings rather than hiding ambiguity:

```text
Location 1 ── N Station
Station 1 ── N EVSE
EVSE 1 ── N Connector
Station 1 ── ? OCPP connection identity
```

Keep these dimensions separate:

```text
static identity and topology
technical connectivity
operational availability
administrative status
maintenance state
commercial availability
roaming publication state
```

A connected station can have an unavailable EVSE. A public Location can contain a connector excluded from roaming. A removed current resource can still appear in historical sessions.

### Live references versus snapshots

Use live references for current management. Use snapshots for historical and financial evidence.

```text
Session.startedAtLocationId   -> live/internal lookup
Session.locationSnapshot      -> what was known during charging
CDR.tariffSnapshot            -> price evidence used for settlement
CDR.credentialSnapshot        -> authorization evidence safe for retention
```

Do not make a historical invoice change because a Location address, account name, or tariff was edited later.

## Credential, Card, Token, Contract, and Authorization

These are separate concepts:

- **Credential medium**: RFID card, key fob, app identity, contract certificate, bank card, QR flow, or another presented medium.
- **Card**: physical or virtual product representation, fulfillment object, or user-facing artifact.
- **Token / identifier**: protocol or platform identifier used to recognize a charging principal.
- **Contract**: commercial relationship under which charging can be billed.
- **Authorization**: a context-specific decision for a charging attempt.
- **Assignment**: relationship attributing a credential to a User, Account, Vehicle, or contract.

```text
Account / contract
  └── CredentialAssignment
        ├── User or Vehicle
        └── Credential
              ├── medium
              ├── identifier(s)
              ├── issuer
              ├── lifecycle status
              └── roaming publication state

Credential + charging context + policy
  └── AuthorizationDecision
        ├── accepted / rejected
        ├── reason
        ├── decision source
        ├── correlation reference
        └── expiry / constraints
```

Sharp rules:

- A recognized credential is not automatically authorized.
- A valid token is not proof of an active contract in every context.
- A physical card and its wire-protocol token need not share a lifecycle.
- Blocking should usually be reversible; deletion should not erase audit history.
- Do not use raw credential secrets as public database identifiers.
- Preserve issuer and scope; identifier strings are rarely globally unique by themselves.

## Authorization, Command, Transaction, Session, and CDR

Do not build one giant `ChargingSession` row that represents every fact.

```text
ChargingIntent
  └── AuthorizationDecision
        └── RemoteCommand or local station action
              └── Station protocol transaction/events
                    └── Operational Session
                          └── CDR / settlement record(s)
                                └── Invoice line(s) / reimbursement
```

These may have different identifiers and clocks.

Important non-equivalences:

```text
command accepted          != physical action completed
authorization accepted    != transaction started
transaction started       != energy flowing
station stopped           != final cost known
session completed         != CDR received
CDR received              != invoice issued
invoice issued            != settlement paid
```

Persist correlation edges explicitly:

```text
client_reference
command_id
OCPI command correlation
OCPP message_id
station transaction identity
internal session_id
external session_id
CDR identity
settlement version
invoice_line_id
```

Do not correlate financial records with timestamps alone.

## One Physical Charge, Multiple Views

A single real-world charging event can produce several records:

```text
Physical charging event
  ├── station transaction view
  ├── CPO operational session
  ├── eMSP customer session
  ├── roaming-hub routing/audit record
  ├── CDR / settlement record
  ├── payment-provider transaction
  └── invoice and reimbursement lines
```

Do not force all views to share one identifier or status enum.

For every view record, store or derive:

```text
view owner
source party
counterparty
external identity
internal correlation identity
protocol and version
state authority
money authority
last observed time
```

A CPO session and an eMSP session may refer to the same charge but differ in data ownership, customer context, prices, taxes, timing, and correction behavior.

## Session State Is Multidimensional

Prefer a state vector over one overloaded status:

```text
command_state
station_transaction_state
energy_delivery_state
operational_session_state
settlement_state
billing_state
reimbursement_state
sync_state
```

Example:

```text
station_transaction_state = ENDED
operational_session_state = STOPPED
settlement_state = PENDING
billing_state = NOT_BILLABLE
```

Vendor APIs may publish a convenient aggregate state machine such as pending → starting → started → stopping → stopped → settled. Treat it as a vendor contract, not a universal OCPI or OCPP state model.

## Metering, Tariff, Price, Settlement, and Invoice

Keep evidence and calculations separate:

```text
MeterObservation
  └── normalized measured quantities

TariffDefinition
  └── prospective pricing rules

AppliedTariffSnapshot
  └── rules selected for this charge

PriceCalculation
  └── deterministic calculation result and trace

CDR / Settlement
  └── counterparty's final or corrected commercial record

InvoiceLine
  └── accounting allocation in a billing period
```

Do not overwrite raw meter evidence with normalized or corrected values. Keep provenance.

Model a financial ledger of obligations:

```text
customer owes eMSP
eMSP owes CPO or hub
CPO owes site host reimbursement
platform charges subscription or transaction fee
tax authority is owed tax
payment provider captures or refunds funds
```

Each edge needs creditor, debtor, amount, currency, basis, tax treatment, status, source record, and correction chain.

### Corrections

Settlement can arrive late and can be corrected after initial completion. Prefer versioned or append-only treatment:

```text
Settlement v1
  └── superseded by Settlement v2
        └── delta posted to downstream ledger
```

Never silently mutate already-invoiced facts. Define whether a correction causes recalculation, a debit/credit note, a future-invoice adjustment, or manual review. Any concrete correction window or settlement counter is vendor-specific unless a governing contract or protocol says otherwise.

## Groups, Policies, and Tariff Selection

Many platforms separate *which infrastructure* a policy covers from *which customer* a rule matches.

```text
ChargingGroup
  └── selects connectors by connector, location, account, tags, or filters

CustomerGroup
  └── selects credentials, contracts, accounts, or user categories

ChargingPolicy
  ├── applies to ChargingGroup(s)
  └── contains TariffRule(s)
        ├── matches CustomerGroup(s)
        ├── may match payment or authorization channel
        └── references or embeds TariffConfiguration
```

Establish:

```text
Are rules first-match, best-match, or compositional?
Can charging groups overlap?
How are conflicts resolved?
Is policy order public and deterministic?
Are updates full replacement or patch?
What happens when a referenced group is deleted?
When is the selected tariff snapshotted?
```

Sharp defaults:

- Most-specific-first is only correct if the contract defines first-match semantics.
- Detect and report overlapping infrastructure selectors.
- Do not rely on hidden database ordering to resolve policy conflicts.
- Full-replacement APIs must be named and tested as replacement; omitted children may be destructive.
- Historical sessions keep applied policy/tariff evidence when groups later change.

## IAM Versus Charging Access

```text
IAM role / grant
  -> who may call an API or administer data

Charging access policy / access group
  -> which credential or principal may use which EVSE under which conditions
```

Do not use the same table or enum for both.

For charging access, establish member type, resource scope, time restrictions, priority, pricing relationship, offline behavior, revocation propagation, validity interval, and audit source.

## Deletion, Blocking, and Historical Retention

| Operation | Meaning | Typical historical behavior |
|---|---|---|
| Disable / block | Temporarily prevent future use | retain entity and references |
| Expire | Validity ended by time | retain evidence |
| Unpublish | Stop sharing externally | retain internal entity |
| Detach / unassign | Remove a relationship | retain assignment history where relevant |
| Soft delete | Remove from active use and discovery | retain row and historical references |
| Hard delete | Erase data | only when safe/legal and not needed for audit |
| Supersede | Replace immutable/versioned fact | retain correction chain |

Ask separately whether it can authorize future charging, appear in searches, be shared with partners, resolve historical sessions, support invoices, or require erasure/pseudonymization.

## Required Schema/API Review Format

When reviewing a schema or API, first use:

| Current model | Better model | Why |
|---|---|---|
| `session.status = COMPLETE` | separate operational, settlement, and billing states | physical stop and financial finality occur at different times |
| `token.user_id` | explicit credential assignment with account/contract scope | credentials can be reassigned or scoped differently |
| CDR points only to mutable tariff | immutable applied-tariff snapshot | later tariff edits must not rewrite history |

Then provide the affected relationship ledger and invariants.

Useful invariants:

```text
Every tenant-scoped object belongs to exactly one tenant boundary.
Every external identifier is unique only within its documented scope.
Historical financial records resolve without mutable current data.
No accepted command is treated as proof of observed charging.
Every correction points to the fact it supersedes.
Every money amount has a currency and provenance.
Every measured value has a unit, timestamp, and source.
Deleting current infrastructure never cascades into CDR deletion.
```

## Domain Modeling Checklist

```text
[ ] Actors and protocol roles identified
[ ] Tenant and account boundaries identified
[ ] Relationship ledger written
[ ] Cardinalities verified
[ ] Owner and source of truth identified per entity
[ ] Internal and external identities separated
[ ] Current references and historical snapshots separated
[ ] Credential, authorization, command, session, and CDR separated
[ ] Physical, operational, and commercial graphs separated
[ ] State represented as independent dimensions where needed
[ ] Correction and late-arrival behavior defined
[ ] Debtor, creditor, and reimbursement relationships explicit
[ ] Deletion/blocking/unpublishing semantics distinct
[ ] Multi-tenant authorization enforced on every traversal
[ ] Protocol-specific DTOs kept outside the domain model
[ ] Invariants and adversarial tests defined
```
