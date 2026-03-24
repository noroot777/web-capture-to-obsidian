#!/usr/bin/env python3
import json
import re
import sys
from urllib.parse import urlparse


URL_PATTERN = re.compile(r"https?://[^\s<>'\"`)\]}]+", re.IGNORECASE)
TRAILING_PUNCTUATION = ".,;:!?)]}'\"，。；：！？）】》、"


def normalize_url(raw: str) -> str:
    candidate = raw.strip().strip(TRAILING_PUNCTUATION)
    parsed = urlparse(candidate)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ""
    return candidate


def collect_input() -> str:
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:]).strip()
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    return ""


def main() -> int:
    raw = collect_input()
    if not raw:
        print("[]")
        return 0

    ordered_urls = []
    seen = set()
    for match in URL_PATTERN.findall(raw):
        url = normalize_url(match)
        if url and url not in seen:
            seen.add(url)
            ordered_urls.append(url)

    print(json.dumps(ordered_urls, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
