---
name: website-release-deploy
description: Safely update a website from a local repository through GitHub and an SSH-managed production server, with data preservation and live verification. Use when the user asks to publish, sync, or update a website; do not use for code-only changes without deployment authorization.
---

# Website release and deployment

Publish the user's intended website changes to GitHub and production with evidence at every boundary: local source, repository, server, application, and public URL.

## Establish the release boundary

Before writing anything, identify or ask for the following only if it cannot be discovered safely:

- canonical local project directory and intended Git branch;
- the public site/domain and which app or subdomain is in scope;
- production SSH alias, application directory, service name, and health endpoint;
- persistent runtime data that must survive deployment (databases, uploads, `.env`, certificates, service configuration).

Do not deploy a similarly named checkout, unrelated subdomain, admin panel, or auxiliary service by assumption. Treat passwords, private keys, API tokens, environment files, database data, and service drop-ins as secrets: do not commit, print, or repeat them.

### Missing information: ask before deploying

If any of the following four inputs is not already available from the user's request or safe local inspection, pause before any Git push, server change, or deployment and ask the user for it. Do not guess or invent values.

1. **Project source** — local project directory and the Git branch to publish.
2. **Website scope** — public domain/URL and the exact app or subdomain to update.
3. **Production connection** — SSH alias (preferred) or the server access details needed to create one, plus the application directory and service name.
4. **Data to preserve** — databases, uploads, `.env`, certificates, and any other runtime files that must not be overwritten.

Use one concise request such as:

> 为了安全上线，请提供或确认：
> 1) 本地项目目录和要发布的 Git 分支；
> 2) 要更新的网站域名/子域名；
> 3) 服务器 SSH 别名（或连接信息）、项目目录和服务名；
> 4) 服务器上需要保留的数据或配置，例如数据库、上传文件和 `.env`。

The user may provide credentials through an approved secret channel if needed. Never ask them to paste secrets into a public repository, source file, or deployment command.

For a reusable intake form, read [references/release-context.md](references/release-context.md). For a local, read-only Git preflight summary, run `python scripts/release_preflight.py <project-directory>`.

## 1. Prepare the local release

1. Inspect `git status --short`, remotes, active branch, and the meaningful diff. Preserve unrelated user changes; stage only the files that belong in this release.
2. Run validation appropriate to the stack: syntax/type checks, tests, build, and a focused local route/API check when relevant. Fix release-blocking issues before deployment.
3. Commit with a clear message and push the approved branch. Record the exact commit SHA and verify the remote branch points to it.

A successful push does not prove production is updated.

## 2. Establish SSH access safely

For an SSH-managed Linux server, read and use `$remote-server-ops` first.

- Resolve or create a stable SSH alias, then use the alias for all normal server operations.
- If the host key changed, first confirm the server identity through the provider console; only then replace the stale known-host entry.
- If password access is needed for recovery, use it only for onboarding/recovery. Never use password injection helpers for routine deployment.
- Before changing `sshd`, back up configuration, run `sshd -t`, reload, and prove a **new** key-authenticated session works.
- Do not leave temporary root/password-login recovery enabled. End with key-only access according to the server's policy.

## 3. Inspect production before choosing a deployment method

Connect through the alias and read, without exposing environment values:

- service state and service unit's working directory;
- app directory, Git status, current SHA, remote, and branch;
- runtime version and dependency state;
- persistent-data paths and available disk space.

Choose the deployment path from evidence.

Read [references/deployment-modes.md](references/deployment-modes.md) before selecting Git checkout, image/container, or targeted incremental deployment.

### Valid production Git checkout

Use the checked-out release commit only when Git has a valid `HEAD`, the expected remote/branch, and a state that can be updated without overwriting user/runtime data. Inspect exact targets before any destructive Git operation. Never reset or clean an unknown production directory.

### Invalid, detached, or hand-copied production checkout

If Git has no valid `HEAD`, site files are untracked, or its remote is unrelated, do **not** force a Git reset just to make deployment convenient. Use a targeted incremental upload from the canonical local checkout instead. Upload only release files; preserve `.env`, databases, uploads, generated user content, certificates, logs, and service configuration unless the user explicitly includes them.

## 4. Safely deploy

1. Put the application into a safe update state. For SQLite or other single-file databases, stop the service before backup/copy and include companion journal/WAL files when present.
2. Create a timestamped, recoverable backup outside the application directory. Report its path.
3. Deploy the release through the chosen method. Install dependencies only when lockfiles or runtime dependencies actually changed.
4. Validate uploaded server-side code before restart when the stack allows it.
5. Start or reload only the intended service. Confirm it is active and inspect recent service logs if it fails.

If validation fails while the service is stopped, prioritize restoring availability from the known-good state or backup. Do not claim the release succeeded.

## 5. Verify the running site

Require all applicable checks:

- service reports active;
- local loopback health/root endpoint returns the expected status;
- a protected API returns the expected unauthenticated response rather than leaking data;
- the public URL returns the expected status and contains release-specific markup or behavior;
- deployed file hashes or the server's release SHA match the pushed release.

HTTP 200, a process being present, or a Git push by itself is not release proof.

## Completion report

Report succinctly:

- GitHub branch and commit SHA;
- deployment method (Git checkout or incremental upload);
- backup location and persistent data preserved;
- service and public verification results;
- any remaining user-visible browser check or precise blocker.

Never include credentials, private service settings, or secret values in the report.
