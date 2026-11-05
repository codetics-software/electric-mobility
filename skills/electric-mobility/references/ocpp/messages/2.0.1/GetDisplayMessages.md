# OCPP 2.0.1: GetDisplayMessages

Direction: **CSMS → Charging Station**. CALL action: `GetDisplayMessages`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `id` | no | `integer[]` | minItems=1 |
| `requestId` | yes | `integer` |  |
| `priority` | no | `MessagePriorityEnumType` |  |
| `state` | no | `MessageStateEnumType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `MessagePriorityEnumType`

Allowed values: `AlwaysFront`, `InFront`, `NormalCycle`

#### `MessageStateEnumType`

Allowed values: `Charging`, `Faulted`, `Idle`, `Unavailable`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `GetDisplayMessagesStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |

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
| `customData` | no | `CustomDataType` |  |
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=512 |

Unknown fields are rejected in this object.
