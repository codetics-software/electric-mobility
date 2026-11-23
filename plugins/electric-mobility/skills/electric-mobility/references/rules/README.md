# Rules common to every language

Do not change the user's chosen stack. Protocol obligations still come from the selected OCPI or OCPP source.
Each language file has a Security controls section. For a language with no file, use
[security capabilities](security-capabilities.md) and its official documentation.

## Current best practices: verify, then apply

1. Inspect compiler/runtime targets, framework/platform versions, dependency
   manifests and lockfiles, build wrappers, CI, lint settings, and deployment
   constraints. Record the relevant versions before choosing APIs or patterns.
2. Check current official language, framework, library, security, and migration
   documentation. Use documentation for the selected release, not examples
   copied from a different major version or model memory. Cite the source and
   access date when a version-sensitive decision depends on it.
3. For new projects, choose current stable, maintained releases compatible with
   the deployment environment; choose an LTS line when support needs justify it.
   For existing projects, apply the latest applicable practices within their
   supported baseline. Address deprecated/insecure APIs and explain upgrades
   needed for a modern practice; do not silently perform unrelated major upgrades.
4. Do not treat a preview, incubating API, nightly compiler, prerelease dependency,
   or experimental framework module as production-stable. Check actual status
   in the selected release; use such features only under an explicit project
   decision with compatibility and support risks stated.
5. Never claim guidance is forever “latest.” Recheck official sources at use time.
   When sources/tools are unavailable, state the unverified version assumption
   and avoid inventing a release number, compatibility guarantee, or API.

## Common implementation rules

- Follow language idioms rather than imposing Java class hierarchies or framework
  annotations on every language.
- Keep parsing/serialization, application orchestration, domain rules, and
  persistence separate. Use explicit identity scopes, units, decimal-safe money,
  UTC protocol timestamps, and supported versioned DTOs.
- Validate runtime input and authorize the actual tenant/party/action. Preserve
  protocol-defined extensions without accepting missing required values.
- Define timeout, cancellation, concurrency limits, queue capacity, retry policy,
  and resource ownership. Never block an event loop or UI thread. Persist
  operations that must survive request cancellation or process loss.
- Propagate failures with typed outcomes or idiomatic errors. Do not swallow
  cancellation, hide protocol rejection as success, or retry an irreversible
  action without scoped idempotency. Make correlation and recovery observable.
- Use maintained dependencies, reproducible builds and platform-compatible
  targets. Avoid mutable globals and unbounded task/thread creation. Close owned
  resources during normal completion, failure, cancellation, and shutdown.
- Run the project's formatter, lint/static analysis, compiler/type checks, and
  tests appropriate to the changed behavior. Use real transport/database
  integration tests when framework semantics matter. Report checks actually run.
