# OCPP 2.1: NotifyPeriodicEventStream

Direction: **Charging Station → CSMS**. OCPP-J frame type: **SEND (6)**. This message is unconfirmed; do not send a CALLRESULT or CALLERROR. Apply stream setup, rate, and backpressure rules from the OCPP 2.1 runtime guide.

Compact wire-field reference derived from the OCA Part 3 JSON schema archive.

## SEND payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `data` | yes | `StreamDataElementType[]` | minItems=1 |
| `id` | yes | `integer` | minimum=0.0 |
| `pending` | yes | `integer` | minimum=0.0 |
| `basetime` | yes | `string` | format=date-time |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `StreamDataElementType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `t` | yes | `number` |  |
| `v` | yes | `string` | maxLength=2500 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
