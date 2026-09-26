# OCPP 2.1: BootNotification

Direction: **Charging Station → CSMS**. CALL action: `BootNotification`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

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
