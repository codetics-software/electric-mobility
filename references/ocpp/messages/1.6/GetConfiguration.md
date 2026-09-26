# OCPP 1.6: GetConfiguration

Direction: **Central System → Charge Point**. CALL action: `GetConfiguration`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA OCPP-J JSON schema set. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `key` | no | `string[]` |  |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `configurationKey` | no | `object[]` |  |
| `unknownKey` | no | `string[]` |  |

Unknown object fields are rejected by this schema.

### `configurationKey` object

| Field | Required | Type | Constraints |
|---|---|---|---|
| `key` | yes | `string` | maxLength=50 |
| `readonly` | yes | `boolean` |  |
| `value` | no | `string` | maxLength=500 |

Unknown fields are rejected in this object.
