# OCPP 2.0.1: TransactionEvent

Direction: **Charging Station → CSMS**. CALL action: `TransactionEvent`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `eventType` | yes | `TransactionEventEnumType` |  |
| `meterValue` | no | `MeterValueType[]` | minItems=1 |
| `timestamp` | yes | `string` | format=date-time |
| `triggerReason` | yes | `TriggerReasonEnumType` |  |
| `seqNo` | yes | `integer` |  |
| `offline` | no | `boolean` | default=false |
| `numberOfPhasesUsed` | no | `integer` |  |
| `cableMaxCurrent` | no | `integer` |  |
| `reservationId` | no | `integer` |  |
| `transactionInfo` | yes | `TransactionType` |  |
| `evse` | no | `EVSEType` |  |
| `idToken` | no | `IdTokenType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `AdditionalInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `additionalIdToken` | yes | `string` | maxLength=36 |
| `type` | yes | `string` | maxLength=50 |

Unknown fields are rejected in this object.

#### `ChargingStateEnumType`

Allowed values: `Charging`, `EVConnected`, `SuspendedEV`, `SuspendedEVSE`, `Idle`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `EVSEType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `id` | yes | `integer` |  |
| `connectorId` | no | `integer` |  |

Unknown fields are rejected in this object.

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

#### `LocationEnumType`

Allowed values: `Body`, `Cable`, `EV`, `Inlet`, `Outlet`

#### `MeasurandEnumType`

Allowed values: `Current.Export`, `Current.Import`, `Current.Offered`, `Energy.Active.Export.Register`, `Energy.Active.Import.Register`, `Energy.Reactive.Export.Register`, `Energy.Reactive.Import.Register`, `Energy.Active.Export.Interval`, `Energy.Active.Import.Interval`, `Energy.Active.Net`, `Energy.Reactive.Export.Interval`, `Energy.Reactive.Import.Interval`, `Energy.Reactive.Net`, `Energy.Apparent.Net`, `Energy.Apparent.Import`, `Energy.Apparent.Export`, `Frequency`, `Power.Active.Export`, `Power.Active.Import`, `Power.Factor`, `Power.Offered`, `Power.Reactive.Export`, `Power.Reactive.Import`, `SoC`, `Voltage`

#### `MeterValueType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `sampledValue` | yes | `SampledValueType[]` | minItems=1 |
| `timestamp` | yes | `string` | format=date-time |

Unknown fields are rejected in this object.

#### `PhaseEnumType`

Allowed values: `L1`, `L2`, `L3`, `N`, `L1-N`, `L2-N`, `L3-N`, `L1-L2`, `L2-L3`, `L3-L1`

#### `ReadingContextEnumType`

Allowed values: `Interruption.Begin`, `Interruption.End`, `Other`, `Sample.Clock`, `Sample.Periodic`, `Transaction.Begin`, `Transaction.End`, `Trigger`

#### `ReasonEnumType`

Allowed values: `DeAuthorized`, `EmergencyStop`, `EnergyLimitReached`, `EVDisconnected`, `GroundFault`, `ImmediateReset`, `Local`, `LocalOutOfCredit`, `MasterPass`, `Other`, `OvercurrentFault`, `PowerLoss`, `PowerQuality`, `Reboot`, `Remote`, `SOCLimitReached`, `StoppedByEV`, `TimeLimitReached`, `Timeout`

#### `SampledValueType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `value` | yes | `number` |  |
| `context` | no | `ReadingContextEnumType` |  |
| `measurand` | no | `MeasurandEnumType` |  |
| `phase` | no | `PhaseEnumType` |  |
| `location` | no | `LocationEnumType` |  |
| `signedMeterValue` | no | `SignedMeterValueType` |  |
| `unitOfMeasure` | no | `UnitOfMeasureType` |  |

Unknown fields are rejected in this object.

#### `SignedMeterValueType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `signedMeterData` | yes | `string` | maxLength=2500 |
| `signingMethod` | yes | `string` | maxLength=50 |
| `encodingMethod` | yes | `string` | maxLength=50 |
| `publicKey` | yes | `string` | maxLength=2500 |

Unknown fields are rejected in this object.

#### `TransactionEventEnumType`

Allowed values: `Ended`, `Started`, `Updated`

#### `TransactionType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `transactionId` | yes | `string` | maxLength=36 |
| `chargingState` | no | `ChargingStateEnumType` |  |
| `timeSpentCharging` | no | `integer` |  |
| `stoppedReason` | no | `ReasonEnumType` |  |
| `remoteStartId` | no | `integer` |  |

Unknown fields are rejected in this object.

#### `TriggerReasonEnumType`

Allowed values: `Authorized`, `CablePluggedIn`, `ChargingRateChanged`, `ChargingStateChanged`, `Deauthorized`, `EnergyLimitReached`, `EVCommunicationLost`, `EVConnectTimeout`, `MeterValueClock`, `MeterValuePeriodic`, `TimeLimitReached`, `Trigger`, `UnlockCommand`, `StopAuthorized`, `EVDeparted`, `EVDetected`, `RemoteStop`, `RemoteStart`, `AbnormalCondition`, `SignedDataReceived`, `ResetCommand`

#### `UnitOfMeasureType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `unit` | no | `string` | maxLength=20; default=Wh |
| `multiplier` | no | `integer` | default=0 |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `totalCost` | no | `number` |  |
| `chargingPriority` | no | `integer` |  |
| `idTokenInfo` | no | `IdTokenInfoType` |  |
| `updatedPersonalMessage` | no | `MessageContentType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `AdditionalInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `additionalIdToken` | yes | `string` | maxLength=36 |
| `type` | yes | `string` | maxLength=50 |

Unknown fields are rejected in this object.

#### `AuthorizationStatusEnumType`

Allowed values: `Accepted`, `Blocked`, `ConcurrentTx`, `Expired`, `Invalid`, `NoCredit`, `NotAllowedTypeEVSE`, `NotAtThisLocation`, `NotAtThisTime`, `Unknown`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `IdTokenEnumType`

Allowed values: `Central`, `eMAID`, `ISO14443`, `ISO15693`, `KeyCode`, `Local`, `MacAddress`, `NoAuthorization`

#### `IdTokenInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `AuthorizationStatusEnumType` |  |
| `cacheExpiryDateTime` | no | `string` | format=date-time |
| `chargingPriority` | no | `integer` |  |
| `language1` | no | `string` | maxLength=8 |
| `evseId` | no | `integer[]` | minItems=1 |
| `groupIdToken` | no | `IdTokenType` |  |
| `language2` | no | `string` | maxLength=8 |
| `personalMessage` | no | `MessageContentType` |  |

Unknown fields are rejected in this object.

#### `IdTokenType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `additionalInfo` | no | `AdditionalInfoType[]` | minItems=1 |
| `idToken` | yes | `string` | maxLength=36 |
| `type` | yes | `IdTokenEnumType` |  |

Unknown fields are rejected in this object.

#### `MessageContentType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `format` | yes | `MessageFormatEnumType` |  |
| `language` | no | `string` | maxLength=8 |
| `content` | yes | `string` | maxLength=512 |

Unknown fields are rejected in this object.

#### `MessageFormatEnumType`

Allowed values: `ASCII`, `HTML`, `URI`, `UTF8`
