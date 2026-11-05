# Building an OCPI module

Identify the version, read the [module reference](README.md#module-reference-files), then design
from it rather than from memory. Add `domain-relationships.md` for entities or ownership, and
`charging-lifecycles.md` for end-to-end operations. Verify normative details against the official
specification.

## Extract the contract first

Module, version availability, sender, receiver, data owner, object hierarchy, primary and nested
entities, enums, shared value objects, sender and receiver interfaces, HTTP methods, URL structure,
path parameters, request and response bodies, envelope, authentication, push, pull, pagination,
`last_updated` semantics, idempotency, reconciliation, version differences, and pitfalls.

## Entities and identity

"Create an OCPI entity" is ambiguous. Determine whether it means a protocol DTO, domain entity,
persistence entity, request or response DTO, value object, enum, or nested object. An OCPI object
should not automatically become a database entity.

```text
OCPI JSON -> protocol DTO -> validate -> application command -> domain -> persistence
persistence or domain -> OCPI mapper -> DTO -> JSON
```

Do not expose ORM annotations, lazy loading, database IDs, internal tenant fields, or
implementation-only properties through the API.

For each object ask: who assigns the ID, is it global or scoped, what is the composite identity, which
parent scopes the child, can the child be addressed alone, can it be updated or deleted, and can history
still refer to it? Preserve the Location > EVSE > Connector hierarchy instead of flattening it for schema
convenience.

## Sender and receiver

The sender interface reads the sender's data, and the receiver interface accepts pushes. For Locations, a
CPO needs its Sender interface and an eMSP its Receiver interface. Derive endpoints from this contract,
not from what looks RESTful.

## Synchronization

Implement the whole lifecycle: initial sync, paginated pull, persist, incremental push, `last_updated`
comparison, retry and idempotency, and reconciliation after an outage. A receiver must rebuild its state
after downtime, missed, duplicate, or out-of-order callbacks, partial sync, restart, and partner retry. Push
alone is not enough.

## Envelope

Use a dedicated protocol response with `status_code`, `status_message`, `timestamp`, and `data`, following
the selected version. Do not return framework shapes such as `{"success": true, "result": {}}`.

## Versions

Never create a universal DTO by unioning fields. Use version-specific DTOs mapped to a common domain, or a
common DTO with version-aware serialization and validation. A version-only field, enum, endpoint, or module
is not exposed in older contracts, silently reinterpreted, or dropped if dropping changes meaning.

## Outbound client

Treat the partner as unreliable. Define connection and read timeouts, TLS validation, authentication,
credential rotation, HTTP and OCPI status handling, retry policy, retryable versus non-retryable errors,
idempotency, rate limits, pagination, response validation, malformed payloads, 5xx, 4xx, and outage. HTTP 200
alone does not prove success: inspect the envelope and module result.

## Controllers

Controllers are protocol adapters: authenticate, deserialize, validate, call the application service, and map
the response. They contain no tariff calculation, session state machines, partner routing, CDR billing, or OCPP
orchestration, and never go straight from request to repository to response.

## Persistence

Persist protocol state needed for reconciliation, idempotency, retry, audit, history, cross-process operations,
and partner sync. Useful fields: `internal_id`, `tenant_id`, `protocol`, `protocol_version`, `country_code`,
`party_id`, `external_id`, `parent_external_id`, `last_updated`, source or owner, sync status, `created_at`,
`updated_at`. A unique identity may need tenant + protocol + version + country code + party ID + external ID.
Do not assume `external_id` alone is globally unique.

## Enums and time

Enums are wire contract: verify the version, keep unknown values safely where interoperability requires it, and
do not rename wire values to match language style. Map them explicitly instead of relying on a language's enum
name. Use timezone-aware types and UTC internally, never local server time as protocol time.

## Adapting existing code

Inspect structure and current version, classify existing classes, read the module reference, reuse what is sound,
and change only the necessary layers. Do not duplicate an entity because the protocol has a similar name. When code
conflicts with the reference, report current implementation, expectation, required change, reason, and
compatibility impact. Do not silently normalize it.

## Checklist

- [ ] Version, references, roles, ownership, entities, enums, and version-only fields identified
- [ ] Request and response DTOs, envelope, paths, methods, and authentication implemented
- [ ] Pagination, pull, push, `last_updated`, idempotency, retry, and recovery defined where required
- [ ] Domain separate from DTOs; persistence identity separate from OCPI identity; tenant isolation enforced
- [ ] Protocol errors mapped; unknown and invalid input handled
- [ ] Tests for serialization, contract, sync, duplicates and retries, and version differences
- [ ] Official specification checked for normative claims
