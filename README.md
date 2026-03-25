# Web Capture to Obsidian

[中文说明](./README.zh-CN.md)

This repository is now a multi-skill collection for turning browser content into Obsidian notes.

## Skills

| Skill | Purpose |
|---|---|
| `url-to-obsidian` | Capture one or more URLs from your current Chrome session into Obsidian notes |
| `x-bookmarks-to-obsidian` | Sync your full X bookmarks list from `https://x.com/i/bookmarks` into Obsidian |

## Repository Layout

```text
skills/
  url-to-obsidian/
  x-bookmarks-to-obsidian/
```

Each skill is self-contained with its own `SKILL.md`, README, scripts, env example, and overrides example.

## Requirements

- macOS
- Chrome 144+
- Python 3
- npm

Enable Chrome remote debugging once from `chrome://inspect#remote-debugging`.

## Install

### Codex / Claude Code / OpenClaw

Install one skill by copying or symlinking the specific skill directory:

```bash
ln -s /path/to/web-capture-to-obsidian/skills/url-to-obsidian ~/.codex/skills/url-to-obsidian
ln -s /path/to/web-capture-to-obsidian/skills/x-bookmarks-to-obsidian ~/.codex/skills/x-bookmarks-to-obsidian
```

For Claude Code or OpenClaw, replace `~/.codex/skills` with the matching client skills directory.

You can also install from GitHub by path:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo noroot777/web-capture-to-obsidian \
  --path skills/url-to-obsidian

python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo noroot777/web-capture-to-obsidian \
  --path skills/x-bookmarks-to-obsidian
```

### OpenCode

Clone the full repo into the skills directory so it can auto-discover both `SKILL.md` files:

```bash
git clone https://github.com/noroot777/web-capture-to-obsidian.git ~/.config/opencode/skills/web-capture-to-obsidian
```

## Skill Docs

- [`skills/url-to-obsidian/README.md`](./skills/url-to-obsidian/README.md)
- [`skills/x-bookmarks-to-obsidian/README.md`](./skills/x-bookmarks-to-obsidian/README.md)

## Rename Note

The old single-skill names `web-capture-to-obsidian` and `x-bookmarks-sync` have been removed in favor of the new split:

- `url-to-obsidian`
- `x-bookmarks-to-obsidian`

## License

[MIT](./LICENSE)
