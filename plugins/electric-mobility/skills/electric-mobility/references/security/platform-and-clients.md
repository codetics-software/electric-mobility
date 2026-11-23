# Securing the platform, clients, and deployment

Read [the security gate](README.md) first. Regulation pointers below show what to
check, not legal advice. Confirm applicability for the deployment's country and role.

## Separate the planes

Run distinct authentication for each kind of caller, and do not let one reach another:

| Plane | Caller | Credential | CSRF applies |
|---|---|---|---|
| Dashboard | Browser | Opaque session cookie | Yes |
| Mobile app | Native app | Opaque bearer token | No |
| Station | Charger | Basic auth or client certificate | No |
| Roaming | Partner backend | Token scoped by role | No |
| Public charging | Anonymous driver | Per-session secret in a header | No |
| Webhook | Payment provider | Signature on raw body | No |
| Machine push | Meter or other equipment | Per-connection token, hashed at rest | No |

Deny by default: routes not listed are refused. Public routes are an explicit, reviewed
list, and each CSRF exemption must name the control that replaces it.

## Tenancy

- **Derive the tenant from the session.** Never from a domain name, or a tenant ID in
  the operation. A tenant slug at login selects the account, and nothing more.
- **Put the tenant in every key and query.** Use composite keys where you can, so a
  forgotten filter becomes a failed lookup.
- **Foreign IDs behave like missing ones.** Return the same 404.
- **Scope drivers again inside the tenant.** A driver sees only their own sessions,
  tokens, and vehicles, and a station list must not be enumerable by them.
- **Keep product roles separate from OCPI market roles.** Administrator or operator is a
  product permission, and CPO or eMSP is a market role. They do not imply each other.
- **Check background jobs too.** Schedulers run without a user, so pass the tenant
  explicitly and test that no job mixes tenants.
- **Be careful with platform administrators.** Cross-tenant power needs its own explicit
  check, tied to a specific account in a specific tenant, and an audit entry.

## Accounts and sessions

- **Use opaque random session values and store only a hash.** A database leak then
  does not yield usable sessions.
- **Cookies:** `HttpOnly`, `Secure` in production, and `SameSite=Lax` or stricter. Use a
  CSRF token plus an origin check on mutations.
- **Use a memory-hard or strong KDF for passwords** with an upgrade path for old hashes,
  and limit input length before hashing.
- **Do not reveal account existence.** Hash against a dummy when the user is unknown,
  keep login errors uniform, and reveal "email not verified" only after a correct
  password.
- **Rate-limit by address and by tenant + account**, and make it atomic. Concurrent
  attempts must all count. Limit reset requests, sign-up, and public payment creation.
- **Re-check on each request** that the user and tenant are still active. Changing
  rights, resetting a password, or logging out everywhere revokes existing sessions.
- **One-time links** are single use, short-lived, and stored as hashes.
- **Keep expiry bounded**, and do not let a configuration value exceed the cap.
- **Offer MFA** for administrators, and consider it mandatory where they control fleets.

## External identity

- **Identify by issuer + subject.** An email match must never link accounts silently,
  because it enables account takeover through a provider that allows unverified email.
  Link only from an already authenticated session, and verify that session on return.
- **Let the framework check state, nonce, signature, issuer, audience, and expiry.** Use
  PKCE where the provider supports it.
- **The provider never chooses tenant or role.** Sign-up through a provider creates only
  the lowest role, in an explicitly configured public tenant.
- **Keep client secrets on the server**, and rotate signed ones such as Apple's before
  expiry.

## Web front end and proxy

When a web app forwards to a private API, it is a security component:

- **Allowlist path prefixes**, and reject `.` and `..` after decoding.
- **Allowlist request and response headers** instead of forwarding everything.
- **Build `X-Forwarded-For` deliberately.** Do not pass through client values unchecked.
- **Check `Origin` on every mutation**, with explicit exemptions for signed callbacks.
- **Limit body size, disable redirects, set a timeout, and set `no-store`** on API
  responses.
- **Keep secrets out of client bundles.** Client-exposed environment variables are
  public. Do not rely on hiding a button: enforce every permission on the server, and in
  frameworks with server actions, check authorization inside each action.
- **Remove test bridges from production builds**, and guard them with a production check.
- **API errors:** return validation messages only. Internal errors become a generic
  message plus a correlation ID. Do not expose stack traces, SQL, or partner responses.
- **Set a strict CSP**, deny framing, and restrict OpenAPI and docs to admins.

## Secrets

- **Keep secrets in the provider's secret manager**, with none in images, repositories,
  or example files. Example files contain placeholders only.
- **Use authenticated encryption with a fresh random nonce** for secrets you must send
  later. Support key versions: rotating a master key needs re-encryption, and a design
  with no key ID makes rotation an outage.
- **Back up the master key separately from the database.** Lose it and encrypted secrets
  are gone. Store both together and encryption gives no protection.
- **Bootstrap credentials** apply only to an empty database, and are removed afterward.
- **Do not leak secrets through a type's string form.** Auto-generated `toString`,
  `Debug`, `repr`, and JSON output print every field. Use a wrapper or an explicit
  exclusion, and test it. See the language rule files.
- **Pass secrets out of band.** Never in URLs, query strings, or error messages.
- **Plan for exposure.** Know how to rotate every secret, and in which order, before you
  need to. Station credentials are the hardest, since they need the station online.

## Logs, audit, and privacy

- **Redact by default:** `Authorization`, cookies, tokens, secrets, certificates' private
  parts, payment data, and raw payloads carrying `idTag`.
