---
name: x-bookmarks-to-obsidian
description: Sync the user's full X bookmark list into Obsidian notes. Use this when the user wants to capture or refresh bookmarks from https://x.com/i/bookmarks.
---

# X Bookmarks to Obsidian

Sync the user's saved X bookmarks from their real Chrome session into Obsidian.

## First Use

Before running the skill, create `x_bookmarks_to_obsidian.env` from `x_bookmarks_to_obsidian.env.example` and set:

- `X_BOOKMARKS_TO_OBSIDIAN_TARGET_DIR` to an absolute Obsidian path

## Workflow

The agent should treat this skill as `export -> current session writes overrides -> generate`.
Do not rely on the scripts to make a second LLM call on their own.

1. Run export-only sync:
   - `python3 scripts/x_bookmarks_to_obsidian.py export`
2. Read the exported JSON from:
   - `X_BOOKMARKS_TO_OBSIDIAN_SOURCE_JSON`
   - default: `~/.dev-browser/tmp/x-bookmarks-to-obsidian-export.json`
3. In the current agent session, create higher-signal `title`, `summary`, and `tags` for the exported items.
   - Keep one output entry per bookmark key.
   - Reuse existing overrides when the file already exists.
   - Only create or update entries for bookmarks present in the current export JSON.
4. Write overrides to:
   - `X_BOOKMARKS_TO_OBSIDIAN_LLM_OVERRIDES_FILE`
   - default: `~/.dev-browser/tmp/x-bookmarks-to-obsidian-llm-overrides.json`
5. Follow the JSON shape from:
   - [`x_bookmarks_to_obsidian_llm_overrides.example.json`](x_bookmarks_to_obsidian_llm_overrides.example.json)
6. Use the prompt template when writing overrides in the current session:
   - [`overrides_prompt_template.md`](overrides_prompt_template.md)
7. Generate final notes:
   - `python3 scripts/x_bookmarks_to_obsidian.py generate`

## Agent Rules

- When the user asks to sync bookmarks, prefer the full agent-assisted flow instead of calling `python3 scripts/x_bookmarks_to_obsidian.py` in default full mode without overrides.
- The current agent session is responsible for writing the overrides JSON.
- If no overrides are needed, say that explicitly and then run the final generate step.
- Keep summaries concrete and compact; do not add filler.


## Output

- One note per bookmark under `X_BOOKMARKS_TO_OBSIDIAN_TARGET_DIR`
- `000 - X 书签索引.md`
- `.x_bookmarks_to_obsidian_state.json`
