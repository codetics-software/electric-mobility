# Answer formats and task template

Load this only for a full architecture, product, schema, implementation, debugging, or protocol answer.
Working rules are in `SKILL.md`. Agent responsibilities stay separate from OCPI market roles,
sender/receiver interfaces, and application permissions.

Task block for assigning work to any assistant:

```text
This is your work to be done. Listen to us.

[Describe the requested work, project context, deliverables, and constraints here.]
```

When the host cannot inspect files, run commands, or generate artifacts, provide the concrete deliverable
it can produce and state which validation remains. Do not delegate, deploy, publish, or change external
systems because a reference suggests it.

### Architecture questions

Answer in this order:

```text
Protocol boundary
Actors and roles
Relationship slice and cardinalities
Ownership and source of truth
Identity scopes
Data flow
State vector and evidence
Failure handling
Persistence and historical snapshots
Financial relationships
Security
Implementation recommendation
```

### Full product and supervision questions

Read `references/full-platform-blueprint.md` and `references/supervision-and-client-apps.md`. Also load `references/gireve-interoperability.md` for Gireve work and the applicable OCPI/OCPP references.

Answer in this order:

```text
Product roles: eMSP, CPO, CSMS, hub-facing, or combined
Users and product surfaces: backend, web, iOS, Android, partner APIs
Protocol/version and partner profile assumptions
Capability map and missing full-cycle responsibilities
Domain modules and ownership
End-to-end charging, metering, settlement, and billing flows
Architecture for the selected language/runtime, including Java, Kotlin, C#/.NET, Swift, and web as applicable
Real-time, offline, recovery, and supervision UX
Security, tenancy, audit, and privacy
Interoperability, Gireve conformance, and certification
Vertical delivery slices
Contract, simulator, integration, mobile, and end-to-end tests
Operations, observability, deployment, and reconciliation
```

Do not stop at backend protocol adapters. A full product answer must account for operator and driver workflows, truthful UI state, mobile lifecycle recovery, billing finality, partner operations, and production support.

### Schema and API model questions

Read `references/domain-relationships.md`, then answer in this order:

```text
Assumptions and terminology
Current model -> better model -> why table
Relationship ledger
Organizational, physical, and commercial graph slices
Identity and ownership rules
Lifecycle and state dimensions
Live references versus historical snapshots
Deletion, correction, and late-arrival behavior
Invariants
Migration and tests
```

Do not produce tables or classes before explaining why each entity has a distinct identity, lifecycle, authority, or audit purpose.

### Implementation questions

Answer in this order:

```text
Security preflight (S2 and S3 tasks)
Where the code goes: module, layer, transaction boundaries
Version assumptions
Protocol operation
Message/endpoint mapping
Implementation
Error handling
Timeouts
Idempotency
Tests, including abuse cases
Interoperability caveats
Vulnerability check for changed dependencies
Remaining security risks
```

### Debugging questions

Answer in this order:

```text
Failure classification
Evidence
Concrete checks
Likely causes
Fix
Regression test
```

### Protocol questions

Start with the smallest useful conceptual model.

Then explain:

```text
roles
lifecycle
messages
ownership
state
edge cases
```

Do not overwhelm a simple question with every protocol module.
