# Go rules

Read [common rules](README.md). Identify the module go directive, toolchain,
dependencies, runtime support, and service deployment constraints. Effective Go
is useful for idioms but is not a complete current guide; consult newer release
notes and standard-library documentation too.

- Prefer small packages, simple values, explicit constructors and narrow
  interfaces at consuming boundaries. Avoid Java-style service hierarchies,
  unnecessary getters, mutable globals, and generic abstractions without need.
- Return idiomatic errors with useful context; preserve errors.Is/errors.As
  behavior. Do not panic for ordinary protocol rejection or ignore returned
  errors. Distinguish zero values, absence, and null in wire DTOs.
- Pass context.Context through request/operation IO and call owned cancel
  functions. Give goroutines an owner, stop condition, and bounded fan-out.
  Define channel closing ownership; prevent blocked sends and goroutine leaks.
- Reuse HTTP clients/transports, configure server/client timeouts, close response
  bodies, and use graceful shutdown. Bound pools and serialize socket writes
  when required by the selected WebSocket library.
- Use exact minor units or a verified decimal strategy for money; never bill
  through float64. Use explicit time zones/units, parameterized SQL, and scoped
  transactions for operation/outbox persistence.
- Run gofmt, go vet, and relevant go test commands. Use the race detector when
  changing concurrent behavior on supported targets; test cancellation, leaks,
  timeouts, serialization, and actual database semantics where relevant.

## Security controls

Names are starting points: confirm them for the installed version.

- **Randomness, comparison, crypto:** crypto/rand, never math/rand, for tokens;
  crypto/subtle.ConstantTimeCompare; cipher.NewGCM with a fresh nonce; x/crypto argon2 or
  scrypt for passwords.
- **Secret leaks:** %+v and %#v print every struct field. Give secret types a String method
  and a slog LogValuer returning a redacted value.
- **Server:** set ReadHeaderTimeout and other timeouts, because the zero values mean none.
  Use http.MaxBytesReader on bodies, and SetReadLimit on WebSockets, since limits vary
  by library. Stations often send no Origin, so handle origin checks deliberately for
  station and browser routes.
- **Client:** set Timeout, and CheckRedirect returning http.ErrUseLastResponse. Never set
  InsecureSkipVerify in production. Use net.Dialer.Control to refuse private addresses
  after DNS resolution, and io.LimitReader on responses.
- **mTLS:** tls.RequireAndVerifyClientCert with ClientCAs, then read r.TLS.VerifiedChains
  and check the identity yourself. Use PeerCertificates only after verification.
- **Proxies:** do not read X-Forwarded-For from a blanket helper. Check RemoteAddr against
  your proxy ranges first.
- **SQL:** placeholders only, tenant in every query.
- **Tooling:** run govulncheck alongside go vet. Use the race detector on connection and
  rate-limit code.

Official sources: [Effective Go](https://go.dev/doc/effective_go),
[current Go release notes](https://go.dev/doc/devel/release), and
[context package](https://pkg.go.dev/context). Verify new APIs against the module's
toolchain rather than assuming all current standard-library features are available.
