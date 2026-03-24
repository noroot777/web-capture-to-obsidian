#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEVTOOLS_FILE="$HOME/Library/Application Support/Google/Chrome/DevToolsActivePort"
EXPORT_SCRIPT="$SKILL_DIR/scripts/export_x_bookmarks.devbrowser.js"
GENERATE_SCRIPT="$SKILL_DIR/scripts/generate_x_obsidian_notes.py"
STATE_FILE="/Users/fjh/obs/foan/origin/X/.x_bookmarks_state.json"
DEV_BROWSER_TMP="$HOME/.dev-browser/tmp"
KNOWN_LINKS_FILE="$DEV_BROWSER_TMP/x-bookmarks-known.json"
CHROME_BIN="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MIN_SUPPORTED_CHROME_MAJOR=144

ensure_dev_browser() {
  if command -v dev-browser >/dev/null 2>&1; then
    return
  fi

  if ! command -v npm >/dev/null 2>&1; then
    echo "dev-browser is not installed, and npm is not available to install it automatically." >&2
    exit 1
  fi

  echo "dev-browser not found. Installing it automatically with npm..."
  npm install -g dev-browser
}

check_chrome_version() {
  if [[ ! -x "$CHROME_BIN" ]]; then
    echo "Google Chrome was not found at: $CHROME_BIN" >&2
    exit 1
  fi

  local version_output major
  version_output="$("$CHROME_BIN" --version 2>/dev/null || true)"
  major="$(printf '%s' "$version_output" | sed -E 's/.* ([0-9]+)\..*/\1/')"

  if [[ -z "$major" || ! "$major" =~ ^[0-9]+$ ]]; then
    echo "Could not determine the installed Chrome version. Output was: $version_output" >&2
    exit 1
  fi

  if (( major < MIN_SUPPORTED_CHROME_MAJOR )); then
    echo "Chrome $major is too old for this skill's current-session remote-debugging flow." >&2
    echo "This skill expects Chrome ${MIN_SUPPORTED_CHROME_MAJOR}+ with chrome://inspect#remote-debugging support for active browser sessions." >&2
    exit 1
  fi
}

ensure_dev_browser
check_chrome_version

if [[ ! -f "$DEVTOOLS_FILE" ]]; then
  echo "Chrome remote debugging is not enabled: $DEVTOOLS_FILE not found" >&2
  echo "Open chrome://inspect#remote-debugging in Chrome and enable remote debugging first." >&2
  exit 1
fi

PORT="$(sed -n '1p' "$DEVTOOLS_FILE" | tr -d '\r')"
WS_PATH="$(sed -n '2p' "$DEVTOOLS_FILE" | tr -d '\r')"

if [[ -z "$PORT" || -z "$WS_PATH" ]]; then
  echo "Invalid DevToolsActivePort contents" >&2
  exit 1
fi

ENDPOINT="ws://127.0.0.1:${PORT}${WS_PATH}"

mkdir -p "$DEV_BROWSER_TMP"

if [[ -f "$STATE_FILE" ]]; then
  python3 - <<'PY' > "$KNOWN_LINKS_FILE"
import json
from pathlib import Path

state = Path("/Users/fjh/obs/foan/origin/X/.x_bookmarks_state.json")
try:
    data = json.loads(state.read_text(encoding="utf-8"))
    entries = data.get("entries", {})
    print(json.dumps(list(entries.keys()), ensure_ascii=False))
except Exception:
    print("[]")
PY
else
  printf '[]' > "$KNOWN_LINKS_FILE"
fi

dev-browser --connect "$ENDPOINT" --timeout 900 run "$EXPORT_SCRIPT"
python3 "$GENERATE_SCRIPT"

echo "Synced X bookmarks into /Users/fjh/obs/foan/origin/X"
