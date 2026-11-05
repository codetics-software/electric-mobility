# OCPP 2.1: NotifyEVChargingNeeds

Direction: **Charging Station → CSMS**. CALL action: `NotifyEVChargingNeeds`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `evseId` | yes | `integer` | minimum=1.0 |
| `maxScheduleTuples` | no | `integer` | minimum=0.0 |
| `chargingNeeds` | yes | `ChargingNeedsType` |  |
| `timestamp` | no | `string` | format=date-time |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ACChargingParametersType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `energyAmount` | yes | `number` |  |
| `evMinCurrent` | yes | `number` |  |
| `evMaxCurrent` | yes | `number` |  |
| `evMaxVoltage` | yes | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `ChargingNeedsType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `acChargingParameters` | no | `ACChargingParametersType` |  |
| `derChargingParameters` | no | `DERChargingParametersType` |  |
| `evEnergyOffer` | no | `EVEnergyOfferType` |  |
| `requestedEnergyTransfer` | yes | `EnergyTransferModeEnumType` |  |
| `dcChargingParameters` | no | `DCChargingParametersType` |  |
| `v2xChargingParameters` | no | `V2XChargingParametersType` |  |
| `availableEnergyTransfer` | no | `EnergyTransferModeEnumType[]` | minItems=1 |
| `controlMode` | no | `ControlModeEnumType` |  |
| `mobilityNeedsMode` | no | `MobilityNeedsModeEnumType` |  |
| `departureTime` | no | `string` | format=date-time |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `ControlModeEnumType`

Allowed values: `ScheduledControl`, `DynamicControl`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `DCChargingParametersType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `evMaxCurrent` | yes | `number` |  |
| `evMaxVoltage` | yes | `number` |  |
| `evMaxPower` | no | `number` |  |
| `evEnergyCapacity` | no | `number` |  |
| `energyAmount` | no | `number` |  |
| `stateOfCharge` | no | `integer` | minimum=0.0; maximum=100.0 |
| `fullSoC` | no | `integer` | minimum=0.0; maximum=100.0 |
| `bulkSoC` | no | `integer` | minimum=0.0; maximum=100.0 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `DERChargingParametersType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `evSupportedDERControl` | no | `DERControlEnumType[]` | minItems=1 |
| `evOverExcitedMaxDischargePower` | no | `number` |  |
| `evOverExcitedPowerFactor` | no | `number` |  |
| `evUnderExcitedMaxDischargePower` | no | `number` |  |
| `evUnderExcitedPowerFactor` | no | `number` |  |
| `maxApparentPower` | no | `number` |  |
| `maxChargeApparentPower` | no | `number` |  |
| `maxChargeApparentPower_L2` | no | `number` |  |
| `maxChargeApparentPower_L3` | no | `number` |  |
| `maxDischargeApparentPower` | no | `number` |  |
| `maxDischargeApparentPower_L2` | no | `number` |  |
| `maxDischargeApparentPower_L3` | no | `number` |  |
| `maxChargeReactivePower` | no | `number` |  |
| `maxChargeReactivePower_L2` | no | `number` |  |
| `maxChargeReactivePower_L3` | no | `number` |  |
| `minChargeReactivePower` | no | `number` |  |
| `minChargeReactivePower_L2` | no | `number` |  |
| `minChargeReactivePower_L3` | no | `number` |  |
| `maxDischargeReactivePower` | no | `number` |  |
| `maxDischargeReactivePower_L2` | no | `number` |  |
| `maxDischargeReactivePower_L3` | no | `number` |  |
| `minDischargeReactivePower` | no | `number` |  |
| `minDischargeReactivePower_L2` | no | `number` |  |
| `minDischargeReactivePower_L3` | no | `number` |  |
| `nominalVoltage` | no | `number` |  |
| `nominalVoltageOffset` | no | `number` |  |
| `maxNominalVoltage` | no | `number` |  |
| `minNominalVoltage` | no | `number` |  |
| `evInverterManufacturer` | no | `string` | maxLength=50 |
| `evInverterModel` | no | `string` | maxLength=50 |
| `evInverterSerialNumber` | no | `string` | maxLength=50 |
| `evInverterSwVersion` | no | `string` | maxLength=50 |
| `evInverterHwVersion` | no | `string` | maxLength=50 |
| `evIslandingDetectionMethod` | no | `IslandingDetectionEnumType[]` | minItems=1 |
| `evIslandingTripTime` | no | `number` |  |
| `evMaximumLevel1DCInjection` | no | `number` |  |
| `evDurationLevel1DCInjection` | no | `number` |  |
| `evMaximumLevel2DCInjection` | no | `number` |  |
| `evDurationLevel2DCInjection` | no | `number` |  |
| `evReactiveSusceptance` | no | `number` |  |
| `evSessionTotalDischargeEnergyAvailable` | no | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `DERControlEnumType`

Allowed values: `EnterService`, `FreqDroop`, `FreqWatt`, `FixedPFAbsorb`, `FixedPFInject`, `FixedVar`, `Gradients`, `HFMustTrip`, `HFMayTrip`, `HVMustTrip`, `HVMomCess`, `HVMayTrip`, `LimitMaxDischarge`, `LFMustTrip`, `LVMustTrip`, `LVMomCess`, `LVMayTrip`, `PowerMonitoringMustTrip`, `VoltVar`, `VoltWatt`, `WattPF`, `WattVar`

#### `EVAbsolutePriceScheduleEntryType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `duration` | yes | `integer` |  |
| `evPriceRule` | yes | `EVPriceRuleType[]` | minItems=1; maxItems=8 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `EVAbsolutePriceScheduleType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `timeAnchor` | yes | `string` | format=date-time |
| `currency` | yes | `string` | maxLength=3 |
| `evAbsolutePriceScheduleEntries` | yes | `EVAbsolutePriceScheduleEntryType[]` | minItems=1; maxItems=1024 |
| `priceAlgorithm` | yes | `string` | maxLength=2000 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `EVEnergyOfferType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `evAbsolutePriceSchedule` | no | `EVAbsolutePriceScheduleType` |  |
| `evPowerSchedule` | yes | `EVPowerScheduleType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `EVPowerScheduleEntryType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `duration` | yes | `integer` |  |
| `power` | yes | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `EVPowerScheduleType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `evPowerScheduleEntries` | yes | `EVPowerScheduleEntryType[]` | minItems=1; maxItems=1024 |
| `timeAnchor` | yes | `string` | format=date-time |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `EVPriceRuleType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `energyFee` | yes | `number` |  |
| `powerRangeStart` | yes | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `EnergyTransferModeEnumType`

