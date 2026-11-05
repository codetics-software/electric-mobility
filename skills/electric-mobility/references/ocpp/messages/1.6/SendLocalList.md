# OCPP 1.6: SendLocalList

Direction: **Central System → Charge Point**. CALL action: `SendLocalList`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA OCPP-J JSON schema set. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state.

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
