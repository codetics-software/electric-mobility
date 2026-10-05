# Engineering rules by language and runtime

Read [agents.md](agents.md) for every task. For design, implementation, review,
and debugging, apply the common rules below and load only the language/runtime
files in scope. Rules apply to all programming languages, including ones not
listed here; this index does not authorize changing the user's chosen stack.

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

- Apply [code-design-and-api.md](../code-design-and-api.md): clean boundaries,
  explicit API versions, generated OpenAPI JSON and attribution, and no
  react-hook-form in Next.js. Follow language idioms rather than imposing Java
  class hierarchies or framework annotations on every language.
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

## Select the relevant files

| Language/runtime | Required rules |
|---|---|
| Java | [java.md](java.md) |
| Java on Vert.x | [java.md](java.md) and [java-vertx.md](java-vertx.md) |
| Pure Jakarta EE | [java.md](java.md) and [java-jakarta.md](java-jakarta.md) |
| Kotlin, including Android/multiplatform | [kotlin.md](kotlin.md) |
| Kotlin on Vert.x/Jakarta | [kotlin.md](kotlin.md) and the corresponding Java runtime file; apply Java-only language advice only where relevant |
| Swift | [swift.md](swift.md) |
| C#/.NET | [csharp.md](csharp.md) |
| Rust | [rust.md](rust.md) |
| Go | [go.md](go.md) |
| Python | [python.md](python.md) |
| TypeScript/JavaScript | [typescript.md](typescript.md) |
| Any other language/framework | Apply this guide; consult its official style, type, concurrency, security, testing, and supported-release documentation before designing code. Record concrete applicable decisions. |

These are engineering rules. Protocol obligations still come from the selected
OCPI/OCPP source. Debugging and trust boundaries are covered in
[implementation-and-debugging.md](../implementation-and-debugging.md).
