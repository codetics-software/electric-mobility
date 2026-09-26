# OCPP 2.1: TransactionEvent

Direction: **Charging Station → CSMS**. CALL action: `TransactionEvent`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `costDetails` | no | `CostDetailsType` |  |
| `eventType` | yes | `TransactionEventEnumType` |  |
| `meterValue` | no | `MeterValueType[]` | minItems=1 |
| `timestamp` | yes | `string` | format=date-time |
| `triggerReason` | yes | `TriggerReasonEnumType` |  |
| `seqNo` | yes | `integer` | minimum=0.0 |
| `offline` | no | `boolean` | default=false |
| `numberOfPhasesUsed` | no | `integer` | minimum=0.0; maximum=3.0 |
| `cableMaxCurrent` | no | `integer` |  |
| `reservationId` | no | `integer` | minimum=0.0 |
| `preconditioningStatus` | no | `PreconditioningStatusEnumType` |  |
| `evseSleep` | no | `boolean` |  |
| `transactionInfo` | yes | `TransactionType` |  |
| `evse` | no | `EVSEType` |  |
| `idToken` | no | `IdTokenType` |  |
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

#### `ChargingPeriodType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `dimensions` | no | `CostDimensionType[]` | minItems=1 |
| `tariffId` | no | `string` | maxLength=60 |
| `startPeriod` | yes | `string` | format=date-time |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `ChargingStateEnumType`

Allowed values: `EVConnected`, `Charging`, `SuspendedEV`, `SuspendedEVSE`, `Idle`

#### `CostDetailsType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `chargingPeriods` | no | `ChargingPeriodType[]` | minItems=1 |
| `totalCost` | yes | `TotalCostType` |  |
| `totalUsage` | yes | `TotalUsageType` |  |
| `failureToCalculate` | no | `boolean` |  |
| `failureReason` | no | `string` | maxLength=500 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CostDimensionEnumType`

Allowed values: `Energy`, `MaxCurrent`, `MinCurrent`, `MaxPower`, `MinPower`, `IdleTIme`, `ChargingTime`

#### `CostDimensionType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `type` | yes | `CostDimensionEnumType` |  |
| `volume` | yes | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `EVSEType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `id` | yes | `integer` | minimum=0.0 |
| `connectorId` | no | `integer` | minimum=0.0 |
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

#### `LocationEnumType`

Allowed values: `Body`, `Cable`, `EV`, `Inlet`, `Outlet`, `Upstream`

#### `MeasurandEnumType`

Allowed values: `Current.Export`, `Current.Export.Offered`, `Current.Export.Minimum`, `Current.Import`, `Current.Import.Offered`, `Current.Import.Minimum`, `Current.Offered`, `Display.PresentSOC`, `Display.MinimumSOC`, `Display.TargetSOC`, `Display.MaximumSOC`, `Display.RemainingTimeToMinimumSOC`, `Display.RemainingTimeToTargetSOC`, `Display.RemainingTimeToMaximumSOC`, `Display.ChargingComplete`, `Display.BatteryEnergyCapacity`, `Display.InletHot`, `Energy.Active.Export.Interval`, `Energy.Active.Export.Register`, `Energy.Active.Import.Interval`, `Energy.Active.Import.Register`, `Energy.Active.Import.CableLoss`, `Energy.Active.Import.LocalGeneration.Register`, `Energy.Active.Net`, `Energy.Active.Setpoint.Interval`, `Energy.Apparent.Export`, `Energy.Apparent.Import`, `Energy.Apparent.Net`, `Energy.Reactive.Export.Interval`, `Energy.Reactive.Export.Register`, `Energy.Reactive.Import.Interval`, `Energy.Reactive.Import.Register`, `Energy.Reactive.Net`, `EnergyRequest.Target`, `EnergyRequest.Minimum`, `EnergyRequest.Maximum`, `EnergyRequest.Minimum.V2X`, `EnergyRequest.Maximum.V2X`, `EnergyRequest.Bulk`, `Frequency`, `Power.Active.Export`, `Power.Active.Import`, `Power.Active.Setpoint`, `Power.Active.Residual`, `Power.Export.Minimum`, `Power.Export.Offered`, `Power.Factor`, `Power.Import.Offered`, `Power.Import.Minimum`, `Power.Offered`, `Power.Reactive.Export`, `Power.Reactive.Import`, `SoC`, `Voltage`, `Voltage.Minimum`, `Voltage.Maximum`

#### `MeterValueType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `sampledValue` | yes | `SampledValueType[]` | minItems=1 |
| `timestamp` | yes | `string` | format=date-time |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `OperationModeEnumType`

Allowed values: `Idle`, `ChargingOnly`, `CentralSetpoint`, `ExternalSetpoint`, `ExternalLimits`, `CentralFrequency`, `LocalFrequency`, `LocalLoadBalancing`

#### `PhaseEnumType`

Allowed values: `L1`, `L2`, `L3`, `N`, `L1-N`, `L2-N`, `L3-N`, `L1-L2`, `L2-L3`, `L3-L1`

#### `PreconditioningStatusEnumType`

Allowed values: `Unknown`, `Ready`, `NotReady`, `Preconditioning`

