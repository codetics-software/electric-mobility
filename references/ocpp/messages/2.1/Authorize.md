# OCPP 2.1: Authorize

Direction: **Charging Station → CSMS**. CALL action: `Authorize`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `idToken` | yes | `IdTokenType` |  |
| `certificate` | no | `string` | maxLength=10000 |
| `iso15118CertificateHashData` | no | `OCSPRequestDataType[]` | minItems=1; maxItems=4 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `AdditionalInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `additionalIdToken` | yes | `string` | maxLength=255 |
| `type` | yes | `string` | maxLength=50 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `HashAlgorithmEnumType`

Allowed values: `SHA256`, `SHA384`, `SHA512`

#### `IdTokenType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `additionalInfo` | no | `AdditionalInfoType[]` | minItems=1 |
| `idToken` | yes | `string` | maxLength=255 |
| `type` | yes | `string` | maxLength=20 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `OCSPRequestDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `hashAlgorithm` | yes | `HashAlgorithmEnumType` |  |
| `issuerNameHash` | yes | `string` | maxLength=128 |
| `issuerKeyHash` | yes | `string` | maxLength=128 |
| `serialNumber` | yes | `string` | maxLength=40 |
| `responderURL` | yes | `string` | maxLength=2000 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `idTokenInfo` | yes | `IdTokenInfoType` |  |
| `certificateStatus` | no | `AuthorizeCertificateStatusEnumType` |  |
| `allowedEnergyTransfer` | no | `EnergyTransferModeEnumType[]` | minItems=1 |
| `tariff` | no | `TariffType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `AdditionalInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `additionalIdToken` | yes | `string` | maxLength=255 |
| `type` | yes | `string` | maxLength=50 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `AuthorizationStatusEnumType`

Allowed values: `Accepted`, `Blocked`, `ConcurrentTx`, `Expired`, `Invalid`, `NoCredit`, `NotAllowedTypeEVSE`, `NotAtThisLocation`, `NotAtThisTime`, `Unknown`

#### `AuthorizeCertificateStatusEnumType`

Allowed values: `Accepted`, `SignatureError`, `CertificateExpired`, `CertificateRevoked`, `NoCertificateAvailable`, `CertChainError`, `ContractCancelled`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `DayOfWeekEnumType`

Allowed values: `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`, `Saturday`, `Sunday`

#### `EnergyTransferModeEnumType`

Allowed values: `AC_single_phase`, `AC_two_phase`, `AC_three_phase`, `DC`, `AC_BPT`, `AC_BPT_DER`, `AC_DER`, `DC_BPT`, `DC_ACDP`, `DC_ACDP_BPT`, `WPT`

#### `EvseKindEnumType`

Allowed values: `AC`, `DC`

#### `IdTokenInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `AuthorizationStatusEnumType` |  |
| `cacheExpiryDateTime` | no | `string` | format=date-time |
| `chargingPriority` | no | `integer` |  |
| `groupIdToken` | no | `IdTokenType` |  |
| `language1` | no | `string` | maxLength=8 |
| `language2` | no | `string` | maxLength=8 |
| `evseId` | no | `integer[]` | minItems=1 |
| `personalMessage` | no | `MessageContentType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `IdTokenType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `additionalInfo` | no | `AdditionalInfoType[]` | minItems=1 |
| `idToken` | yes | `string` | maxLength=255 |
| `type` | yes | `string` | maxLength=20 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

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
