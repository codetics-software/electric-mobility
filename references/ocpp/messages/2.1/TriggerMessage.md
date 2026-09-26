# OCPP 2.1: TriggerMessage

Direction: **CSMS → Charging Station**. CALL action: `TriggerMessage`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `evse` | no | `EVSEType` |  |
| `requestedMessage` | yes | `MessageTriggerEnumType` |  |
| `customTrigger` | no | `string` | maxLength=50 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `EVSEType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `id` | yes | `integer` | minimum=0.0 |
| `connectorId` | no | `integer` | minimum=0.0 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `MessageTriggerEnumType`

Allowed values: `BootNotification`, `LogStatusNotification`, `FirmwareStatusNotification`, `Heartbeat`, `MeterValues`, `SignChargingStationCertificate`, `SignV2GCertificate`, `SignV2G20Certificate`, `StatusNotification`, `TransactionEvent`, `SignCombinedCertificate`, `PublishFirmwareStatusNotification`, `CustomTrigger`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `TriggerMessageStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TriggerMessageStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `NotImplemented`
