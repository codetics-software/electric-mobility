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

TOKEN_A and the Sender's `/versions` URL are exchanged **outside OCPI** (email, portal, secure message). There is no in-protocol mechanism for initial contact.

---

## Registration Flow

```
[Out of band]
  Receiver → Sender: TOKEN_A + Receiver's /versions URL

[In OCPI]
Step 1 — Sender discovers versions
  Sender → GET /versions (using TOKEN_A)
  ← [{ version: "2.2.1", url: "..." }, ...]

Step 2 — Sender discovers endpoints for chosen version
  Sender → GET /versions/2.2.1 (using TOKEN_A)
  ← { version: "2.2.1", endpoints: [{ identifier: "credentials", url: "..." }, ...] }

Step 3 — Sender registers itself
  Sender → POST /credentials (using TOKEN_A)
  Body: { token: TOKEN_B, url: Sender's /versions URL, roles: [...] }
  ← { token: TOKEN_C, url: Receiver's /versions URL, roles: [...] }

Step 4 — Receiver discovers Sender's endpoints
  Receiver → GET Sender's /versions (using TOKEN_B)
  Receiver → GET Sender's /versions/2.2.1 (using TOKEN_B)
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

`"2.0"`, `"2.1"`, `"2.1.1"`, `"2.2"`, `"2.2.1"`, `"2.3"`

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
| `charging_profiles` | ChargingProfiles (2.2.1+) |
| `hub_client_info` | HubClientInfo (2.2.1+) |
| `direct_payment` | DirectPayment (2.3.0+) |

---

## Version Differences

### 2.1.1
- `roles` field in Credentials object doesn't exist — only CPO or eMSP, identified by the URL path (`/ocpi/cpo/` vs `/ocpi/emsp/`)
- `party_id` and `country_code` top-level on Credentials (not inside `roles`)

### 2.2.1
- **`roles` array** introduced — a single platform can declare multiple roles (CPO, eMSP, Hub, NSP, NAP, SCSP) in one Credentials object
- `party_id` and `country_code` move inside each role entry
- Hub routing headers added to all requests (not part of Credentials object itself, but established after handshake)

### 2.3.0
- Same structure as 2.2.1
- Stronger wording on TOKEN_A scope restrictions
- Clearer guidance on version negotiation when one party supports 2.3.0 and the other only 2.2.1

---

## Implementation Notes

### Token Storage
Store per-partner:
- Their TOKEN_B (you call them with this)
- Your TOKEN_C (they call you with this — validate on every incoming request)
- Their `/versions` URL
- Their declared roles and `party_id`/`country_code`

### Token Rotation (PUT /credentials)
Either party can initiate a token rotation at any time. Same flow as POST but replaces the existing TOKEN_C with a new one. The old token MUST remain valid until the new one is confirmed.

### Version Negotiation
Both parties must agree on a single version for the connection. Choose the **highest version both support**. If no overlap, connection cannot be established.

### Security
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
- **Multi-role confusion (2.2.1+)**: A platform with CPO + eMSP roles sends both in the same Credentials POST. The receiver must store both role contexts

---

## Spec References

- 2.1.1: `credentials.md` — `release-2.1.1-bugfixes`
- 2.2.1: `credentials.asciidoc` — `release-2.2.1-bugfixes`
- 2.3.0: `credentials.asciidoc` — `2.3.0/release/core`
