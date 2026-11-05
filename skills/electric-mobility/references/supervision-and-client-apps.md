# Web, iOS, and Android Supervision and Driver Apps

Use this reference when building frontend experiences for CPO operators, eMSP drivers/fleets, installers, support agents, or site hosts.

Read `full-platform-blueprint.md`, `domain-relationships.md`, and `charging-lifecycles.md` for the corresponding backend facts.

## 1. Build Role-Based Products

Do not make one dashboard where every role sees every concept.

| Persona | Primary jobs |
|---|---|
| CPO operations | supervise connectivity/status, sessions, commands, incidents, firmware, tariffs, roaming health |
| Support agent | find driver/session/station, inspect timeline, safely retry or escalate, protect PII |
| Installer/maintainer | commission station, verify connection/topology, run diagnostics, record intervention |
| Site host | view usage, availability, revenue/reimbursement, incidents, limited controls |
| eMSP driver | find compatible charging, understand price, start/stop, track session, receive receipt/support |
| Fleet manager | manage users/cards/vehicles, policies, budgets, allocation, invoices, exports |
| Finance/reconciliation | inspect CDRs, corrections, disputes, invoices, payouts, unmatched records |
| Platform administrator | configure tenants, partners, credentials, roles, features, and audit |

Menus, permissions, terminology, and data density should match the persona.

## 2. CPO Supervision Information Architecture

```text
Overview
  ├── network availability and freshness
  ├── active/stuck sessions
  ├── disconnected/degraded stations
  ├── open incidents
  └── roaming/integration failures

Infrastructure
  ├── map and list
  ├── Location
  ├── Station
  ├── EVSE
  ├── Connector
  ├── configuration/capabilities
  └── maintenance history

Operations
  ├── live sessions
  ├── command history
  ├── alarms/incidents
  ├── diagnostics/firmware
  └── smart charging

Commercial
  ├── tariffs/policies/groups
  ├── CDRs and corrections
  ├── payment sessions
  ├── reimbursements
  └── reports

Interoperability
  ├── OCPI parties/connections
  ├── module sync health
  ├── rejected payloads
  ├── retries/reconciliation
  └── Gireve/direct-partner health
```

## 3. Station Supervision Screen

A station detail view should separate current facts from history.

### Header

- station identity, vendor/model, tenant/account/location;
- connectivity state and last seen time;
- OCPP version/security profile;
- administrative and maintenance status;
- active incident severity;
- command permissions and capability gates.

### EVSE/connector cards

- operational status with observation timestamp;
- occupancy/transaction/energy-flow distinctions;
- active session and credential-safe reference;
- latest power/energy with unit and freshness;
- configured/effective charging limit;
- connector type and electrical capability;
- status timeline rather than only current color.

### Command experience

For reset, unlock, stop, availability, firmware, or diagnostics:

```text
confirm intent and impact
  -> require reason for sensitive action
  -> create operation
  -> show DISPATCHED/PENDING, not success
  -> stream/poll updates
  -> show station response and later observed evidence
  -> retain command timeline and actor
```

Disable only when capability or authorization is known. If state is stale, explain uncertainty instead of pretending the command is safe.

## 4. Incident and Support Timeline

Combine correlated facts without pretending they are one event type:

```text
14:02:01 station disconnected
14:02:15 driver start requested
14:02:15 OCPI command accepted for processing
14:02:45 downstream command timed out
14:03:10 station reconnected
14:03:12 transaction start observed
14:03:13 session projection updated
```

Each item should show source, timestamp, correlation, confidence/finality, and safe payload details. Redact credentials and secrets.

## 5. eMSP Driver Experience

Core journey:

```text
map/search
  -> location detail
  -> compatible EVSE/connector
  -> transparent tariff and restrictions
  -> select credential/payment method
  -> request start
  -> track operation
  -> active session with freshness
  -> request stop
  -> stopped/provisional summary
  -> settled receipt/correction
```

