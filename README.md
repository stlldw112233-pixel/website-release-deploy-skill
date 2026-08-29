# website-release-deploy

A reusable [Codex](https://openai.com/codex/) skill for safely updating a website from a local repository through GitHub to an SSH-managed production server, with data preservation and live verification at every boundary.

## What it does

Publishes the user's intended website changes to GitHub and production with evidence at each stage:

1. **Local release** — inspect `git status`, validate the stack, commit and push the approved branch, record the exact commit SHA.
2. **SSH access** — resolve a stable SSH alias, verify host keys, keep key-only auth.
3. **Production inspection** — read service state, app Git status/SHA, dependencies, persistent-data paths, disk space; then choose the deployment method from evidence.
4. **Safe deploy** — stop single-file database services before backup, create a timestamped recoverable backup, deploy via the chosen method, restart only the intended service.
5. **Live verification** — service active, loopback health, protected API behavior, public URL content, and release SHA/hash match. (HTTP 200 alone is not proof of release.)

The skill is careful about secrets (never committing/printing `.env`, keys, tokens) and about persistent data (databases, uploads, certificates) surviving every deployment.

## Installation

Clone the complete folder so that Codex can use the Skill, deployment references, and read-only preflight helper together:

```powershell
# Windows / typical Codex layout
git clone https://github.com/stlldw112233-pixel/website-release-deploy-skill `
  "$env:USERPROFILE\.codex\skills\website-release-deploy"
```

On Linux/macOS:

```bash
git clone https://github.com/stlldw112233-pixel/website-release-deploy-skill \
  ~/.codex/skills/website-release-deploy
```

Then ask Codex to deploy or update a website (e.g. "发布网站" / "push my site to production") and the skill will be picked up automatically.

## Usage flow

The skill will ask for (only if not discoverable) and then walk through:

- the local project directory and Git branch to publish;
- the public site/domain and the app/subdomain in scope;
- the production SSH alias, app directory, and service name;
- persistent runtime data that must survive deployment.

It ends with a succinct completion report: branch/commit SHA, deployment method, backup location, verification results, and any remaining user-visible check.

## Included resources

- `SKILL.md` — deployment workflow and decision boundaries.
- `scripts/release_preflight.py` — a read-only local Git summary; it never reads `.env` or contacts production.
- `references/release-context.md` — the exact four-item intake template used when a deployment request is missing required details.
- `references/deployment-modes.md` — when to use a normal Git deploy versus a targeted file upload.
- `agents/openai.yaml` — Skill picker metadata and a ready-to-use prompt.

Run the preflight helper from any Git project:

```bash
python /path/to/website-release-deploy/scripts/release_preflight.py .
```

## Requirements

- [GitHub CLI](https://cli.github.com/) (`gh`) authenticated, or equivalent Git access to GitHub
- SSH access to the production server (see the `$remote-server-ops` skill for SSH onboarding)
- Read/write access to the local project repository

## License

MIT
