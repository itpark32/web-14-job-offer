"""Verify every published Web-handbook URL used in docs (requires network)."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import time
from urllib.parse import unquote, urlsplit

import requests

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "https://itpark32.github.io/web-14-metodichka/"


class Document(HTMLParser):
    def __init__(self, source: str):
        super().__init__()
        self.in_h1 = False
        self.heading: list[str] = []
        self.ids: set[str] = set()
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.in_h1 = self.in_h1 or tag == "h1"
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])

    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_h1 = False

    def handle_data(self, data):
        if self.in_h1:
            self.heading.append(data)


def check(url: str) -> tuple[str, str | None]:
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            if not response.url.startswith(PREFIX):
                raise ValueError(f"Unexpected redirect: {response.url}")
            doc = Document(response.text)
            heading = " ".join("".join(doc.heading).split()).replace("¶", "").strip()
            if not heading or "404" in heading:
                raise ValueError(f"Missing article or soft 404: {heading!r}")
            if "/interview/" in url and not any(word in heading.lower() for word in ("интервью", "собеседован")):
                raise ValueError(f"Unexpected interview article: {heading!r}")
            fragment = unquote(urlsplit(url).fragment)
            if fragment and fragment not in doc.ids:
                raise ValueError(f"Missing anchor: {fragment}")
            return f"OK {response.status_code} {url} — {heading}", None
        except (requests.RequestException, ValueError) as exc:
            if attempt < 2:
                time.sleep(attempt + 1)
            else:
                return url, str(exc)
    raise AssertionError("Unreachable")


def main() -> int:
    urls = set()
    for path in (ROOT / "docs").rglob("*.md"):
        urls.update(re.findall(re.escape(PREFIX) + r'[^\s)<>\]"`]*', path.read_text(encoding="utf-8")))
    if not urls:
        print("ERROR: no technical handbook links found", file=sys.stderr)
        return 1
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(check, sorted(urls)))
    errors = 0
    for label, error in results:
        if error:
            print(f"ERROR {label}: {error}", file=sys.stderr)
            errors += 1
        else:
            print(label)
    print(f"Checked {len(urls)} unique technical handbook URLs; errors: {errors}.")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
