# Java rules

Apply [common rules](README.md) and the selected runtime rules. Identify the JDK,
compiler release target, Maven/Gradle toolchain, framework BOM, JSON mapper, and
deployment runtime. Use the current supported baseline; do not assume Spring.

## Design and types

- Prefer immutable values, explicit constructors, narrow visibility, and small
  cohesive classes. Use records for suitable DTO/value carriers and sealed types
  for bounded outcomes when supported by the target. Records are not a default
  substitute for mutable/proxied persistence entities.
- Keep nullability and absence explicit. Validate boundary data; use Optional for
  deliberate return-value absence rather than hiding required values. Separate
  serialization annotations and persistence concerns from domain invariants.
- Use BigDecimal from decimal text or exact values with explicit rounding; avoid
  constructing billed amounts from binary floating-point. Use java.time types
  and an injectable Clock. Do not use legacy mutable date APIs for new code.
- Preserve causes and distinguish validation, protocol rejection, infrastructure
  failure, and cancellation. Do not catch Exception and return a default success.
- Use try-with-resources for owned AutoCloseable resources. Reuse managed clients
  and pools; define application shutdown ownership.

## Concurrency and runtime

- Choose one execution model deliberately: nonblocking event-loop IO or bounded
  blocking work. Virtual threads are useful for supported blocking IO workloads,
  not a way to make CPU work faster or permit blocking a Vert.x event loop.
- Bound downstream concurrency by actual database/partner capacity even with
  virtual threads. Avoid pooling virtual threads as scarce worker threads;
  control access to scarce external resources instead.
- Avoid implicit common-pool work for application IO. Propagate deadlines,
  interrupts/cancellation, tenant identity, and correlation through explicit
  executors or framework context bridges. Respect interruption during cleanup.
- Verify the release status of structured-concurrency and other modern APIs for
  the selected JDK. Do not enable preview/incubator features merely to modernize
  code. Framework thread/transaction context must survive any supported bridge.

## Verification

Use the project's wrapper and existing formatter/static analyzer. Compile for
the actual deployment target; test JSON compatibility, transaction rollback,
timeouts, duplicate operations, and resource shutdown where changed. Measure
thread/queue/pool behavior when changing concurrency, using JFR or runtime tools
as appropriate. Do not introduce a new test framework without need.

Read [Vert.x rules](java-vertx.md) or [pure Jakarta rules](java-jakarta.md) before
implementing those runtimes. For other Java frameworks, check their own current
official documentation and apply the same boundaries.

## Security controls

Names are starting points: confirm them for the installed version.

- **Randomness, comparison, crypto:** SecureRandom; MessageDigest.isEqual for secret
  comparison; AES/GCM/NoPadding with a fresh 12-byte nonce per encryption. Never
  java.util.Random, String.equals on secrets, ECB, or a reused nonce.
- **Secret leaks:** a record's generated toString prints every component, including
  tokens. Wrap secrets in a type that overrides toString, or exclude them explicitly.
- **Outbound:** java.net.http.HttpClient does not follow redirects by default; keep it
  that way and set connect and request timeouts. Read through a capped stream instead of
  an unbounded BodyHandlers.ofString. Never install a trust-all TrustManager or a
  permissive HostnameVerifier.
- **Parsing:** never use ObjectInputStream on untrusted data. Keep Jackson default typing
  off and set StreamReadConstraints. Disable external entities for XML, including OCPP
  1.6 SOAP.
- **Addresses:** InetAddress.getByName on a forwarded header performs DNS for hostnames.
  Use InetAddress.ofLiteral where available, or validate the literal first.
- **SQL:** PreparedStatement or JPA parameters only. Include tenant in the key or query.
- **Certificates:** validate with PKIX, then check identity and key usage yourself.
  Decide how revocation works, because disabling revocation checking leaves it to you.
- **Runtime:** the JDK's cacerts and blocked.certs are part of your attack surface. Pin
  the image, and run without root.

Official sources: [Dev.java learning and release references](https://dev.java/learn/),
[JDK documentation](https://docs.oracle.com/en/java/), and
[Java virtual-thread guide](https://dev.java/learn/api/virtual-threads/).
Recheck release-specific APIs and runtime corrections at use time.
