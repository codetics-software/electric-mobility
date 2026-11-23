# OCPI Canonical Examples

The examples before the final 2.3.0 section illustrate the **2.2.1** wire
contract, adapted from the official specification. Do not send their legacy
Price or Tariff shapes to a 2.3.0 peer. The final section provides explicitly
labeled 2.3.0 implementation fixtures; read
[the migration guide](../references/ocpi/ocpi-2.3.0.md) and pin the partner edition.

## Credentials Registration

### POST /credentials — Sender registers with Receiver
```json
{
  "token": "ebf3b399-779f-4497-9b9d-ac6ad3cc44d2",
  "url": "https://example.com/ocpi/versions",
  "roles": [{
    "role": "CPO",
    "party_id": "EXA",
    "country_code": "NL",
    "business_details": {
      "name": "Example Operator",
      "logo": {
        "url": "https://example.com/img/logo.png",
        "category": "OPERATOR",
        "type": "png",
        "width": 512,
        "height": 512
      },
      "website": "https://example.com"
    }
  }]
}
```

## Location with EVSEs

### Full Location object
```json
{
  "country_code": "BE",
  "party_id": "BEC",
  "id": "LOC1",
  "publish": true,
  "name": "Gent Zuid",
  "address": "F.Rooseveltlaan 3A",
  "city": "Gent",
  "postal_code": "9000",
  "country": "BEL",
  "coordinates": { "latitude": "51.047599", "longitude": "3.729944" },
  "parking_type": "ON_STREET",
  "evses": [{
    "uid": "3256",
    "evse_id": "BE*BEC*E041503001",
    "status": "AVAILABLE",
    "capabilities": ["RESERVABLE"],
    "connectors": [{
      "id": "1",
      "standard": "IEC_62196_T2",
      "format": "CABLE",
      "power_type": "AC_3_PHASE",
      "max_voltage": 220,
      "max_amperage": 16,
      "tariff_ids": ["11"],
      "last_updated": "2015-03-16T10:10:02Z"
    }],
    "floor_level": "-1",
    "last_updated": "2015-06-28T08:12:01Z"
  }],
  "operator": { "name": "BeCharged" },
  "time_zone": "Europe/Brussels",
  "last_updated": "2015-06-29T20:39:09Z"
}
```

### PATCH — update EVSE status only
```json
PATCH .../locations/BE/BEC/LOC1/3256
{
  "status": "CHARGING",
  "last_updated": "2024-01-15T10:17:09Z"
}
```

## Sessions

### Session start (PENDING)
```json
{
  "country_code": "NL", "party_id": "STK",
  "id": "101",
  "start_date_time": "2020-03-09T10:17:09Z",
  "kwh": 0.0,
  "cdr_token": {
    "country_code": "NL", "party_id": "TST",
    "uid": "123abc", "type": "RFID",
    "contract_id": "NL-TST-C12345678-S"
  },
  "auth_method": "WHITELIST",
  "location_id": "LOC1", "evse_uid": "3256", "connector_id": "1",
  "currency": "EUR",
  "total_cost": { "excl_vat": 0.0 },
  "status": "PENDING",
  "last_updated": "2020-03-09T10:17:09Z"
}
```

### PATCH Session — add energy reading mid-session
```json
{
  "kwh": 5.120,
  "total_cost": { "excl_vat": 1.28 },
  "charging_periods": [{
    "start_date_time": "2020-03-09T10:17:09Z",
    "dimensions": [{ "type": "ENERGY", "volume": 5.120 }],
    "tariff_id": "TARIFF-01"
  }],
  "last_updated": "2020-03-09T10:45:00Z"
}
```

## CDR

