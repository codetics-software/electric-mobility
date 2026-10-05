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

Official sources: [TypeScript compiler configuration](https://www.typescriptlang.org/tsconfig/),
[Node.js event-loop guidance](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop),
and [Next.js forms](https://nextjs.org/docs/app/guides/forms).
Use documentation for the installed framework and supported runtime targets.
