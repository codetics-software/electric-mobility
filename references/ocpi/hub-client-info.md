# OCPI — HubClientInfo Module

## Purpose

The HubClientInfo module lets a **Hub inform connected platforms about which other platforms are reachable and what versions they support**. Without it, a CPO connecting through a hub would have no way to know which eMSPs are available or what OCPI versions they speak.

**Data owner**: Hub  
**Direction**: Hub (Sender) → CPO / eMSP (Receiver)

---

## Version Availability

| Version | Available |
|---|---|
| 2.1.1 | No |
| 2.2.1 | Yes (new in 2.2.1) |
| 2.3.0 | Yes |

---

## When You Need This

Only relevant in **hub-based topologies**. If you are doing direct peer-to-peer OCPI, skip this module.

In a hub topology:
- CPO connects to Hub (one connection, not N connections to each eMSP)
- eMSP connects to Hub (one connection, not M connections to each CPO)
- Hub routes messages between them using routing headers

The CPO needs to know:
- Which eMSPs are currently online/reachable through this hub?
- What OCPI versions do those eMSPs support?
- Is the eMSP I want to reach currently connected?

HubClientInfo answers these questions.

---

## Key Data Model

### `ClientInfo`

| Field | Type | Description |
|---|---|---|
| `party_id` | string(3) | Party ID of the connected platform |
| `country_code` | string(2) | Country of the connected platform |
| `role` | Role | `CPO`, `EMSP`, `HUB`, `NAP`, `NSP`, `SCSP` |
| `status` | ConnectionStatus | Current connection status |
| `last_updated` | DateTime | When this status was last changed |

### `ConnectionStatus` Enum

| Value | Meaning |
|---|---|
| `CONNECTED` | Platform is currently connected and reachable |
| `OFFLINE` | Platform has disconnected / not reachable |
| `PLANNED` | Platform is expected to connect in the future |
| `SUSPENDED` | Platform temporarily suspended |

---

## HTTP Endpoints

### Sender Interface (Hub exposes this — platforms pull)

| Method | Path | Description |
|---|---|---|
| `GET` | `/ocpi/hub/2.x/hubclientinfo` | Get all known client statuses |

### Receiver Interface (CPO/eMSP exposes this — Hub pushes to)

| Method | Path | Description |
|---|---|---|
| `PUT` | `/ocpi/cpo/2.x/hubclientinfo/{country_code}/{party_id}` | Push a client status update |
| `PATCH` | `/ocpi/cpo/2.x/hubclientinfo/{country_code}/{party_id}` | Partial update |
| `GET` | `/ocpi/cpo/2.x/hubclientinfo/{country_code}/{party_id}` | Hub validates stored status |

---

## Usage Pattern

```
[Initial sync — pull all clients]
CPO → GET /ocpi/hub/2.x/hubclientinfo
  ← [
      { "party_id": "MSP", "country_code": "FR", "role": "EMSP", "status": "CONNECTED" },
      { "party_id": "ABC", "country_code": "DE", "role": "EMSP", "status": "OFFLINE" },
      ...
    ]

[Hub pushes real-time updates]
Hub → PUT /ocpi/cpo/2.x/hubclientinfo/FR/MSP
  { "status": "OFFLINE", "last_updated": "2025-06-01T14:05:00Z" }
```

---

## Implementation Notes

### Routing Decision
Before sending a command or pushing data to an eMSP through the hub, check HubClientInfo to verify the target eMSP is `CONNECTED`. Sending to an `OFFLINE` eMSP wastes a network call and the hub returns an error.

### Version Discovery
HubClientInfo provides reachability; it does not tell you which OCPI modules or versions the remote party supports. For that, you still need to do a Credentials handshake with the hub acting as a relay.

### Hub vs Direct Connection
Some hubs support **both hub-routed and direct connections**. A platform might be `OFFLINE` to the hub but still reachable directly. HubClientInfo only reflects hub-side reachability.

---

## Spec References

- 2.2.1: `mod_hub_client_info.asciidoc` — `release-2.2.1-bugfixes`
- 2.3.0: `mod_hub_client_info.asciidoc` — `2.3.0/release/core`
