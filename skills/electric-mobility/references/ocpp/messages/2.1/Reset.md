# OCPP 2.1: Reset

Direction: **CSMS → Charging Station**. CALL action: `Reset`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `type` | yes | `ResetEnumType` |  |
| `evseId` | no | `integer` | minimum=0.0 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `ResetEnumType`

Allowed values: `Immediate`, `OnIdle`, `ImmediateAndResume`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `ResetStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `ResetStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `Scheduled`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
