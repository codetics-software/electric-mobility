# Vert.x runtime rules for Java and Kotlin

Read [common rules](README.md) and the applicable language rules. Pin the Vert.x
release/BOM, JDK, web/client/database modules, and coroutine bridge if used. Check
the selected major's lifecycle APIs; do not mix older examples with newer APIs.

## Execution and lifecycle

- Keep event-loop handlers nonblocking: no sleep, synchronous JDBC/filesystem IO,
  Future.get/join, locks held across work, or expensive billing/cryptography.
- Compose asynchronous Futures with the release's compose/map/recover APIs;
  propagate failures. Await startup work before signaling readiness. Await owned
  resources' closure during shutdown; stop timers and reject or drain new work.
- Use supported executeBlocking/worker facilities for bounded blocking work.
  Virtual-thread execution needs a supported configuration; it does not change
  ordinary event-loop rules. Match ordering to the resource/operation invariant.
- Preserve Vert.x context when bridging CompletionStage, executors, or coroutines.
  State owned by one context is not globally thread-safe; isolate cross-context
  state with explicit synchronization or message ownership.
- Apply stream backpressure, write-queue bounds, read pause/resume, payload caps,
  and partner timeouts. End each HTTP response once; use centralized failures.

These execution rules follow the [Vert.x Core manual](https://vertx.io/docs/vertx-core/java/);
select the installed release before copying signatures or lifecycle classes.

## Protocol and persistence decisions

Keep routing handlers and verticles as adapters around application use cases.
Use a compatible asynchronous database client, or explicitly offload blocking
drivers. Commit an operation/outbox transaction before claiming durable acceptance.
An event-bus message alone is not evidence that a business operation is persisted
or recoverable; make its delivery contract explicit in the application design.

Preserve station/connection ownership, request IDs, partner identity, credential
scope, and callback deadlines across every dispatch. Manage reconnect/replay
through persisted operations rather than timer-only state.

For Kotlin, use the supported Vert.x coroutine integration and its context.
Do not use runBlocking in a handler or silently move context-bound state to a
generic dispatcher. Follow [kotlin.md](kotlin.md) for cancellation and scope.

Generate the required OpenAPI JSON from shared runtime contracts or the project's
compatible generator. Verify maturity and supported OpenAPI versions of any
Vert.x OpenAPI module; do not infer production stability from its presence in
the documentation sidebar.

Test real asynchronous completion, handler failures, blocking-work boundaries,
stream backpressure, transaction failure, undeploy/shutdown, and reconnection
when those behaviors change. Ensure asynchronous test failures reach the test
runner instead of becoming unobserved callback errors.
