# Kotlin rules

Read [common rules](README.md). Identify Kotlin/compiler/Gradle plugin versions,
JVM or multiplatform targets, coroutine and serialization versions, framework,
and platform support. Apply idiomatic Kotlin rather than mechanically translating
Java or assuming every Kotlin backend uses Spring.

## Types and maintainability

- Follow official naming/formatting; use val, small functions, expression bodies
  when clear, data classes for suitable immutable data, and sealed outcomes for
  bounded states. Limit scope functions/chains when they obscure ownership.
- Model absence with nullable types and deliberate defaults. Avoid !!, unsafe
  casts, platform-type assumptions, and lateinit for business invariants. Validate
  Java/JSON boundary nullability; a non-null declaration is not input validation.
- Expose read-only collections and avoid leaking mutable backing references;
  read-only interfaces do not guarantee deeply immutable objects.
- On JVM, use BigDecimal with explicit rounding and java.time types. In common
  multiplatform code, choose target-compatible decimal/time abstractions;
  do not import JVM-only types or use Double as a monetary shortcut.
- Keep persistence/proxy entities distinct from data-class DTO/value semantics.
  Verify no-arg/all-open/plugin requirements for the actual ORM or container.

Style source: [official Kotlin coding conventions](https://kotlinlang.org/docs/coding-conventions.html).

## Coroutines and failure

- Own CoroutineScopes at request, service, or platform lifecycle boundaries.
  Prefer coroutineScope for related work; use supervisorScope only when sibling
  independence is intended. Avoid GlobalScope and detached unowned work.
- Use suspend functions for suspending APIs, bounded parallelism, and explicit
  deadlines. suspend does not make blocking IO nonblocking. Offload actual
  blocking IO through the runtime's supported mechanism; keep CPU work off the
  event loop/UI thread and do not leak context-owned state across dispatchers.
- Do not use runBlocking in HTTP/WebSocket handlers or UI code. Preserve
  CancellationException; broad catch/runCatching must not swallow cancellation.
  Await Deferred results and handle failed Jobs; a handler is not a replacement
  for observing failures. Release resources with use/finally as appropriate.
- Use structured concurrency for in-process work, persisted operations/outbox
  for work that must survive cancellation or restart. Cancellation of an HTTP
  request is not proof the remote charging command was undone.

Sources: [coroutine scopes and structured concurrency](https://kotlinlang.org/docs/coroutines-basics.html)
and [CancellationException contract](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-cancellation-exception/).

## Runtime integration and verification

For Vert.x/Jakarta, read their runtime rules. For Spring/Ktor or another framework,
verify its current coroutine, transaction, context, and client integration.
Do not run parallel coroutine work on a shared non-thread-safe persistence
context or assume transaction annotations propagate through arbitrary dispatchers.

On Android, tie work/state collection to the appropriate lifecycle and model
process death/restart; backend state remains charging evidence. In multiplatform
code, keep target-specific adapters outside common business rules.

Use configured Kotlin formatting/static analysis and explicit target compilation.
Test coroutine timeout/cancellation, failure propagation, serializer unknown
values, transaction behavior, and relevant platform lifecycles. Prefer the
project's coroutine test scheduler for deterministic timing tests over sleeps.

## Security controls

Names are starting points: confirm them for the installed version.

- **JVM primitives:** same as [Java](java.md): SecureRandom, MessageDigest.isEqual,
  AES-GCM with a fresh nonce.
- **Secret leaks:** a data class's generated toString prints every property, and logging
  one leaks its tokens. Use a dedicated secret class with its own toString, or keep
  secrets out of data classes.
- **Coroutines:** password hashing and blocking crypto belong on a suitable dispatcher,
  and never on an event loop. Do not swallow CancellationException in a catch used for an
  auth failure.
- **Serialization:** kotlinx.serialization and Jackson do not validate business rules, and
  non-null declarations do not authorize anything. Limit input size before parsing.
- **Ktor and Spring:** set WebSocket frame limits, and enable forwarded-header handling
  only behind a trusted proxy. Authenticate in the upgrade step.
- **Android storage:** tokens go under a Keystore-backed AES-GCM key, not plain
  SharedPreferences. Handle key loss by clearing the credential and signing in again.
- **Android platform:** network security config with cleartext off;
  allowBackup="false" with data extraction rules; only necessary components exported;
  verified App Links with autoVerify. Treat Intents and deep links as untrusted input.
- **Android logs:** remove tokens and idTags from Logcat in every build type.
