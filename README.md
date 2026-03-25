# Web Capture to Obsidian

**English** | [中文](#中文)

Two AI agent skills that turn browser content into Obsidian notes, powered by your real Chrome session.

| Skill | What it does |
|---|---|
| [url-to-obsidian](./skills/url-to-obsidian/) | Capture any URL — WeChat, GitHub, X, or generic pages |
| [x-bookmarks-to-obsidian](./skills/x-bookmarks-to-obsidian/) | Sync your full X bookmark list (incremental) |

Works with Codex, Claude Code, OpenCode, and OpenClaw. Connects to your logged-in Chrome via remote debugging — no cookies to export, no extra login.

## Prerequisites

Chrome 144+, Python 3, npm.

One-time Chrome setup: open `chrome://inspect#remote-debugging` and turn it on.

## Install

Tell your AI agent to install the skill you need. The agent handles everything — you don't run any commands yourself.

**Codex / Claude Code / OpenClaw:**

> Install the url-to-obsidian skill from GitHub repo noroot777/web-capture-to-obsidian, path skills/url-to-obsidian

> Install the x-bookmarks-to-obsidian skill from GitHub repo noroot777/web-capture-to-obsidian, path skills/x-bookmarks-to-obsidian

**OpenCode:**

> Clone https://github.com/noroot777/web-capture-to-obsidian.git into your skills directory so both skills are available

After installing, tell the agent where your Obsidian vault is:

> Set up the url-to-obsidian skill. My Obsidian vault is at /Users/me/Obsidian/URL Capture

The agent will create the env file for you.

## Usage

Just tell your agent what you want in natural language:

> Save this page to Obsidian: https://github.com/openai/openai-python

> Capture these URLs to Obsidian: https://mp.weixin.qq.com/s/abc https://x.com/user/status/123

> Sync my X bookmarks to Obsidian

The agent reads the skill definition, runs the scripts, generates titles/summaries/tags, and writes the notes — all automatically.

## Repo structure

```
skills/
  url-to-obsidian/          ← general URL capture
  x-bookmarks-to-obsidian/  ← X bookmark sync
```

Each skill has its own SKILL.md, README, scripts, env example, and overrides example.

## License

[MIT](./LICENSE)

---

<a id="中文"></a>

# Web Capture to Obsidian

[English](#web-capture-to-obsidian) | **中文**

两个 AI agent skill，把浏览器内容变成 Obsidian 笔记。直接连你登录好的 Chrome，走 remote debugging，不用导 cookie，不用重新登录。

| Skill | 干啥的 |
|---|---|
| [url-to-obsidian](./skills/url-to-obsidian/) | 抓任意 URL——微信、GitHub、X、普通网页 |
| [x-bookmarks-to-obsidian](./skills/x-bookmarks-to-obsidian/) | 同步完整的 X 书签列表（可增量） |

Codex、Claude Code、OpenCode、OpenClaw 都能用。

## 环境要求

Chrome 144+、Python 3、npm。

Chrome 只要设置一次：打开 `chrome://inspect#remote-debugging`，开启远程调试。

## 安装

直接让你的 AI agent 装就行，不需要自己跑任何命令。

**Codex / Claude Code / OpenClaw：**

> 从 GitHub 仓库 noroot777/web-capture-to-obsidian 安装 url-to-obsidian skill，路径 skills/url-to-obsidian

> 从 GitHub 仓库 noroot777/web-capture-to-obsidian 安装 x-bookmarks-to-obsidian skill，路径 skills/x-bookmarks-to-obsidian

**OpenCode：**

> 把 https://github.com/noroot777/web-capture-to-obsidian.git 克隆到你的 skills 目录，这样两个 skill 都能用

装完之后，告诉 agent 你的 Obsidian 笔记目录在哪：

> 配置 url-to-obsidian skill，我的 Obsidian 目录是 /Users/我/Obsidian/URL Capture

agent 会自动帮你创建 env 文件。

## 使用

用自然语言告诉你的 agent 就行：

> 把这个页面存到 Obsidian：https://github.com/openai/openai-python

> 把这些 URL 抓到 Obsidian：https://mp.weixin.qq.com/s/abc https://x.com/user/status/123

> 把我的 X 书签同步到 Obsidian

agent 会读取 skill 定义，跑脚本，生成标题/摘要/标签，写好笔记——全自动。

## 仓库结构

```
skills/
  url-to-obsidian/          ← 通用 URL 抓取
  x-bookmarks-to-obsidian/  ← X 书签同步
```

每个 skill 自带 SKILL.md、README、脚本、env 示例和 overrides 示例。

## 许可

[MIT](./LICENSE)
