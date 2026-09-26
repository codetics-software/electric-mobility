# OCPP 2.0.1: NotifyEVChargingSchedule

Direction: **Charging Station → CSMS**. CALL action: `NotifyEVChargingSchedule`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `timeBase` | yes | `string` | format=date-time |
| `chargingSchedule` | yes | `ChargingScheduleType` |  |
| `evseId` | yes | `integer` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ChargingRateUnitEnumType`

Allowed values: `W`, `A`

#### `ChargingSchedulePeriodType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `startPeriod` | yes | `integer` |  |
| `limit` | yes | `number` |  |
| `numberPhases` | no | `integer` |  |
| `phaseToUse` | no | `integer` |  |

Unknown fields are rejected in this object.

#### `ChargingScheduleType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `id` | yes | `integer` |  |
| `startSchedule` | no | `string` | format=date-time |
| `duration` | no | `integer` |  |
| `chargingRateUnit` | yes | `ChargingRateUnitEnumType` |  |
| `chargingSchedulePeriod` | yes | `ChargingSchedulePeriodType[]` | minItems=1; maxItems=1024 |
| `minChargingRate` | no | `number` |  |
| `salesTariff` | no | `SalesTariffType` |  |

Unknown fields are rejected in this object.

#### `ConsumptionCostType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `startValue` | yes | `number` |  |
| `cost` | yes | `CostType[]` | minItems=1; maxItems=3 |

Unknown fields are rejected in this object.

#### `CostKindEnumType`

Allowed values: `CarbonDioxideEmission`, `RelativePricePercentage`, `RenewableGenerationPercentage`

#### `CostType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `costKind` | yes | `CostKindEnumType` |  |
| `amount` | yes | `integer` |  |
| `amountMultiplier` | no | `integer` |  |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `RelativeTimeIntervalType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `start` | yes | `integer` |  |
| `duration` | no | `integer` |  |

Unknown fields are rejected in this object.

#### `SalesTariffEntryType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `relativeTimeInterval` | yes | `RelativeTimeIntervalType` |  |
| `ePriceLevel` | no | `integer` | minimum=0.0 |
| `consumptionCost` | no | `ConsumptionCostType[]` | minItems=1; maxItems=3 |

Unknown fields are rejected in this object.

#### `SalesTariffType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `id` | yes | `integer` |  |
| `salesTariffDescription` | no | `string` | maxLength=32 |
| `numEPriceLevels` | no | `integer` |  |
| `salesTariffEntry` | yes | `SalesTariffEntryType[]` | minItems=1; maxItems=1024 |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `GenericStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `GenericStatusEnumType`

Allowed values: `Accepted`, `Rejected`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=512 |

Unknown fields are rejected in this object.
