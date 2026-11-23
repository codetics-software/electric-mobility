# OCPP 1.6: UpdateFirmware

Direction: **Central System → Charge Point**. CALL action: `UpdateFirmware`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `location` | yes | `string` | format=uri |
| `retries` | no | `integer` |  |
| `retrieveDate` | yes | `string` | format=date-time |
| `retryInterval` | no | `integer` |  |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| *(empty object)* | — | — | — |

Unknown object fields are rejected by this schema.
