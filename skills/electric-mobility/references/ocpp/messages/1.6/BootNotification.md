# OCPP 1.6: BootNotification

Direction: **Charge Point → Central System**. CALL action: `BootNotification`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA OCPP-J JSON schema set. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state.

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
