# Implementation, incident debugging, and security

Apply this guide to OCPI or OCPP code in Java, Kotlin, Swift, C#, Rust, Go, Python, and TypeScript. First read the applicable protocol/version reference. Match the existing framework and deployment model; the language notes below identify failure modes, not required libraries.

## Code boundaries that preserve protocol meaning

- Keep wire DTOs, validated protocol values, application commands, domain state, and persistence records separate. Include protocol version and partner/station identity in the adapter context.
- Validate on ingress before changing state: syntax/schema, message direction, identity scope, authorization, allowed state transition, units, and time. Validate egress against the recipient's negotiated version and capability.
- Persist an operation ID and protocol correlation ID before sending a remote command. Model `requested → accepted/rejected → observed outcome → reconciled/expired` with timestamps and evidence; avoid synchronous success booleans.
- Define deduplication keys at the owning boundary: OCPI party + module + object ID/version or command correlation; OCPP station + unique message ID for calls, and station + transaction ID + sequence/event evidence for transactions. A retry can have a new HTTP or WebSocket request ID while representing the same business operation.
- Preserve raw redacted evidence for diagnosis, the parsed message, schema/use-case validation result, and domain transition. Use separate event time and receive time. Store money as decimal/minor units with currency and tariff snapshot; annotate energy units and direction.
- Test actual boundaries with fixtures from the exact spec/schema: invalid enum, missing required field, tenant mismatch, replay, timeout, duplicate, reordered, reconnect, and late CDR/transaction correction. Avoid tests that merely reproduce the mapper implementation.

## Language-specific decisions

| Language | Use and checks |
|---|---|
| Java | In Spring or another stack, isolate WebSocket/HTTP handlers from blocking database work. Bound executors and queues; propagate cancellation/timeouts and correlation through async work. Use `BigDecimal` for money, `Instant`/`OffsetDateTime` for protocol time, and explicit JSON enum policy. Check transaction boundaries around inbox/outbox persistence. |
| Kotlin | Use structured concurrency for station calls; cancel pending work on disconnect without erasing persisted operation state. Avoid blocking coroutine event loops. Use sealed results for protocol rejection versus transport failure, `BigDecimal` for money, and explicit nullable/unknown wire fields. On Android, recover work after process death. |
| Swift | Use `Codable` DTOs with explicit coding keys and versioned enum fallback; keep actor-isolated socket/session state. Cancel tasks on disconnect, retain persisted operation status, and use `Decimal` for money. In SwiftUI, show confirmed versus pending charging state from backend evidence and handle background/resume lifecycle. |
| C# | In ASP.NET/.NET, use `CancellationToken`, bounded channels, and nonblocking WebSocket handlers. Use `decimal` for money, `DateTimeOffset` for timestamps, and explicit `System.Text.Json` converters for versioned enums. Persist operations with outbox/inbox semantics; keep EF entities separate from wire DTOs. |
| Rust | Use typed serde DTOs per protocol version and explicit unknown-value handling; avoid `unwrap` on untrusted wire data. Bound Tokio tasks/channels and guard connection ownership. Represent money and measured quantities with safe units/decimal types, and make retries idempotent at the storage boundary. |
| Go | Give each connection a clear read/write owner, bounded goroutine lifetime, `context` deadlines, and serialized writes where the WebSocket library requires them. Avoid `float64` for billed money. Validate JSON with the correct version schema and distinguish zero, missing, and null fields. |
| Python | In asyncio servers, keep blocking ORM and CPU-heavy validation off the event loop; set task timeouts and bound concurrency. Use `Decimal`, timezone-aware datetimes, and strict validated DTOs with explicit unknown-field policy. Persist command state before scheduling background work. |
| TypeScript | Validate runtime JSON even when compile-time types exist; generate/version types from the correct schema and narrow unknown enums at ingress. Use `bigint` or decimal libraries for monetary/minor-unit arithmetic, UTC-safe timestamp handling, abortable requests, and bounded WebSocket message queues. Never trust client UI state as charging evidence. |

## Server debugging path

1. State the affected protocol, version/edition, endpoint or action, parties/station, environment, and expected versus observed result.
2. Build one redacted timeline: transport connection, authentication, request/frame ID, schema result, protocol response, application operation ID, database commit, subsequent event/callback, and retry/reconnect. Include both event and receive times.
3. Find the first divergence. Check negotiated subprotocol/OCPI version, role and endpoint direction, token/certificate binding, schema, state preconditions, station capabilities, then persistence and queue delivery.
4. Reproduce with the smallest real wire fixture or simulator trace. Compare to the correct official spec and errata; classify a vendor deviation explicitly.
5. Fix at the owning boundary, add a regression test for the observed failure and its duplicate/timeout variant when meaningful, and verify final state plus audit trail. Reconcile affected existing records if the bug produced incorrect sessions, CDRs, or invoices.

## Security review path

- Inventory trust boundaries: driver/app → product API; partner → OCPI; station → OCPP WebSocket; worker → broker/database; operator → remote-control endpoint.
- Bind every credential or certificate to an allowed party, tenant, station, role, and operation. Check authorization after parsing the identity and before routing commands or reading another party's data.
- Use TLS validation, secret rotation, least privilege, safe certificate enrollment/revocation, and authenticated firmware delivery appropriate to the deployed OCPP security profile. Do not use an insecure development profile as a silent production fallback.
- Treat URL paths, OCPI callback URLs, vendor diagnostics, firmware URLs, and uploaded files as untrusted. Validate targets against allowlists and network policy to prevent server-side request forgery; cap payload size and decompression, and sanitize logs.
- Prevent replay and cross-tenant substitution with scoped IDs, idempotency, freshness where specified, and auditable command ownership. Rate-limit authentication failures and remote operations without hiding legitimate recovery traffic.
- Redact credentials tokens, authorization IDs, certificates/private keys, payment data, and personal data from logs and traces. Keep enough nonsecret correlation to investigate incidents.
- For a found issue, document exploit path, affected scope, fix, tests, rotation/reconciliation needs, and residual risk. Do not claim a protocol mandates a defense unless the selected specification says so.
