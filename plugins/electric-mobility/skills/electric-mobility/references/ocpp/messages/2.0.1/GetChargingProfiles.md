# OCPP 2.0.1: GetChargingProfiles

Direction: **CSMS → Charging Station**. CALL action: `GetChargingProfiles`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `requestId` | yes | `integer` |  |
| `evseId` | no | `integer` |  |
| `chargingProfile` | yes | `ChargingProfileCriterionType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ChargingLimitSourceEnumType`

Allowed values: `EMS`, `Other`, `SO`, `CSO`

#### `ChargingProfileCriterionType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `chargingProfilePurpose` | no | `ChargingProfilePurposeEnumType` |  |
| `stackLevel` | no | `integer` |  |
| `chargingProfileId` | no | `integer[]` | minItems=1 |
| `chargingLimitSource` | no | `ChargingLimitSourceEnumType[]` | minItems=1; maxItems=4 |

Unknown fields are rejected in this object.

#### `ChargingProfilePurposeEnumType`

Allowed values: `ChargingStationExternalConstraints`, `ChargingStationMaxProfile`, `TxDefaultProfile`, `TxProfile`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `GetChargingProfileStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |

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
| `customData` | no | `CustomDataType` |  |
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=512 |

Unknown fields are rejected in this object.
