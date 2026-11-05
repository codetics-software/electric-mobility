# OCPP 2.0.1: ClearChargingProfile

Direction: **CSMS → Charging Station**. CALL action: `ClearChargingProfile`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `chargingProfileId` | no | `integer` |  |
| `chargingProfileCriteria` | no | `ClearChargingProfileType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ChargingProfilePurposeEnumType`

Allowed values: `ChargingStationExternalConstraints`, `ChargingStationMaxProfile`, `TxDefaultProfile`, `TxProfile`

#### `ClearChargingProfileType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `evseId` | no | `integer` |  |
| `chargingProfilePurpose` | no | `ChargingProfilePurposeEnumType` |  |
| `stackLevel` | no | `integer` |  |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `ClearChargingProfileStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |

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
| `customData` | no | `CustomDataType` |  |
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=512 |

Unknown fields are rejected in this object.