#### `PriceType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `exclTax` | no | `number` |  |
| `inclTax` | no | `number` |  |
| `taxRates` | no | `TaxRateType[]` | minItems=1; maxItems=5 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `ReadingContextEnumType`

Allowed values: `Interruption.Begin`, `Interruption.End`, `Other`, `Sample.Clock`, `Sample.Periodic`, `Transaction.Begin`, `Transaction.End`, `Trigger`

#### `ReasonEnumType`

Allowed values: `DeAuthorized`, `EmergencyStop`, `EnergyLimitReached`, `EVDisconnected`, `GroundFault`, `ImmediateReset`, `MasterPass`, `Local`, `LocalOutOfCredit`, `Other`, `OvercurrentFault`, `PowerLoss`, `PowerQuality`, `Reboot`, `Remote`, `SOCLimitReached`, `StoppedByEV`, `TimeLimitReached`, `Timeout`, `ReqEnergyTransferRejected`

#### `SampledValueType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `value` | yes | `number` |  |
| `measurand` | no | `MeasurandEnumType` |  |
| `context` | no | `ReadingContextEnumType` |  |
| `phase` | no | `PhaseEnumType` |  |
| `location` | no | `LocationEnumType` |  |
| `signedMeterValue` | no | `SignedMeterValueType` |  |
| `unitOfMeasure` | no | `UnitOfMeasureType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `SignedMeterValueType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `signedMeterData` | yes | `string` | maxLength=32768 |
| `signingMethod` | no | `string` | maxLength=50 |
| `encodingMethod` | yes | `string` | maxLength=50 |
| `publicKey` | no | `string` | maxLength=2500 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TariffCostEnumType`

Allowed values: `NormalCost`, `MinCost`, `MaxCost`

#### `TaxRateType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `type` | yes | `string` | maxLength=20 |
| `tax` | yes | `number` |  |
| `stack` | no | `integer` | minimum=0.0 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TotalCostType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `currency` | yes | `string` | maxLength=3 |
| `typeOfCost` | yes | `TariffCostEnumType` |  |
| `fixed` | no | `PriceType` |  |
| `energy` | no | `PriceType` |  |
| `chargingTime` | no | `PriceType` |  |
| `idleTime` | no | `PriceType` |  |
| `reservationTime` | no | `PriceType` |  |
| `reservationFixed` | no | `PriceType` |  |
| `total` | yes | `TotalPriceType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TotalPriceType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `exclTax` | no | `number` |  |
| `inclTax` | no | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TotalUsageType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `energy` | yes | `number` |  |
| `chargingTime` | yes | `integer` |  |
| `idleTime` | yes | `integer` |  |
| `reservationTime` | no | `integer` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TransactionEventEnumType`

Allowed values: `Ended`, `Started`, `Updated`

#### `TransactionLimitType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `maxCost` | no | `number` |  |
| `maxEnergy` | no | `number` |  |
| `maxTime` | no | `integer` |  |
| `maxSoC` | no | `integer` | minimum=0.0; maximum=100.0 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TransactionType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `transactionId` | yes | `string` | maxLength=36 |
| `chargingState` | no | `ChargingStateEnumType` |  |
| `timeSpentCharging` | no | `integer` |  |
| `stoppedReason` | no | `ReasonEnumType` |  |
| `remoteStartId` | no | `integer` |  |
| `operationMode` | no | `OperationModeEnumType` |  |
| `tariffId` | no | `string` | maxLength=60 |
| `transactionLimit` | no | `TransactionLimitType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TriggerReasonEnumType`

Allowed values: `AbnormalCondition`, `Authorized`, `CablePluggedIn`, `ChargingRateChanged`, `ChargingStateChanged`, `CostLimitReached`, `Deauthorized`, `EnergyLimitReached`, `EVCommunicationLost`, `EVConnectTimeout`, `EVDeparted`, `EVDetected`, `LimitSet`, `MeterValueClock`, `MeterValuePeriodic`, `OperationModeChanged`, `RemoteStart`, `RemoteStop`, `ResetCommand`, `RunningCost`, `SignedDataReceived`, `SoCLimitReached`, `StopAuthorized`, `TariffChanged`, `TariffNotAccepted`, `TimeLimitReached`, `Trigger`, `TxResumed`, `UnlockCommand`

#### `UnitOfMeasureType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `unit` | no | `string` | maxLength=20; default=Wh |
| `multiplier` | no | `integer` | default=0 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `totalCost` | no | `number` |  |
| `chargingPriority` | no | `integer` |  |
| `idTokenInfo` | no | `IdTokenInfoType` |  |
| `transactionLimit` | no | `TransactionLimitType` |  |
| `updatedPersonalMessage` | no | `MessageContentType` |  |
| `updatedPersonalMessageExtra` | no | `MessageContentType[]` | minItems=1; maxItems=4 |
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

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

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

#### `TransactionLimitType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `maxCost` | no | `number` |  |
| `maxEnergy` | no | `number` |  |
| `maxTime` | no | `integer` |  |
| `maxSoC` | no | `integer` | minimum=0.0; maximum=100.0 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
