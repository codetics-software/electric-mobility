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

## Security controls

Names are starting points: confirm them for the installed version.

- **Secret storage:** Keychain with kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly or
  stricter. Never UserDefaults, plist, or files. Check SecItem status codes, because a
  failed write that goes unnoticed loses the session. Items can survive reinstall, so
  clear them on first launch if your policy requires it.
- **Crypto:** SecRandomCopyBytes or SystemRandomNumberGenerator for secrets; CryptoKit
  AES.GCM; no hand-written comparison of signatures, use the framework's verification.
- **Network:** keep App Transport Security on with no broad exceptions. Never accept every
  server trust in a URLSession delegate. Implement the redirect delegate where a token
  could follow a redirect.
- **Links and QR:** prefer Universal Links over custom schemes. Validate host and path from
  deep links and scans, and require confirmation in the app before starting or paying.
- **Secret leaks:** a struct prints all fields in string interpolation and dump. Use
  CustomStringConvertible on secret types. Mark Logger values privacy: .private.
- **Truth:** the app displays backend evidence only. Do not compute authorization or final
  charging state locally. Treat a push as a prompt to refresh, not as proof.
- **Server-side Swift:** use swift-crypto and SwiftNIO TLS, with explicit frame and body
  limits.

Official sources: [Swift API design guidelines](https://www.swift.org/documentation/api-design-guidelines/)
and [Swift concurrency language guide](https://docs.swift.org/latest/documentation/the-swift-programming-language/concurrency/).
Check the installed language mode and platform availability before selecting APIs.
