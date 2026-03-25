#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def env_path(name: str, default: str) -> Path:
    return Path(os.environ.get(name, default)).expanduser()


def first_env(*names: str, default: str) -> str:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return default


REPO_DIR = Path(__file__).resolve().parents[1]
SOURCE_JSON = Path(
    first_env(
        "URL_TO_OBSIDIAN_SOURCE_JSON",
        default="~/.dev-browser/tmp/url-to-obsidian-export.json",
    )
).expanduser()
OVERRIDES_FILE = Path(
    first_env(
        "URL_TO_OBSIDIAN_LLM_OVERRIDES_FILE",
        default="~/.dev-browser/tmp/url-to-obsidian-llm-overrides.json",
    )
).expanduser()
MODEL = first_env("URL_TO_OBSIDIAN_LLM_MODEL", default="gpt-5.4").strip() or "gpt-5.4"
BATCH_SIZE = max(1, int(first_env("URL_TO_OBSIDIAN_LLM_BATCH_SIZE", default="8")))
RETRIES = max(0, int(first_env("URL_TO_OBSIDIAN_LLM_RETRIES", default="2")))
RESUME = first_env("URL_TO_OBSIDIAN_LLM_RESUME", default="1") == "1"

SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": ["items"],
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["key", "title", "summary", "tags"],
                "properties": {
                    "key": {"type": "string"},
                    "title": {"type": "string"},
                    "summary": {
                        "type": "array",
                        "minItems": 2,
                        "maxItems": 4,
                        "items": {"type": "string"},
                    },
                    "tags": {
                        "type": "array",
                        "minItems": 2,
                        "maxItems": 6,
                        "items": {"type": "string"},
                    },
                },
            },
        }
    },
}

PROMPT_PREFIX = """You are organizing captured URLs into Obsidian notes.
The input items may come from WeChat articles, GitHub pages, X posts, or general web pages.
For each item, produce a better title, summary, and tags.

Requirements:
1. Return one output item for every input item, preserving the exact key.
2. Title must be concise Chinese, filename-friendly, and should highlight the core idea, project, article, or discussion.
3. Summary must contain 2 to 4 Chinese bullet-style sentences with concrete signal, not boilerplate.
4. Tags must contain 2 to 6 lowercase short labels in English or pinyin kebab-case.
5. Make the source type useful when relevant, but do not redundantly repeat brand names in every title.
6. Do not invent facts. If the page is thin, summarize conservatively.
7. When the page is a tool, repo, tutorial, or workflow, make the practical value explicit.
8. Output must strictly match the schema.

Input item JSON list:
"""


def compact_item(item: dict) -> dict:
    return {
        "key": item.get("key") or item.get("finalUrl") or item.get("requestedUrl", ""),
        "source_type": item.get("sourceType", "web"),
        "requested_url": item.get("requestedUrl", ""),
        "final_url": item.get("finalUrl", ""),
        "title": item.get("title", ""),
        "meta_title": item.get("metaTitle", ""),
        "meta_description": item.get("metaDescription", ""),
        "site_name": item.get("siteName", ""),
        "published_time": item.get("publishedTime", ""),
        "headings": item.get("headings") or [],
        "excerpt": item.get("excerpt", ""),
        "links": item.get("links") or [],
        "error": item.get("error", ""),
    }


