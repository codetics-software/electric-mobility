# OCPP 2.0.1: NotifyEVChargingNeeds

Direction: **Charging Station → CSMS**. CALL action: `NotifyEVChargingNeeds`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `maxScheduleTuples` | no | `integer` |  |
| `chargingNeeds` | yes | `ChargingNeedsType` |  |
| `evseId` | yes | `integer` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ACChargingParametersType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `energyAmount` | yes | `integer` |  |
| `evMinCurrent` | yes | `integer` |  |
| `evMaxCurrent` | yes | `integer` |  |
| `evMaxVoltage` | yes | `integer` |  |

Unknown fields are rejected in this object.

#### `ChargingNeedsType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `acChargingParameters` | no | `ACChargingParametersType` |  |
| `dcChargingParameters` | no | `DCChargingParametersType` |  |
| `requestedEnergyTransfer` | yes | `EnergyTransferModeEnumType` |  |
| `departureTime` | no | `string` | format=date-time |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `DCChargingParametersType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `evMaxCurrent` | yes | `integer` |  |
| `evMaxVoltage` | yes | `integer` |  |
| `energyAmount` | no | `integer` |  |
| `evMaxPower` | no | `integer` |  |
| `stateOfCharge` | no | `integer` | minimum=0.0; maximum=100.0 |
| `evEnergyCapacity` | no | `integer` |  |
| `fullSoC` | no | `integer` | minimum=0.0; maximum=100.0 |
| `bulkSoC` | no | `integer` | minimum=0.0; maximum=100.0 |

Unknown fields are rejected in this object.

#### `EnergyTransferModeEnumType`

Allowed values: `DC`, `AC_single_phase`, `AC_two_phase`, `AC_three_phase`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `NotifyEVChargingNeedsStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `NotifyEVChargingNeedsStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `Processing`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=512 |

Unknown fields are rejected in this object.
