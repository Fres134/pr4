#!/usr/bin/env python3
"""Smoke test for deploy/test (variant 3: create and read a test ticket)."""

from __future__ import annotations

import datetime
import os
import sys


def main() -> int:
    deploy_dir = sys.argv[1] if len(sys.argv) > 1 else "deploy/test"
    sys.path.insert(0, os.path.abspath(deploy_dir))
    import tickets

    db = os.path.join(deploy_dir, "smoke_tickets.csv")
    if os.path.exists(db):
        os.remove(db)

    lines = [
        "=== deployment report ===",
        f"datetime: {datetime.datetime.now(datetime.timezone.utc).isoformat()}",
        f"commit: {os.environ.get('GITHUB_SHA', 'local')}",
        f"run_id: {os.environ.get('GITHUB_RUN_ID', 'local')}",
        f"environment: {os.environ.get('ENV_NAME', 'test')}",
        f"url: {os.environ.get('ENV_URL', 'http://localhost:8103/test/tickets')}",
        f"deploy_dir: {deploy_dir}",
        "files: " + ", ".join(sorted(os.listdir(deploy_dir))),
    ]

    tid = tickets.create_ticket("Smoke ticket", "low", "created by smoke test", db=db)
    lines.append(f"smoke 1: create ticket -> id={tid} ... OK")

    ticket = tickets.read_ticket(tid, db=db)
    assert ticket["title"] == "Smoke ticket", ticket
    assert ticket["priority"] == "low", ticket
    lines.append(f"smoke 2: read ticket id={tid} -> {ticket} ... OK")

    try:
        tickets.create_ticket("Bad ticket", "unknown", db=db)
        lines.append("smoke 3: invalid priority accepted ... FAIL")
        lines.append("result: FAIL")
        _write("\n".join(lines) + "\n", deploy_dir)
        print("\n".join(lines))
        return 1
    except ValueError:
        lines.append("smoke 3: invalid priority rejected ... OK")

    lines.append("result: PASS")
    report = "\n".join(lines) + "\n"
    _write(report, deploy_dir)
    print(report)
    return 0


def _write(report: str, deploy_dir: str) -> None:
    with open(os.path.join(deploy_dir, "deployment.txt"), "w", encoding="utf-8") as f:
        f.write(report)
    with open("deployment.txt", "w", encoding="utf-8") as f:
        f.write(report)


if __name__ == "__main__":
    sys.exit(main())