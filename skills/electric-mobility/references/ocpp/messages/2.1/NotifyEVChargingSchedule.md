# OCPP 2.1: NotifyEVChargingSchedule

Direction: **Charging Station → CSMS**. CALL action: `NotifyEVChargingSchedule`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `timeBase` | yes | `string` | format=date-time |
| `chargingSchedule` | yes | `ChargingScheduleType` |  |
| `evseId` | yes | `integer` | minimum=1.0 |
| `selectedChargingScheduleId` | no | `integer` | minimum=0.0 |
| `powerToleranceAcceptance` | no | `boolean` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `AbsolutePriceScheduleType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `timeAnchor` | yes | `string` | format=date-time |
| `priceScheduleID` | yes | `integer` | minimum=0.0 |
| `priceScheduleDescription` | no | `string` | maxLength=160 |
| `currency` | yes | `string` | maxLength=3 |
| `language` | yes | `string` | maxLength=8 |
| `priceAlgorithm` | yes | `string` | maxLength=2000 |
| `minimumCost` | no | `RationalNumberType` |  |
| `maximumCost` | no | `RationalNumberType` |  |
| `priceRuleStacks` | yes | `PriceRuleStackType[]` | minItems=1; maxItems=1024 |
| `taxRules` | no | `TaxRuleType[]` | minItems=1; maxItems=10 |
| `overstayRuleList` | no | `OverstayRuleListType` |  |
| `additionalSelectedServices` | no | `AdditionalSelectedServicesType[]` | minItems=1; maxItems=5 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `AdditionalSelectedServicesType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `serviceFee` | yes | `RationalNumberType` |  |
| `serviceName` | yes | `string` | maxLength=80 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `ChargingRateUnitEnumType`

Allowed values: `W`, `A`

#### `ChargingSchedulePeriodType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `startPeriod` | yes | `integer` |  |
| `limit` | no | `number` |  |
| `limit_L2` | no | `number` |  |
| `limit_L3` | no | `number` |  |
| `numberPhases` | no | `integer` | minimum=0.0; maximum=3.0 |
| `phaseToUse` | no | `integer` | minimum=0.0; maximum=3.0 |
| `dischargeLimit` | no | `number` | maximum=0.0 |
| `dischargeLimit_L2` | no | `number` | maximum=0.0 |
| `dischargeLimit_L3` | no | `number` | maximum=0.0 |
| `setpoint` | no | `number` |  |
| `setpoint_L2` | no | `number` |  |
| `setpoint_L3` | no | `number` |  |
| `setpointReactive` | no | `number` |  |
| `setpointReactive_L2` | no | `number` |  |
| `setpointReactive_L3` | no | `number` |  |
| `preconditioningRequest` | no | `boolean` |  |
| `evseSleep` | no | `boolean` |  |
| `v2xBaseline` | no | `number` |  |
| `operationMode` | no | `OperationModeEnumType` |  |
| `v2xFreqWattCurve` | no | `V2XFreqWattPointType[]` | minItems=1; maxItems=20 |
| `v2xSignalWattCurve` | no | `V2XSignalWattPointType[]` | minItems=1; maxItems=20 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `ChargingScheduleType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `id` | yes | `integer` |  |
| `limitAtSoC` | no | `LimitAtSoCType` |  |
| `startSchedule` | no | `string` | format=date-time |
| `duration` | no | `integer` |  |
| `chargingRateUnit` | yes | `ChargingRateUnitEnumType` |  |
| `minChargingRate` | no | `number` |  |
| `powerTolerance` | no | `number` |  |
| `signatureId` | no | `integer` | minimum=0.0 |
| `digestValue` | no | `string` | maxLength=88 |
| `useLocalTime` | no | `boolean` |  |
| `chargingSchedulePeriod` | yes | `ChargingSchedulePeriodType[]` | minItems=1; maxItems=1024 |
| `randomizedDelay` | no | `integer` | minimum=0.0 |
| `salesTariff` | no | `SalesTariffType` |  |
| `absolutePriceSchedule` | no | `AbsolutePriceScheduleType` |  |
| `priceLevelSchedule` | no | `PriceLevelScheduleType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `ConsumptionCostType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `startValue` | yes | `number` |  |
| `cost` | yes | `CostType[]` | minItems=1; maxItems=3 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CostKindEnumType`

