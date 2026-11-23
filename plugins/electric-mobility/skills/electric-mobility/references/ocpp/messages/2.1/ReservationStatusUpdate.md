# OCPP 2.1: ReservationStatusUpdate

Direction: **Charging Station → CSMS**. CALL action: `ReservationStatusUpdate`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reservationId` | yes | `integer` | minimum=0.0 |
| `reservationUpdateStatus` | yes | `ReservationUpdateStatusEnumType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `ReservationUpdateStatusEnumType`

Allowed values: `Expired`, `Removed`, `NoTransaction`


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
