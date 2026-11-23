# OCPP 2.1: NotifyDERStartStop

Direction: **Charging Station → CSMS**. CALL action: `NotifyDERStartStop`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `controlId` | yes | `string` | maxLength=36 |
| `started` | yes | `boolean` |  |
| `timestamp` | yes | `string` | format=date-time |
| `supersededIds` | no | `string[]` | minItems=1; maxItems=24 |
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
