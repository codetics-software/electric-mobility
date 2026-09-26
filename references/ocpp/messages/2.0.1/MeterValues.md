# OCPP 2.0.1: MeterValues

Direction: **Charging Station → CSMS**. CALL action: `MeterValues`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `evseId` | yes | `integer` |  |
| `meterValue` | yes | `MeterValueType[]` | minItems=1 |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

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

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |
