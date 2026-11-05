# OCPP 1.6: SendLocalList

Direction: **Central System → Charge Point**. CALL action: `SendLocalList`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `listVersion` | yes | `integer` |  |
| `localAuthorizationList` | no | `object[]` |  |
| `updateType` | yes | `string` | values: Differential, Full |

Unknown object fields are rejected by this schema.

### `localAuthorizationList` object

| Field | Required | Type | Constraints |
|---|---|---|---|
| `idTag` | yes | `string` | maxLength=20 |
| `idTagInfo` | no | `object` |  |

Unknown fields are rejected in this object.

### `localAuthorizationList.idTagInfo` object

| Field | Required | Type | Constraints |
|---|---|---|---|
| `expiryDate` | no | `string` | format=date-time |
| `parentIdTag` | no | `string` | maxLength=20 |
| `status` | yes | `string` | values: Accepted, Blocked, Expired, Invalid, ConcurrentTx |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `string` | values: Accepted, Failed, NotSupported, VersionMismatch |

Unknown object fields are rejected by this schema.
