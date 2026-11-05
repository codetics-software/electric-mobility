# OCPP 2.0.1: NotifyEvent

Direction: **Charging Station → CSMS**. CALL action: `NotifyEvent`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `generatedAt` | yes | `string` | format=date-time |
| `tbc` | no | `boolean` | default=false |
| `seqNo` | yes | `integer` |  |
| `eventData` | yes | `EventDataType[]` | minItems=1 |

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

#### `EventDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `eventId` | yes | `integer` |  |
| `timestamp` | yes | `string` | format=date-time |
| `trigger` | yes | `EventTriggerEnumType` |  |
| `cause` | no | `integer` |  |
| `actualValue` | yes | `string` | maxLength=2500 |
| `techCode` | no | `string` | maxLength=50 |
| `techInfo` | no | `string` | maxLength=500 |
| `cleared` | no | `boolean` |  |
| `transactionId` | no | `string` | maxLength=36 |
| `component` | yes | `ComponentType` |  |
| `variableMonitoringId` | no | `integer` |  |
| `eventNotificationType` | yes | `EventNotificationEnumType` |  |
| `variable` | yes | `VariableType` |  |

Unknown fields are rejected in this object.

#### `EventNotificationEnumType`

Allowed values: `HardWiredNotification`, `HardWiredMonitor`, `PreconfiguredMonitor`, `CustomMonitor`

#### `EventTriggerEnumType`

Allowed values: `Alerting`, `Delta`, `Periodic`

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
