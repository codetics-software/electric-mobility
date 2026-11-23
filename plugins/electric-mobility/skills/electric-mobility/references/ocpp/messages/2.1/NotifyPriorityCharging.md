# OCPP 2.1: NotifyPriorityCharging

Direction: **Charging Station → CSMS**. CALL action: `NotifyPriorityCharging`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `transactionId` | yes | `string` | maxLength=36 |
| `activated` | yes | `boolean` |  |
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
