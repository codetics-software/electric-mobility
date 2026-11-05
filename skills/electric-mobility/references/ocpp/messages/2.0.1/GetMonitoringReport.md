# OCPP 2.0.1: GetMonitoringReport

Direction: **CSMS → Charging Station**. CALL action: `GetMonitoringReport`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `componentVariable` | no | `ComponentVariableType[]` | minItems=1 |
| `requestId` | yes | `integer` |  |
| `monitoringCriteria` | no | `MonitoringCriterionEnumType[]` | minItems=1; maxItems=3 |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ComponentType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `evse` | no | `EVSEType` |  |
| `name` | yes | `string` | maxLength=50 |
| `instance` | no | `string` | maxLength=50 |

Unknown fields are rejected in this object.

#### `ComponentVariableType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `component` | yes | `ComponentType` |  |
| `variable` | no | `VariableType` |  |

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

#### `MonitoringCriterionEnumType`

Allowed values: `ThresholdMonitoring`, `DeltaMonitoring`, `PeriodicMonitoring`

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
| `status` | yes | `GenericDeviceModelStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `GenericDeviceModelStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `NotSupported`, `EmptyResultSet`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=512 |

Unknown fields are rejected in this object.
