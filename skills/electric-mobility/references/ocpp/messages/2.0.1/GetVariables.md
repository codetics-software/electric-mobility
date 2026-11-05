# OCPP 2.0.1: GetVariables

Direction: **CSMS → Charging Station**. CALL action: `GetVariables`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `getVariableData` | yes | `GetVariableDataType[]` | minItems=1 |

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

#### `EVSEType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `id` | yes | `integer` |  |
| `connectorId` | no | `integer` |  |

Unknown fields are rejected in this object.

#### `GetVariableDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `attributeType` | no | `AttributeEnumType` |  |
| `component` | yes | `ComponentType` |  |
| `variable` | yes | `VariableType` |  |

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
| `getVariableResult` | yes | `GetVariableResultType[]` | minItems=1 |

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

#### `EVSEType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `id` | yes | `integer` |  |
| `connectorId` | no | `integer` |  |

Unknown fields are rejected in this object.

#### `GetVariableResultType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `attributeStatusInfo` | no | `StatusInfoType` |  |
| `attributeStatus` | yes | `GetVariableStatusEnumType` |  |
| `attributeType` | no | `AttributeEnumType` |  |
| `attributeValue` | no | `string` | maxLength=2500 |
| `component` | yes | `ComponentType` |  |
| `variable` | yes | `VariableType` |  |

Unknown fields are rejected in this object.

#### `GetVariableStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `UnknownComponent`, `UnknownVariable`, `NotSupportedAttributeType`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=512 |

Unknown fields are rejected in this object.

#### `VariableType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `name` | yes | `string` | maxLength=50 |
| `instance` | no | `string` | maxLength=50 |

Unknown fields are rejected in this object.
