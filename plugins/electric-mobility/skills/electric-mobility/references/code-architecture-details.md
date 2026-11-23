# Code architecture details

Extends [code-architecture.md](code-architecture.md). Read only the section you need.

## Data rules

- **Internal IDs are separate from protocol IDs.** Store both, with partner and tenant scope.
- **Tenant first in keys and indexes** wherever it fits.
- **Copy facts that must not change:** tariff, location, and identity details on a session or CDR.
- **Append, do not overwrite:** events, audit, meter values, and corrections.
- **Soft-delete anything history refers to.** Anonymize people instead of deleting financial records.
- **Exact types only:** decimal or minor units for money, explicit units for energy and power, UTC instants
  for time.
- **Inject the clock** everywhere, so that time-based logic can be tested.
- **Evolve the schema through migrations**, in backward-compatible steps, so that old and new instances can
  run side by side during a rollout.
- **Each module owns its tables.** Other modules use its public interface, not a join into its tables.

## Client applications

Web and mobile apps follow the same principle. The backend owns truth, and clients display it.

```text
screen -> view model or state holder -> use case -> repository -> API client
```

- Organize by feature, with no business logic in screens or route files.
- No charging decisions on the client: it shows the evidence-based state the backend reports.
- Keep generated API contracts in one place, and map to view models.
- Secure storage, network access, and platform services sit behind interfaces.
- Handle suspension, process death, and network loss: refetch truth on return, and never assume the session
  continued as expected.

## Growing the system

Change one thing at a time, when a measurement requires it.

1. **Single instance:** an in-process socket map and a database-backed command queue.
2. **Several instances:** each station's socket lives on one instance, and that instance claims that
   station's queued commands. No sticky routing is needed for the queue itself.
3. **Separate connection tier:** when socket load needs independent scaling or deployments must not drop
   connections. Add a connection registry at this point.
4. **Read replicas and analytics store:** for statistics that are slowing down the main database.
5. **Time-series storage:** for meter data when its volume measurably hurts.
6. **Extract services:** only for the reasons listed at the top of this guide.

Plan for reconnect storms at every stage: a restart reconnects the entire fleet at once. Stagger shutdowns,
limit handshake concurrency, and load-test it.

## Testing by layer

| Layer | Test with | What to prove |
|---|---|---|
| Domain | Plain unit tests, property tests | Every legal and illegal transition, price calculations, rounding |
| Application | Fake ports | Permission, tenant isolation, idempotency |
| Adapters | Real serialization fixtures from the specification | Wire contract, version differences, malformed input |
| Infrastructure | The real database engine and real locks | Migrations, concurrency, constraints |
| End to end | Station, partner, and provider simulators | Full flows, restart, reconnect, late messages |
| Architecture | Boundary rules in CI | Dependency direction, no domain imports of frameworks |

Inject failures: crash between commit and send, a duplicate event, a reply after timeout, and a partner outage.

## Record decisions

Write a short decision record for choices that are expensive to reverse: a split, a database, a protocol
version, a payment model, or a trust boundary.

```text
Decision:      What we chose
Context:       The problem, with numbers where possible
Options:       What else we considered, and why not
Consequences:  What this makes harder, and the security impact
Revisit when:  The condition that would change this
```

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| One `status` column | Connected, available, authorized, and charging change independently | One state dimension per fact |
| Controller calling a repository | Logic and permission checks scatter | A use case between them |
| ORM entity as the API or protocol response | Leaks fields, and couples the wire format to the schema | Explicit DTOs and mappers |
| Remote call in a transaction | Locks held while waiting, and failures can't be undone | Outbox, then send after commit |
| Returning `success: true` after sending a command | Accepted is not done | An operation ID and observed state |
| `if vendor == X` throughout the core | Every new station adds risk everywhere | A vendor adapter layer |
| Universal DTO across versions | Wrong fields in the wrong version | Per-version DTOs |
| A `utils` or `common` dumping ground | Hidden coupling | Move it to its owner |
| Tenant passed from the client | Cross-tenant access | Tenant from the principal |
| Microservices on day one | Distributed transactions with no scaling need | A modular monolith |
| A broker with no measured need | More failure modes and operations | A database-backed queue first |
| A class and interface for every function | Noise, and Java style forced on other languages | Ports only at real boundaries |