Never present “charging” solely because a start command was accepted. Distinguish:

```text
Requesting start
Waiting for station
Charging started
Connected but not delivering energy
Stopping
Stopped; final price pending
Settled
Failed or outcome unknown
```

Vendor/application labels can differ, but they must map to truthful backend facts.

## 6. Map and Location Search

- cluster large datasets server-side or through an appropriate geospatial service;
- query by viewport and zoom, not the entire network;
- include data freshness and status aggregation rules;
- distinguish temporarily unavailable from unsupported/incompatible;
- filter by connector, power, access, payment, operator, availability, and vehicle compatibility where reliable;
- avoid displaying a price without currency, tax context, unit, restrictions, and source freshness;
- deep-link reliably from map result to Location/EVSE/Connector identity;
- cache static data longer than dynamic status;
- support accessible non-map list search.

## 7. Web Application Guidance

Use the repository's existing framework. For React/Next.js or similar:

- keep authorization enforcement on the server/API; UI permission checks are only presentation;
- use server rendering for stable initial data where beneficial, then subscribe for live state;
- normalize query/cache keys by tenant and resource identity;
- reconcile real-time events by version, not arrival order;
- virtualize large station/session tables;
- put filter/sort/pagination state in the URL for operator workflows;
- use optimistic UI only for reversible local state, not uncertain physical commands;
- provide keyboard navigation, visible focus, semantic tables, labels, and non-color status indicators;
- show UTC/source timestamp and localized display time where operationally useful;
- preserve correlation IDs in support links and error details without exposing secrets.

## 8. C# Web and Cross-Platform Client Guidance

When the existing product uses C#, support ASP.NET Core/Blazor for web and .NET MAUI for iOS/Android rather than forcing a TypeScript or fully native rewrite.

For Blazor:

- enforce authorization in the backend; component visibility is not security;
- use typed API clients and explicit DTO/domain mapping;
- scope cached state by tenant/account and dispose subscriptions correctly;
- reconnect SignalR or other real-time channels and refetch versioned projections;
- avoid blocking rendering/UI synchronization contexts with protocol or database work;
- virtualize large supervision tables and preserve filters in navigable URLs where possible;
- test prerendering/hydration or WebAssembly connectivity according to the hosting model.

For .NET MAUI:

- separate pages/view models, domain use cases, networking, secure storage, persistence, and notifications;
- use async/cancellation through network and lifecycle paths;
- store credentials with platform secure storage, not plain preferences;
- persist operation IDs and recover after suspension or process termination;
- treat push notifications as hints and refetch authoritative session/operation state;
- keep platform-specific maps, background execution, deep links, and notification behavior behind tested interfaces;
- verify behavior separately on physical iOS and Android devices;
- support VoiceOver/TalkBack, dynamic text, contrast, touch targets, and reduced motion;
- do not assume one shared implementation means identical platform lifecycle behavior.

Shared C# clients must still follow the same truthful command, freshness, settlement, and offline-recovery rules as native clients.

## 9. Native iOS Guidance

Use Swift and SwiftUI unless the project dictates otherwise.

Recommended boundaries:

```text
App/UI
Features
Domain
Networking
Persistence
Notifications
DesignSystem
```

Practices:

- use structured concurrency and cancellation for network operations;
- keep `Codable` API DTOs separate from durable/domain models where evolution differs;
- store tokens in Keychain, never plain preferences;
- use background push notifications as hints, then refetch authoritative state;
- persist active operation/session summaries for app restart and poor connectivity;
- design start/stop as resumable operation screens;
- support deep links from notifications to operation/session/location;
- use MapKit responsibly with clustered annotations and accessible list fallback;
- format energy, power, money, duration, and dates with locale-aware formatters;
- support VoiceOver, Dynamic Type, contrast, reduced motion, and sufficiently large controls;
- never perform silent repeated start/stop retries from the device.

## 10. Native Android Guidance

Use Kotlin and Jetpack Compose unless the project dictates otherwise.

