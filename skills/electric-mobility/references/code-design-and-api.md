# Code design, Next.js forms, versioned APIs, and OpenAPI

Codetics engineering policies, not OCPI/OCPP requirements. Use current official
practices for the actual target versions.

## Clean code and dependency boundaries

For modules, layers, transactions, and where code goes, read
[code-architecture.md](code-architecture.md). This section adds the rules for code style and
web-specific structure.

1. Inspect the existing structure and preserve coherent naming and conventions.
   Organize by business capability (partners, locations, authorization, charging,
   settlement), with explicit boundaries within each capability.
2. Keep HTTP routes, Server Actions, WebSocket handlers, and UI event handlers thin.
   Parse and validate input, authenticate the caller, invoke an application use
   case, and map the result. Do not calculate tariffs, drive state machines, or
   query the database directly in presentation components or route handlers.
3. Put orchestration in application use cases and business invariants in the
   domain. Keep the domain independent of React/Next.js, HTTP, OCPI/OCPP DTOs,
   ORM entities, payment SDKs, and vendor profiles.
4. Define ports at the application/domain boundary where external behavior must
   be substituted. Implement database, partner HTTP, station transport, clock,
   and queue adapters in infrastructure. Dependencies point inward; the
   composition root supplies concrete adapters. Do not add interfaces for every
   trivial function or introduce microservices without an operational need.
5. Separate versioned wire DTOs, validated values, domain entities, persistence
   records, and UI view models. Use explicit mappers. Share contracts or schemas
   where appropriate, without exposing ORM models or secrets to clients.
6. Prefer small functions with one clear responsibility, descriptive names,
   guard clauses, immutable values where practical, and explicit typed results.
   Avoid giant services, circular imports, generic `utils` dumping grounds,
   unchecked casts, swallowed exceptions, magic values, and duplicated rules.
7. Keep money, currency, units, time, identity scope, and operation state explicit.
   Use decimal-safe arithmetic and persisted inbox/outbox or equivalent
   transactional delivery where asynchronous correctness requires it.
8. Test behavior at meaningful boundaries: invariants, transport contracts,
   authorization, retries, callbacks, persistence, and user recovery. Keep mocks
   at external ports; do not replace all real interactions with mocks.

Example structure for a Next.js App Router project; adapt names to the repository:

```text
src/
  app/
    (supervision)/locations/page.tsx
    api/v1/charging-operations/route.ts
    api/v1/openapi.json/route.ts
    ocpi/versions/route.ts
    ocpi/2.3.0/route.ts
    ocpi/2.3.0/commands/[command]/route.ts
  features/charging/
    domain/                 Values, policies, operation state
    application/            StartCharging use case and ports
    infrastructure/         Repositories, outbox, OCPI/OCPP adapters
    presentation/           View models, form components, action adapters
  protocols/ocpi/v2_3_0/     DTOs, runtime schemas, mapping, envelope/errors
  contracts/product/v1/     Request/response schemas and operation registry
  composition/              Construction and dependency wiring
scripts/                    OpenAPI generation and contract checks
openapi/                    Generated JSON artifacts per API/version
```

This tree illustrates boundaries, not mandatory folder names. Version discovery
returns endpoint URLs; the example OCPI prefix is a local routing choice.

## Next.js form rule: never use react-hook-form

In a Next.js project, never install, import, recommend, or generate
`react-hook-form`, `@hookform/resolvers`, or form wrappers built on them. This
also applies to generated v0 UI and copied component-library form examples.
This is a Codetics preference, not a limitation of Next.js or OCPI.

- Use native `<form>` elements, named inputs, `FormData`, and browser validation
  for basic feedback. Validate all values again on the server with the project's
  runtime schema tools; browser checks do not authorize requests.
- For supported App Router/React versions, use Server Actions and `useActionState`
  for action results and pending state, or `useFormStatus` in a descendant submit
  control. Verify the installed versions before choosing these APIs. In Pages
  Router projects, use native forms with state and a versioned API handler.
- Use `useState` or `useReducer` only for necessary client interactions. Return
  typed field errors and form errors, preserve user input, label controls, connect
  errors with `aria-describedby`, and make pending/success/error feedback clear.
