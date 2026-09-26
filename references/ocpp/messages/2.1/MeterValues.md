# OCPP 2.1: MeterValues

Direction: **Charging Station → CSMS**. CALL action: `MeterValues`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `evseId` | yes | `integer` | minimum=0.0 |
| `meterValue` | yes | `MeterValueType[]` | minItems=1 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

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

#### `PhaseEnumType`

Allowed values: `L1`, `L2`, `L3`, `N`, `L1-N`, `L2-N`, `L3-N`, `L1-L2`, `L2-L3`, `L3-L1`

#### `ReadingContextEnumType`

Allowed values: `Interruption.Begin`, `Interruption.End`, `Other`, `Sample.Clock`, `Sample.Periodic`, `Transaction.Begin`, `Transaction.End`, `Trigger`

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
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |
