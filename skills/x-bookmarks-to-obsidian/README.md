# X Bookmarks to Obsidian

Sync your full X bookmarks list into Obsidian notes using your existing Chrome session.

This skill is the X-bookmark half of the `web-capture-to-obsidian` repository. For regular URLs and web pages, use the separate `url-to-obsidian` skill.

## Setup

```bash
cp x_bookmarks_to_obsidian.env.example x_bookmarks_to_obsidian.env
```

Set:

```bash
X_BOOKMARKS_TO_OBSIDIAN_TARGET_DIR="/Users/you/Obsidian/X Bookmarks"
```

Enable Chrome remote debugging once from `chrome://inspect#remote-debugging`.

## Usage

```bash
./scripts/x_bookmarks_to_obsidian.sh
```

## Agent Workflow

```bash
X_BOOKMARKS_TO_OBSIDIAN_SKIP_GENERATE=1 ./scripts/x_bookmarks_to_obsidian.sh
python3 scripts/generate_x_bookmarks_obsidian_notes.py
```

Overrides format:

- [`x_bookmarks_to_obsidian_llm_overrides.example.json`](x_bookmarks_to_obsidian_llm_overrides.example.json)

