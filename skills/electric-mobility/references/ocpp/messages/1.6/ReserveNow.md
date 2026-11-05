# OCPP 1.6: ReserveNow

Direction: **Central System → Charge Point**. CALL action: `ReserveNow`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA OCPP-J JSON schema set. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state.

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
