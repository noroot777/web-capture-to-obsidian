# url-to-obsidian

**English** | [中文](#中文)

Grab one or more URLs from your Chrome session and turn them into Obsidian notes. Works with WeChat articles, GitHub pages, X/Twitter posts, and any normal website.

Part of [web-capture-to-obsidian](../../). For X bookmark sync, see [x-bookmarks-to-obsidian](../x-bookmarks-to-obsidian/).

## Install

Tell your AI agent:

> Install the url-to-obsidian skill from GitHub repo noroot777/web-capture-to-obsidian, path skills/url-to-obsidian

For OpenCode, ask the agent to clone the whole repo into its skills directory.

## First-time setup

Tell your agent where your Obsidian vault is. The agent will create the env file automatically:

> Set up the url-to-obsidian skill. My Obsidian vault is at /Users/me/Obsidian/URL Capture

Prerequisites: Chrome 144+, Python 3, npm. Chrome remote debugging must be turned on once: `chrome://inspect#remote-debugging`.

## Usage

Talk to your agent in natural language:

> Save this page to Obsidian: https://github.com/openai/openai-python

> Capture these URLs: https://mp.weixin.qq.com/s/abc and https://x.com/user/status/123

> Save whatever's on my clipboard to Obsidian

The agent exports the pages from Chrome, generates titles/summaries/tags via LLM, and writes Obsidian notes — all in one step.

## Output

Notes go to `URL_TO_OBSIDIAN_TARGET_DIR` (default `~/Obsidian/URL to Obsidian`):

- Numbered Markdown notes with frontmatter + summary + excerpts
- `000 - URL 采集索引.md` — index file
- `.url_to_obsidian_state.json` — state for incremental runs

## Config

All optional. See [`url_to_obsidian.env.example`](url_to_obsidian.env.example) for the full list: LLM model, Chrome binary path, DevToolsActivePort path, timezone, etc.

## Files

| | |
|---|---|
| `SKILL.md` | Skill definition — the agent reads this to know what to do |
| `scripts/url_to_obsidian.py` | Main cross-platform entry point |
| `scripts/export_urls.devbrowser.js` | Chrome automation |
| `scripts/extract_input_urls.py` | URL extraction from text |
| `scripts/generate_url_obsidian_notes.py` | JSON → Obsidian notes |
| `scripts/generate_url_llm_overrides.py` | Standalone Codex LLM helper |

---

<a id="中文"></a>

# url-to-obsidian

[English](#url-to-obsidian) | **中文**

从你的 Chrome 里抓一个或多个 URL，变成 Obsidian 笔记。微信文章、GitHub 页面、X 帖子、普通网页都行。

属于 [web-capture-to-obsidian](../../) 仓库。X 书签同步看 [x-bookmarks-to-obsidian](../x-bookmarks-to-obsidian/)。

## 安装

告诉你的 AI agent：

> 从 GitHub 仓库 noroot777/web-capture-to-obsidian 安装 url-to-obsidian skill，路径 skills/url-to-obsidian

OpenCode 的话，让 agent 把整个仓库 clone 到 skills 目录。

## 首次配置

告诉 agent 你的 Obsidian 笔记目录，agent 会自动创建 env 文件：

> 配置 url-to-obsidian skill，我的 Obsidian 目录是 /Users/我/Obsidian/URL Capture

环境要求：Chrome 144+、Python 3、npm。Chrome 远程调试要先开一次：`chrome://inspect#remote-debugging`。

## 使用

用自然语言跟 agent 说就行：

> 把这个页面存到 Obsidian：https://github.com/openai/openai-python

> 抓这些 URL：https://mp.weixin.qq.com/s/abc 和 https://x.com/user/status/123

> 把我剪贴板里的链接存到 Obsidian

agent 会自动从 Chrome 导出页面，通过 LLM 生成标题/摘要/标签，写好 Obsidian 笔记——一步到位。

## 输出

笔记写到 `URL_TO_OBSIDIAN_TARGET_DIR`（默认 `~/Obsidian/URL to Obsidian`）：

- 编号 Markdown 笔记，带 frontmatter + 摘要 + 页面摘录
- `000 - URL 采集索引.md` —— 索引
- `.url_to_obsidian_state.json` —— 增量运行状态

## 配置项

都是可选的。完整列表看 [`url_to_obsidian.env.example`](url_to_obsidian.env.example)：LLM 模型、Chrome 路径、DevToolsActivePort 路径、时区等。

## 文件

| | |
|---|---|
| `SKILL.md` | Skill 定义——agent 读这个来知道该怎么做 |
| `scripts/url_to_obsidian.py` | 跨平台主入口 |
| `scripts/export_urls.devbrowser.js` | Chrome 自动化 |
| `scripts/extract_input_urls.py` | 从文本提取 URL |
| `scripts/generate_url_obsidian_notes.py` | JSON → Obsidian 笔记 |
| `scripts/generate_url_llm_overrides.py` | 独立 Codex LLM 辅助 |
