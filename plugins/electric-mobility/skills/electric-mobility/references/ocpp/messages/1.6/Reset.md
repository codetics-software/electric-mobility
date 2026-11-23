# OCPP 1.6: Reset

Direction: **Central System → Charge Point**. CALL action: `Reset`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `type` | yes | `string` | values: Hard, Soft |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `string` | values: Accepted, Rejected |

Unknown object fields are rejected by this schema.
