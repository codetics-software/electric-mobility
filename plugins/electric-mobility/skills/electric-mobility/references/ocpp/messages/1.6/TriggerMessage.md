# OCPP 1.6: TriggerMessage

Direction: **Central System → Charge Point**. CALL action: `TriggerMessage`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `requestedMessage` | yes | `string` | values: BootNotification, DiagnosticsStatusNotification, FirmwareStatusNotification, Heartbeat, MeterValues, StatusNotification |
| `connectorId` | no | `integer` |  |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `string` | values: Accepted, Rejected, NotImplemented |

Unknown object fields are rejected by this schema.