- **Prevent log injection.** Strip control characters from station and partner strings.
- **Separate audit from debug logs.** Audit records are append-only, with actor, tenant,
  action, target, outcome, and time. Test that rejected attempts appear where you intend.
- **Treat charging data as personal data.** A session history reveals where a person
  lives, works, and travels. Token UIDs, vehicle identifiers, licence plates, and precise
  timestamps can all identify someone, directly or indirectly.
- **Set retention per data type**, and enforce it with a job. Financial records have
  their own legal period, so deleting a user must anonymize rather than destroy invoices.
- **Make deletion real:** anonymize the account, free or revoke its tokens, and handle
  partner copies. Plan for data subject requests.
- **Limit operator access** to what the role needs, including in support tools and exports.

## Files and exports

- **Spreadsheet exports:** neutralize cells starting with `=`, `+`, `-`, `@`, tab, or
  carriage return, while keeping real numbers intact. Station, user, and partner text all
  end up in a spreadsheet eventually.
- **CSV imports:** limit rows and size, and validate every row in a transaction.
- **Uploads:** allowlist types, check magic bytes rather than trusting the declared type,
  limit size and count per object, and serve them with a safe content type and
  `Content-Disposition`. Do not serve user files from the app's own origin if they might
  execute.
- **Archive imports:** cap decompression size and entry count, and reject path traversal.
- **Parsers:** disable external entities for XML, which matters for OCPP 1.6 SOAP. Never
  use a native object deserializer on untrusted input. Limit JSON depth and size.

## Mobile apps

**Keep state truthful.** The backend's evidence is the only charging truth. The app shows
pending until the backend confirms.

| Concern | iOS | Android |
|---|---|---|
| Token storage | Keychain, this-device-only accessibility | Keystore-backed key with AES-GCM |
| Backups | Keep tokens out of backups via this-device-only accessibility | `allowBackup="false"` plus data extraction rules |
| Cleartext traffic | Keep App Transport Security on, no broad exceptions | Network security config with cleartext off |
| Links | Universal Links | Verified App Links (`autoVerify`) |
| Attestation (optional) | App Attest | Play Integrity |

Also:

- **Do not treat a custom scheme as proof of origin.** Another app can register it.
- **Validate deep links and scanned QR codes** as untrusted input. A link must never start
  charging or pay without confirmation inside the app.
- **Export only the components you must.** Check each exported component's inputs.
- **Clear secrets on sign-out**, and on first launch after reinstall, since iOS Keychain
  items can survive an uninstall.
- **Keep secrets out of the app binary.** A public app cannot keep an API key. Anything
  bundled should be considered public, and the backend enforces all limits.
- **Push notifications:** no sensitive details in the payload, and treat a push as a hint
  to refresh rather than as evidence.
- **Scope guest order data** to the device, using secure storage for tracking secrets.
- **Consider certificate pinning only with a recovery plan.** A bad pin locks drivers out
  at the charger. Backend API pinning is a trade-off, not a default.

## Deployment and supply chain

- **Run as non-root** with minimal images and no secrets in layers. Separate networks so
  the database is private and only the edge is public.
- **Set idle timeouts for WebSockets** long enough for station behavior (at least 600
  seconds), and send pings. Otherwise proxies cause reconnect storms.
- **Fail at startup on dangerous configuration:** a public URL over `http`, insecure
  cookies in production, or an unknown database scheme.
- **Enforce patched runtimes.** Pin versions in the image, `.nvmrc`, `engines`, or toolchain
  files, and fail CI below a patched minimum. Old base images are often the real exposure.
- **Treat the runtime trust store as configuration.** The JVM, Node, or OS trust list
  decides which CAs can impersonate partners. Update it deliberately, remove distrusted
  CAs, and fail the build if the expected removal did not happen.
- **Check CVEs and manage the supply chain** using
  [vulnerability management](vulnerability-management.md).
- **Keep test adapters and profiles out of production artifacts**, including in-memory
  databases and fake payment gateways.
- **Plan for incidents:** a way to disable a partner, a station, a tenant, or public
  payments quickly, without redeploying.

## Regulation to check

| Area | Pointers |
|---|---|
| Personal data | GDPR and national equivalents |
| Payment | PCI DSS, PSD2/SCA, and AFIR rules on ad-hoc payment for EU public charging |
| Metering | MID, and national rules such as Germany's Eichrecht |
| Product cybersecurity | EU RED delegated act (EN 18031), EU Cyber Resilience Act (reporting duties described in [vulnerability management](vulnerability-management.md)), UK Smart Charge Points Regulations |
| Critical infrastructure | NIS2, where the operator falls in scope |

Check the current text. State clearly that an applicability claim needs legal review, and
never claim compliance or certification without evidence.

## Tests every platform change needs

- Anonymous, wrong-role, and CSRF-free mutation are refused.
- A cross-tenant ID returns the same response as a missing one.
- SQL-like search strings remain inert and tenant-scoped.
- A driver cannot enumerate stations or see another driver's sessions.
- Password reset is single use and revokes existing sessions.
- An email match does not link an external identity.
- Rate-limit counting holds under concurrency.
- Forwarded addresses are honored only from trusted proxies.
- CSV exports neutralize formulas.
- An upload with a mismatched type is refused.
- Secret-bearing types do not print secrets through their string form.
- The encryption key missing or malformed disables the feature safely.
- Tampered ciphertext is refused.
- OpenAPI and docs are restricted to admins.
