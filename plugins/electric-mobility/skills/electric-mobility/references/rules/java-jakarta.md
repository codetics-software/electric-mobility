# Pure Jakarta EE runtime rules

Read [common rules](README.md) and [Java rules](java.md), or Kotlin rules for a
Kotlin project. Identify the Jakarta EE edition, Full/Web/Core Profile, selected
runtime implementation, JDK, and each required specification. Spec availability
does not mean the deployed runtime implements it.

## Portable application code

- Use supported jakarta.* APIs on a Jakarta namespace baseline; do not mix javax.*
  Java EE imports with incompatible Jakarta dependencies. Use the platform/profile
  API in the appropriate provided/compile-only scope for the managed runtime.
- Keep Jakarta REST resources thin; use CDI for application wiring, Jakarta
  Validation for constraints, and supported JSON-B/JSON-P or the existing provider
  for explicit wire mappings. Validate nested DTOs and OCPI extension policies.
- Put transaction boundaries around application use cases using the applicable
  Jakarta Transactions/Persistence integration. Keep entities separate from DTOs;
  specify fetch/query behavior and avoid lazy serialization and N+1 queries.
- Do not share an application-managed EntityManager across concurrent tasks.
  Respect CDI scopes, interceptor/proxy semantics, and container thread safety.
- Use supported managed concurrency facilities in a managed container. Do not
  assume manually created threads preserve security or transaction context.
  Container-managed execution does not automatically propagate transactions.
- Apply Jakarta Security or the runtime's configured authentication integration,
  plus explicit tenant/party/action authorization. Map REST exceptions to the
  versioned API contract and OCPI envelopes.

Portable API/profile obligations come from the [Jakarta EE Platform specifications](https://jakarta.ee/specifications/platform/11/).
Choose the actual supported edition; use current component specifications and
the implementation's documentation for behavior that portability does not cover.

## Deployment, async work, and delivery

Honor a pure Jakarta assignment: do not introduce Spring Boot, Spring annotations,
or a vendor framework as a hidden dependency. MicroProfile extensions (including
OpenAPI) are separate from Jakarta EE; confirm runtime support before using them.
Standalone use of a Jakarta component needs its own explicit bootstrap and
resource management; do not assume a full container exists.

Do not hold a database transaction open while waiting for a remote OCPI/OCPP
outcome. Persist the operation and outbox atomically; use configured durable
delivery or recovery workers after commit. Gate async APIs and virtual-thread
facilities on the selected component/runtime rather than JDK availability alone.

Provide repeatable OpenAPI JSON generation even when the pure Jakarta runtime
has no built-in generator. Preserve versioned contracts and Codetics metadata.
Test CDI wiring/interceptors, validation, transaction rollback, security scope,
serialization, deployment, and shutdown in the selected container where changed;
plain unit tests alone do not verify container semantics.

## Security controls

Names are starting points: confirm them for the installed version.

- **Handshake:** use a ServerEndpointConfig.Configurator to authenticate in
  modifyHandshake, and put the verified identity in the endpoint's user properties. An
  @ServerEndpoint with only a path parameter has no authentication at all.
- **Limits:** set Session max text buffer size and idle timeout, along with container
  request-body limits.
- **Authorization:** use @RolesAllowed or Jakarta Security on application services as well
  as resources. Test it in the real container, because plain unit tests skip interceptors.
- **Context:** CDI request scope may not be active in WebSocket callbacks. Do not read the
  tenant from a scope that could be stale. Pass the verified identity explicitly.
- **mTLS:** read the jakarta.servlet.request.X509Certificate attribute. Client address and
  scheme behind a proxy are container settings, such as a remote-IP valve, so restrict
  them to your proxy ranges.
- **Persistence:** JPA named parameters only. Add tenant to queries, or use container
  filtering you have tested.
