# OCPP 1.6: UnlockConnector

Direction: **Central System → Charge Point**. CALL action: `UnlockConnector`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `connectorId` | yes | `integer` |  |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `string` | values: Unlocked, UnlockFailed, NotSupported |

Unknown object fields are rejected by this schema.