Allowed values: `CarbonDioxideEmission`, `RelativePricePercentage`, `RenewableGenerationPercentage`

#### `CostType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `costKind` | yes | `CostKindEnumType` |  |
| `amount` | yes | `integer` |  |
| `amountMultiplier` | no | `integer` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `LimitAtSoCType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `soc` | yes | `integer` | minimum=0.0; maximum=100.0 |
| `limit` | yes | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `OperationModeEnumType`

Allowed values: `Idle`, `ChargingOnly`, `CentralSetpoint`, `ExternalSetpoint`, `ExternalLimits`, `CentralFrequency`, `LocalFrequency`, `LocalLoadBalancing`

#### `OverstayRuleListType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `overstayPowerThreshold` | no | `RationalNumberType` |  |
| `overstayRule` | yes | `OverstayRuleType[]` | minItems=1; maxItems=5 |
| `overstayTimeThreshold` | no | `integer` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `OverstayRuleType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `overstayFee` | yes | `RationalNumberType` |  |
| `overstayRuleDescription` | no | `string` | maxLength=32 |
| `startTime` | yes | `integer` |  |
| `overstayFeePeriod` | yes | `integer` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `PriceLevelScheduleEntryType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `duration` | yes | `integer` |  |
| `priceLevel` | yes | `integer` | minimum=0.0 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `PriceLevelScheduleType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `priceLevelScheduleEntries` | yes | `PriceLevelScheduleEntryType[]` | minItems=1; maxItems=100 |
| `timeAnchor` | yes | `string` | format=date-time |
| `priceScheduleId` | yes | `integer` | minimum=0.0 |
| `priceScheduleDescription` | no | `string` | maxLength=32 |
| `numberOfPriceLevels` | yes | `integer` | minimum=0.0 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `PriceRuleStackType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `duration` | yes | `integer` |  |
| `priceRule` | yes | `PriceRuleType[]` | minItems=1; maxItems=8 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `PriceRuleType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `parkingFeePeriod` | no | `integer` |  |
| `carbonDioxideEmission` | no | `integer` | minimum=0.0 |
| `renewableGenerationPercentage` | no | `integer` | minimum=0.0; maximum=100.0 |
| `energyFee` | yes | `RationalNumberType` |  |
| `parkingFee` | no | `RationalNumberType` |  |
| `powerRangeStart` | yes | `RationalNumberType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `RationalNumberType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `exponent` | yes | `integer` |  |
| `value` | yes | `integer` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `RelativeTimeIntervalType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `start` | yes | `integer` |  |
| `duration` | no | `integer` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `SalesTariffEntryType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `relativeTimeInterval` | yes | `RelativeTimeIntervalType` |  |
| `ePriceLevel` | no | `integer` | minimum=0.0 |
| `consumptionCost` | no | `ConsumptionCostType[]` | minItems=1; maxItems=3 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `SalesTariffType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `id` | yes | `integer` | minimum=0.0 |
| `salesTariffDescription` | no | `string` | maxLength=32 |
| `numEPriceLevels` | no | `integer` | minimum=0.0 |
| `salesTariffEntry` | yes | `SalesTariffEntryType[]` | minItems=1; maxItems=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TaxRuleType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `taxRuleID` | yes | `integer` | minimum=0.0 |
| `taxRuleName` | no | `string` | maxLength=100 |
| `taxIncludedInPrice` | no | `boolean` |  |
| `appliesToEnergyFee` | yes | `boolean` |  |
| `appliesToParkingFee` | yes | `boolean` |  |
| `appliesToOverstayFee` | yes | `boolean` |  |
| `appliesToMinimumMaximumCost` | yes | `boolean` |  |
| `taxRate` | yes | `RationalNumberType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `V2XFreqWattPointType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `frequency` | yes | `number` |  |
| `power` | yes | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `V2XSignalWattPointType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `signal` | yes | `integer` |  |
| `power` | yes | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `GenericStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

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
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
