# OCPP 1.6: GetConfiguration

Direction: **Central System → Charge Point**. CALL action: `GetConfiguration`.

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
