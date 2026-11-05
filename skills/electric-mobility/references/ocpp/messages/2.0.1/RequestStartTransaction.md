# OCPP 2.0.1: RequestStartTransaction

Direction: **CSMS → Charging Station**. CALL action: `RequestStartTransaction`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `evseId` | no | `integer` |  |
| `groupIdToken` | no | `IdTokenType` |  |
| `idToken` | yes | `IdTokenType` |  |
| `remoteStartId` | yes | `integer` |  |
| `chargingProfile` | no | `ChargingProfileType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `AdditionalInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `additionalIdToken` | yes | `string` | maxLength=36 |
| `type` | yes | `string` | maxLength=50 |

Unknown fields are rejected in this object.

#### `ChargingProfileKindEnumType`

Allowed values: `Absolute`, `Recurring`, `Relative`

#### `ChargingProfilePurposeEnumType`

Allowed values: `ChargingStationExternalConstraints`, `ChargingStationMaxProfile`, `TxDefaultProfile`, `TxProfile`

#### `ChargingProfileType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `id` | yes | `integer` |  |
| `stackLevel` | yes | `integer` |  |
| `chargingProfilePurpose` | yes | `ChargingProfilePurposeEnumType` |  |
| `chargingProfileKind` | yes | `ChargingProfileKindEnumType` |  |
| `recurrencyKind` | no | `RecurrencyKindEnumType` |  |
| `validFrom` | no | `string` | format=date-time |
| `validTo` | no | `string` | format=date-time |
| `chargingSchedule` | yes | `ChargingScheduleType[]` | minItems=1; maxItems=3 |
| `transactionId` | no | `string` | maxLength=36 |

Unknown fields are rejected in this object.

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

#### `IdTokenEnumType`

Allowed values: `Central`, `eMAID`, `ISO14443`, `ISO15693`, `KeyCode`, `Local`, `MacAddress`, `NoAuthorization`

#### `IdTokenType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `additionalInfo` | no | `AdditionalInfoType[]` | minItems=1 |
| `idToken` | yes | `string` | maxLength=36 |
| `type` | yes | `IdTokenEnumType` |  |

Unknown fields are rejected in this object.

#### `RecurrencyKindEnumType`

Allowed values: `Daily`, `Weekly`

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
| `status` | yes | `RequestStartStopStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `transactionId` | no | `string` | maxLength=36 |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `RequestStartStopStatusEnumType`

Allowed values: `Accepted`, `Rejected`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=512 |

Unknown fields are rejected in this object.
