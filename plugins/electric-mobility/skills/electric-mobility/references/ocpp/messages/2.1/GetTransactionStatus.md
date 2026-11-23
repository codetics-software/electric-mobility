# OCPP 2.1: GetTransactionStatus

Direction: **CSMS → Charging Station**. CALL action: `GetTransactionStatus`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `transactionId` | no | `string` | maxLength=36 |
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
| `ongoingIndicator` | no | `boolean` |  |
| `messagesInQueue` | yes | `boolean` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |
