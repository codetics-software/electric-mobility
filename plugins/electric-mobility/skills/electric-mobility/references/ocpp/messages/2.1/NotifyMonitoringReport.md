# OCPP 2.1: NotifyMonitoringReport

Direction: **Charging Station → CSMS**. CALL action: `NotifyMonitoringReport`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `monitor` | no | `MonitoringDataType[]` | minItems=1 |
| `requestId` | yes | `integer` |  |
| `tbc` | no | `boolean` | default=false |
| `seqNo` | yes | `integer` | minimum=0.0 |
| `generatedAt` | yes | `string` | format=date-time |
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

#### `EventNotificationEnumType`

Allowed values: `HardWiredNotification`, `HardWiredMonitor`, `PreconfiguredMonitor`, `CustomMonitor`

#### `MonitorEnumType`

Allowed values: `UpperThreshold`, `LowerThreshold`, `Delta`, `Periodic`, `PeriodicClockAligned`, `TargetDelta`, `TargetDeltaRelative`

#### `MonitoringDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `component` | yes | `ComponentType` |  |
| `variable` | yes | `VariableType` |  |
| `variableMonitoring` | yes | `VariableMonitoringType[]` | minItems=1 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `VariableMonitoringType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `id` | yes | `integer` | minimum=0.0 |
| `transaction` | yes | `boolean` |  |
| `value` | yes | `number` |  |
| `type` | yes | `MonitorEnumType` |  |
| `severity` | yes | `integer` | minimum=0.0 |
| `eventNotificationType` | yes | `EventNotificationEnumType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `VariableType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `name` | yes | `string` | maxLength=50 |
| `instance` | no | `string` | maxLength=50 |
| `customData` | no | `CustomDataType` |  |

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
