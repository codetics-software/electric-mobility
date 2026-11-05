# OCPP 2.1: PullDynamicScheduleUpdate

Direction: **Charging Station → CSMS**. CALL action: `PullDynamicScheduleUpdate`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `chargingProfileId` | yes | `integer` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `scheduleUpdate` | no | `ChargingScheduleUpdateType` |  |
| `status` | yes | `ChargingProfileStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ChargingProfileStatusEnumType`

Allowed values: `Accepted`, `Rejected`

#### `ChargingScheduleUpdateType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `limit` | no | `number` |  |
| `limit_L2` | no | `number` |  |
| `limit_L3` | no | `number` |  |
| `dischargeLimit` | no | `number` | maximum=0.0 |
| `dischargeLimit_L2` | no | `number` | maximum=0.0 |
| `dischargeLimit_L3` | no | `number` | maximum=0.0 |
| `setpoint` | no | `number` |  |
| `setpoint_L2` | no | `number` |  |
| `setpoint_L3` | no | `number` |  |
| `setpointReactive` | no | `number` |  |
| `setpointReactive_L2` | no | `number` |  |
| `setpointReactive_L3` | no | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
