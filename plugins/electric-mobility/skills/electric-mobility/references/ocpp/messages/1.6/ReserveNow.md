# OCPP 1.6: ReserveNow

Direction: **Central System → Charge Point**. CALL action: `ReserveNow`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `connectorId` | yes | `integer` |  |
| `expiryDate` | yes | `string` | format=date-time |
| `idTag` | yes | `string` | maxLength=20 |
| `parentIdTag` | no | `string` | maxLength=20 |
| `reservationId` | yes | `integer` |  |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `string` | values: Accepted, Faulted, Occupied, Rejected, Unavailable |

Unknown object fields are rejected by this schema.
