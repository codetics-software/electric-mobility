# OCPP 1.6: Heartbeat

Direction: **Charge Point → Central System**. CALL action: `Heartbeat`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| *(empty object)* | — | — | — |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `currentTime` | yes | `string` | format=date-time |

Unknown object fields are rejected by this schema.
