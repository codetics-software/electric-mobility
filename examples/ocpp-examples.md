# OCPP Canonical Examples

Source: OCPP 1.6 JSON schemas + specification.

## OCPP-J Wire Format

```
[MessageTypeId, UniqueId, Action, Payload]   // Request (type 2)
[MessageTypeId, UniqueId, Payload]           // Response (type 3)
[MessageTypeId, UniqueId, ErrorCode, ErrorDescription, ErrorDetails]  // Error (type 4)
```

## Startup Sequence

### BootNotification (CP → CS)
```json
[2, "19223201", "BootNotification", {
  "chargePointVendor": "VendorX",
  "chargePointModel": "ModelY",
  "chargePointSerialNumber": "vcpb-1234",
  "firmwareVersion": "1.2.0",
  "iccid": "89014103211118510720",
  "imsi": "123456789"
}]
```

### BootNotification Response (CS → CP)
```json
[3, "19223201", {
  "currentTime": "2024-01-15T10:00:00Z",
  "interval": 300,
  "status": "Accepted"
}]
```

### StatusNotification — connector available (CP → CS)
```json
[2, "19223202", "StatusNotification", {
  "connectorId": 1,
  "status": "Available",
  "errorCode": "NoError",
  "timestamp": "2024-01-15T10:00:05Z"
}]
[3, "19223202", {}]
```

## Authorization

### Authorize — RFID presented (CP → CS)
```json
[2, "19223203", "Authorize", {
  "idTag": "012345678"
}]
```

### Authorize Response — accepted
```json
[3, "19223203", {
  "idTagInfo": {
    "status": "Accepted",
    "expiryDate": "2025-01-15T00:00:00Z",
    "parentIdTag": "GROUP001"
  }
}]
```

### Authorize Response — invalid
```json
[3, "19223203", {
  "idTagInfo": {
    "status": "Invalid"
  }
}]
```

## Charging Session

### StartTransaction (CP → CS)
```json
[2, "19223204", "StartTransaction", {
  "connectorId": 1,
  "idTag": "012345678",
  "meterStart": 1204307,
  "timestamp": "2024-01-15T10:17:09Z"
}]
```

### StartTransaction Response
```json
[3, "19223204", {
  "transactionId": 1,
  "idTagInfo": {
    "status": "Accepted"
  }
}]
```

### MeterValues — periodic during charging (CP → CS)
```json
[2, "19223210", "MeterValues", {
  "connectorId": 1,
  "transactionId": 1,
  "meterValue": [{
    "timestamp": "2024-01-15T10:30:00Z",
    "sampledValue": [
      {
        "value": "1215850",
        "context": "Sample.Periodic",
        "measurand": "Energy.Active.Import.Register",
        "unit": "Wh"
      },
      {
        "value": "7350",
        "context": "Sample.Periodic",
        "measurand": "Power.Active.Import",
        "unit": "W"
      },
      {
        "value": "32.1",
        "context": "Sample.Periodic",
        "measurand": "Current.Import",
        "phase": "L1",
        "unit": "A"
      },
      {
        "value": "228.4",
        "context": "Sample.Periodic",
        "measurand": "Voltage",
        "phase": "L1-N",
        "unit": "V"
      }
    ]
  }]
}]
```

### StopTransaction (CP → CS)
```json
[2, "19223205", "StopTransaction", {
  "transactionId": 1,
  "idTag": "012345678",
  "meterStop": 1229649,
  "timestamp": "2024-01-15T12:05:22Z",
  "reason": "Local",
  "transactionData": [{
    "timestamp": "2024-01-15T12:05:22Z",
    "sampledValue": [
      {
        "value": "1229649",
        "context": "Transaction.End",
        "measurand": "Energy.Active.Import.Register",
        "unit": "Wh"
      }
    ]
  }]
}]
```

**Energy delivered = meterStop - meterStart = 1229649 - 1204307 = 25342 Wh = 25.342 kWh**

## Remote Commands

### RemoteStartTransaction (CS → CP)
```json
[2, "CS-001", "RemoteStartTransaction", {
  "connectorId": 1,
  "idTag": "012345678"
}]
```

### RemoteStartTransaction Response
```json
[3, "CS-001", {
  "status": "Accepted"
}]
```

### RemoteStopTransaction (CS → CP)
```json
[2, "CS-002", "RemoteStopTransaction", {
  "transactionId": 1
}]
[3, "CS-002", { "status": "Accepted" }]
```

### ChangeAvailability — take connector offline (CS → CP)
```json
[2, "CS-003", "ChangeAvailability", {
  "connectorId": 1,
  "type": "Inoperative"
}]
[3, "CS-003", { "status": "Accepted" }]
```

### Reset — soft reboot (CS → CP)
```json
[2, "CS-004", "Reset", { "type": "Soft" }]
[3, "CS-004", { "status": "Accepted" }]
```

## Smart Charging

### SetChargingProfile (CS → CP)
```json
[2, "CS-010", "SetChargingProfile", {
  "connectorId": 1,
  "csChargingProfiles": {
    "chargingProfileId": 1,
    "stackLevel": 0,
    "chargingProfilePurpose": "TxProfile",
    "chargingProfileKind": "Relative",
    "transactionId": 1,
    "chargingSchedule": {
      "chargingRateUnit": "W",
      "chargingSchedulePeriod": [
        { "startPeriod": 0, "limit": 11000 },
        { "startPeriod": 3600, "limit": 7400 },
        { "startPeriod": 7200, "limit": 3700 }
      ],
      "duration": 14400,
      "minChargingRate": 1400
    }
  }
}]
[3, "CS-010", { "status": "Accepted" }]
```

### GetCompositeSchedule (CS → CP) — query effective schedule
```json
[2, "CS-011", "GetCompositeSchedule", {
  "connectorId": 1,
  "duration": 3600,
  "chargingRateUnit": "W"
}]
```

## Reservation

### ReserveNow (CS → CP)
```json
[2, "CS-020", "ReserveNow", {
  "connectorId": 1,
  "expiryDate": "2024-01-15T11:00:00Z",
  "idTag": "012345678",
  "reservationId": 42
}]
[3, "CS-020", { "status": "Accepted" }]
```

### StatusNotification — reserved state
```json
[2, "19223300", "StatusNotification", {
  "connectorId": 1,
  "status": "Reserved",
  "errorCode": "NoError",
  "timestamp": "2024-01-15T10:05:00Z"
}]
```

## Configuration

### GetConfiguration (CS → CP)
```json
[2, "CS-030", "GetConfiguration", {
  "key": ["HeartbeatInterval", "MeterValueSampleInterval", "ConnectionTimeOut"]
}]
```

### GetConfiguration Response
```json
[3, "CS-030", {
  "configurationKey": [
    { "key": "HeartbeatInterval", "readonly": false, "value": "300" },
    { "key": "MeterValueSampleInterval", "readonly": false, "value": "60" },
    { "key": "ConnectionTimeOut", "readonly": false, "value": "60" }
  ]
}]
```

### ChangeConfiguration (CS → CP)
```json
[2, "CS-031", "ChangeConfiguration", {
  "key": "MeterValueSampleInterval",
  "value": "30"
}]
[3, "CS-031", { "status": "Accepted" }]
```

## Error Handling

### OCPP-J Error Response
```json
[4, "19223201", "InternalError", "Unable to process request", {}]
```

Error codes: `NotImplemented`, `NotSupported`, `InternalError`, `ProtocolError`, `SecurityError`, `FormationViolation`, `PropertyConstraintViolation`, `OccurenceConstraintViolation`, `TypeConstraintViolation`, `GenericError`
