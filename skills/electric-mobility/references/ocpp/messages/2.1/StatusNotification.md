# OCPP 2.1: StatusNotification

Direction: **Charging Station → CSMS**. CALL action: `StatusNotification`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `timestamp` | yes | `string` | format=date-time |
| `connectorStatus` | yes | `ConnectorStatusEnumType` |  |
| `evseId` | yes | `integer` | minimum=0.0 |
| `connectorId` | yes | `integer` | minimum=0.0 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ConnectorStatusEnumType`

Allowed values: `Available`, `Occupied`, `Reserved`, `Unavailable`, `Faulted`

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
