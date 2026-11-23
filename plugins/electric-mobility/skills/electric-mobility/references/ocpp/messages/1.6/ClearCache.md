# OCPP 1.6: ClearCache

Direction: **Central System → Charge Point**. CALL action: `ClearCache`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| *(empty object)* | — | — | — |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `string` | values: Accepted, Rejected |

Unknown object fields are rejected by this schema.