```json
{
  "country_code": "BE", "party_id": "BEC",
  "id": "12345",
  "start_date_time": "2015-06-29T21:39:09Z",
  "end_date_time": "2015-06-29T23:37:32Z",
  "cdr_token": {
    "country_code": "DE", "party_id": "TNM",
    "uid": "012345678", "type": "RFID",
    "contract_id": "DE8ACC12E46L89"
  },
  "auth_method": "WHITELIST",
  "cdr_location": {
    "id": "LOC1", "name": "Gent Zuid",
    "address": "F.Rooseveltlaan 3A", "city": "Gent",
    "postal_code": "9000", "country": "BEL",
    "coordinates": { "latitude": "3.729944", "longitude": "51.047599" },
    "evse_uid": "3256", "evse_id": "BE*BEC*E041503003",
    "connector_id": "1",
    "connector_standard": "IEC_62196_T2",
    "connector_format": "SOCKET",
    "connector_power_type": "AC_1_PHASE"
  },
  "currency": "EUR",
  "tariffs": [{
    "country_code": "BE", "party_id": "BEC", "id": "12",
    "currency": "EUR",
    "elements": [{ "price_components": [{ "type": "TIME", "price": 2.00, "vat": 10.0, "step_size": 300 }] }],
    "last_updated": "2015-02-02T14:15:01Z"
  }],
  "charging_periods": [{
    "start_date_time": "2015-06-29T21:39:09Z",
    "dimensions": [{ "type": "TIME", "volume": 1.973 }],
    "tariff_id": "12"
  }],
  "total_cost": { "excl_vat": 4.00, "incl_vat": 4.40 },
  "total_energy": 15.342,
  "total_time": 1.973,
  "total_time_cost": { "excl_vat": 4.00, "incl_vat": 4.40 },
  "last_updated": "2015-06-29T22:01:13Z"
}
```

## Tariffs

### Simple per-kWh tariff
```json
{
  "country_code": "DE", "party_id": "ALL",
  "id": "TARIFF-SIMPLE",
  "currency": "EUR",
  "elements": [{
    "price_components": [{
      "type": "ENERGY", "price": 0.25, "vat": 10.0, "step_size": 1
    }]
  }],
  "last_updated": "2024-01-01T00:00:00Z"
}
```

### Complex tariff (flat + time-based with restrictions)
```json
{
  "country_code": "DE", "party_id": "ALL",
  "id": "TARIFF-COMPLEX",
  "currency": "EUR",
  "elements": [
    {
      "price_components": [{ "type": "FLAT", "price": 2.50, "vat": 15.0, "step_size": 1 }]
    },
    {
      "price_components": [{ "type": "TIME", "price": 1.00, "vat": 20.0, "step_size": 900 }],
      "restrictions": { "max_current": 32.00 }
    },
    {
      "price_components": [{ "type": "TIME", "price": 2.00, "vat": 20.0, "step_size": 600 }],
      "restrictions": { "min_current": 32.00, "day_of_week": ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY"] }
    },
    {
      "price_components": [{ "type": "PARKING_TIME", "price": 5.00, "vat": 10.0, "step_size": 300 }],
      "restrictions": { "start_time": "09:00", "end_time": "18:00", "day_of_week": ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY"] }
    }
  ],
  "last_updated": "2024-01-01T00:00:00Z"
}
```

## Tokens

### RFID token
```json
{
  "country_code": "DE", "party_id": "TNM",
  "uid": "012345678", "type": "RFID",
  "contract_id": "DE8ACC12E46L89",
  "issuer": "TheNewMotion",
  "valid": true,
  "whitelist": "ALLOWED",
  "last_updated": "2024-01-15T09:00:00Z"
}
```

### App user token (NEVER whitelist — real-time auth required)
```json
{
  "country_code": "DE", "party_id": "TNM",
  "uid": "bdf21bce-fc97-11e8-8eb2-f2801f1b9fd1",
  "type": "APP_USER",
  "contract_id": "DE8ACC12E46L89",
  "issuer": "TheNewMotion",
  "valid": true,
  "whitelist": "NEVER",
  "last_updated": "2024-01-15T09:00:00Z"
}
```

## Commands

### START_SESSION request (eMSP → CPO)
```json
POST /ocpi/cpo/2.2.1/commands/START_SESSION
{
  "response_url": "https://emsp.example.com/ocpi/commands/result/cmd-001",
  "token": {
    "country_code": "DE", "party_id": "TNM",
    "uid": "012345678", "type": "RFID",
    "contract_id": "DE8ACC12E46L89",
    "issuer": "TheNewMotion",
    "valid": true,
    "whitelist": "ALLOWED",
    "last_updated": "2024-01-15T09:00:00Z"
  },
  "location_id": "LOC1",
  "evse_uid": "3256"
}
```

### CommandResponse (CPO → eMSP, immediate)
```json
{
  "result": "ACCEPTED",
  "timeout": 30,
  "message": [{ "language": "en", "text": "Command forwarded to charge point" }]
}
```

