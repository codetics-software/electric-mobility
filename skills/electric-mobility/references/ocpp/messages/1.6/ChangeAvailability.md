# OCPP 1.6: ChangeAvailability

Direction: **Central System → Charge Point**. CALL action: `ChangeAvailability`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `connectorId` | yes | `integer` |  |
| `type` | yes | `string` | values: Inoperative, Operative |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `string` | values: Accepted, Rejected, Scheduled |

Unknown object fields are rejected by this schema.
