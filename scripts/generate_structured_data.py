#!/usr/bin/env python3

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import json
import re

DOCS = Path("docs")
BASE_URL = "https://raporipo.github.io/ai-value-exploration-notes/"
SITE_NAME = "AI Value Exploration Notes"
SITE_ID = BASE_URL + "#website"
AUTHOR_ID = BASE_URL + "about/#author"
AUTHOR_URL = BASE_URL + "about/"

STRUCTURED_DATA_RE = re.compile(
    r'<script\s+id=["\']structured-data["\']\s+type=["\']application/ld\+json["\']>.*?</script>\s*',
    re.IGNORECASE | re.DOTALL,
)
DATE_RE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")

SECTION_LABELS = {
    "about": "About",
    "core": "Core",
    "explorations": "Explorations",
    "glossary": "Glossary",
    "practice": "Practice",
    "questions": "Questions",
    "theses": "Theses",
}


class PageMetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.title_parts: list[str] = []
        self.h1_parts: list[str] = []
        self.meta_parts: list[str] = []
        self.description = ""
        self.canonical = ""
        self._in_title = False
        self._in_h1 = False
        self._captured_h1 = False
        self._in_page_meta = False
        self._captured_page_meta = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        tag = tag.lower()

        if tag == "html":
            self.lang = values.get("lang") or self.lang
        elif tag == "title":
            self._in_title = True
        elif tag == "h1" and not self._captured_h1:
            self._in_h1 = True
        elif tag == "meta" and (values.get("name") or "").lower() == "description":
            self.description = values.get("content") or ""
        elif tag == "link":
            rel = (values.get("rel") or "").lower().split()
            if "canonical" in rel:
                self.canonical = values.get("href") or ""

        classes = (values.get("class") or "").split()
        if "meta" in classes and not self._captured_page_meta:
            self._in_page_meta = True

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        elif tag == "h1" and self._in_h1:
            self._in_h1 = False
            self._captured_h1 = True
        elif self._in_page_meta:
            self._in_page_meta = False
            self._captured_page_meta = True

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)
        if self._in_h1:
            self.h1_parts.append(data)
        if self._in_page_meta:
            self.meta_parts.append(data)

    @property
    def title(self) -> str:
        return " ".join("".join(self.title_parts).split())

    @property
    def h1(self) -> str:
        return " ".join("".join(self.h1_parts).split())

    @property
    def modified_date(self) -> str | None:
        text = " ".join("".join(self.meta_parts).split())
        match = DATE_RE.search(text)
        return match.group(0) if match else None


def localized_segments(page: Path) -> tuple[str, list[str]]:
    parts = list(page.relative_to(DOCS).parts[:-1])
    if parts and parts[0] == "en":
        return "en", parts[1:]
    return "ja", parts


def is_article(segments: list[str]) -> bool:
    if segments in (["core"], ["practice"]):
        return True
    return len(segments) == 2 and segments[0] in {"theses", "explorations"}


def page_type(segments: list[str]) -> str:
    if segments == ["about"]:
        return "AboutPage"
    if len(segments) == 1 and segments[0] in {
        "theses",
        "explorations",
        "questions",
        "glossary",
    }:
        return "CollectionPage"
    return "WebPage"


def breadcrumb_items(lang: str, segments: list[str], current_name: str) -> list[dict]:
    if not segments:
        return []

    home_url = BASE_URL + ("en/" if lang == "en" else "")
    items = [
        {
            "@type": "ListItem",
            "position": 1,
            "name": SITE_NAME,
            "item": home_url,
        }
    ]

    accumulated: list[str] = []
    for index, segment in enumerate(segments, start=2):
        accumulated.append(segment)
        item_url = home_url + "/".join(accumulated) + "/"
        item_name = current_name if segment == segments[-1] else SECTION_LABELS.get(segment, segment)
        items.append(
            {
                "@type": "ListItem",
                "position": index,
                "name": item_name,
                "item": item_url,
            }
        )

    return items


def build_graph(page: Path, meta: PageMetadataParser) -> dict:
    lang, segments = localized_segments(page)
    canonical = meta.canonical.strip()
    name = meta.h1 or meta.title or SITE_NAME
    description = meta.description.strip()

    if not canonical:
        raise ValueError(f"Missing canonical URL: {page}")

    webpage_id = canonical + "#webpage"
    graph: list[dict] = []

    if not segments and lang == "ja":
        graph.append(
            {
                "@type": "WebSite",
                "@id": SITE_ID,
                "url": BASE_URL,
                "name": SITE_NAME,
            }
        )

    webpage: dict = {
        "@type": page_type(segments),
        "@id": webpage_id,
        "url": canonical,
        "name": name,
        "inLanguage": lang,
        "isPartOf": {"@id": SITE_ID},
    }
    if description:
        webpage["description"] = description

    breadcrumbs = breadcrumb_items(lang, segments, name)
    if breadcrumbs:
        breadcrumb_id = canonical + "#breadcrumb"
        webpage["breadcrumb"] = {"@id": breadcrumb_id}
        graph.append(
            {
                "@type": "BreadcrumbList",
                "@id": breadcrumb_id,
                "itemListElement": breadcrumbs,
            }
        )

    if is_article(segments):
        article_id = canonical + "#article"
        webpage["mainEntity"] = {"@id": article_id}

        article: dict = {
            "@type": "Article",
            "@id": article_id,
            "headline": name,
            "url": canonical,
            "mainEntityOfPage": {"@id": webpage_id},
            "inLanguage": lang,
            "author": {
                "@type": "Person",
                "@id": AUTHOR_ID,
                "name": "raporipo",
                "url": AUTHOR_URL,
            },
        }
        if description:
            article["description"] = description
        if meta.modified_date:
            article["dateModified"] = meta.modified_date
        graph.append(article)

    insert_at = 1 if graph and graph[0].get("@type") == "WebSite" else 0
    graph.insert(insert_at, webpage)

    return {"@context": "https://schema.org", "@graph": graph}


def render_block(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    payload = payload.replace("</", "<\\/")
    return f'<script id="structured-data" type="application/ld+json">\n{payload}\n</script>\n'


def update_page(page: Path) -> bool:
    text = page.read_text(encoding="utf-8")
    clean = STRUCTURED_DATA_RE.sub("", text)

    parser = PageMetadataParser()
    parser.feed(clean)
    block = render_block(build_graph(page, parser))

    match = re.search(r"</head>", clean, re.IGNORECASE)
    if match is None:
        raise ValueError(f"Missing </head>: {page}")

    updated = clean[: match.start()] + block + clean[match.start() :]

    if updated == text:
        return False

    page.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    pages = sorted(DOCS.rglob("index.html"))
    changed = 0
    articles = 0

    for page in pages:
        _, segments = localized_segments(page)
        articles += int(is_article(segments))
        changed += int(update_page(page))

    print(
        f"Structured data processed for {len(pages)} pages "
        f"({articles} Article pages); {changed} files changed"
    )


if __name__ == "__main__":
    main()