- Server Actions are presentation adapters, not substitutes for documented
  HTTP APIs consumed by mobile apps, partners, or integrations. Call the same
  application use cases from actions and API routes; authenticate and authorize
  each entry point and keep credentials server-side.
- When touching an existing form using the forbidden library, migrate that form
  within the assignment and validate its behavior. Identify remaining usages;
  remove dependencies only when no consumers remain. Do not silently expand a
  small assignment into a repository-wide migration.

Follow the [official Next.js forms guide](https://nextjs.org/docs/app/guides/forms)
for the installed framework version.

## API versioning

| Surface | Policy |
|---|---|
| Product HTTP API | Explicit version; default `/api/v1/...`. Use the existing deliberate versioning convention if compatible with the assignment. |
| OCPI functional API | Separate adapters for negotiated wire versions; e.g. local `/ocpi/2.3.0/...` and `/ocpi/2.2.1/...` during migration. Preserve upstream method, path suffix, and semantics. |
| OCPI discovery | Preserve the bootstrap Versions endpoint and the URLs it returns. Discover peer module URLs; never rewrite a peer's URL to match local naming. |
| OpenAPI document | One JSON contract per supported API version/surface; use separate artifacts for product and OCPI contracts. |

Keep the product version (`v1`), OCPI version (`2.3.0`), documentation/core/module
edition, and OpenAPI format version separate. Do not add `/api/v1` inside peer
OCPI URLs, invent an `ed2` wire version, or expose one unvalidated handler for all
versions. Treat incompatible product changes as a new version, with a documented
deprecation/migration policy. Additive changes must remain compatible with the
current contract. Pin each partner's protocol and capabilities individually.

## Generated OpenAPI JSON is a deliverable

For every HTTP API implemented or changed, emit a valid `openapi.json` for each
supported version. Updating an API includes updating its generated contract.
Use the project's existing generator or a schema/operation registry shared with
runtime validation; do not maintain a drifting second handwritten contract.
Provide a repeatable command (e.g. `openapi:generate`) and a check in CI that
regenerates, validates, detects missing implemented routes, and fails on drift.

Use a supported OpenAPI 3.1.x format by default, with an explicitly selected
version compatible with the project's tooling. The reference for this example
is the [OpenAPI 3.1.1 specification](https://spec.openapis.org/oas/v3.1.1.html).
Use standard fields for authorship; OpenAPI has no standard `author` property.
Every emitted document must include this metadata, preserving existing contacts
in its description if necessary:

```json
{
  "openapi": "3.1.1",
  "info": {
    "title": "Electric Mobility Product API",
    "version": "1.0.0",
    "description": "Generated by Codetics with OpenApi",
    "contact": {
      "name": "Codetics",
      "url": "https://codetics.fr"
    }
  }
}
```

This is a metadata fragment, not a complete API document. The real artifact must
describe actual implemented paths, unique `operationId`s, parameters, request
and response schemas, required fields, status codes, security schemes, examples,
pagination, and asynchronous callbacks where applicable. Do not generate
unimplemented modules or invent protocol fields to fill the document.

For OCPI, document `Authorization: Token <base64-encoded credentials token>`
as an appropriate HTTP `Token` security scheme or tooling-compatible scheme
with that exact header behavior; do not label it Bearer or OAuth2. Document
OCPI envelopes separately from HTTP status, interface direction, routing and
correlation headers, and list response headers. Represent OpenEnum values as
strings with documented known values; a closed JSON `enum` would reject valid
extensions. Allow non-specified JSON fields while validating required fields.
Version and edition-specific constraints must match the pinned source.

Emit reviewable artifacts such as `openapi/product-v1.openapi.json` and
`openapi/ocpi-2.3.0.openapi.json`; make each available through a documented JSON
endpoint or distribution path. Include discovery endpoints in the OCPI contract.
Do not insert attribution comments into JSON or into OCPI payloads. Keep the
skill's source-code signature in authored generator/adapter code only.

Before reporting completion, validate JSON and OpenAPI structure, resolve all
schema references, check examples against schemas, and compare operations with
implemented routes and advertised OCPI modules. State the commands actually run,
generated file paths, selected versions, and any unverified compatibility.