def load_items() -> list[dict]:
    source_file = SOURCE_JSON
    data = json.loads(source_file.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise RuntimeError(f"Expected a list in {source_file}")
    return data


def load_existing_entries() -> dict:
    if not RESUME or not OVERRIDES_FILE.exists():
        return {}
    try:
        data = json.loads(OVERRIDES_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}
    entries = data.get("entries", data)
    return entries if isinstance(entries, dict) else {}


def run_batch(batch_items: list[dict], batch_index: int, total_batches: int, tmpdir: Path) -> list[dict]:
    schema_path = tmpdir / "schema.json"
    output_path = tmpdir / f"output-{batch_index:03d}.json"
    schema_path.write_text(json.dumps(SCHEMA, ensure_ascii=False), encoding="utf-8")

    payload = [compact_item(item) for item in batch_items]
    prompt = PROMPT_PREFIX + json.dumps(payload, ensure_ascii=False)
    expected_keys = [item.get("key") or item.get("finalUrl") or item.get("requestedUrl", "") for item in batch_items]

    cmd = [
        "codex",
        "exec",
        "--ephemeral",
        "--skip-git-repo-check",
        "--color",
        "never",
        "-m",
        MODEL,
        "--output-schema",
        str(schema_path),
        "-C",
        str(REPO_DIR),
        "-o",
        str(output_path),
        "-",
    ]

    for attempt in range(1, RETRIES + 2):
        started = time.time()
        proc = subprocess.run(
            cmd,
            input=prompt,
            text=True,
            capture_output=True,
            timeout=900,
        )
        elapsed = time.time() - started
        if proc.returncode == 0 and output_path.exists():
            try:
                data = json.loads(output_path.read_text(encoding="utf-8"))
                items = data["items"]
                keys = [item["key"] for item in items]
                if sorted(keys) != sorted(expected_keys):
                    raise RuntimeError("returned keys did not match input keys")
                print(f"batch {batch_index + 1}/{total_batches} ok in {elapsed:.1f}s", file=sys.stderr)
                return items
            except Exception as exc:
                error = f"parse/validate failed: {exc}"
        else:
            error = f"command failed rc={proc.returncode}"

        tail = ((proc.stdout or "") + "\n" + (proc.stderr or ""))[-2000:]
        print(f"batch {batch_index + 1}/{total_batches} attempt {attempt} failed: {error}", file=sys.stderr)
        if tail.strip():
            print(tail, file=sys.stderr)
        time.sleep(2)

    raise RuntimeError(f"batch {batch_index + 1} failed after retries")


def main() -> int:
    source_file = SOURCE_JSON
    if not source_file.exists():
        print(f"Missing source JSON: {SOURCE_JSON}", file=sys.stderr)
        return 1

    if shutil.which("codex") is None:
        print(
            "codex CLI is required for standalone shell automation when URL_TO_OBSIDIAN_USE_LLM=1",
            file=sys.stderr,
        )
        return 1

    items = load_items()
    entries = load_existing_entries()
    pending = [item for item in items if (item.get("key") or item.get("finalUrl") or item.get("requestedUrl", "")) not in entries]
    total = len(items)
    OVERRIDES_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not pending:
        print(json.dumps({"count": total, "overrides_file": str(OVERRIDES_FILE)}, ensure_ascii=False))
        return 0

    total_batches = (len(pending) + BATCH_SIZE - 1) // BATCH_SIZE
    with tempfile.TemporaryDirectory(prefix="url-to-obsidian-codex-") as raw_tmpdir:
        tmpdir = Path(raw_tmpdir)
        for batch_index in range(total_batches):
            batch = pending[batch_index * BATCH_SIZE : (batch_index + 1) * BATCH_SIZE]
            result = run_batch(batch, batch_index, total_batches, tmpdir)
            for item in result:
                entries[item["key"]] = {
                    "title": item["title"].strip(),
                    "summary": [line.strip() for line in item["summary"] if line.strip()],
                    "tags": [tag.strip().lstrip("#") for tag in item["tags"] if tag.strip()],
                }
            OVERRIDES_FILE.write_text(
                json.dumps({"entries": entries}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            print(f"checkpoint {len(entries)}/{total} saved to {OVERRIDES_FILE}", file=sys.stderr)

    if len(entries) != total:
        print(f"Expected {total} overrides, got {len(entries)}", file=sys.stderr)
        return 1

    print(json.dumps({"count": total, "overrides_file": str(OVERRIDES_FILE)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
