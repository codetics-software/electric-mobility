# Rust rules

Read [common rules](README.md). Identify stable toolchain/MSRV, edition, crate
versions/features, async runtime, deployment target, and lockfile policy.

- Model units and scoped identities with newtypes and bounded state with enums.
  Use ownership/borrowing to express lifetimes; prefer narrow traits where a
  boundary needs substitution. Do not add Arc/Mutex everywhere to bypass design.
- Use Result/Option and preserve error causes; avoid panic, unwrap, and expect on
  untrusted payloads or recoverable partner failures. Keep unsafe code minimal,
  justify its invariant, and verify it rather than assuming memory safety.
- Define task ownership and observe join results. Bound tasks/channels, provide
  deadlines and shutdown signals, and handle canceled/dropped futures without
  losing persisted operation state. Do not hold a blocking lock across await;
  use runtime-supported blocking work facilities for blocking dependencies.
- Do not assume a timed-out future canceled a remote charging action. Preserve
  idempotency and reconciliation; protect connection ownership during reconnects.
- Use versioned serde contracts with explicit required/optional/unknown-value
  handling. Do not apply deny_unknown_fields where OCPI permits extensions.
  Use exact decimal/minor-unit money and explicit time/unit types.
- Run cargo fmt/check, configured Clippy rules, and relevant tests/features on
  the supported toolchain. Test cancellation, wire round trips, storage
  idempotency, and concurrent access where changed.

## Security controls

Names are starting points: confirm them for the installed version.

- **Randomness, comparison, crypto:** OsRng or getrandom; constant-time comparison from
  the subtle crate; ring or RustCrypto AEADs with a fresh nonce; the argon2 crate for
  passwords. Do not write your own primitives.
- **Secret leaks:** derive(Debug) prints every field, and tracing will happily record it.
  Use secrecy::SecretString or a manual Debug implementation, and zeroize where it helps.
- **Outbound:** reqwest with redirect::Policy::none() and timeouts. Never use
  danger_accept_invalid_certs. Limit the response size while streaming, and check resolved
  addresses for partner calls with a custom resolver or connector.
- **WebSockets and HTTP:** set max_message_size and max_frame_size in tungstenite's config
  or axum's upgrade, and a DefaultBodyLimit. Authenticate in the upgrade handler.
- **mTLS:** rustls with a client-certificate verifier, then check identity yourself. Rustls
  proves the chain but does not know which station it should be.
- **Async:** password hashing and other CPU-heavy work belong in spawn_blocking. An
  unwrap on untrusted input is a denial of service, so return typed errors.
- **Parsing and SQL:** avoid deny_unknown_fields where the protocol allows extensions, but
  validate values. Use bound parameters in sqlx or Diesel, and treat format! SQL as a defect.
- **Dependencies:** use cargo audit or cargo deny, with Cargo.lock committed for services.
  Keep unsafe out of protocol parsing.

Official sources: [Rust language book](https://doc.rust-lang.org/book/),
[Rust error handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html),
and [Tokio task ownership and spawning](https://tokio.rs/tokio/tutorial/spawning).
For another runtime or serializer, verify its own current documentation.
