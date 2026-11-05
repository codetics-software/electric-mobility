# OCPP 2.0.1: NotifyReport

Direction: **Charging Station → CSMS**. CALL action: `NotifyReport`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `requestId` | yes | `integer` |  |
| `generatedAt` | yes | `string` | format=date-time |
| `reportData` | no | `ReportDataType[]` | minItems=1 |
| `tbc` | no | `boolean` | default=false |
| `seqNo` | yes | `integer` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `AttributeEnumType`

Allowed values: `Actual`, `Target`, `MinSet`, `MaxSet`

#### `ComponentType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `evse` | no | `EVSEType` |  |
| `name` | yes | `string` | maxLength=50 |
| `instance` | no | `string` | maxLength=50 |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `DataEnumType`

Allowed values: `string`, `decimal`, `integer`, `dateTime`, `boolean`, `OptionList`, `SequenceList`, `MemberList`

#### `EVSEType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `id` | yes | `integer` |  |
| `connectorId` | no | `integer` |  |

Unknown fields are rejected in this object.

#### `MutabilityEnumType`

Allowed values: `ReadOnly`, `WriteOnly`, `ReadWrite`

#### `ReportDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `component` | yes | `ComponentType` |  |
| `variable` | yes | `VariableType` |  |
| `variableAttribute` | yes | `VariableAttributeType[]` | minItems=1; maxItems=4 |
| `variableCharacteristics` | no | `VariableCharacteristicsType` |  |

Unknown fields are rejected in this object.

#### `VariableAttributeType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `type` | no | `AttributeEnumType` |  |
| `value` | no | `string` | maxLength=2500 |
| `mutability` | no | `MutabilityEnumType` |  |
| `persistent` | no | `boolean` | default=false |
| `constant` | no | `boolean` | default=false |

Unknown fields are rejected in this object.

#### `VariableCharacteristicsType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `unit` | no | `string` | maxLength=16 |
| `dataType` | yes | `DataEnumType` |  |
| `minLimit` | no | `number` |  |
| `maxLimit` | no | `number` |  |
| `valuesList` | no | `string` | maxLength=1000 |
| `supportsMonitoring` | yes | `boolean` |  |

Unknown fields are rejected in this object.

#### `VariableType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `name` | yes | `string` | maxLength=50 |
| `instance` | no | `string` | maxLength=50 |

Unknown fields are rejected in this object.


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
