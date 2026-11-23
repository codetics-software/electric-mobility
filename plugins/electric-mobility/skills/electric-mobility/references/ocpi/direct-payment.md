# OCPI 2.3.0 Payments module

Source: [published Payments module](https://github.com/ocpi/ocpi/blob/2.3.0/release/payments/mod_payments.asciidoc). This file retains its old filename for existing skill links; the official module is **Payments**, with wire ModuleID `payments`. Pin the Payments branch/tag and compatible core edition. It is not a `directpayments` endpoint or a `DirectPaymentSession` object.

## Scope and roles

The module supports direct payment through a payment terminal in a roaming arrangement. The source identifies the **Payment Terminal Provider (PTP)** as data owner. It describes `Terminal` and `FinancialAdviceConfirmation` objects, terminal assignments to locations/EVSEs, activation, tariff display, payment preauthorization, a StartSession command, CDR transfer, and financial advice confirmation when the CPO issues the invoice. The CPO, PTP, and payment service provider are distinct roles in the business flow; do not rename every party to PSP.

## Implementation decisions

- Keep terminal identity and the set of assigned locations/EVSEs separate from a charging Session and its CDR. A terminal can serve multiple locations or EVSEs.
- Fetch the applicable connector and tariff information before presenting a price and requesting payment preauthorization. Preserve the tariff version, amount, and currency used for the decision.
- Correlate preauthorization, StartSession, OCPP attempt, Session, CDR, capture, and invoice/financial-advice confirmation. A successful preauthorization or command response does not prove energy delivery or final payment.
- Treat `FinancialAdviceConfirmation` as a distinct object when required by the invoicing arrangement. Reconcile captures and CDR totals; preserve corrections rather than overwriting settled history.
- Use the exact sender/receiver endpoint definitions and object schemas in the pinned Payments source. The source contains Terminals and Financial Advice Confirmation interfaces; do not create a generic `/directpayments` API and call it OCPI.
- Keep cardholder data with the payment provider. Log only nonsecret references and protocol correlation; authorize terminal activation, assignment, and payment-related callbacks.

This module can help with ad hoc payment architecture, but implementing it alone does not establish compliance with any regional payment regulation. Verify applicable legal requirements separately.
