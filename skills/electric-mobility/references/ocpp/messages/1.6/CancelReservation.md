# OCPP 1.6: CancelReservation

Direction: **Central System → Charge Point**. CALL action: `CancelReservation`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reservationId` | yes | `integer` |  |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `string` | values: Accepted, Rejected |

Unknown object fields are rejected by this schema.
