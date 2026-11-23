# OCPP 2.1: GetDisplayMessages

Direction: **CSMS → Charging Station**. CALL action: `GetDisplayMessages`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `id` | no | `integer[]` | minItems=1 |
| `requestId` | yes | `integer` |  |
| `priority` | no | `MessagePriorityEnumType` |  |
| `state` | no | `MessageStateEnumType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `MessagePriorityEnumType`

Allowed values: `AlwaysFront`, `InFront`, `NormalCycle`

#### `MessageStateEnumType`

Allowed values: `Charging`, `Faulted`, `Idle`, `Unavailable`, `Suspended`, `Discharging`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `GetDisplayMessagesStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `GetDisplayMessagesStatusEnumType`

Allowed values: `Accepted`, `Unknown`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
