# Securing stations and OCPP

Read [the security gate](README.md) first. Pair this guide with
[the WebSocket runtime guide](../ocpp/websocket-and-runtime.md) and the message
cards for your version. Security profile details depend on the version, edition,
and OCA security extension, so check the selected source before claiming a
protocol requirement. Everything else here is engineering policy from production
experience.

## The threat model

A station is a computer in a public car park, on a cellular network, often running
old firmware with a credential that can be read from its flash. Assume that:

- one station can be physically compromised, so its credential must only ever
  unlock that station's own identity;
- station messages can be false, including meter values, status, and identifiers;
- anyone can reach the WebSocket endpoint and try station IDs printed on the
  hardware;
- a displaced connection is an attack as well as a network event.

## Connection handshake

Do all of this during the HTTP upgrade, before the socket is accepted:

1. **Validate the path.** Check tenant and station ID against strict patterns.
   Reject `.` and `..`. Limit length.
2. **Rate-limit first.** Limit by client address and by address + station, before
   any slow password hash. Rate limits must allow for a fleet sharing one carrier
   NAT address and for everything reconnecting after a server restart. Prefer
   counting failures, and test a full-fleet reconnect against the limit.
3. **Look up the station within the tenant.** Key on tenant + station ID, because
   station IDs are not globally unique. Refuse deleted or disabled stations.
4. **Bind the credential to this station.** The Basic username must equal the
   station ID from the path. The credential is checked against that station only,
   so it can never authenticate a neighbor. A client certificate must carry this
   station's identity or match its pinned fingerprint.
5. **Work out the level actually achieved, then compare.** Compute effective
   profile from verified facts (TLS present, password valid, certificate valid) and
   refuse if it is below the station's required level.
6. **Give one external answer.** Unknown tenant, unknown station, and wrong password
   all return the same 401, so nobody can enumerate a fleet. Record the real reason
   privately in the known station's event history, throttled to avoid log flooding,
   and never with a secret.

## Security levels

| Level | What it means | Use |
|---|---|---|
| No authentication | Anyone can claim the identity | Legacy only: server-wide setting off by default, plus a per-station opt-in, audited |
| Profile 1 | Basic auth without TLS | The password crosses the network in clear. Only on a private network you control |
| Profile 2 | TLS and Basic auth | Minimum for anything crossing the internet |
| Profile 3 | Mutual TLS | Preferred. The identity comes from a certificate rather than a shared password |

Rules that keep these levels meaningful:

- A station may connect above its required level, never below.
- Raising a level has two phases. Send the setting, keep accepting the old level,
  and apply the new one only on the first connection that reaches it. A rejected or
  unanswered request cancels the change. Otherwise one failed command strands the
  station.
- Refuse to raise a station to a level it cannot reach: no TLS connection seen yet,
  no client certificate known, or no CA configured on the server.
- Lowering is server-side, privileged, audited, and needs an on-site reconfiguration.
- After raising a requirement, disconnect any socket below the new level.

Use a dedicated hostname for mutual TLS. Browsers then never get a certificate
prompt on the dashboard, and the TLS policy can be strict for that host alone.

## Reverse proxies

Most deployments terminate TLS at a proxy, so the proxy's claims become your
security decision.

- Trust `X-Forwarded-For`, `X-Forwarded-Proto`, and client-certificate headers only
  when the **TCP peer** is in a configured list of proxy ranges. With an empty list,
  trust none.
- Pick the client as the rightmost untrusted hop, because everything to its left can
  be forged by the client.
- Allow a narrower proxy list for certificate headers than for address headers.
- The proxy must verify the client certificate itself and **overwrite** any copy
  from the client. On hosts without mutual TLS, it must clear that header.
- Block direct network access to the backend, for example with a network policy.
  Anyone who can reach the backend directly and pass the proxy check can forge a
  certificate header. Check that your cluster's network plugin enforces the policy.
- Publish only `/ocpp` and `/ocpi` from the backend to the internet. Keep actuator,
  API docs, and internal routes private.

## Credentials and rotation

- Generate station passwords from a CSPRNG. Show them once and store only a hash.
- Rotate with overlap: store a pending hash, send the new key, accept both, and
  promote the pending one when the station reconnects with it. An operator can also
  revoke the old one explicitly.
- Do not allow a rotation to be cancelled once the station may have received the new
  key. It might now hold only that key.
- The new secret passes through the command record. Redact it as soon as the command
  finishes, and also on cancellation. Prefer never persisting it in clear: encrypt the
  queued payload, and keep it out of logs and any UI that shows command history.
- Slow password hashes make reconnect storms expensive. Limit concurrent verification
  and size the cost for a whole-fleet reconnect.

## Certificates

Validate a presented certificate in this order: validity dates, pin if one is set,
chain to a configured anchor, then identity equals the station ID. Then handle these
easy-to-miss points:

- **Revocation must really revoke.** Tracking the last certificate you issued only
  covers certificates you signed. A certificate from an external CA still chains
  correctly after an operator clicks "revoke", unless you also keep a deny list or
  check CRL or OCSP. Decide how each trust path revokes, and test that a revoked
  certificate fails on reconnect.
- **Check key usage on presented certificates**, so that a server or signing
  certificate from the same CA cannot pass as a station.
- **Signing station CSRs:** verify the CSR signature and require the subject to equal
  the authenticated station's ID. Issue with `CA:false`, client-auth usage only, a
  fresh random serial, and a lifetime no longer than the CA's. Ignore extensions
  requested by the station. A station must never be able to request another
  station's identity or a CA certificate.
