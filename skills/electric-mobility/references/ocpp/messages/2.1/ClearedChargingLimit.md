# OCPP 2.1: ClearedChargingLimit

Direction: **Charging Station → CSMS**. CALL action: `ClearedChargingLimit`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `chargingLimitSource` | yes | `string` | maxLength=20 |
| `evseId` | no | `integer` | minimum=0.0 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

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
