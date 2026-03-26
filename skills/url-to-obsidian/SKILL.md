---
name: url-to-obsidian
description: Capture one or more URLs into Obsidian notes. Use this when the user wants to save a URL, paste text containing URLs, or turn WeChat/GitHub/X/general web pages into Obsidian notes.
---

# URL to Obsidian

Capture one or more URLs from the user's real Chrome session and save them as Obsidian notes.

## First Use

Before running the skill, create `url_to_obsidian.env` from `url_to_obsidian.env.example` and set:

- `URL_TO_OBSIDIAN_TARGET_DIR` to an absolute Obsidian path

## Workflow

The agent should treat this skill as `export -> current session writes overrides -> generate`.
Do not rely on the scripts to make a second LLM call on their own.

1. Run export-only capture:
   - `python3 scripts/url_to_obsidian.py export "<user input>"`
2. Read the exported JSON from:
   - `URL_TO_OBSIDIAN_SOURCE_JSON`
   - default: `~/.dev-browser/tmp/url-to-obsidian-export.json`
3. In the current agent session, create higher-signal `title`, `summary`, and `tags` for the exported items.
   - Keep one output entry per item key.
   - Reuse existing overrides when the file already exists.
   - Only create or update entries for URLs present in the current export JSON.
4. Write overrides to:
   - `URL_TO_OBSIDIAN_LLM_OVERRIDES_FILE`
   - default: `~/.dev-browser/tmp/url-to-obsidian-llm-overrides.json`
5. Follow the JSON shape from:
   - [`url_to_obsidian_llm_overrides.example.json`](url_to_obsidian_llm_overrides.example.json)
6. Use the prompt template when writing overrides in the current session:
   - [`overrides_prompt_template.md`](overrides_prompt_template.md)
7. Generate final notes:
   - `python3 scripts/url_to_obsidian.py generate`

## Agent Rules

- When the user asks to capture URLs, prefer the full agent-assisted flow instead of calling `python3 scripts/url_to_obsidian.py` in default full mode without overrides.
- The current agent session is responsible for writing the overrides JSON.
- If no overrides are needed, say that explicitly and then run the final generate step.
- Keep summaries concrete and compact; do not add filler.


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
