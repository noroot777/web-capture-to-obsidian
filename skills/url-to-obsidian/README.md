# URL to Obsidian

Capture one or more URLs from your real Chrome session and save them as Obsidian notes.

This skill is the general web-capture half of the `web-capture-to-obsidian` repository. It handles WeChat, GitHub, X posts, and regular web pages. The separate `x-bookmarks-to-obsidian` skill is for full bookmark sync from `https://x.com/i/bookmarks`.

## Setup

```bash
cp url_to_obsidian.env.example url_to_obsidian.env
```

Set:

```bash
URL_TO_OBSIDIAN_TARGET_DIR="/Users/you/Obsidian/URL Capture"
```

Enable Chrome remote debugging once from `chrome://inspect#remote-debugging`.

## Usage

```bash
./scripts/url_to_obsidian.sh "https://github.com/openai/openai-python"
```

Multiple URLs also work:

```bash
./scripts/url_to_obsidian.sh "https://mp.weixin.qq.com/s/abc and https://x.com/user/status/123"
```

Clipboard input:

```bash
pbpaste | ./scripts/url_to_obsidian.sh
```

## Agent Workflow

```bash
URL_TO_OBSIDIAN_SKIP_GENERATE=1 ./scripts/url_to_obsidian.sh "https://example.com"
python3 scripts/generate_url_obsidian_notes.py
```

Overrides format:

- [`url_to_obsidian_llm_overrides.example.json`](url_to_obsidian_llm_overrides.example.json)

