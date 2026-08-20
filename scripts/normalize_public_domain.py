#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

DOCS = Path("docs")
OLD_BASE = "https://raporipo.github.io/ai-value-exploration-notes/"
NEW_BASE = "https://fuminose.com/ai-value-exploration-notes/"
TEXT_SUFFIXES = {".html", ".txt", ".xml"}


def normalize_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    updated = text.replace(OLD_BASE, NEW_BASE)
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    files = sorted(
        path
        for path in DOCS.rglob("*")
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES
    )
    changed = sum(normalize_file(path) for path in files)
    print(f"Normalized public domain in {len(files)} text files; {changed} files changed")


if __name__ == "__main__":
    main()
