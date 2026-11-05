# OCPP 1.6: StopTransaction

Direction: **Charge Point → Central System**. CALL action: `StopTransaction`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA OCPP-J JSON schema set. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `idTag` | no | `string` | maxLength=20 |
| `meterStop` | yes | `integer` |  |
| `timestamp` | yes | `string` | format=date-time |
| `transactionId` | yes | `integer` |  |
| `reason` | no | `string` | values: EmergencyStop, EVDisconnected, HardReset, Local, Other, PowerLoss, Reboot, Remote, SoftReset, UnlockCommand, DeAuthorized |
| `transactionData` | no | `object[]` |  |

Unknown object fields are rejected by this schema.

### `transactionData` object

| Field | Required | Type | Constraints |
|---|---|---|---|
| `timestamp` | yes | `string` | format=date-time |
| `sampledValue` | yes | `object[]` |  |

Unknown fields are rejected in this object.

### `transactionData.sampledValue` object

| Field | Required | Type | Constraints |
|---|---|---|---|
| `value` | yes | `string` |  |
| `context` | no | `string` | values: Interruption.Begin, Interruption.End, Sample.Clock, Sample.Periodic, Transaction.Begin, Transaction.End, Trigger, Other |
| `format` | no | `string` | values: Raw, SignedData |
| `measurand` | no | `string` | values: Energy.Active.Export.Register, Energy.Active.Import.Register, Energy.Reactive.Export.Register, Energy.Reactive.Import.Register, Energy.Active.Export.Interval, Energy.Active.Import.Interval, Energy.Reactive.Export.Interval, Energy.Reactive.Import.Interval, Power.Active.Export, Power.Active.Import, Power.Offered, Power.Reactive.Export, Power.Reactive.Import, Power.Factor, Current.Import, Current.Export, Current.Offered, Voltage, Frequency, Temperature, SoC, RPM |
| `phase` | no | `string` | values: L1, L2, L3, N, L1-N, L2-N, L3-N, L1-L2, L2-L3, L3-L1 |
| `location` | no | `string` | values: Cable, EV, Inlet, Outlet, Body |
| `unit` | no | `string` | values: Wh, kWh, varh, kvarh, W, kW, VA, kVA, var, kvar, A, V, K, Celcius, Celsius, Fahrenheit, Percent |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `idTagInfo` | no | `object` |  |

Unknown object fields are rejected by this schema.

### `idTagInfo` object

| Field | Required | Type | Constraints |
|---|---|---|---|
| `expiryDate` | no | `string` | format=date-time |
| `parentIdTag` | no | `string` | maxLength=20 |
| `status` | yes | `string` | values: Accepted, Blocked, Expired, Invalid, ConcurrentTx |

Unknown fields are rejected in this object.
