# OCPI — Tokens Module

## Purpose

The Tokens module exchanges **driver authorization tokens** — the credentials that identify a driver and determine whether they can start a charging session. The eMSP owns tokens (RFID cards, app-based identifiers); the CPO receives and caches them for local authorization.

**Data owner**: eMSP  
**Direction**: eMSP (Sender) → CPO (Receiver)

---

## Version Availability

| Version | Mandatory |
|---|---|
| 2.1.1 | Required for roaming |
| 2.2.1 | Required for roaming |
| 2.3.0 | Required for roaming |

---

## Authorization Models

### Whitelist (Offline Authorization)
The eMSP pushes all valid tokens to the CPO. The CPO authorizes locally without calling back to the eMSP. Fast, resilient to network outages, but token state can drift.

### Real-Time Authorization (Online Authorization)
When a driver presents a token, the CPO calls back to the eMSP with a `POST /authorize` request and waits for a response. Always current, but adds latency and requires connectivity.

Both can coexist: the CPO can fall back to whitelist if real-time fails.

---

## Key Data Models

### `Token`

| Field | Type | Description |
|---|---|---|
| `country_code` | string(2) | eMSP's country |
| `party_id` | string(3) | eMSP's party ID |
| `uid` | string(36) | Physical token identifier (RFID UID, app token) |
| `type` | TokenType | Type of token |
| `contract_id` | string(36) | eMI3 Contract ID (`FR*MCP*C12345*6`) |
| `visual_number` | string? | Human-readable number printed on card |
| `issuer` | string | Name of the eMSP that issued this token |
| `group_id` | string? (2.2.1+) | Groups tokens (e.g., employee cards for one company) |
| `valid` | boolean | Whether this token is currently valid |
| `whitelist` | WhitelistType | How CPO should handle this token |
| `language` | string? | ISO 639-1 preferred language |
| `default_profile_type` | ProfileType? (2.2.1+) | Default smart charging preference |
| `energy_contract` | EnergyContract? (2.2.1+) | Direct energy contract details |
| `last_updated` | DateTime | |

### `TokenType` Enum

| Value | Meaning |
|---|---|
| `AD_HOC_USER` (2.2.1+) | One-time use / guest token |
| `APP_USER` (2.2.1+) | App-based token (no physical card) |
| `OTHER` | Non-standard token type |
| `RFID` | Physical RFID card |

### `WhitelistType` Enum

| Value | CPO Behavior |
|---|---|
| `ALWAYS` | Always allow offline (never call eMSP) |
| `ALLOWED` | Allow offline; may call eMSP in real-time if desired |
| `ALLOWED_OFFLINE` | Use offline when eMSP unreachable; prefer real-time |
| `NEVER` | Always require real-time authorization — reject if eMSP unreachable |

---

## HTTP Endpoints

### Sender Interface (eMSP exposes this — CPO pulls from)

| Method | Path | Description |
|---|---|---|
| `GET` | `/ocpi/emsp/2.x/tokens` | Get all tokens (paginated) |
| `GET` | `/ocpi/emsp/2.x/tokens/{token_uid}/authorize` | Real-time authorization request |

### Receiver Interface (CPO exposes this — eMSP pushes to)

| Method | Path | Description |
|---|---|---|
| `PUT` | `/ocpi/cpo/2.x/tokens/{country_code}/{party_id}/{token_uid}` | Push / update token |
| `PATCH` | `/ocpi/cpo/2.x/tokens/{country_code}/{party_id}/{token_uid}` | Partial update (e.g., `valid: false`) |
| `GET` | `/ocpi/cpo/2.x/tokens/{country_code}/{party_id}/{token_uid}` | eMSP validates token on CPO |

---

## Real-Time Authorization Flow

```
Driver presents RFID card at charger
  ↓
CPO checks local whitelist — not found (or NEVER whitelist)
  ↓
CPO → GET /ocpi/emsp/2.x/tokens/{token_uid}/authorize
  Query params:
    type: RFID (optional — token type hint)
  Body (2.2.1+):
    { "location_id": "LOC001", "evse_uid": "EV001", "connector_id": "1" }
  ← AuthorizationInfo:
    {
      "allowed": "ALLOWED",
      "token": { ...Token object... },
      "location": { "location_id": "LOC001", ... },
      "authorization_reference": "AUTH-XYZ-123",
      "info": { "language": "fr", "text": "Bienvenue !" }
    }
  ↓
If "allowed" = "ALLOWED" → start session
If "allowed" = "BLOCKED" / "EXPIRED" / "NO_CREDIT" / "NOT_ALLOWED" → reject
```