Allowed values: `AC_single_phase`, `AC_two_phase`, `AC_three_phase`, `DC`, `AC_BPT`, `AC_BPT_DER`, `AC_DER`, `DC_BPT`, `DC_ACDP`, `DC_ACDP_BPT`, `WPT`

#### `IslandingDetectionEnumType`

Allowed values: `NoAntiIslandingSupport`, `RoCoF`, `UVP_OVP`, `UFP_OFP`, `VoltageVectorShift`, `ZeroCrossingDetection`, `OtherPassive`, `ImpedanceMeasurement`, `ImpedanceAtFrequency`, `SlipModeFrequencyShift`, `SandiaFrequencyShift`, `SandiaVoltageShift`, `FrequencyJump`, `RCLQFactor`, `OtherActive`

#### `MobilityNeedsModeEnumType`

Allowed values: `EVCC`, `EVCC_SECC`

#### `V2XChargingParametersType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `minChargePower` | no | `number` |  |
| `minChargePower_L2` | no | `number` |  |
| `minChargePower_L3` | no | `number` |  |
| `maxChargePower` | no | `number` |  |
| `maxChargePower_L2` | no | `number` |  |
| `maxChargePower_L3` | no | `number` |  |
| `minDischargePower` | no | `number` |  |
| `minDischargePower_L2` | no | `number` |  |
| `minDischargePower_L3` | no | `number` |  |
| `maxDischargePower` | no | `number` |  |
| `maxDischargePower_L2` | no | `number` |  |
| `maxDischargePower_L3` | no | `number` |  |
| `minChargeCurrent` | no | `number` |  |
| `maxChargeCurrent` | no | `number` |  |
| `minDischargeCurrent` | no | `number` |  |
| `maxDischargeCurrent` | no | `number` |  |
| `minVoltage` | no | `number` |  |
| `maxVoltage` | no | `number` |  |
| `evTargetEnergyRequest` | no | `number` |  |
| `evMinEnergyRequest` | no | `number` |  |
| `evMaxEnergyRequest` | no | `number` |  |
| `evMinV2XEnergyRequest` | no | `number` |  |
| `evMaxV2XEnergyRequest` | no | `number` |  |
| `targetSoC` | no | `integer` | minimum=0.0; maximum=100.0 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `NotifyEVChargingNeedsStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `NotifyEVChargingNeedsStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `Processing`, `NoChargingProfile`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
