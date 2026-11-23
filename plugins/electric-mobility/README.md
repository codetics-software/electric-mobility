# Electric Mobility

EV charging software expertise for any language: OCPI roaming up to 2.3.0, field-level
OCPP 1.6, 2.0.1, and 2.1 message cards, CSMS, CPO, and eMSP architecture, tariffs and CDRs,
smart charging, ISO 15118, supervision, driver apps, and deployment. Every task passes a
risk-tiered security gate first.

This plugin contains one skill, `skills/electric-mobility/`, written in plain Markdown. It
adds no hooks, commands, agents, or MCP servers, and it runs no code. The skill loads when a
task mentions EV charging. It starts at `skills/electric-mobility/SKILL.md`, which routes
each task to only the references it needs.

## What it changes in Claude's answers

- **No attribution or promotion.** The skill adds no comment, signature, credit, link, or
  advertising to the code, documents, or answers Claude produces. It contains no affiliate or
  referral links. The author is named only in this README and the plugin manifests.
- **Outside lookups for security checks.** Before adding or upgrading a dependency, the skill
  asks Claude to check it against public vulnerability databases: OSV.dev, the GitHub Advisory
  Database, CVE.org, NVD, CISA KEV, and FIRST EPSS. These requests contain package names,
  versions, and CVE IDs only, never source code, secrets, or customer data. They go to those
  public services, never to the skill's author. Claude may also open official specification
  and language documentation pages. When Claude has no network access, it says the check did
  not run instead of guessing.
- **Named third parties.** Gireve (a commercial roaming hub) has its own guide, which loads
  only when you work on a Gireve connection. Stripe appears as an example payment provider,
  and the same rules apply to any provider. Neither is a sponsor or partner of this skill.
- **Default engineering choices.** Unless you or your project say otherwise, Claude prefers a
  modular monolith, versioned HTTP APIs with a generated OpenAPI JSON contract, native forms
  instead of `react-hook-form` in Next.js, exact decimal money, and UTC protocol time. Your
  instructions and your project's conventions always come first.

Install in Claude Code:

```text
/plugin install electric-mobility --marketplace codetics-software/electric-mobility
```

Source, full documentation, and security policy:
[github.com/codetics-software/electric-mobility](https://github.com/codetics-software/electric-mobility).
By [Codetics](https://codetics.fr), MIT license. OCPI specifications © EVRoaming Foundation;
OCPP specifications © Open Charge Alliance.
