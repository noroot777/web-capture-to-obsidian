# Web Capture to Obsidian

[English README](./README.md)

这个仓库现在是一个多 skill 集合，目标是把浏览器里的内容整理进 Obsidian。

## Skills

| Skill | 用途 |
|---|---|
| `url-to-obsidian` | 把一个或多个 URL 从当前 Chrome 会话抓成 Obsidian 笔记 |
| `x-bookmarks-to-obsidian` | 把 `https://x.com/i/bookmarks` 的整份 X 书签同步到 Obsidian |

## 仓库结构

```text
skills/
  url-to-obsidian/
  x-bookmarks-to-obsidian/
```

每个 skill 都是自包含的，带自己的 `SKILL.md`、README、脚本、env 示例和 overrides 示例。

## 运行要求

- macOS
- Chrome 144+
- Python 3
- npm

Chrome 远程调试只要开一次：`chrome://inspect#remote-debugging`

## 安装

### Codex / Claude Code / OpenClaw

按 skill 单独安装，直接软链接或复制对应目录：

```bash
ln -s /path/to/web-capture-to-obsidian/skills/url-to-obsidian ~/.codex/skills/url-to-obsidian
ln -s /path/to/web-capture-to-obsidian/skills/x-bookmarks-to-obsidian ~/.codex/skills/x-bookmarks-to-obsidian
```

如果你用的是 Claude Code 或 OpenClaw，把 `~/.codex/skills` 换成对应客户端的 skills 目录即可。

也可以直接按 GitHub 子路径安装：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo noroot777/web-capture-to-obsidian \
  --path skills/url-to-obsidian

python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo noroot777/web-capture-to-obsidian \
  --path skills/x-bookmarks-to-obsidian
```

### OpenCode

整仓 clone 到 skills 目录，让它自动发现两个 `SKILL.md`：

```bash
git clone https://github.com/noroot777/web-capture-to-obsidian.git ~/.config/opencode/skills/web-capture-to-obsidian
```

## Skill 文档

- [`skills/url-to-obsidian/README.md`](./skills/url-to-obsidian/README.md)
- [`skills/x-bookmarks-to-obsidian/README.md`](./skills/x-bookmarks-to-obsidian/README.md)

## 改名说明

旧的单 skill 名称已经移除：

- `web-capture-to-obsidian`
- `x-bookmarks-sync`

现在统一拆成：

- `url-to-obsidian`
- `x-bookmarks-to-obsidian`

## License

[MIT](./LICENSE)
