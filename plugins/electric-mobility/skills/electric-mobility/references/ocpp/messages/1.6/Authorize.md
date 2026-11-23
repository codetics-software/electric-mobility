# OCPP 1.6: Authorize

Direction: **Charge Point → Central System**. CALL action: `Authorize`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `idTag` | yes | `string` | maxLength=20 |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `idTagInfo` | yes | `object` |  |

Unknown object fields are rejected by this schema.

### `idTagInfo` object

| Field | Required | Type | Constraints |
|---|---|---|---|
| `expiryDate` | no | `string` | format=date-time |
| `parentIdTag` | no | `string` | maxLength=20 |
| `status` | yes | `string` | values: Accepted, Blocked, Expired, Invalid, ConcurrentTx |

Unknown fields are rejected in this object.
