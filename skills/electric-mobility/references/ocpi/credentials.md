# OCPI — Credentials & Registration Module

## Purpose

The Credentials module handles the **initial handshake** between two platforms before any other OCPI data can flow. It establishes mutual authentication tokens and lets each side discover which modules the other supports.

> Every subsequent OCPI call (Locations, Sessions, CDRs, etc.) is authorized by the token exchanged here.

---

## Version Availability

| Version | Mandatory |
|---|---|
| 2.1.1 | Yes |
| 2.2.1 | Yes |
| 2.3.0 | Yes |

---

## Core Concepts

### Token Lifecycle

Three tokens are involved during registration:

Here “Sender” means the registration initiator and “Receiver” means the
registration acceptor. These labels are not permanent market roles or the
functional modules' InterfaceRole values; either platform can initiate.

| Token | Created by | Used by | Purpose |
|---|---|---|---|
| `CREDENTIALS_TOKEN_A` | Receiver | Sender | Bootstrap — allows Sender to call `/versions` and `/credentials` only |
| `CREDENTIALS_TOKEN_B` | Sender | Receiver | Sent in the POST body so Receiver can call back into Sender |
| `CREDENTIALS_TOKEN_C` | Receiver | Sender | Final operational token; returned in POST response; replaces A |

After the handshake:
- Sender uses **TOKEN_C** for all future requests to Receiver
- Receiver uses **TOKEN_B** for all future requests back to Sender
- TOKEN_A is discarded

> TOKEN_A is **only** valid for `/versions` and `/credentials` endpoints. Any other endpoint receiving TOKEN_A MUST return HTTP 401.

### Out-of-Band Exchange

The acceptor supplies TOKEN_A and its own Versions URL **outside OCPI** through
an agreed secure channel. There is no in-protocol mechanism for initial contact.

---

## Registration Flow

```
[Out of band]
  Receiver → Sender: TOKEN_A + Receiver's /versions URL

[In OCPI]
Step 1 — Sender discovers versions
  Sender → GET /versions (using TOKEN_A)
  ← [{ version: "2.3.0", url: "..." }, ...]

Step 2 — Sender discovers endpoints for chosen version
  Sender → GET discovered 2.3.0 details URL (using TOKEN_A)
  ← { version: "2.3.0", endpoints: [{ identifier: "credentials", role: "SENDER", url: "..." }, ...] }

Step 3 — Sender registers itself
  Sender → POST /credentials (using TOKEN_A)
  Body: { token: TOKEN_B, url: Sender's /versions URL, roles: [...] }
  ← { token: TOKEN_C, url: Receiver's /versions URL, roles: [...] }

Step 4 — Receiver discovers Sender's endpoints
  Receiver → GET Sender's /versions (using TOKEN_B)
  Receiver → GET Sender's discovered 2.3.0 details URL (using TOKEN_B)
  (Receiver now knows all Sender endpoints)

Post-handshake state:
  Sender uses TOKEN_C  → calls Receiver
  Receiver uses TOKEN_B → calls Sender
  TOKEN_A is expired/discarded
```

---

## HTTP Endpoints

### Receiver Interface (you expose this if others register with you)

| Method | Path | Description |
|---|---|---|
| `GET` | `/ocpi/{version}/credentials` | Returns your current credentials for the calling party |
| `POST` | `/ocpi/{version}/credentials` | Initial registration — exchange tokens |
| `PUT` | `/ocpi/{version}/credentials` | Update credentials (token rotation) |
| `DELETE` | `/ocpi/{version}/credentials` | Unregister a partner |

### Versions Discovery (mandatory, separate from credentials)

| Method | Path | Description |
|---|---|---|
| `GET` | `/versions` | Returns list of supported OCPI versions |
| `GET` | `/versions/{version}` | Returns endpoints for that version |

---

## Data Models

### `Credentials` Object

```json
{
  "token": "ZWJmM2IzOTktNzc5Zi00NDk3...",
  "url": "https://partner.example.com/ocpi/versions",
  "roles": [
    {
      "role": "CPO",
      "business_details": {
        "name": "My Charging Network",
        "website": "https://example.com",
        "logo": { "url": "...", "category": "OPERATOR", "type": "png", "width": 512, "height": 512 }
      },
      "party_id": "MCP",
      "country_code": "FR"
    }
  ]
}
```

### `VersionNumber` Enum

`"2.0"`, `"2.1"`, `"2.1.1"`, `"2.2"`, `"2.2.1"`, `"2.3.0"`

