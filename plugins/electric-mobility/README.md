# Electric Mobility

EV charging software expertise for any language: OCPI roaming up to 2.3.0, field-level
OCPP 1.6, 2.0.1, and 2.1 message cards, CSMS, CPO, and eMSP architecture, tariffs and CDRs,
smart charging, ISO 15118, supervision, driver apps, and deployment. Every task passes a
risk-tiered security gate first.

This plugin contains one skill, `skills/electric-mobility/`, written in plain Markdown. It
adds no hooks, commands, agents, or MCP servers, and it runs no code. The skill loads when a
task mentions EV charging. It starts at `skills/electric-mobility/SKILL.md`, which routes
each task to only the references it needs.

Install in Claude Code:

```text
/plugin install electric-mobility --marketplace codetics-software/electric-mobility
```

Source, full documentation, and security policy:
[github.com/codetics-software/electric-mobility](https://github.com/codetics-software/electric-mobility).
By [Codetics](https://codetics.fr), MIT license. OCPI specifications © EVRoaming Foundation;
OCPP specifications © Open Charge Alliance.
