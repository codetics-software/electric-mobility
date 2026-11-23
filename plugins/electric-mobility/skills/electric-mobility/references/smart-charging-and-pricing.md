# Smart charging and pricing algorithms

Read this when implementing site load management or tariff calculation in a CSMS or CPO.
These are `IMPLEMENTATION CHOICE`s that worked in production. Protocol limits come from the
selected OCPP version and the [OCPI tariffs module](ocpi/tariffs.md); behavior notes are in
[field lessons](field-lessons.md).

## Site load management

### Model

- Areas form a tree (site, then building, then car park, and so on). Each area may set a
  maximum power and a voltage and phase count. An area's limit covers its whole subtree.
- A session can sit under several limited areas. Compute each area separately and keep the
  **lowest** grant per session.
- Stations can be excluded from management. Their live power still counts as load.
- Energy assets (building meters, solar, batteries) add or remove load. Use the latest
  measurement if it is recent (for example under 30 minutes), otherwise a configured static
  value. Producing assets subtract.

### Algorithm

```text
available = area max − excluded stations' power − asset load      (floor at 0)
for each active managed session, oldest first:
    min = voltage × phases × 6 A      (capped at the session's max)
    max = min(connector max, station max, voltage × phases × 32 A)
    grant min if available ≥ min, else grant 0 (the car pauses)
repeat while power remains and some sessions are below max:
    give each open session an equal share, capped at its max
```

- Arrival order decides who pauses when the site is full. Make it visible to operators.
- Work in watts with exact decimals. Convert to amps per phase at the end and round
  **down**, so the sum never exceeds the limit.
- Send a profile only when the grant changes by more than about 5 %, or to or from zero.
  Stations and cars dislike rapid changes, and each profile costs a command slot.
- Use a transaction-scoped `TxProfile`, relative, in amps, with a fixed stack level and a
  profile ID derived from the connector. On session stop, delete the stored profile.
- Recompute on session start and stop (mark the tenant dirty, then compute every ~15 s),
  plus a periodic pass (~5 min) to catch missed events. Isolate failures per tenant.
- Persist the computed plan (available power, grants, time) so the operator can see why a
  car got its current. Compare grants against measured power.
- Set a safe default or fallback profile on stations for when supervision goes silent.

### ISO 15118 and vehicle needs

When a station reports the vehicle's needs (`NotifyEVChargingNeeds` in 2.0.1), build the
profile from the smaller of the vehicle's and the connector's limits, then apply site limits
on top.

## Tariff resolution

### Choose the tariff

1. Keep tariffs that are active and valid at the **session start**.
2. Match scope: connector, station, area, site, or tenant-wide. A scoped field that is set
   must equal the session's value.
3. Match restrictions, evaluated in the **site's time zone**: days of week, time window
   (a window where `from > to` crosses midnight), and energy and duration bounds.
4. Order by scope specificity (most specific first), then explicit priority, then name and
   ID, so the choice is deterministic.

Snapshot the chosen tariff onto the session at start. Later edits must not change it.

### Compute the amount

```text
energy   = max(0, meter stop − meter start)        fall back to the last reading
billed   = energy rounded UP to the tariff's step, if a step is set
hours    = duration in seconds / 3600              (12-digit precision)
parking  = min(idle time, duration)
amount   = flat + billed kWh × energy price + hours × time price + parking hours × parking price
round once, at the end, to the currency's minor unit
```

- Never round intermediate values. Use exact decimals or integer minor units.
- Keep the measured facts, the tariff snapshot, and the amount separately, so a dispute
  can be recalculated.
- A tariff with energy and duration bounds is evaluated twice: once at start to choose a
  provisional tariff, and again at stop with the final energy and duration.
- For a prepaid session, cap the bill at the credit and refund the rest. Stop the session
  when the running estimate reaches the credit, and judge only meter samples that fall
  between the session start and now plus a small clock-skew allowance. See
  [payments](security/payments-and-public-charging.md).
- Publishing to roaming partners maps the internal tariff to OCPI elements and
  restrictions. Check the negotiated version's tax and price rules first.

## Tests

- Allocation: limit below one minimum, exact multiples of the minimum, uneven connector
  maximums, nested areas, excluded stations, a producing asset, stale asset data, and the
  5 % threshold.
- Pricing: scope precedence, priority ties, overnight windows, a different time zone, a
  daylight-saving change, energy steps, negative meter differences, missing stop reading,
  parking longer than the session, and rounding to minor units.