`2.1` and `2.2` are deprecated in the current version definition; discovery can still encounter them in legacy integrations. Match the selected specification revision when parsing this open enum.

### `ModuleID` (Endpoint Identifier)

Each endpoint in `/versions/{version}` response has an `identifier`:

| Identifier | Module |
|---|---|
| `credentials` | Credentials |
| `locations` | Locations |
| `sessions` | Sessions |
| `cdrs` | CDRs |
| `tariffs` | Tariffs |
| `tokens` | Tokens |
| `commands` | Commands |
| `chargingprofiles` | ChargingProfiles (2.2+) |
| `hubclientinfo` | HubClientInfo (2.2+) |
| `invoicereconciliation` | InvoiceReconciliation (2.3.0 core edition 2) |
| `payments` | Payments (2.3.0 Payments package) |

Booking uses a separate 2.3.0 package; read that package's version endpoint and module identifier instead of inferring it from the core list. These are wire identifiers, not snake_case application names.

---

## Version Differences

### 2.1.1
- `roles` field in Credentials object doesn't exist — only CPO or eMSP, identified by the URL path (`/ocpi/cpo/` vs `/ocpi/emsp/`)
- `party_id` and `country_code` top-level on Credentials (not inside `roles`)

### 2.2 / 2.2.1
- **`roles` array** introduced in 2.2 — a single platform can declare multiple roles (CPO, eMSP, Hub, NSP, NAP, SCSP) in one Credentials object
- `party_id` and `country_code` move inside each role entry
- Hub routing headers added to all requests (not part of Credentials object itself, but established after handshake)

### 2.3.0
- Adds optional `hub_party_id` (`CiString(5)`), formed from country code plus party ID. A platform supporting hub routing must provide it.
- Hub platforms include reachable parties as ordinary CredentialsRole entries in `roles`; retain each `(country_code, party_id, role)` identity.
- The inspected core Role enum lists `CPO`, `EMSP`, `NAP`, `NSP`, `OTHER`, and `SCSP`, without the older `HUB` value. Read [roles.md](roles.md) for mapping and authorization.
- Keep bootstrap TOKEN_A restricted to Versions/Credentials. Pin the edition's HTTP error behavior and discover actual URLs. See [ocpi-2.3.0.md](ocpi-2.3.0.md).

---

## Implementation Notes

### Token Storage
Store per-partner:
- The outbound credentials token supplied by the peer, used to call them
- The inbound credentials token supplied by you, verified when they call you
- Their `/versions` URL
- Their declared roles and `party_id`/`country_code`

If you initiated the handshake, outbound is TOKEN_C and inbound is TOKEN_B.
If you accepted registration, outbound is TOKEN_B and inbound is TOKEN_C.
Avoid hard-coded B/C storage labels that reverse when the initiating side changes.

### Token Rotation (PUT /credentials)
Either party can initiate a token rotation at any time. Same flow as POST but replaces the existing TOKEN_C with a new one. The old token MUST remain valid until the new one is confirmed.

### Version Negotiation
Both parties must agree on a single version for the connection. Choose the **highest version both support**. If no overlap, connection cannot be established.

### Security
For token scope, server-side request forgery, and ownership checks, read
[securing OCPI and roaming](../security/ocpi-roaming.md).

- Always use TLS (HTTPS) — the spec requires server-side certificates
- Tokens are base64-encoded UUIDs; rotate them regularly
- TOKEN_A must be single-use scoped — reject any other endpoint call with it

### Soft-Delete / Unregister
`DELETE /credentials` removes the partner. After deletion, their tokens are invalid. Some hubs require notifying them before deleting.

---

## Common Pitfalls

- **Forgetting TOKEN_A scope**: Accepting TOKEN_A on non-credentials endpoints is a security bug — always validate token type before routing
- **Missing step 4**: The Receiver must also call back into the Sender's `/versions` endpoint to discover the Sender's module URLs — many implementations skip this and hardcode URLs
- **Stale module URLs**: After a `PUT /credentials` rotation, re-fetch `/versions/{version}` to get updated endpoint URLs — the partner may have changed their URL structure
- **Multi-role confusion (2.2+)**: A platform with CPO + eMSP roles sends both in the same Credentials POST. The receiver must store both role contexts

---

## Spec References

- 2.1.1: `credentials.md` — `release-2.1.1-bugfixes`
- 2.2.1: `credentials.asciidoc` — `release-2.2.1-bugfixes`
- 2.3.0: `credentials.asciidoc` — `2.3.0/release/core`
