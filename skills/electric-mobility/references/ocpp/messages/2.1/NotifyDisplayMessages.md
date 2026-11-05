# OCPP 2.1: NotifyDisplayMessages

Direction: **Charging Station → CSMS**. CALL action: `NotifyDisplayMessages`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `messageInfo` | no | `MessageInfoType[]` | minItems=1 |
| `requestId` | yes | `integer` |  |
| `tbc` | no | `boolean` | default=false |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ComponentType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `evse` | no | `EVSEType` |  |
| `name` | yes | `string` | maxLength=50 |
| `instance` | no | `string` | maxLength=50 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `EVSEType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `id` | yes | `integer` | minimum=0.0 |
| `connectorId` | no | `integer` | minimum=0.0 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `MessageContentType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `format` | yes | `MessageFormatEnumType` |  |
| `language` | no | `string` | maxLength=8 |
| `content` | yes | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `MessageFormatEnumType`

Allowed values: `ASCII`, `HTML`, `URI`, `UTF8`, `QRCODE`

#### `MessageInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `display` | no | `ComponentType` |  |
| `id` | yes | `integer` | minimum=0.0 |
| `priority` | yes | `MessagePriorityEnumType` |  |
| `state` | no | `MessageStateEnumType` |  |
| `startDateTime` | no | `string` | format=date-time |
| `endDateTime` | no | `string` | format=date-time |
| `transactionId` | no | `string` | maxLength=36 |
| `message` | yes | `MessageContentType` |  |
| `messageExtra` | no | `MessageContentType[]` | minItems=1; maxItems=4 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `MessagePriorityEnumType`

Allowed values: `AlwaysFront`, `InFront`, `NormalCycle`

#### `MessageStateEnumType`

Allowed values: `Charging`, `Faulted`, `Idle`, `Unavailable`, `Suspended`, `Discharging`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |
