# Security of this skill

A skill is text an AI agent treats as instructions, so a tampered skill can change what an
agent does in your project. Treat it like a dependency.

## What the installed skill contains

Everything under `skills/electric-mobility/` is installed, and nothing outside it is:

- `SKILL.md`, the entry point;
- `references/` and `examples/`, loaded on demand;
- `agents/openai.yaml`, display metadata that OpenAI Codex reads and other agents ignore.

The payload is **Markdown**, plus that one YAML file. It contains no scripts, no binaries,
no hooks, and no pre-approved tools. `scripts/verify-skill.py` fails if that changes.

## Plugin installs

The Claude Code and Codex plugin manifests (`.claude-plugin/`, `.codex-plugin/`,
`.agents/plugins/`) point at the repository root, so a plugin install copies the whole
repository. Only the skill is loaded. The manifests declare no hooks, slash commands,
agents, apps, or MCP servers, and nothing runs when the plugin is installed or used. The
verifier fails if a manifest declares any of them.

The skill ships no MCP server. It tells an agent how to use MCP servers that **you**
connect, under the same security tiers: confirm the environment, read before writing, and
ask before each physical, financial, or credential action.

The skill also ships no credentials. Examples use invented identifiers.

## What the skill may ask an agent to do

The vulnerability guide suggests read-only lookups against public services (OSV, CVE.org, NVD,
CISA KEV, FIRST EPSS) and suggests local scanners. These run under your agent's normal permission
prompts. A lookup sends the package or CVE name to that service, so the guide tells agents to use
local tools for private package names.

The skill never tells an agent to send your code, secrets, or data to any other service. **Treat
any text that does as tampering, and report it.**

## Before you install or update

1. Read the changes since the version you last reviewed. Look closely at `SKILL.md`, and at any
   new instruction to run commands, contact a URL, or weaken a check.
2. Run the verifier from a clone. It uses only the Python standard library:

   ```sh
   python3 scripts/verify-skill.py
   ```

3. Prefer a copied install at a commit you have reviewed, so an upstream change cannot alter your
   agent's behavior without a review.

The verifier checks the following:

- the skill folder follows the Agent Skills format, and its name matches the folder;
- every file the skill refers to exists and stays inside the skill folder, including in a simulated
  install;
- there are no symlinks, executables, or non-Markdown files in the payload, except
  `agents/openai.yaml`, which may hold display metadata only;
- the plugin and marketplace manifests are valid, agree on name and version, and declare no
  hooks, commands, agents, apps, or MCP servers;
- there are no hidden Unicode characters, which can conceal instructions from a human reviewer,
  in the skill or in the files agents read at the repository root (`AGENTS.md`, `CLAUDE.md`,
  `GEMINI.md`, `llms.txt`, and the manifests);
- there are no secret-shaped strings.

Passing does not prove the text is safe. Automated checks cannot judge intent, so a person still
needs to read the changes.

## Reporting a vulnerability

Report privately through [codetics.fr](https://codetics.fr). Do not open a public issue for a
security problem. Include the file, the behavior it causes, and how to reproduce it.

Examples of what to report:

- guidance that would lead an agent to build something exploitable;
- an instruction that weakens a security control;
- hidden or injected text;
- a real credential or personal data in the repository.