### AsyncResult (CPO → eMSP response_url, after OCPP round-trip)
```json
POST https://emsp.example.com/ocpi/commands/result/cmd-001
{
  "result": "ACCEPTED"
}
```

## OCPI 2.3.0 fixtures

These illustrative payloads use the stable `v2.3.0` types and inspected maintained
core. They are not proof of partner conformance. Object payloads appear inside
OCPI response envelopes where the endpoint requires an envelope.

### Price with multiple taxes (Session/CDR cost type)

Required `before_taxes` replaces 2.2.1's `excl_vat`. Tax entries require `name`
and `amount`; percentages and tax account numbers are optional.

```json
{
  "before_taxes": 10.0,
  "taxes": [
    { "name": "Example tax A", "percentage": 5.0, "amount": 0.5 },
    { "name": "Example tax B", "amount": 1.0 }
  ]
}
```

### Tariff with explicit tax basis and PriceLimit

PriceLimit is distinct from Price; it uses `before_taxes` and optional
`after_taxes`. `tax_included` is required in 2.3.0. ENERGY prices are per kWh
while step_size is in Wh. Tax labels/rates here are illustrative.

```json
{
  "country_code": "FR",
  "party_id": "CPO",
  "id": "ENERGY-230",
  "currency": "EUR",
  "tax_included": "NO",
  "min_price": { "before_taxes": 1.0, "after_taxes": 1.2 },
  "elements": [
    {
      "price_components": [
        { "type": "ENERGY", "price": 0.35, "vat": 20.0, "step_size": 1 }
      ]
    }
  ],
  "last_updated": "2026-10-05T09:00:00Z"
}
```

### Location with Parking and EVSEParking

`vehicle_types` belongs to Parking. An EVSE links to a parking object's id;
`evse_position` describes its placement. Provider names are informational,
independent of party identity and authorization.

```json
{
  "country_code": "FR",
  "party_id": "CPO",
  "id": "LOC-230",
  "publish": true,
  "address": "1 Example Street",
  "city": "Paris",
  "country": "FRA",
  "coordinates": { "latitude": "48.856600", "longitude": "2.352200" },
  "time_zone": "Europe/Paris",
  "help_phone": "+33100000000",
  "parking_places": [
    {
      "id": "P1",
      "vehicle_types": ["PERSONAL_VEHICLE"],
      "restricted_to_type": false,
      "reservation_required": false
    }
  ],
  "evses": [
    {
      "uid": "EVSE-230",
      "status": "AVAILABLE",
      "parking": [{ "parking_id": "P1", "evse_position": "LEFT" }],
      "accepted_service_providers": ["Example Mobility"],
      "connectors": [
        {
          "id": "1",
          "standard": "IEC_62196_T2_COMBO",
          "format": "CABLE",
          "power_type": "DC",
          "max_voltage": 1000,
          "max_amperage": 200,
          "capabilities": ["ISO_15118_2_PLUG_AND_CHARGE"],
          "last_updated": "2026-10-05T09:00:00Z"
        }
      ],
      "last_updated": "2026-10-05T09:00:00Z"
    }
  ],
  "last_updated": "2026-10-05T09:00:00Z"
}
```

### Hub Credentials with reachable parties

The hub identity is distinct from represented CPO/EMSP parties; do not add the
legacy `HUB` role to this core contract. The token is a fictitious placeholder,
provided unencoded in Credentials; the Authorization header base64-encodes it.

```json
{
  "token": "example-placeholder-token",
  "url": "https://hub.example.com/ocpi/versions",
  "hub_party_id": "FRHUB",
  "roles": [
    {
      "role": "CPO",
      "country_code": "FR",
      "party_id": "CPO",
      "business_details": { "name": "Example Operator" }
    },
    {
      "role": "EMSP",
      "country_code": "FR",
      "party_id": "MSP",
      "business_details": { "name": "Example Mobility" }
    }
  ]
}
```

### OpenEnum and unknown-field handling

Retain an unknown connector classification as a string without claiming support
for it. Accept a non-specified descriptive JSON field while continuing to reject
missing required fields and unauthorized actions. This fragment is not a full
Connector object:

```json
{
  "standard": "EXAMPLE_FUTURE_CONNECTOR",
  "maintenance_contact": "Example operator desk"
}
```
