# OCPP 2.1: ClearChargingProfile

Direction: **CSMS → Charging Station**. CALL action: `ClearChargingProfile`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `chargingProfileId` | no | `integer` |  |
| `chargingProfileCriteria` | no | `ClearChargingProfileType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ChargingProfilePurposeEnumType`

Allowed values: `ChargingStationExternalConstraints`, `ChargingStationMaxProfile`, `TxDefaultProfile`, `TxProfile`, `PriorityCharging`, `LocalGeneration`

#### `ClearChargingProfileType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `evseId` | no | `integer` | minimum=0.0 |
| `chargingProfilePurpose` | no | `ChargingProfilePurposeEnumType` |  |
| `stackLevel` | no | `integer` | minimum=0.0 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `ClearChargingProfileStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ClearChargingProfileStatusEnumType`

Allowed values: `Accepted`, `Unknown`

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
