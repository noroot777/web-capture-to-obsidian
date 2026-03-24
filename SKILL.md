---
name: x-bookmarks-sync
description: Sync the user's X.com bookmarks into Obsidian notes using the user's already logged-in Chrome session. Use this when the user asks to sync, refresh, import, capture, or update X bookmarks into Obsidian, especially for requests like "同步 X 书签", "抓取我的 X 书签", "更新 Obsidian 里的 X 书签", or "把最新书签同步进去".
---

# X Bookmarks Sync

Syncs X bookmarks from the user's real Chrome session into a configurable Obsidian directory.

## Workflow

1. By default, run:
   - `./scripts/sync_x_bookmarks.sh`
2. That script now:
   - exports bookmarks
   - uses the model to generate `title`, `summary`, and `tags`
   - writes overrides to `X_BOOKMARKS_LLM_OVERRIDES_FILE`
   - default: `~/.dev-browser/tmp/x-bookmarks-llm-overrides.json`
   - generates the final Obsidian notes
3. If the user explicitly says not to use the model, run:
   - `X_BOOKMARKS_USE_LLM=0 ./scripts/sync_x_bookmarks.sh`
4. Report how many bookmarks were synced and where the notes were written.

## User Choice

Treat LLM participation as the default.

- If the user says `同步 X 书签`, `抓取我的 X 书签`, or similar, let the model participate.
- If the user says `不要让 LLM 参与`, `不用模型`, `without llm`, or similar, set `X_BOOKMARKS_USE_LLM=0`.
- If the user wants a custom model, set `X_BOOKMARKS_LLM_MODEL`.

## LLM Override Format

Write JSON in either of these shapes:

```json
{
  "entries": {
    "https://x.com/.../status/123": {
      "title": "Better title here",
      "summary": [
        "First key point",
        "Second key point",
        "Third key point"
      ],
      "tags": [
        "automation",
        "agents",
        "workflow"
      ]
    }
  }
}
```

Or:

```json
{
  "https://x.com/.../status/123": {
    "title": "Better title here",
    "summary": "- First key point\n- Second key point",
    "tags": [
      "automation",
      "agents"
    ]
  }
}
```

See also:

- [`x_bookmarks_llm_overrides.example.json`](x_bookmarks_llm_overrides.example.json)

## Extraction Guidance

When generating `title` and `summary`:

- Prefer the real core idea over the first visible line.
- Remove handles, metrics, and low-signal UI boilerplate.
- For link-heavy posts, summarize what the linked resource is about.
- Keep `title` concise and filename-friendly.
- Keep `summary` to 2-4 concrete bullets.
- Return tags that are specific enough to be useful in Obsidian.

## Shell Entry Point

[`scripts/sync_x_bookmarks.sh`](scripts/sync_x_bookmarks.sh) will:

- verify that the installed Chrome version supports the current-session remote-debugging flow
- auto-install `dev-browser` if it is missing
- reuse the user's logged-in Chrome session via `chrome://inspect#remote-debugging`
- export bookmarks
- generate LLM overrides by default
- optionally skip LLM participation when `X_BOOKMARKS_USE_LLM=0`
- optionally skip final generation when `X_BOOKMARKS_SKIP_GENERATE=1`

If Chrome shows a remote-debugging permission prompt, wait for the user to click `Allow`, then rerun the sync script.
If the user wants a custom location, tell them to create `x_bookmarks_sync.env` from `x_bookmarks_sync.env.example` instead of editing the scripts directly.

## What It Writes

- One note per bookmark under `X_BOOKMARKS_TARGET_DIR`
- Stable numbered filenames like `001 - 标题 - 时间 - 作者.md`
- Numbering follows bookmark-list order from bottom to top: the oldest bookmark currently at the bottom of the list is `001`, and newer bookmarks continue upward with larger numbers
- `000 - X 书签索引.md` for ordered browsing
- `.x_bookmarks_state.json` to preserve numbering across future syncs

## Notes

- This uses the user's authenticated Chrome session, so it is much more reliable than a normal unauthenticated scraper, but it is not a guaranteed bypass for every X anti-bot check.
- This skill expects a Chrome version that supports the current-session remote-debugging flow from `chrome://inspect#remote-debugging`. If the local Chrome is too old, the script exits with a clear message instead of failing silently.
- If the user wants a different Obsidian path, use `x_bookmarks_sync.env`. If they want a different naming scheme or note format, update [`scripts/generate_x_obsidian_notes.py`](scripts/generate_x_obsidian_notes.py) and rerun the sync.
