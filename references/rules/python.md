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

Official sources: [Python asyncio tasks and structured concurrency](https://docs.python.org/3/library/asyncio-task.html),
[decimal arithmetic](https://docs.python.org/3/library/decimal.html), and
[PEP 8](https://peps.python.org/pep-0008/). Select documentation matching the
supported interpreter; do not use new syntax or APIs on older runtime targets.
