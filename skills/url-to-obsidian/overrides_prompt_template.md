# URL Overrides Prompt Template

Use this after running:

`python3 scripts/url_to_obsidian.py export "<user input>"`

## Goal

Read the current URL export JSON, then write a compact overrides JSON for the current exported items only.

## Inputs

- Export JSON: `URL_TO_OBSIDIAN_SOURCE_JSON`
  Default: `~/.dev-browser/tmp/url-to-obsidian-export.json`
- Overrides JSON to write: `URL_TO_OBSIDIAN_LLM_OVERRIDES_FILE`
  Default: `~/.dev-browser/tmp/url-to-obsidian-llm-overrides.json`
- Existing overrides file: optional, reuse it if it already exists
- Example shape: [`url_to_obsidian_llm_overrides.example.json`](url_to_obsidian_llm_overrides.example.json)

## Required Output Shape

```json
{
  "entries": {
    "https://example.com/article": {
      "title": "...",
      "summary": ["...", "..."],
      "tags": ["url-to-obsidian", "..."]
    }
  }
}
```

## Rules

- Keep exactly one entry per exported item key.
- Use `item.key` when present, otherwise fall back to `finalUrl` or `requestedUrl`.
- Reuse existing overrides when they are still good.
- Only add or update entries that appear in the current export JSON.
- Remove stale override entries that are not in the current export JSON.
- `title`: short, concrete, and better than the raw page title when possible.
- `summary`: 1 to 3 plain strings, no markdown bullets in the strings.
- `tags`: 2 to 6 short tags, lowercase preferred, no `#` prefix.
- Do not invent claims that are not supported by the page metadata, excerpt, or error field.
- If extraction failed, summarize the failure plainly instead of pretending the page content was captured.
- Prefer tags that reflect source type, topic, and use case.

## Suggested Process

1. Read the export JSON.
2. Build the set of current item keys.
3. Read existing overrides JSON if present.
4. For each current item, keep or improve `title`, `summary`, and `tags`.
5. Write back a full JSON object with top-level `entries`.

## Ready-to-Use Prompt

```text
Read URL_TO_OBSIDIAN_SOURCE_JSON and URL_TO_OBSIDIAN_LLM_OVERRIDES_FILE if it already exists. Create a fresh overrides JSON object with top-level key "entries". Keep exactly one entry per current exported item key. Use item.key when present, otherwise use finalUrl or requestedUrl. Remove stale entries that are no longer in the current export.

For each current item, write:
- title: concise and higher-signal
- summary: 1-3 plain strings, no bullet markers inside the strings
- tags: 2-6 short tags, no # prefix

Do not invent unsupported claims. If a page has an error, reflect that honestly. Reuse good existing overrides when possible. Then write the final JSON to URL_TO_OBSIDIAN_LLM_OVERRIDES_FILE.
```
