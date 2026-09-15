# OCPI — DirectPayment Module

## Purpose

The DirectPayment module standardizes **ad-hoc (contract-free) payment flows** — specifically when a driver pays directly at the charger with a credit/debit card or QR code, without an eMSP contract. The CPO backend communicates with the payment terminal's backend using this module.

> This module is the OCPI response to **EU AFIR Article 5**, which mandates that all publicly accessible chargers support ad-hoc payment (no app, no contract required).

**Data owner**: CPO (terminal operator)  
**Direction**: CPO ↔ Payment Service Provider (PSP) backend

---

## Version Availability

| Version | Available |
|---|---|
| 2.1.1 | No |
| 2.2.1 | No |
| 2.3.0 | Yes (new in 2.3.0) |

---

## What Problem It Solves

Before DirectPayment:
- OCPI covered roaming (eMSP ↔ CPO)
- Ad-hoc card payments were handled by proprietary integrations (Stripe, local PSPs) with no standard
- CDRs from ad-hoc sessions couldn't be exchanged in a standard way

With DirectPayment:
- Standardized data exchange between CPO backend and payment terminal backend
- Ad-hoc sessions produce standard OCPI CDRs
- Price shown to driver before session start (AFIR transparency requirement)

---

## Architecture

```
Driver → inserts card at charger terminal
          ↓
Terminal → Terminal Backend (PSP)
          ↓  [DirectPayment OCPI]
PSP ↔ CPO Backend
          ↓
CPO → starts OCPP session on charger
          ↓
Session ongoing → CPO sends live data to PSP
          ↓
Session ends → CPO creates CDR → sends to PSP
          ↓
PSP charges driver's card
```

---

## Key Objects

### `DirectPaymentSession`

Tracks the state of an ad-hoc payment session:

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique session ID |
| `start_date_time` | DateTime | When payment session started |
| `kwh` | number | Energy delivered so far |
| `location_id` | string | Location |
| `evse_uid` | string | EVSE |
| `connector_id` | string | Connector |
| `tariff` | Tariff | Tariff shown to driver at session start (snapshot) |
| `currency` | string | ISO 4217 |
| `total_cost` | Price? | Running total |
| `status` | DirectPaymentStatus | Current status |
| `last_updated` | DateTime | |

### `DirectPaymentStatus`

| Value | Meaning |
|---|---|
| `STARTING` | Payment initiated, session starting |
| `ACTIVE` | Charging in progress |
| `STOPPING` | Session ending |
| `COMPLETED` | Session complete, CDR generated |
| `FAILED` | Payment or session failed |

---

## HTTP Endpoints

The module defines endpoints between CPO and PSP backends. Exact path structure follows OCPI conventions but is specific to the DirectPayment context.

| Method | Path | Description |
|---|---|---|
| `POST` | `/ocpi/cpo/2.x/directpayments` | PSP initiates a payment session |
| `GET` | `/ocpi/cpo/2.x/directpayments/{id}` | PSP checks session status |
| `PUT` | `/ocpi/psp/2.x/directpayments/{country}/{party}/{id}` | CPO pushes session updates to PSP |

---

## AFIR Compliance Context

EU AFIR (Alternative Fuels Infrastructure Regulation, effective April 2024) requires:

1. **Ad-hoc access**: Drivers must be able to charge without a subscription or app
2. **Price transparency**: The price must be shown before starting a session (per kWh, per minute, or per session — not just "see app")
3. **Payment method**: Credit/debit card at the terminal (or QR code)

The DirectPayment module ensures that when a driver taps their card:
- The CPO backend knows the tariff to show
- The PSP backend knows when charging starts/stops
- Both systems get a CDR for settlement

---

## Implementation Notes

### Tariff Display Before Start
The CPO must provide the applicable `AD_HOC_PAYMENT` tariff to the terminal before the driver confirms. This is coordinated through the DirectPayment session initiation flow.

### CDR Generation
Ad-hoc sessions generate standard OCPI CDRs. The CDR is sent to the PSP (not an eMSP) via this module. The CDR structure is identical to roaming CDRs.

### VAT and Tax
AFIR requires price displayed to include VAT. For North American deployments (2.3.0), tax fields on the CDR support state/province-level tax breakdown.

---

## Spec References

- 2.3.0: `mod_direct_payment.asciidoc` — `2.3.0/release/core`
