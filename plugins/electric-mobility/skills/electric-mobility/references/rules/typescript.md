# TypeScript and JavaScript rules

Read [common rules](README.md) and [code-design-and-api.md](../code-design-and-api.md).
Identify runtime/browser targets, TypeScript/compiler options, framework version,
package manager/lockfile, ESM/CommonJS conventions, and lint/type-check setup.

- For new TypeScript code, use strict checking and deliberate nullability. Use
  unknown and runtime narrowing at external boundaries; avoid any, unchecked as
  casts, and non-null assertions that hide invalid input. Adopt extra compiler
  strictness only with its effects on the existing project understood.
- Prefer discriminated unions, small cohesive modules, explicit exports, and
  immutable values where useful. Keep browser/server code and secrets separate;
  compile-time types are not JSON validation or authorization.
- Await/observe promise failures, propagate cancellation/deadlines with supported
  abort APIs, bound concurrency and queues, and own listeners/timers/sockets.
  Do not perform blocking IO or expensive computation on Node's event loop.
- Use exact minor units/decimal tools for billed amounts. JSON cannot serialize
  bigint directly: map domain values to the documented wire number/string shape
  without silently changing OCPI's required number representation.
- In JavaScript projects, use runtime validation, clear modules, JSDoc/type-check
  support where configured, and linting; do not force a TypeScript migration.
- In React/Next.js, keep render pure, state ownership explicit, and effects for
  external synchronization. Use framework-supported server/client boundaries.
  Never install/import/recommend react-hook-form, its resolvers, or dependent
  form wrappers for Next.js; follow the separate native-form rules.
- Run the project's type checker, formatter/linter, production build, and relevant
  tests. Verify runtime schemas, abort behavior, server/client separation, and
  generated OpenAPI route coverage where changed.

## Security controls

Names are starting points: confirm them for the installed version.

- **Randomness, comparison, crypto:** crypto.randomBytes or crypto.randomUUID, never
  Math.random; crypto.timingSafeEqual, which throws on unequal lengths, so compare fixed-length
  hashes; aes-256-gcm with a fresh IV, checking the auth tag; async crypto.scrypt, never the
  sync form on a server.
- **Secret leaks:** JSON.stringify and console.log print every enumerable property. Map to an
  explicit response type, and do not return ORM objects from an API.
- **Outbound:** fetch with redirect: 'manual' or 'error', and AbortSignal.timeout. Never set
  NODE_TLS_REJECT_UNAUTHORIZED=0 or rejectUnauthorized: false. Read bodies through a size
  cap, and check resolved addresses for partner calls using a custom lookup.
- **WebSockets:** in ws, set maxPayload and authenticate in the upgrade handler before
  handleUpgrade. Handle subprotocols with handleProtocols.
- **mTLS:** requestCert and rejectUnauthorized on the server, then check socket.authorized
  and getPeerCertificate against the station identity.
- **Proxies:** Express trust proxy takes explicit addresses, never true.
- **Parsing:** types vanish at runtime, so validate with a schema. Reject __proto__ and
  constructor keys when merging objects. Large meter values lose precision as JavaScript
  numbers, so keep precise decimal strings for billing.
- **Next.js:** NEXT_PUBLIC_ values are public; add the server-only import guard to secret
  modules; check authorization inside each Server Action and route handler. Middleware alone
  is not an authorization layer. A catch-all backend proxy needs path, header, and origin
  allowlists and a body limit.
- **Supply chain:** commit lockfiles and use npm ci, enforce patched Node versions via engines
  and .nvmrc, and be wary of install scripts.

Official sources: [TypeScript compiler configuration](https://www.typescriptlang.org/tsconfig/),
[Node.js event-loop guidance](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop),
and [Next.js forms](https://nextjs.org/docs/app/guides/forms).
Use documentation for the installed framework and supported runtime targets.
