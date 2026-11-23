# OCPP 1.6: BootNotification

Direction: **Charge Point → Central System**. CALL action: `BootNotification`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `chargePointVendor` | yes | `string` | maxLength=20 |
| `chargePointModel` | yes | `string` | maxLength=20 |
| `chargePointSerialNumber` | no | `string` | maxLength=25 |
| `chargeBoxSerialNumber` | no | `string` | maxLength=25 |
| `firmwareVersion` | no | `string` | maxLength=50 |
| `iccid` | no | `string` | maxLength=20 |
| `imsi` | no | `string` | maxLength=20 |
| `meterType` | no | `string` | maxLength=25 |
| `meterSerialNumber` | no | `string` | maxLength=25 |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `string` | values: Accepted, Pending, Rejected |
| `currentTime` | yes | `string` | format=date-time |
| `interval` | yes | `integer` |  |

Unknown object fields are rejected by this schema.
