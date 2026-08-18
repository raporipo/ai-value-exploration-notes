#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import re

DOCS = Path("docs")
FAVICON_BLOCK_RE = re.compile(
    r'<!-- generated-favicon:start -->.*?<!-- generated-favicon:end -->\s*',
    re.IGNORECASE | re.DOTALL,
)

FAVICON_BLOCK = """<!-- generated-favicon:start -->
<link rel="icon" href="/ai-value-exploration-notes/favicon.svg" type="image/svg+xml"/>
<link rel="icon" href="/ai-value-exploration-notes/favicon.ico" sizes="any"/>
<link rel="apple-touch-icon" href="/ai-value-exploration-notes/apple-touch-icon.png"/>
<!-- generated-favicon:end -->
"""


def update_page(page: Path) -> bool:
    text = page.read_text(encoding="utf-8")
    clean = FAVICON_BLOCK_RE.sub("", text)

    match = re.search(r"</head>", clean, re.IGNORECASE)
    if match is None:
        raise ValueError(f"Missing </head>: {page}")

    updated = clean[: match.start()] + FAVICON_BLOCK + clean[match.start() :]
    if updated == text:
        return False

    page.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    pages = sorted(DOCS.rglob("*.html"))
    changed = sum(update_page(page) for page in pages)
    print(f"Favicon metadata processed for {len(pages)} HTML pages; {changed} files changed")


if __name__ == "__main__":
    main()
