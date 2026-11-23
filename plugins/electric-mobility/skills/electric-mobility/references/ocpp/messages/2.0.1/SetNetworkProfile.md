# OCPP 2.0.1: SetNetworkProfile

Direction: **CSMS → Charging Station**. CALL action: `SetNetworkProfile`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `configurationSlot` | yes | `integer` |  |
| `connectionData` | yes | `NetworkConnectionProfileType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `APNAuthenticationEnumType`

Allowed values: `CHAP`, `NONE`, `PAP`, `AUTO`

#### `APNType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `apn` | yes | `string` | maxLength=512 |
| `apnUserName` | no | `string` | maxLength=20 |
| `apnPassword` | no | `string` | maxLength=20 |
| `simPin` | no | `integer` |  |
| `preferredNetwork` | no | `string` | maxLength=6 |
| `useOnlyPreferredNetwork` | no | `boolean` | default=false |
| `apnAuthentication` | yes | `APNAuthenticationEnumType` |  |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `NetworkConnectionProfileType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `apn` | no | `APNType` |  |
| `ocppVersion` | yes | `OCPPVersionEnumType` |  |
| `ocppTransport` | yes | `OCPPTransportEnumType` |  |
| `ocppCsmsUrl` | yes | `string` | maxLength=512 |
| `messageTimeout` | yes | `integer` |  |
| `securityProfile` | yes | `integer` |  |
| `ocppInterface` | yes | `OCPPInterfaceEnumType` |  |
| `vpn` | no | `VPNType` |  |

Unknown fields are rejected in this object.

#### `OCPPInterfaceEnumType`

Allowed values: `Wired0`, `Wired1`, `Wired2`, `Wired3`, `Wireless0`, `Wireless1`, `Wireless2`, `Wireless3`

#### `OCPPTransportEnumType`

Allowed values: `JSON`, `SOAP`

#### `OCPPVersionEnumType`

Allowed values: `OCPP12`, `OCPP15`, `OCPP16`, `OCPP20`

#### `VPNEnumType`

Allowed values: `IKEv2`, `IPSec`, `L2TP`, `PPTP`

#### `VPNType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `server` | yes | `string` | maxLength=512 |
| `user` | yes | `string` | maxLength=20 |
| `group` | no | `string` | maxLength=20 |
| `password` | yes | `string` | maxLength=20 |
| `key` | yes | `string` | maxLength=255 |
| `type` | yes | `VPNEnumType` |  |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `SetNetworkProfileStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `SetNetworkProfileStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `Failed`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=512 |

Unknown fields are rejected in this object.
