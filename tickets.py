"""tickets - simple CSV-backed ticket storage (variant 3)."""

from __future__ import annotations

import csv
import os

VALID_PRIORITIES = ("low", "medium", "high", "critical")
DEFAULT_DB = "tickets.csv"
HEADER = ["id", "title", "priority", "description"]


def _validate(priority: str) -> None:
    if priority not in VALID_PRIORITIES:
        raise ValueError(f"Unknown priority: {priority}. Valid: {VALID_PRIORITIES}")


def _next_id(db: str) -> int:
    if not os.path.exists(db):
        return 1
    with open(db, newline="", encoding="utf-8") as f:
        return sum(1 for _ in csv.reader(f))


def create_ticket(title: str, priority: str, description: str = "", db: str = DEFAULT_DB) -> int:
    _validate(priority)
    new = not os.path.exists(db)
    tid = _next_id(db)
    with open(db, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new:
            writer.writerow(HEADER)
        writer.writerow([tid, title, priority, description])
    return tid


def read_ticket(tid: int, db: str = DEFAULT_DB) -> dict:
    with open(db, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if int(row["id"]) == tid:
                return dict(row)
    raise KeyError(f"ticket {tid} not found in {db}")


def list_tickets(db: str = DEFAULT_DB) -> list[dict]:
    if not os.path.exists(db):
        return []
    with open(db, newline="", encoding="utf-8") as f:
        return [dict(r) for r in csv.DictReader(f)]