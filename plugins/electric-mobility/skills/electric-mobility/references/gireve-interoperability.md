# Gireve Interoperability Playbook

Use this reference when connecting a CPO, eMSP, CPMS/CSMS, or multi-role platform to Gireve.

Gireve is a roaming hub and integration partner. Its implementation guide and onboarding rules can add constraints or extensions around OCPI. Keep three layers separate:

```text
OCPI standard for the selected version
Gireve implementation profile for the selected guide version
bilateral commercial/onboarding configuration for this operator
```

Never present a Gireve requirement or extension as universal OCPI behavior.

## 1. Required Source Order

Before implementation, obtain and record:

1. selected OCPI version;
2. exact Gireve implementation-guide title, version, and publication date;
3. onboarding/environment documentation supplied for the connection;
4. assigned platform/operator/party identities;
5. enabled role: CPO, eMSP, or both;
6. required and optional use cases/modules;
7. commercial roaming offer and B2B tariff rules;
8. test/certification plan and production acceptance criteria.

Use current official Gireve sources from [gireve.com/download](https://www.gireve.com/download/) and connection-specific material supplied by Gireve. Do not implement from an old guide or this skill alone.

## 2. Build a Conformance Matrix

For every module/operation, maintain:

| Concern | OCPI standard | Gireve profile | Our implementation | Evidence/test |
|---|---|---|---|---|
| Credentials/Versions | selected spec behavior | guide delta | endpoint/config | test case |
| Locations | sender/receiver contract | required fields/frequency | mapper/sync | payload evidence |
| Tokens/Authorize | standard flow | hub constraints/extensions | auth service | roaming scenario |
| Commands | async command contract | supported command profile | operation mapping | callback test |
| Sessions | update contract | timing/store-forward rules | session publisher | outage test |
| CDRs | CDR contract | content/frequency/correction rules | settlement exporter | duplicate/correction test |
| Tariffs | tariff contract | B2B/publication rules | tariff projection | price scenario |

A successful HTTP exchange is not conformance evidence by itself.

## 3. Hub Topology and Ownership

```text
Our CPO role
  -> publishes CPO-owned Locations, Tariffs, Sessions, and CDRs
  -> receives/uses eMSP authorization data and Commands as applicable

Our eMSP role
  -> publishes eMSP-owned Tokens/authorization capability as applicable
  -> consumes Locations/Tariffs/Sessions/CDRs
  -> initiates Commands

Gireve hub
  -> routes, validates, profiles, and may provide store-and-forward behavior
  -> does not automatically become owner of each party's domain object
```

Verify ownership and sender/receiver directions per module and selected version. In a multi-role platform, isolate CPO and eMSP projections and credentials even if they share a tenant.

## 4. Identity and Routing

Model identities explicitly:

```text
internal tenant/account ID
OCPI country_code + party_id + role
Gireve platform/operator identifiers where assigned
source party
counterparty/destination party
external object ID
connection/environment
protocol and guide version
```

Do not assume an object ID is globally unique. Do not derive routing solely from an RFID prefix, hostname, or database tenant without the configured party context.

Where the current guide specifies additional correlation/request headers or routing identifiers, implement them in the Gireve adapter and propagate safe correlation into logs. Verify exact names and requirements from the selected guide rather than memory.

## 5. Connection and Environments

Treat each environment as an independent connection:

```text
credentials
base URLs/version endpoints
party identities
allowed modules/roles
certificates/secrets
IP/network constraints if any
rate/pagination limits
test data
monitoring and alerting
```

Never reuse production credentials in test. Support credential rotation and version endpoint changes without redeploying hardcoded secrets.

Connection state should include:

```text
CONFIGURED
REGISTERING
ACTIVE
DEGRADED
SUSPENDED
ROTATING_CREDENTIALS
FAILED
```

These are application states, not OCPI enums.

## 6. Locations and Tariffs

For a CPO connection:

- separate static site/topology data from dynamic EVSE status;
- preserve OCPI identity and `last_updated` semantics for the selected version;
- validate all Gireve-required fields and publication rules before sending;
- define whether tariff attachment occurs at Location, EVSE, or Connector according to the selected profile;
- snapshot and version tariff publication;
- detect rejected or partially synchronized objects;
- reconcile through supported pull/store-forward mechanisms after outages;
- retain historical references when infrastructure is unpublished or removed.

For an eMSP connection:

- ingest source-attributed locations without claiming ownership;
- process pagination/deltas safely;
- protect against stale/out-of-order updates;
- maintain searchable read models separately from raw partner projections;
- display tariff source, currency, tax context, restrictions, and freshness.

Do not encode one Gireve guide's required fields into universal OCPI DTOs. Use profile validation or an adapter layer.

## 7. Tokens and Authorization

Model:

```text
credential/token publication strategy
authorization request
Gireve routing/correlation
CPO decision
station authorization result
session/CDR authorization reference
```

Verify from the selected guide:

- push/pull or real-time authorization expectations;
- mandatory contextual Location/EVSE/Connector references;
- any Gireve-specific authorization or correlation extension;
- timeout and offline behavior;
- token update/block propagation;
- allowed token types and identifier constraints.

Do not download or replicate all tokens merely because an endpoint exists if the selected profile recommends or requires another authorization strategy.

## 8. Commands

```text
eMSP command
  -> Gireve routing
  -> CPO command receiver
  -> durable internal operation
  -> OCPP version-specific station command
  -> station response/event
  -> Gireve/OCPI callback
  -> eMSP operation/session update
```

Check the profile's supported commands, required request context, callback behavior, timeout, and any extension fields.

Never map immediate Gireve/OCPI acceptance to “charging started.” Preserve:

```text
OCPI command identity
Gireve/request correlation
internal operation ID
OCPP message ID
station transaction identity
session identity
callback attempts
```

## 9. Sessions, CDRs, and Store-and-Forward

Design for temporary hub or partner outage:

```text
committed domain fact
  -> durable outbound record
  -> send attempt
  -> HTTP and OCPI result validation
  -> retry according to profile
  -> acknowledgement
  -> reconciliation
```

For Sessions:

- distinguish live operational updates from final commercial data;
- respect profile frequency/minimum-interval rules;
- coalesce updates only when permitted without losing final transitions;
- make PUT/PATCH behavior version- and profile-correct;
- ensure final session state can be reconstructed after missed updates.

For CDRs:

- use stable idempotency identity;
- retain exact outbound payload and response evidence as policy permits;
- validate required location, token, tariff, energy, time, cost, tax, and signed-data information;
- process duplicates without duplicate billing;
- implement Credit CDR or the correction mechanism required by the selected standard/profile;
- reconcile accepted technical delivery with commercial settlement separately.

Any store-and-forward behavior must be verified against the selected Gireve guide; do not invent retry semantics.

## 10. Multi-Tenant and Multi-Role Platforms

A shared Gireve adapter must not leak data between operators.

```text
Inbound request
  -> authenticate connection/environment
  -> resolve OCPI party and role
  -> resolve internal tenant
  -> authorize module and object scope
  -> process with tenant-scoped repositories
  -> respond with selected version/profile
```

Test:

- same external object ID under different parties;
- one tenant with CPO and eMSP roles;
- wrong party path/body identity;
- credential mapped to wrong environment;
- cross-tenant pagination cursor reuse;
- callback URL/correlation mix-up;
- logs and metrics without sensitive or cross-tenant payloads.

## 11. Adapter Architecture

```text
Official OCPI DTO/version contract
              |
       standard validation
              |
      Gireve profile adapter
      ├── extra validation
      ├── supported-use-case gates
      ├── extension mapping
      ├── headers/correlation
      └── retry/store-forward policy
              |
       application services
              |
          domain model
```

Do not scatter `if partner == GIREVE` through controllers, domain entities, and billing logic. Keep partner profile behavior isolated and testable.

## 12. Operational Dashboard

Expose per environment, party, role, and module:

```text
connection/credential status
last successful inbound/outbound call
last full and incremental synchronization
queue depth and oldest pending age
retry and rejection counts
schema/profile validation errors
object lag by module
command callback latency
late/missing CDR count
correction and reconciliation backlog
```

Provide redacted request/response evidence and correlation search for support. Alert on freshness and backlog, not only HTTP error rate.

## 13. Test and Certification Pack

### Contract tests

- exact selected OCPI schemas and response envelopes;
- Gireve profile-required fields and extension handling;
- headers, identity/routing, pagination, and errors;
- sender and receiver interfaces for enabled roles.

### Scenario tests

```text
CPO Location/Tariff publication and update
eMSP Location/Tariff ingestion
RFID authorization through the hub
remote start and async result
remote stop and final session
session updates during hub outage
CDR delivery, duplicate, rejection, and correction
token block propagation
credential rotation
multi-tenant/multi-role routing
```

### Failure tests

- HTTP success with non-success OCPI envelope;
- malformed or profile-incomplete payload;
- timeout before/after remote acceptance;
- duplicate and out-of-order update;
- rate/pagination limit;
- expired or wrong-environment credentials;
- callback failure;
- restart with pending store-and-forward work;
- hub recovery and reconciliation.

Retain certification evidence by guide version so a later profile update can be assessed as a controlled migration.

## 14. Gireve Quality Gate

```text
[ ] OCPI version recorded
[ ] Exact Gireve guide version/date recorded
[ ] CPO/eMSP roles and required use cases confirmed
[ ] Standard/profile/bilateral differences documented
[ ] Party/platform identities and routing tested
[ ] Profile behavior isolated in adapter
[ ] Locations/Tariffs synchronization and rejection recovery tested
[ ] Token/authorization strategy confirmed
[ ] Commands correlated through station evidence and callback
[ ] Sessions/CDRs survive outage, retry, duplicate, and restart
[ ] Corrections do not duplicate or silently rewrite billing
[ ] Multi-tenant and multi-role isolation tested
[ ] Credential rotation and environment separation tested
[ ] Operational dashboard exposes lag, backlog, and failures
[ ] Certification evidence retained
[ ] Production behavior verified against current official documentation
```
