#!/usr/bin/env python3
"""Вариант 3: отклоняем .py-файлы, в которых строки начинаются с табуляции.

Запуск:  python ci/check_tabs.py [каталог]
Код возврата 1 — табы найдены, конвейер обязан упасть.
"""

from __future__ import annotations

import pathlib
import sys

SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "dist", ".pytest_cache"}


def python_files(root: pathlib.Path):
    for path in sorted(root.rglob("*.py")):
        if SKIP_DIRS.intersection(path.parts):
            continue
        yield path


def find_leading_tabs(path: pathlib.Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"{path}: не удалось прочитать ({exc})"]
    return [
        f"{path}:{num}"
        for num, line in enumerate(text.splitlines(), start=1)
        if line.startswith("\t")
    ]


def main(argv: list[str]) -> int:
    root = pathlib.Path(argv[1] if len(argv) > 1 else ".")
    problems: list[str] = []
    checked = 0

    for path in python_files(root):
        checked += 1
        problems.extend(find_leading_tabs(path))

    print(f"Проверено .py-файлов: {checked}")
    if problems:
        print("ОШИБКА: найдена табуляция в начале строк (нужны пробелы, PEP 8):")
        for item in problems:
            file, _, line = item.partition(":")
            print(f"::error file={file},line={line}::{item}")
        return 1

    print("OK: ведущих табов нет")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))