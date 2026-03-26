# X Overrides Prompt Template

Use this after running:

`python3 scripts/x_bookmarks_to_obsidian.py export`

## Goal

Read the current X bookmark export JSON, then write a compact overrides JSON for the current export set only.

## Inputs

- Export JSON: `X_BOOKMARKS_TO_OBSIDIAN_SOURCE_JSON`
  Default: `~/.dev-browser/tmp/x-bookmarks-to-obsidian-export.json`
- Overrides JSON to write: `X_BOOKMARKS_TO_OBSIDIAN_LLM_OVERRIDES_FILE`
  Default: `~/.dev-browser/tmp/x-bookmarks-to-obsidian-llm-overrides.json`
- Existing overrides file: optional, reuse it if it already exists
- Example shape: [`x_bookmarks_to_obsidian_llm_overrides.example.json`](x_bookmarks_to_obsidian_llm_overrides.example.json)

## Required Output Shape

```json
{
  "entries": {
    "https://x.com/.../status/...": {
      "title": "...",
      "summary": ["...", "..."],
      "tags": ["x-bookmarks-to-obsidian", "..."]
    }
  }
}
```

## Rules

- Keep exactly one entry per `statusLink` in the current export JSON.
- Reuse existing overrides when they are still good.
- Only add or update entries that appear in the current export JSON.
- Remove stale override entries that are not in the current export JSON.
- `title`: short, concrete, higher-signal than the raw first line.
- `summary`: 1 to 3 bullets as plain strings, no markdown bullets in the strings.
- `tags`: 2 to 6 short tags, lowercase preferred, no `#` prefix.
- Do not invent claims that are not supported by the exported bookmark text or links.
- Prefer describing the value of the bookmark, not restating filler phrases from the post.
- Keep Chinese output natural when the source is Chinese; keep English when that is clearly better.

## Suggested Process

1. Read the export JSON.
2. Build the set of current `statusLink` keys.
3. Read existing overrides JSON if present.
4. For each current key, keep or improve `title`, `summary`, and `tags`.
5. Write back a full JSON object with top-level `entries`.

## Ready-to-Use Prompt

```text
Read X_BOOKMARKS_TO_OBSIDIAN_SOURCE_JSON and X_BOOKMARKS_TO_OBSIDIAN_LLM_OVERRIDES_FILE if it already exists. Create a fresh overrides JSON object with top-level key "entries". Keep exactly one entry per current bookmark statusLink. Remove stale entries that are no longer in the current export.

For each current bookmark, write:
- title: concise and higher-signal
- summary: 1-3 plain strings, no bullet markers inside the strings
- tags: 2-6 short tags, no # prefix

Do not invent unsupported claims. Reuse good existing overrides when possible. Then write the final JSON to X_BOOKMARKS_TO_OBSIDIAN_LLM_OVERRIDES_FILE.
```