- **Protect the signing key.** It can mint any station identity, so prefer an HSM or
  KMS over an environment variable when the deployment allows it.
- **Alert before expiry.** Notify well ahead (30 days works), because an expired
  certificate takes a station offline and may require a site visit.
- **Certificate actions are admin-only**, on dedicated paths, and audited.

## Command authorization

| Effect | Examples | Minimum control |
|---|---|---|
| Disruptive | `Reset`, `ChangeAvailability`, `UnlockConnector` | Operator or higher, tenant check, audit, state check where possible |
| Session control | Remote start and stop | Authorized for that session or token, correlated, audit |
| Power | `SetChargingProfile`, `ClearChargingProfile` | Operator or higher, bounded values, site limits respected |
| Code on the device | `UpdateFirmware`, `SignedUpdateFirmware`, `PublishFirmware` | Admin only, approved source, signed where supported, audit |
| Data leaving the device | `GetDiagnostics`, `GetLog` | Admin or a restricted role, approved destination, retention rule |
| Security | `SecurityProfile`, `AuthorizationKey`, certificate actions, network profiles | Dedicated flow only, never the generic path |

- **Allowlist actions by direction.** A station cannot call a CSMS-only action, and
  the reverse also holds.
- **Firmware and diagnostics URLs are a real risk.** Validating only that `location`
  is present lets anyone with command access point a station at any server. It could
  install attacker firmware on stations without signed firmware support, or upload
  diagnostics to the attacker. Allow only approved hosts and schemes, restrict by
  role, and prefer signed firmware. Generate the URL server-side where you can.
- **Protected keys stay off generic paths.** Block them in the generic command path,
  in configuration templates, and in anything applied automatically at boot. Compare
  case-insensitively.
- **Validate commands going out**, as well as messages coming in. A malformed
  outbound payload is still your bug in the field.
- **Commit before sending.** Mark the command as sent and commit, then write to the
  socket. A crash must not replay something the station may have already executed.
- **Do not trust a response just because the ID matches.** Match the command to the
  tenant and station of the connection that answered. Ignore responses to commands
  already finished, and treat a late response as evidence rather than as a new result.

## Messages and sessions

- Limit frame size, message ID length, and calls per connection. Close on garbage
  that has no recoverable message ID.
- Serialize writes per socket. Many WebSocket libraries are not safe for concurrent
  writes.
- **Replace a duplicate connection only after the new one authenticates.** With weak
  authentication, the "newest connection wins" rule lets an attacker kick a real
  station off and hijack its commands. Alert when a station's connections flap.
- **Deduplicate by tenant, station, and message ID, with the payload hash.** The same
  ID with the same payload gets the stored response. The same ID with different
  content on one connection is a protocol error. Across reconnects, replay only
  transaction and meter messages, since many stations restart their counter from 1.
- **Treat vendor `DataTransfer` as untrusted.** Accept only declared vendors for that
  station. Record the rest, and never let the payload drive logic directly.
- **Reject impossible measurements.** Refuse timestamps too far in the future, ignore
  samples before the session start, and sanity-check energy and session duration. A
  meter value can be false as well as late. See
  [payments](payments-and-public-charging.md) for how billing uses meter evidence.
- **Sanitize stored text.** Vendor, model, and firmware strings end up in dashboards,
  so truncate them and escape on display.

## Identifiers are not secrets

**An RFID UID can be read and cloned.** Treat it as an identifier with limited
assurance. Decide with the operator whether a site's risk accepts that, and keep the
ability to block a token immediately. Also limit offline authorization lists, and
remember a station may accept a token you have since blocked.

**A vehicle MAC (EVCCID, AutoCharge) can also be read and copied.** If you offer plug-
and-charge by MAC, build these guardrails in, and tell the operator about the residual
risk:

- Off by default, enabled per station, and enforced server-side, whatever the station
  claims about its own settings.
- Accept only within a short window after a physically observed plug-in, and only on
  that connector. Unplugging clears the observed value.
- Enroll from a recent session of the same driver where the station reported the
  identifier. Only an administrator may type one in.
- One owner per identifier. Refuse broadcast, multicast, and all-zero addresses.
- Same rules as other tokens: enabling, expiry, site access. Never publish through
  roaming.
- Revoke when the vehicle or user is deleted, or when the vehicle changes owner.

ISO 15118 Plug & Charge is the cryptographic alternative, using contract certificates
and a PKI. It has its own trust chain and revocation checks, so verify the exact
edition and do not treat it as a variant of MAC-based AutoCharge.

## Tests every station change needs

- Wrong password, no password, wrong username, and another station's password.
- Required level above the effective one, with and without TLS.
- Forwarded headers from an untrusted peer are ignored.
- Certificate headers from an untrusted peer are ignored, and a client-supplied copy
  is overwritten at the proxy.
- Wrong identity, foreign CA, expired certificate, and **revoked certificate on
  reconnect**, for each trust path.
- A CSR naming another station is refused.
- Rotation: old works, new works, new promotes, and a lost response leaves a working
  credential.
- Generic path cannot set protected keys, including with different casing.
- Firmware or diagnostics URL from an unapproved host is refused.
- Response from another station's connection does not complete a command.
- Message replay across a reconnect does not duplicate a transaction.
- Displaced connection requires authentication first.
