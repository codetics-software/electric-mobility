# OCPP 2.1: ChangeTransactionTariff

Direction: **CSMS → Charging Station**. CALL action: `ChangeTransactionTariff`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `tariff` | yes | `TariffType` |  |
| `transactionId` | yes | `string` | maxLength=36 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `DayOfWeekEnumType`

Allowed values: `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`, `Saturday`, `Sunday`

#### `EvseKindEnumType`

Allowed values: `AC`, `DC`

#### `MessageContentType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `format` | yes | `MessageFormatEnumType` |  |
| `language` | no | `string` | maxLength=8 |
| `content` | yes | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `MessageFormatEnumType`

Allowed values: `ASCII`, `HTML`, `URI`, `UTF8`, `QRCODE`

#### `PriceType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `exclTax` | no | `number` |  |
| `inclTax` | no | `number` |  |
| `taxRates` | no | `TaxRateType[]` | minItems=1; maxItems=5 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TariffConditionsFixedType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `startTimeOfDay` | no | `string` |  |
| `endTimeOfDay` | no | `string` |  |
| `dayOfWeek` | no | `DayOfWeekEnumType[]` | minItems=1; maxItems=7 |
| `validFromDate` | no | `string` |  |
| `validToDate` | no | `string` |  |
| `evseKind` | no | `EvseKindEnumType` |  |
| `paymentBrand` | no | `string` | maxLength=20 |
| `paymentRecognition` | no | `string` | maxLength=20 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TariffConditionsType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `startTimeOfDay` | no | `string` |  |
| `endTimeOfDay` | no | `string` |  |
| `dayOfWeek` | no | `DayOfWeekEnumType[]` | minItems=1; maxItems=7 |
| `validFromDate` | no | `string` |  |
| `validToDate` | no | `string` |  |
| `evseKind` | no | `EvseKindEnumType` |  |
| `minEnergy` | no | `number` |  |
| `maxEnergy` | no | `number` |  |
| `minCurrent` | no | `number` |  |
| `maxCurrent` | no | `number` |  |
| `minPower` | no | `number` |  |
| `maxPower` | no | `number` |  |
| `minTime` | no | `integer` |  |
| `maxTime` | no | `integer` |  |
| `minChargingTime` | no | `integer` |  |
| `maxChargingTime` | no | `integer` |  |
| `minIdleTime` | no | `integer` |  |
| `maxIdleTime` | no | `integer` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TariffEnergyPriceType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `priceKwh` | yes | `number` |  |
| `conditions` | no | `TariffConditionsType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TariffEnergyType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `prices` | yes | `TariffEnergyPriceType[]` | minItems=1 |
| `taxRates` | no | `TaxRateType[]` | minItems=1; maxItems=5 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TariffFixedPriceType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `conditions` | no | `TariffConditionsFixedType` |  |
| `priceFixed` | yes | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TariffFixedType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `prices` | yes | `TariffFixedPriceType[]` | minItems=1 |
| `taxRates` | no | `TaxRateType[]` | minItems=1; maxItems=5 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TariffTimePriceType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `priceMinute` | yes | `number` |  |
| `conditions` | no | `TariffConditionsType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TariffTimeType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `prices` | yes | `TariffTimePriceType[]` | minItems=1 |
| `taxRates` | no | `TaxRateType[]` | minItems=1; maxItems=5 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TariffType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `tariffId` | yes | `string` | maxLength=60 |
| `description` | no | `MessageContentType[]` | minItems=1; maxItems=10 |
| `currency` | yes | `string` | maxLength=3 |
| `energy` | no | `TariffEnergyType` |  |
| `validFrom` | no | `string` | format=date-time |
| `chargingTime` | no | `TariffTimeType` |  |
| `idleTime` | no | `TariffTimeType` |  |
| `fixedFee` | no | `TariffFixedType` |  |
| `reservationTime` | no | `TariffTimeType` |  |
| `reservationFixed` | no | `TariffFixedType` |  |
| `minCost` | no | `PriceType` |  |
| `maxCost` | no | `PriceType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TaxRateType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `type` | yes | `string` | maxLength=20 |
| `tax` | yes | `number` |  |
| `stack` | no | `integer` | minimum=0.0 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `TariffChangeStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

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

#### `TariffChangeStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `TooManyElements`, `ConditionNotSupported`, `TxNotFound`, `NoCurrencyChange`