### `AllowedType` Enum

| Value | Meaning |
|---|---|
| `ALLOWED` | Token valid — allow charging |
| `BLOCKED` | Token explicitly blocked |
| `EXPIRED` | Token past its validity date |
| `NO_CREDIT` | Insufficient credit (prepaid eMSP) |
| `NOT_ALLOWED` | Not allowed at this location/EVSE |

---

## Token Sync Strategy

### Full Pull (Initial Sync)
```
GET /ocpi/emsp/2.x/tokens?limit=1000
→ walk all pages via Link: rel="next"
→ store each token with uid + last_updated
```

### Delta Sync (Periodic)
```
GET /ocpi/emsp/2.x/tokens?date_from=<last_sync>&limit=1000
→ apply changes to local whitelist
```

### Push (Real-Time)
```
eMSP → PUT /ocpi/cpo/2.x/tokens/FR/MCP/RFID123
{ "valid": false, "last_updated": "2025-06-01T12:00:00Z" }
```

Immediately invalidates a lost or stolen card on the CPO's local whitelist.

---

## Version Differences

### 2.1.1
- `type` values: `RFID`, `OTHER` only
- No `group_id`
- No `APP_USER` or `AD_HOC_USER`
- No `default_profile_type`
- No `energy_contract`
- `auth_id` used (later renamed to `uid` in 2.2.1)
- Real-time auth body is simpler (no location context sent)

### 2.2.1
- `APP_USER` and `AD_HOC_USER` token types added
- `group_id` for grouping related tokens (fleet/corporate)
- `default_profile_type` for smart charging preference per token
- `energy_contract` for direct energy supplier contracts
- Real-time auth request body includes location context
- `authorization_reference` in real-time auth response — CPO embeds this in Session/CDR for traceability
- `contract_id` format clarified (eMI3 standard)

### 2.3.0
- Expanded `CdrToken` (used in CDRs/Sessions) with `country_code` + `party_id` for global identification
- Token type `AD_HOC_USER` semantics clarified for AFIR direct payment flows
- Stronger guidance on `NEVER` whitelist behavior — CPO must reject if eMSP is unreachable

---

## Implementation Notes

### Whitelist Size
Large eMSPs can have millions of tokens. Plan for a token store that supports:
- Fast lookup by `uid` (primary access pattern)
- Efficient delta sync via `last_updated`
- Indexed by `(country_code, party_id, uid)` for multi-eMSP deployments

### Token Revocation
When a driver reports a lost card, the eMSP PATCHes `{ "valid": false }` and pushes it to all connected CPOs. CPOs should apply this within seconds on push; the delta sync cadence covers CPOs that only pull.

### `group_id` Use Cases
Useful for corporate fleet cards — multiple physical cards map to one account. Some eMSPs use group_id to enforce per-group usage policies (e.g., max concurrent sessions for a company).

### Token UID vs Contract ID
- **`uid`**: Physical identifier on the card or app token. Not unique globally.
- **`contract_id`**: eMI3 standard identifier unique to a driver–eMSP contract. Used in CDRs.

Both are needed. The CPO uses `uid` for authorization; the CDR references `contract_id` for billing.

---

## Common Pitfalls

- **`uid` is not globally unique**: Two different eMSPs can issue different cards with the same physical UID. Always index tokens by `(country_code, party_id, uid)` triplet — not by uid alone
- **Ignoring `whitelist: NEVER`**: Some eMSPs require real-time auth for every session (prepaid accounts). If your CPO silently falls back to whitelist for these, you'll accept unauthorized sessions
- **Stale whitelist**: If you don't process push updates promptly, revoked tokens remain valid. Implement push receiver with low latency
- **Missing real-time auth location context (2.2.1+)**: Some eMSPs use the location context to apply different authorization rules per site. Omitting it may result in incorrect authorization decisions

---

## Spec References

- 2.1.1: `mod_tokens.md` — `release-2.1.1-bugfixes`
- 2.2.1: `mod_tokens.asciidoc` — `release-2.2.1-bugfixes`
- 2.3.0: `mod_tokens.asciidoc` — `2.3.0/release/core`
