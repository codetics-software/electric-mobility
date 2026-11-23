# Operations and deployment

Read this when deploying, scaling, upgrading, or operating a CSMS, CPO, or eMSP backend.
Values below are **recommendations** that worked in production, not protocol rules. Tune
them per fleet and verify them in the target environment.

## Reference topology

```text
            Internet
  browsers / apps      stations (wss://)
         │                  │
  ┌──────▼──────────────────▼──────┐
  │ proxy / load balancer           │  TLS, WebSocket upgrade, client certs
  └──────┬──────────────────┬──────┘
   everything else     /ocpp/*  /ocpi/*
         ▼                  ▼
  ┌─────────────┐    ┌─────────────┐
  │ web front   │───▶│ backend     │  private network only
  └─────────────┘    └──────┬──────┘
                            ▼
                  managed database (private)
```

- Publish only the station and partner paths on the backend. Admin endpoints, health
  details, metrics, and OpenAPI stay private; browsers reach the API through the web
  front's server-side proxy.
- Use a separate host name for stations that use client certificates (security level 3).
  Browsers then never get a certificate prompt, and that host can enforce strict TLS.
- Images carry no secrets, run as a non-root user, and take configuration from the
  environment at start. Build for both amd64 and arm64 when the target may be Arm.
- Size a JVM or similar runtime from the container limits (for example a max-RAM
  percentage and exit on out-of-memory), not from fixed heap flags baked into the image.

## The proxy in front of stations

Station connections are long lived. Most outages at commissioning come from the proxy.

1. Forward the WebSocket upgrade over HTTP/1.1 (`Upgrade`, `Connection`).
2. Idle timeout of at least 600 s, ideally 3600 s, on both the client and upstream side.
   Send WebSocket pings from the server (about every 30 s) so NAT and proxies keep the path.
3. No maximum connection lifetime, or several hours. Every cut is a reconnect storm.
4. Overwrite `X-Forwarded-For`, `X-Forwarded-Proto`, and any client-certificate header
   sent by the client. Never append to a client-supplied value.
5. The backend reads forwarding headers only when the TCP peer is in a configured trusted
   proxy list. Without it, every station shares the proxy's address and its rate limit.
6. Rate-limit connection attempts per source address and per station identity, sized for
   a full-fleet reconnect after a restart.
7. Record every rejected connection of a known station as a station event with the reason
   and no secret. It is the first place to look during commissioning.

## Terminating TLS and client certificates

| Option | When | Rules |
|---|---|---|
| Proxy terminates TLS (levels 1 and 2) | Default | Proxy sets `X-Forwarded-Proto: https`; backend trusts it only from the proxy |
| Proxy verifies client certificates (level 3) | Recommended for level 3 | Proxy verifies the chain itself and forwards the leaf in one header it overwrites |
| TCP passthrough, backend terminates TLS | Only if no proxy can verify | Whole port becomes HTTPS; certificate renewal needs a restart; real client address may be lost |

- **Forbidden modes:** any setting that forwards an unverified client certificate, such
  as passthrough, "optional without CA", or "request" modes. The backend would trust a
  header the attacker wrote.
- The proxy's trust store holds the station CAs and, if the backend signs station
  certificates, its signing CA. When the proxy forwards only the leaf, give the backend
  the intermediates too.
- The backend re-verifies the chain, validity, and binding (common name equals station
  identity, or a pinned fingerprint). Read the certificate header only from the
  certificate-verifying proxy's addresses.
- Encodings differ per proxy (DER Base64, URL-encoded PEM, RFC 9440 colon-wrapped). Parse
  each explicitly and test with the real proxy.

## Scaling

A station has one socket, held in one process's memory. Before adding replicas, solve both:

- **Connection ownership.** Keep a registry of which instance holds each station's current
  connection epoch. Route commands and forced disconnects (disable, delete, credential
  rotation) to that owner, and ignore a late close from an old epoch so a station that
  reconnected elsewhere is not marked offline.
- **Scheduled work.** Smart-charging computation, partner pushes, payment workers, and
  supervision jobs must run once. Use a lease or leader election, or claim rows with locks.

Until both exist, run **one backend replica**, scale it vertically, and deploy with a
"recreate" strategy. The web front is stateless and can scale out. A database-backed
command queue (one outstanding command per station) removes the need for sticky sessions
or a broker at moderate scale. A single VM plus a managed database is often the most
stable and cheapest setup for a few hundred stations. Load-test before quoting capacity.

## Shutdown and upgrades

- On stop, drain in-flight requests (about 20 s per phase), then close each station socket
  with close code 1012 (service restart). Stations reconnect on their own schedule and
  replay queued transaction messages; deduplication must absorb them.
- Give the orchestrator a grace period of at least 40 s. Push the new image before
  replacing the container, and upgrade outside peak hours.
- Apply schema migrations at start only after a backup. Never edit an applied migration.
- A pending command at disconnect is closed as timed out with an unknown outcome. Never
  replay it automatically after the restart.

## Data, secrets, and backups

- PostgreSQL is the safe default. A document database needs real multi-document
  transactions (for example a MongoDB replica set). "Compatible" managed services differ in
  transactions and indexes; validate before supporting them.
- Size the connection pool below the plan's limit, leaving room for admin and backup.
- Keep in the secret manager: database password, bootstrap password (remove after first
  use), payment keys and webhook secret, the application encryption key, CA private keys,
  push and wallet credentials, and partner tokens.
- Back up the **application encryption key** separately from the database. Losing it makes
  encrypted columns unreadable; leaking it with a dump exposes them.
- Daily database backups, point-in-time restore over at least 7 days, an encrypted copy
  outside the account, and a restore drill at least once a quarter.
- Fail to start when a required certificate set is incomplete, expired, does not chain to
  its root, or does not match its key (for example an ISO 15118 CPO sub-CA). Print each
  problem. A half-working PKI is worse than a refused start.

## Health, logs, and alerts

- **Liveness** checks only that the process answers. **Readiness** says it can take
  traffic. Neither should fail on a database failover, or the orchestrator restarts a
  healthy fleet gateway. Report database health to monitoring, not to the liveness probe.
- Structured JSON logs to stdout, without secrets, tokens, or full card or badge numbers.
- Alert on: failed health, container restarts, memory above about 85 %, database storage
  and connections, no OCPP traffic for several minutes, webhook delivery failures, expired
  commands, rejected station connections, partner push failures, and certificates expiring
  within 30 days.

## Outbound dependencies

- Email: port 25 is usually blocked. Use an authenticated relay on 587 with STARTTLS, and
  publish SPF, DKIM, and DMARC for the sender domain.
- Payment webhooks must arrive byte-for-byte: no WAF or proxy may rewrite the body.
- Allow egress only to known hosts: payment provider, OCSP responders, push services,
  partners. Refuse private addresses for outbound URLs unless explicitly configured.

## Release checklist

- [ ] Backend paths published: stations and partners only; admin and docs private.
- [ ] Proxy idle timeout, lifetime, header overwrite, and trusted proxy list verified.
- [ ] Level 3: proxy verifies client certificates; no passthrough of unverified certs.
- [ ] One backend replica, or ownership routing and job leasing are in place.
- [ ] Backup taken, migration reviewed, encryption key backed up separately.
- [ ] Graceful shutdown and 1012 close tested; reconnect storm stays inside rate limits.
- [ ] Probes split; alerts wired; a real station, the real proxy, and payment test mode tried.
