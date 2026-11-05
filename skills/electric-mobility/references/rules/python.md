# Python rules

Read [common rules](README.md). Identify the interpreter version, supported
targets, pyproject/dependency lockfiles, web/async frameworks, and type/lint tools.

- Use explicit types, small modules/functions, dataclasses or validated models
  where appropriate, and narrow protocols at actual boundaries. Type hints do
  not validate received JSON; validate runtime required fields and open enums.
- Follow current Python style conventions. Avoid mutable default arguments,
  hidden global state, wildcard imports, and broad exception suppression. Use
  context managers and try/finally for owned resources.
- Use structured asyncio task lifetime, such as TaskGroup on supported versions,
  explicit deadlines, bounded queues/semaphores, and graceful shutdown. Observe
  task failures and propagate CancelledError after cleanup.
- Do not run blocking ORM/HTTP/file work or heavy CPU computation on the event
  loop. Use framework-supported sync boundaries or asyncio.to_thread for suitable
  blocking IO; CPU-bound work needs an appropriate executor/process strategy.
  Do not share a non-thread-safe ORM session across concurrent tasks.
- Use Decimal from decimal text with explicit quantization/rounding, timezone-aware
  timestamps, explicit units, and parameterized storage operations. Persist remote
  operation/outbox state before launching work that can outlive a request.
- Run the project's formatter/linter/type checker and behavior tests on supported
  interpreters. Test schema coercion policy, cancellation, task failures, decimal
  boundaries, and framework transaction behavior where changed.

## Security controls

Names are starting points: confirm them for the installed version.

- **Randomness, comparison, crypto:** secrets for tokens, never random; hmac.compare_digest;
  AESGCM from the cryptography package with a fresh nonce; argon2-cffi or hashlib.scrypt for
  passwords. Run hashing in a worker thread under asyncio, or it blocks every connection.
- **Secret leaks:** a dataclass or pydantic repr prints fields. Use field(repr=False) or
  SecretStr, and test the log output.
- **Outbound:** requests follows redirects by default, so pass allow_redirects=False; httpx
  does not follow by default. Always set timeouts, since requests has none by default. Never
  use verify=False. Stream with a byte cap. Check resolved addresses for partner calls.
- **WebSockets:** set max_size in the websockets library or the framework's equivalent, and
  authenticate before accepting.
- **Proxies:** restrict forwarded-header trust to your proxy addresses, for example uvicorn's
  forwarded-allow-ips, never `*`. Django's SECURE_PROXY_SSL_HEADER is only safe behind a
  proxy that overwrites the header.
- **Parsing:** never pickle or yaml.load on untrusted data; use yaml.safe_load. Use
  defusedxml for XML, including OCPP 1.6 SOAP. Pydantic models validate shape, not whether
  this caller may act on this tenant.
- **SQL:** bound parameters, no f-string SQL, and tenant in every query.
- **Dependencies:** lock with hashes where possible, and run pip-audit.

Official sources: [Python asyncio tasks and structured concurrency](https://docs.python.org/3/library/asyncio-task.html),
[decimal arithmetic](https://docs.python.org/3/library/decimal.html), and
[PEP 8](https://peps.python.org/pep-0008/). Select documentation matching the
supported interpreter; do not use new syntax or APIs on older runtime targets.
