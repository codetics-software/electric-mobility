# OCPP 2.1: GetBaseReport

Direction: **CSMS → Charging Station**. CALL action: `GetBaseReport`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `requestId` | yes | `integer` |  |
| `reportBase` | yes | `ReportBaseEnumType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `ReportBaseEnumType`

Allowed values: `ConfigurationInventory`, `FullInventory`, `SummaryInventory`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `GenericDeviceModelStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `GenericDeviceModelStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `NotSupported`, `EmptyResultSet`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
