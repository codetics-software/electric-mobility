# OCPP 2.1: SecurityEventNotification

Direction: **Charging Station → CSMS**. CALL action: `SecurityEventNotification`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `type` | yes | `string` | maxLength=50 |
| `timestamp` | yes | `string` | format=date-time |
| `techInfo` | no | `string` | maxLength=255 |
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
