# OCPP 2.1: GetChargingProfiles

Direction: **CSMS → Charging Station**. CALL action: `GetChargingProfiles`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `requestId` | yes | `integer` |  |
| `evseId` | no | `integer` | minimum=0.0 |
| `chargingProfile` | yes | `ChargingProfileCriterionType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ChargingProfileCriterionType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `chargingProfilePurpose` | no | `ChargingProfilePurposeEnumType` |  |
| `stackLevel` | no | `integer` | minimum=0.0 |
| `chargingProfileId` | no | `integer[]` | minItems=1 |
| `chargingLimitSource` | no | `string[]` | minItems=1; maxItems=4 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `ChargingProfilePurposeEnumType`

Allowed values: `ChargingStationExternalConstraints`, `ChargingStationMaxProfile`, `TxDefaultProfile`, `TxProfile`, `PriorityCharging`, `LocalGeneration`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `GetChargingProfileStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `GetChargingProfileStatusEnumType`

Allowed values: `Accepted`, `NoProfiles`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