Recommended boundaries:

```text
app/ui
feature
core/domain
core/network
core/database
core/designsystem
core/notifications
```

Practices:

- use coroutines with structured concurrency and lifecycle-aware collection;
- expose immutable UI state from ViewModels;
- keep serialization DTOs separate from domain/database models;
- store secrets with platform-backed secure storage;
- use Room/DataStore according to sensitivity and data shape;
- use WorkManager only for deferrable, recoverable background synchronization—not immediate physical-command guarantees;
- treat FCM as a notification/hint and refetch authoritative state;
- persist operation IDs and recover active screens after process death;
- use Maps Compose or project conventions with clustering and list fallback;
- format units, currency, dates, and durations by locale;
- support TalkBack, scalable text, contrast, touch targets, and reduced motion;
- never tie command success to the lifetime of one Activity or ViewModel.

## 11. Shared or Cross-Platform Clients

If using .NET MAUI, Kotlin Multiplatform, Compose Multiplatform, React Native, Flutter, or another shared stack:

- share deterministic domain logic and API contracts where valuable;
- keep platform security, notifications, maps, background execution, and accessibility native-aware;
- do not choose a shared framework solely to maximize code reuse;
- test process death, background restrictions, deep links, and notification delivery separately per platform;
- retain one source of truth for operation/session state while allowing platform-specific presentation.

## 12. Client API Contracts

Prefer intent-oriented resources:

```text
LocationSummary
LocationDetail
EVSEAvailability
ChargingQuote or TariffDisplay
ChargingOperation
ActiveSession
SessionReceipt
StationSupervision
IncidentTimeline
IntegrationHealth
```

For live resources include:

```text
id
state
stateVersion or updatedAt
observedAt
isStale / freshness policy
capabilities
allowedActions
correlation/support reference
```

The server, not the client, decides tenant authorization, protocol mappings, tariff truth, and whether a command may be sent.

## 13. Offline and Recovery UX

Web/mobile connectivity and station connectivity are independent.

Explain which link is unavailable:

```text
Your device is offline
Platform cannot reach partner
Station is disconnected
Status is stale
Command outcome is unknown
Final billing is pending
```

Recovery rules:

- persist operation IDs before navigating away;
- on reconnect, fetch operation/session by ID;
- do not automatically create a second start operation;
- deduplicate notification and socket updates;
- show last known state with time and stale indication;
- provide safe support/escalation when physical outcome is unknown.

## 14. Frontend Testing

### Unit

- state reducers/view models;
- units, money, date, and duration formatting;
- capability and permission presentation;
- event version ordering;
- provisional/settled/corrected receipt rendering.

### Integration

- start/stop operation polling and push updates;
- reconnect and missed-event recovery;
- tenant/account switching and cache isolation;
- deep links and push notifications;
- map/list filtering and pagination;
- command confirmation and audit reason.

### End-to-end

```text
sign in
  -> find location
  -> inspect tariff
  -> request start
  -> receive async start evidence
  -> view active metering
  -> stop
  -> view provisional summary
  -> receive settlement
  -> receive corrected settlement
```

Also test offline device, offline station, duplicate tap, late callback, expired authentication, inaccessible resource, and process/browser restart.

## 15. UX Quality Gate

```text
[ ] UI language distinguishes requests, acknowledgements, observations, and settlement
[ ] Every live status shows or accounts for freshness
[ ] Commands expose pending and unknown outcomes
[ ] Permissions are enforced server-side and reflected client-side
[ ] Maps have scalable queries and accessible list alternatives
[ ] Money, units, dates, and durations are locale-safe
[ ] Web subscriptions recover missed events
[ ] iOS recovers after suspension/termination
[ ] Android recovers after process death/background limits
[ ] Push notifications trigger authoritative refetch
[ ] Sensitive identifiers and payloads are redacted
[ ] Operator timelines preserve source and correlation
[ ] Driver receipts distinguish provisional, settled, and corrected values
```
