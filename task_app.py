"""task_app - CI pipeline demo (variant 3)."""

from __future__ import annotations

__version__ = "1.0.0"

TAB_WIDTH = 4


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


def main() -> int:
    print(f"task_app {__version__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())