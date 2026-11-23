# OCPP 2.0.1: NotifyCustomerInformation

Direction: **Charging Station → CSMS**. CALL action: `NotifyCustomerInformation`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `data` | yes | `string` | maxLength=512 |
| `tbc` | no | `boolean` | default=false |
| `seqNo` | yes | `integer` |  |
| `generatedAt` | yes | `string` | format=date-time |
| `requestId` | yes | `integer` |  |

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
