#!/usr/bin/env python3
"""Print a read-only Git release summary without inspecting secret files."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def git(project: Path, *args: str) -> tuple[int, str, str]:
    result = subprocess.run(
        ["git", "-C", str(project), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def value(project: Path, *args: str) -> str | None:
    code, output, _ = git(project, *args)
    return output if code == 0 and output else None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize a local Git project before a website release."
    )
    parser.add_argument("project", nargs="?", default=".", help="local project directory")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    if not project.is_dir():
        print(f"Project directory does not exist: {project}", file=sys.stderr)
        return 2
    if value(project, "rev-parse", "--is-inside-work-tree") != "true":
        print(f"Not a Git working tree: {project}", file=sys.stderr)
        return 2

    _, status, _ = git(project, "status", "--short")
    summary = {
        "project": str(project),
        "branch": value(project, "branch", "--show-current"),
        "commit": value(project, "rev-parse", "HEAD"),
        "subject": value(project, "log", "-1", "--format=%s"),
        "origin": value(project, "remote", "get-url", "origin"),
        "working_tree_clean": not bool(status),
        "changed_paths": status.splitlines() if status else [],
    }

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    print("Website release preflight (read-only)")
    print(f"Project: {summary['project']}")
    print(f"Branch: {summary['branch'] or '(detached or unavailable)'}")
    print(f"Commit: {summary['commit'] or '(unavailable)'}")
    print(f"Latest message: {summary['subject'] or '(unavailable)'}")
    print(f"Origin: {summary['origin'] or '(not configured)'}")
    print(f"Working tree: {'clean' if summary['working_tree_clean'] else 'has changes'}")
    if status:
        print("Changed paths:")
        print(status)
    print("Next: confirm website scope, production SSH alias, service, and persistent data.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
