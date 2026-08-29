# Selecting a deployment mode

Inspect the production directory before selecting a method. Do not treat a remote URL or a directory named `.git` as proof that it is a usable checkout.

| Observed production state | Preferred method | Guardrail |
| --- | --- | --- |
| Valid `HEAD`, expected remote and branch, no unexplained changes | Fetch the approved commit and update the checkout | Inspect the exact SHA and working tree before any reset or clean operation. |
| Valid checkout with intentional local config/data | Deploy application code while excluding persistent paths | Do not overwrite `.env`, databases, uploads, or certificates. |
| No valid `HEAD`, untracked application files, unrelated remote, or hand-copied folder | Targeted incremental upload from the canonical local checkout | Copy only explicitly selected release files after a backup. Do not force Git history onto the directory. |
| Container/image based deployment | Build and publish the approved image, then update only the intended service | Preserve named volumes, secrets, and rollback image references. |
| Static site host or CI/CD provider | Push the intended branch and verify the provider's deployed revision | Confirm the public URL serves the new asset/version, not only that the pipeline finished. |

## Persistent data backup

Before stopping or replacing an application, identify its durable state. For SQLite, stop the writer and back up the database with its `-wal` and `-shm` companions when present. For other systems, use the database's consistent backup method rather than copying active files blindly.

## Minimum acceptance checks

1. The intended service is active.
2. A local health or root endpoint returns its expected status.
3. Protected routes deny unauthenticated access correctly.
4. The public URL returns expected content.
5. The deployed release SHA or file hashes match the intended source.
