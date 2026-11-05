# Security capabilities every language must provide

Every stack, listed or not, must answer each row below with a concrete, current API from its
own official documentation. If a row has no safe answer in the chosen stack, report that
as a risk instead of improvising. Do not write your own cryptography.

| Capability | Requirement | Common mistake to avoid |
|---|---|---|
| Random secrets | Operating-system CSPRNG, 256 bits for tokens | General-purpose random functions, timestamps, UUIDs from a weak generator |
| Secret comparison | Constant-time comparison, on hashes where length could vary | `==` on tokens, signatures, or hashes |
| Password hashing | Memory-hard or strong KDF, off the event loop, with input length limited | Fast hash for human passwords; slow hash on an unprotected event loop |
| Token hashing | Fast cryptographic hash is fine for high-entropy random tokens | Storing session or partner tokens in clear |
| Encryption at rest | Authenticated encryption with a fresh nonce and a key version | ECB or CBC without authentication; reused nonce; key in the same place as data |
| Secret-safe types | The generated string, debug, and JSON form cannot print a secret | Records, data classes, `Debug`, `repr`, `%+v`, `JSON.stringify` printing tokens |
| TLS client | Chain and hostname verified, private CAs added explicitly | Disabling verification, even "temporarily" |
| Mutual TLS | Chain verified, then identity and key usage checked against the station | Accepting any certificate from the CA as any station |
| HTTP server limits | Header, body, and time limits set | Relying on defaults, some of which are unlimited |
| WebSocket limits | Authenticate before accepting; cap message and frame size; serialize writes | Authenticating in the first message; unlimited frames |
| HTTP client safety | Timeouts, redirects off, capped response, resolved-address check | Default clients that follow redirects with credentials attached |
| Proxy trust | Forwarded headers honored only from configured proxy ranges | Blanket "trust proxy" settings, or reading the header directly |
| Queries | Bound parameters, with tenant part of the key or query | String-built queries; a tenant filter that can be forgotten |
| Parsing | Size and depth limits; no native object deserialization; no XML external entities | Treating a successful parse as authorization |
| Logs | Structured, redacted, with control characters stripped | Logging headers, raw payloads, or `idTag` values |
| Concurrency | Atomic rate-limit counters; locks around check-then-act on money and commands | Check outside the transaction, then act inside it |
| Dependencies | Lockfile, live vulnerability check, patched runtime enforced in CI ([how](../security/vulnerability-management.md)) | Floating versions; old base images; "no CVEs" from memory |

**For a language not listed below,** write this table's concrete answers into your design
before coding, citing the official documentation for the installed version. If a library is
unmaintained or lacks a capability, say so.

