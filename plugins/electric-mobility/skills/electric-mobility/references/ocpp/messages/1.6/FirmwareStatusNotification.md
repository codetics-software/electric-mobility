# OCPP 1.6: FirmwareStatusNotification

Direction: **Charge Point → Central System**. CALL action: `FirmwareStatusNotification`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `string` | values: Downloaded, DownloadFailed, Downloading, Idle, InstallationFailed, Installing, Installed |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| *(empty object)* | — | — | — |

Unknown object fields are rejected by this schema.
