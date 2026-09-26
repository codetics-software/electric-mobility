# OCPP 1.6: StartTransaction

Direction: **Charge Point → Central System**. CALL action: `StartTransaction`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA OCPP-J JSON schema set. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `connectorId` | yes | `integer` |  |
| `idTag` | yes | `string` | maxLength=20 |
| `meterStart` | yes | `integer` |  |
| `reservationId` | no | `integer` |  |
| `timestamp` | yes | `string` | format=date-time |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `idTagInfo` | yes | `object` |  |
| `transactionId` | yes | `integer` |  |

Unknown object fields are rejected by this schema.

### `idTagInfo` object

| Field | Required | Type | Constraints |
|---|---|---|---|
| `expiryDate` | no | `string` | format=date-time |
| `parentIdTag` | no | `string` | maxLength=20 |
| `status` | yes | `string` | values: Accepted, Blocked, Expired, Invalid, ConcurrentTx |

Unknown fields are rejected in this object.
