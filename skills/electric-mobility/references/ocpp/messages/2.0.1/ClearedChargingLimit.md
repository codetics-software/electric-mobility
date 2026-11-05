# OCPP 2.0.1: ClearedChargingLimit

Direction: **Charging Station → CSMS**. CALL action: `ClearedChargingLimit`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `chargingLimitSource` | yes | `ChargingLimitSourceEnumType` |  |
| `evseId` | no | `integer` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ChargingLimitSourceEnumType`

Allowed values: `EMS`, `Other`, `SO`, `CSO`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |


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
