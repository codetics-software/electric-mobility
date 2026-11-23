# OCPP 1.6: StatusNotification

Direction: **Charge Point → Central System**. CALL action: `StatusNotification`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `connectorId` | yes | `integer` |  |
| `errorCode` | yes | `string` | values: ConnectorLockFailure, EVCommunicationError, GroundFailure, HighTemperature, InternalError, LocalListConflict, NoError, OtherError, OverCurrentFailure, PowerMeterFailure, PowerSwitchFailure, ReaderFailure, ResetFailure, UnderVoltage, OverVoltage, WeakSignal |
| `info` | no | `string` | maxLength=50 |
| `status` | yes | `string` | values: Available, Preparing, Charging, SuspendedEVSE, SuspendedEV, Finishing, Reserved, Unavailable, Faulted |
| `timestamp` | no | `string` | format=date-time |
| `vendorId` | no | `string` | maxLength=255 |
| `vendorErrorCode` | no | `string` | maxLength=50 |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| *(empty object)* | — | — | — |

Unknown object fields are rejected by this schema.
