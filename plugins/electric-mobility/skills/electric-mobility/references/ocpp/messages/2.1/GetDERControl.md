# OCPP 2.1: GetDERControl

Direction: **CSMS → Charging Station**. CALL action: `GetDERControl`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `requestId` | yes | `integer` |  |
| `isDefault` | no | `boolean` |  |
| `controlType` | no | `DERControlEnumType` |  |
| `controlId` | no | `string` | maxLength=36 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `DERControlEnumType`

Allowed values: `EnterService`, `FreqDroop`, `FreqWatt`, `FixedPFAbsorb`, `FixedPFInject`, `FixedVar`, `Gradients`, `HFMustTrip`, `HFMayTrip`, `HVMustTrip`, `HVMomCess`, `HVMayTrip`, `LimitMaxDischarge`, `LFMustTrip`, `LVMustTrip`, `LVMomCess`, `LVMayTrip`, `PowerMonitoringMustTrip`, `VoltVar`, `VoltWatt`, `WattPF`, `WattVar`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `DERControlStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `DERControlStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `NotSupported`, `NotFound`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
