# Securing OCPI and roaming

Read [the security gate](README.md) first. Pair this guide with
[credentials](../ocpi/credentials.md), [roles](../ocpi/roles.md), and the module
reference. Token encoding, hub routing, and message routing headers vary by version,
so verify them in the selected version. For example, 2.2 and later define Base64
encoding of the token in the `Authorization` header, while 2.1.1 does not.

## The threat model

A roaming partner is a separate company with its own bugs and its own breaches.
Treat every partner as authenticated but not trusted:

- it can send objects claiming to belong to someone else;
- it can supply URLs that your server will then call, with your credential attached;
- it can be compromised, so one partner's token must expose one partner's scope only;
- a hub may relay data from parties you have never met.

## Token lifecycle

- **Scope the bootstrap token.** The registration token (TOKEN_A) may reach only
  version discovery and credentials. Every other module requires a completed
  registration.
- **Scope tokens by role and partner.** A token issued for the CPO interface must not
  work on the eMSP interface of the same platform. Look it up with the role as part of
  the query, and resolve the tenant from the token.
- **Generate from a CSPRNG** with at least 256 bits of entropy, within the version's
  length limit.
- **Store two forms for two purposes.** Keep a hash of inbound tokens for lookup, since
  high-entropy tokens do not need a slow hash. Keep the outbound token, and any token
  you must return from `GET /credentials`, in authenticated encryption.
- **Rotate during the exchange.** `POST` and `PUT` issue a new token and invalidate the
  old one, inside a transaction that re-reads the partner under lock. If the token
  changed meanwhile, answer with a conflict instead of overwriting it.
- **Do the remote calls before taking the lock**, so a slow partner cannot hold your
  row lock.
- **`DELETE` clears everything:** both tokens, stored endpoints, and registered state.
  Reject `POST` when registered and `PUT` when not registered.
- **Answer identically** for an unknown token and a malformed one. Limit header length
  before hashing. Check that the tenant is active.

## Outbound calls and server-side request forgery

Partner-supplied URLs reach your server in the credentials body, the versions
response, the endpoints list, `Link` pagination headers, and `response_url` on
commands. Each one would be called carrying your token.

Run all of them through one validator:

1. `https` only, standard port, no embedded credentials, no fragment.
2. Host must match the partner origin an administrator configured. Do not take the
   origin from the partner's own message, and do not let it change after registration
   without an admin action.
3. **Check the resolved address too.** Origin pinning stops most abuse, but the admin
   might enter a bad origin and DNS can change. Refuse private, loopback, link-local,
   and metadata ranges at connection time, on the address actually connected to, so
   DNS rebinding fails too.
4. Redirects stay off. A redirect sends your credential to wherever it points.
5. Set connect and total timeouts. Read a bounded number of bytes and refuse anything
   larger. Limit pages and objects per sync.
6. Check both the HTTP status and the OCPI `status_code`. Never surface the partner's
   raw response or token in an error.

Validate `next` page links with the same validator. If a link fails, stop and record
the failure rather than continuing silently.

## Ownership of received objects

- **Path identity must match the credential.** In
  `/{country_code}/{party_id}/{id}`, `country_code` and `party_id` must belong to the
  authenticated partner. Without this check one partner can overwrite another's data.
- **Body must match path.** Refuse an object whose own ID differs from the path.
- **Validate path segments** with a strict pattern and length before using them as keys.
- **Store with partner and tenant in the key**, so that two partners using the same ID
  cannot collide.
- **Validate received fields** and required values. Reject an update with no
  `last_updated`, and ignore one older than the stored version.
- **Never let a received object change your own data.** A partner's Location never
  updates your stations, and a partner's Token never modifies a local badge.
- **Only allow modules valid for that role and direction.** Push and pull allowlists
  depend on role.
- **With a hub**, the authenticated party is the hub, and routing headers name the
  claimed parties. Verify the hub's routing rules for that version, then authorize both.

## CDRs and financial data

A received CDR is immutable, and the same ID must not overwrite or double-bill. A
correction arrives as a credit CDR, per protocol. Keep the original bytes or a hash for
dispute evidence. Do not trust a partner's totals blindly either: reconcile them
against the tariff and session, and flag differences instead of correcting silently.

## Commands

- Accept commands only on the interface that may receive them, for the partner that
  owns the token, on EVSEs that this tenant publishes.
- Map to a station through your own mapping. Never build a station ID from partner text
  without checking it.
- Run `response_url` through the outbound validator **before** accepting the command,
  and store it with the command record.
- Return the protocol's immediate result, then deliver the real result by callback.
  Persist the callback so a restart cannot lose it, and retry with a limit.
- Check the token and the site's roaming policy before queuing the station command.
- Do not expose every local command through roaming. `UNLOCK_CONNECTOR` needs extra
  thought: confirm it is enabled and that the requester is linked to that session.

## Roaming authorization

- **Decide your failure posture for each whitelist value.** A partner being unreachable
  should fail closed where real-time authorization is required, and may fail open only
  where the token's rules allow offline use. Document that choice, since it trades
  availability for financial risk.
- **Do not cross tenants when matching tokens.** Match on tenant, module, and direction,
  and compare the exact UID at the end instead of relying on a substring match.
- **Send the minimum** in authorization requests, and bound the time you wait, so a
  driver is not left standing at the charger because a partner is slow.

## What crosses the border

Decide deliberately what each partner sees:

- Publish only sites marked for roaming, and only the fields needed.
- **Never roam local-only identifiers** such as AutoCharge vehicle identifiers or
  one-time payment badges.
- **Tokens, sessions, and CDRs are personal data.** They reveal where and when a person
  charged. Limit retention, record the legal basis, and make deletion reach stored
  partner copies where required.

## Tests every OCPI change needs

- TOKEN_A refused on every non-credentials module.
- A CPO token refused on the eMSP interface.
- A partner's token writing under another party's `country_code` and `party_id` is refused.
- Body ID differing from path ID is refused.
- Credentials exchange with a URL on another host is refused, and no token was sent there.
- A redirect from a partner is not followed.
- `Link` pagination to another host stops the sync.
- `response_url` on another host rejects the command before any station call.
- A response above the size limit fails safely.
- An HTTP 200 with a failing `status_code` counts as a failure.
- A repeated CDR is idempotent and cannot overwrite the original.
- Concurrent credential update: the loser receives a conflict and the winner's token survives.
- `DELETE /credentials` makes the old tokens fail immediately.
