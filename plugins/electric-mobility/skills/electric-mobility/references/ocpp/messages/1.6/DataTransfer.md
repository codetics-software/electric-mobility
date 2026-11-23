# OCPP 1.6: DataTransfer

Direction: **either peer**. CALL action: `DataTransfer`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |
| `messageId` | no | `string` | maxLength=50 |
| `data` | no | `string` |  |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `string` | values: Accepted, Rejected, UnknownMessageId, UnknownVendorId |
| `data` | no | `string` |  |

Unknown object fields are rejected by this schema.
