---
name: url-to-obsidian
description: Capture one or more URLs into Obsidian notes. Use this when the user wants to save a URL, paste text containing URLs, or turn WeChat/GitHub/X/general web pages into Obsidian notes.
---

# URL to Obsidian

Capture one or more URLs from the user's real Chrome session and save them as Obsidian notes.

## First Use

Before running the skill, create `url_to_obsidian.env` from `url_to_obsidian.env.example` and set:

- `URL_TO_OBSIDIAN_TARGET_DIR` to an absolute Obsidian path

## Recommended Workflow

### Agent-assisted mode

1. Run export-only capture:
   - `URL_TO_OBSIDIAN_SKIP_GENERATE=1 ./scripts/url_to_obsidian.sh "<user input>"`
2. Read the exported JSON from:
   - `URL_TO_OBSIDIAN_SOURCE_JSON`
   - default: `~/.dev-browser/tmp/url-to-obsidian-export.json`
3. Generate better `title`, `summary`, and `tags` in the current agent session.
4. Write overrides to:
   - `URL_TO_OBSIDIAN_LLM_OVERRIDES_FILE`
   - default: `~/.dev-browser/tmp/url-to-obsidian-llm-overrides.json`
5. Follow the JSON shape from:
   - [`url_to_obsidian_llm_overrides.example.json`](url_to_obsidian_llm_overrides.example.json)
6. Generate final notes:
   - `python3 scripts/generate_url_obsidian_notes.py`

### Standalone shell mode

- `./scripts/url_to_obsidian.sh "<user input>"`

If LLM participation is enabled, this requires the local `codex` CLI.

## Input Handling

- Accepts a direct URL
- Accepts pasted text containing one or more URLs
- Accepts piped text from stdin
- Extracts unique `http://` and `https://` URLs in appearance order

## Supported Sources

- WeChat articles
- GitHub repositories, issues, pull requests, discussions, and README pages
- X / Twitter posts
- General web pages available in the user's current Chrome session

## Output

- One note per captured URL under `URL_TO_OBSIDIAN_TARGET_DIR`
- `000 - URL 采集索引.md`
- `.url_to_obsidian_state.json`

