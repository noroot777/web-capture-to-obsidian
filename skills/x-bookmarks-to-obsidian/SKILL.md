---
name: x-bookmarks-to-obsidian
description: Sync the user's full X bookmark list into Obsidian notes. Use this when the user wants to capture or refresh bookmarks from https://x.com/i/bookmarks.
---

# X Bookmarks to Obsidian

Sync the user's saved X bookmarks from their real Chrome session into Obsidian.

## First Use

Before running the skill, create `x_bookmarks_to_obsidian.env` from `x_bookmarks_to_obsidian.env.example` and set:

- `X_BOOKMARKS_TO_OBSIDIAN_TARGET_DIR` to an absolute Obsidian path

## Recommended Workflow

### Agent-assisted mode

1. Run export-only sync:
   - `X_BOOKMARKS_TO_OBSIDIAN_SKIP_GENERATE=1 ./scripts/x_bookmarks_to_obsidian.sh`
2. Read the exported JSON from:
   - `X_BOOKMARKS_TO_OBSIDIAN_SOURCE_JSON`
   - default: `~/.dev-browser/tmp/x-bookmarks-to-obsidian-export.json`
3. Generate better `title`, `summary`, and `tags` in the current agent session.
4. Write overrides to:
   - `X_BOOKMARKS_TO_OBSIDIAN_LLM_OVERRIDES_FILE`
   - default: `~/.dev-browser/tmp/x-bookmarks-to-obsidian-llm-overrides.json`
5. Follow the JSON shape from:
   - [`x_bookmarks_to_obsidian_llm_overrides.example.json`](x_bookmarks_to_obsidian_llm_overrides.example.json)
6. Generate final notes:
   - `python3 scripts/generate_x_bookmarks_obsidian_notes.py`

### Standalone shell mode

- `./scripts/x_bookmarks_to_obsidian.sh`

If LLM participation is enabled, this requires the local `codex` CLI.

## Output

- One note per bookmark under `X_BOOKMARKS_TO_OBSIDIAN_TARGET_DIR`
- `000 - X 书签索引.md`
- `.x_bookmarks_to_obsidian_state.json`

