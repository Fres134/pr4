"""task_app - CI pipeline demo (variant 3)."""

from __future__ import annotations

__version__ = "1.0.0"

TAB_WIDTH = 4

VALID_PRIORITIES = {"low", "medium", "high", "critical"}


def expand_leading_tabs(text: str, width: int = TAB_WIDTH) -> str:
    result = []
    for line in text.splitlines():
        body = line.lstrip("\t")
        tabs = len(line) - len(body)
        result.append(" " * tabs * width + body)
    return "\n".join(result)


def lines_with_leading_tab(text: str) -> list[int]:
    return [
        num
        for num, line in enumerate(text.splitlines(), start=1)
        if line.startswith("\t")
    ]


class Ticket:
    def __init__(self, title: str, priority: str, description: str = ""):
        if priority not in VALID_PRIORITIES:
            raise ValueError(
                f"Unknown priority: {priority}. Valid: {VALID_PRIORITIES}"
            )
        self.title = title
        self.priority = priority
        self.description = description

    def __repr__(self) -> str:
        return f"Ticket({self.title!r}, {self.priority!r})"


def main() -> int:
    print(f"task_app {__version__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())