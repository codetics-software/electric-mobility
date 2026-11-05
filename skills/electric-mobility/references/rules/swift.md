# Swift rules

Read [common rules](README.md). Identify Swift language mode, Xcode/toolchain,
deployment targets, package constraints, and concurrency settings. Check current
Swift migration guidance before changing isolation defaults or annotations.

- Use clear argument labels, value types where appropriate, deliberate optionals,
  and narrow protocols at real boundaries. Avoid force unwraps and try! for
  untrusted protocol data. Give wire DTOs explicit Codable keys and enum policy.
- Prefer structured async/await and task groups for related work. Own unstructured
  tasks explicitly; avoid Task.detached as a generic background-work shortcut.
- Protect shared state with actors and explicit isolation; update UI-owned state
  on MainActor. Do not suppress compiler diagnostics with unchecked Sendable or
  unsafe isolation annotations without a proven synchronization invariant.
- Treat actor reentrancy across await as a state-machine concern: revalidate
  assumptions before committing state. Propagate cancellation and keep task
  lifetime tied to the owning screen/service; async is not proof CPU work leaves
  the UI executor. Avoid blocking waits on asynchronous results.
- Use Decimal or exact minor units for money, explicit units, and wire-compatible
  UTC dates. Preserve pending/confirmed charging states from backend evidence;
  persist recovery state for app suspension or process loss.
- Run target builds, concurrency diagnostics, the project's formatter/linter,
  and relevant tests. Verify Codable compatibility, actor transitions, canceled
  tasks, and foreground/background recovery where changed.

Official sources: [Swift API design guidelines](https://www.swift.org/documentation/api-design-guidelines/)
and [Swift concurrency language guide](https://docs.swift.org/latest/documentation/the-swift-programming-language/concurrency/).
Check the installed language mode and platform availability before selecting APIs.
