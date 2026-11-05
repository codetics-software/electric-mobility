# OCPP 2.1: BootNotification

Direction: **Charging Station → CSMS**. CALL action: `BootNotification`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `chargingStation` | yes | `ChargingStationType` |  |
| `reason` | yes | `BootReasonEnumType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `BootReasonEnumType`

Allowed values: `ApplicationReset`, `FirmwareUpdate`, `LocalReset`, `PowerUp`, `RemoteReset`, `ScheduledReset`, `Triggered`, `Unknown`, `Watchdog`

#### `ChargingStationType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `serialNumber` | no | `string` | maxLength=25 |
| `model` | yes | `string` | maxLength=20 |
| `modem` | no | `ModemType` |  |
| `vendorName` | yes | `string` | maxLength=50 |
| `firmwareVersion` | no | `string` | maxLength=50 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `ModemType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `iccid` | no | `string` | maxLength=20 |
| `imsi` | no | `string` | maxLength=20 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `currentTime` | yes | `string` | format=date-time |
| `interval` | yes | `integer` |  |
| `status` | yes | `RegistrationStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `RegistrationStatusEnumType`

Allowed values: `Accepted`, `Pending`, `Rejected`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
