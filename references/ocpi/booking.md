# OCPI 2.3.0 Bookings module

Source: [published Bookings module](https://github.com/ocpi/ocpi/blob/2.3.0/release/bookings/mod_bookings.asciidoc). It is a separately packaged optional 2.3.0 module. Pin its tag/branch and the compatible core edition; the Bookings branch may contain changes beyond the `v2.3.0-bookings` tag.

## Model and lifecycle

The CPO publishes `BookingLocation` information and a `Calendar` of bookable availability. An eMSP requests a `Booking`; the CPO owns the resulting booking information. The current module source describes a lifecycle beginning at `PENDING`, then `RESERVED`, `REJECTED`, or `FAILED`. A reserved booking can end as `FULFILLED`, `CANCELED`, or `NO_SHOW`. `CHECKED_IN`, `CHARGING`, `COMPLETED`, and `INVALID` are **not** states in that published lifecycle; keep those as separate product or Session facts if needed.

The booking request/response also carries processing status distinct from the booking's reservation status. Preserve both dimensions rather than reducing them to one enum. A booking becoming `FULFILLED` is associated with actual use and may be connected to a charging Session; do not infer delivered energy from the booking state alone.

## Implementation decisions

- Discover the module's advertised endpoints and roles. The sender side exposes bookable locations/calendars and bookings, including a request operation; receiver/push interfaces propagate changes. Use the exact paths, methods, and object names from the pinned source.
- Keep booking location and calendar identity separate from physical Location, EVSE, connector, and charging Session identity. Store the specific availability and terms shown when the request was made.
- Enforce atomic capacity checks when accepting overlapping requests. Make repeated booking requests and callbacks idempotent; retain a stable request and booking correlation.
- Model cancellation and no-show policy from the published booking terms and commercial agreement. A fee is a billing decision, not an automatic consequence of a status string.
- Reconcile booking status after outages, and test concurrent requests, stale calendars, accepted changes, rejection, cancellation, no-show, and Session linkage.

`RESERVE_NOW` in the Commands module is a different operation. Do not expose Bookings to partners that only advertise Commands.
