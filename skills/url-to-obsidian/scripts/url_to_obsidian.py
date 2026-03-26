#!/usr/bin/env python3
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


SKILL_DIR = Path(__file__).resolve().parents[1]
CONFIG_FILE = Path(os.environ.get("URL_TO_OBSIDIAN_CONFIG_FILE", str(SKILL_DIR / "url_to_obsidian.env"))).expanduser()
EXTRACT_SCRIPT = SKILL_DIR / "scripts" / "extract_input_urls.py"
EXPORT_SCRIPT = SKILL_DIR / "scripts" / "export_urls.devbrowser.js"
GENERATE_SCRIPT = SKILL_DIR / "scripts" / "generate_url_obsidian_notes.py"
MIN_SUPPORTED_CHROME_MAJOR = int(os.environ.get("URL_TO_OBSIDIAN_MIN_CHROME_MAJOR", "144"))


def bool_env(name: str, default: str) -> bool:
    return os.environ.get(name, default).strip() == "1"


def parse_env_file(path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        value = os.path.expandvars(value)
        value = str(Path(value).expanduser()) if value.startswith("~") else value
        values[key] = value
    return values


def load_config() -> None:
    for key, value in parse_env_file(CONFIG_FILE).items():
        os.environ[key] = value


def common_home() -> Path:
    return Path.home()


def default_target_dir() -> Path:
    return common_home() / "Obsidian" / "URL to Obsidian"


def target_dir_configured() -> bool:
    return bool(os.environ.get("URL_TO_OBSIDIAN_TARGET_DIR", "").strip())


def env_path(name: str, default: Path) -> Path:
    raw = os.environ.get(name, "").strip()
    if raw:
        return Path(raw).expanduser()
    return default.expanduser()


def default_devtools_candidates() -> List[Path]:
    home = common_home()
    system = platform.system()
    if system == "Darwin":
        base = home / "Library" / "Application Support" / "Google" / "Chrome"
        return [base / "DevToolsActivePort"]
    if system == "Windows":
        candidates: List[Path] = []
        local = os.environ.get("LOCALAPPDATA", "")
        roaming = os.environ.get("APPDATA", "")
        if local:
            candidates.append(Path(local) / "Google" / "Chrome" / "User Data" / "DevToolsActivePort")
        if roaming:
            candidates.append(Path(roaming) / "Google" / "Chrome" / "User Data" / "DevToolsActivePort")
        return candidates

    config_home = Path(os.environ.get("XDG_CONFIG_HOME", str(home / ".config"))).expanduser()
    return [
        config_home / "google-chrome" / "DevToolsActivePort",
        config_home / "google-chrome-beta" / "DevToolsActivePort",
        config_home / "chromium" / "DevToolsActivePort",
        config_home / "chromium-browser" / "DevToolsActivePort",
    ]


def resolve_devtools_file() -> Path:
    explicit = os.environ.get("URL_TO_OBSIDIAN_DEVTOOLS_FILE", "").strip()
    if explicit:
        return Path(explicit).expanduser()

    candidates = default_devtools_candidates()
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0] if candidates else Path("DevToolsActivePort")


def default_chrome_candidates() -> List[str]:
    system = platform.system()
    if system == "Darwin":
        return ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    if system == "Windows":
        candidates: List[str] = []
        for base in (
            os.environ.get("LOCALAPPDATA", ""),
            os.environ.get("PROGRAMFILES", ""),
            os.environ.get("PROGRAMFILES(X86)", ""),
        ):
            if not base:
                continue
            candidates.append(str(Path(base) / "Google" / "Chrome" / "Application" / "chrome.exe"))
        return candidates

    discovered: List[str] = []
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        match = shutil.which(name)
        if match:
            discovered.append(match)
    discovered.extend(
        [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
        ]
    )
    return discovered


def resolve_chrome_bin() -> str:
    explicit = os.environ.get("URL_TO_OBSIDIAN_CHROME_BIN", "").strip()
    if explicit:
        return explicit

    for candidate in default_chrome_candidates():
        if candidate and Path(candidate).exists():
            return candidate
    return default_chrome_candidates()[0]


def ensure_target_dir_configured() -> None:
    if target_dir_configured():
        return
    raise SystemExit(
        "First-time setup required before using url-to-obsidian.\n"
        "Create url_to_obsidian.env from url_to_obsidian.env.example and set "
        "URL_TO_OBSIDIAN_TARGET_DIR to your Obsidian notes folder using an absolute path."
    )


def ensure_absolute_target_dir(target_dir: Path) -> None:
    if target_dir.is_absolute():
        return
    raise SystemExit(
        "URL_TO_OBSIDIAN_TARGET_DIR must be an absolute path. "
        f"Current value: {target_dir}\n"
        "Update url_to_obsidian.env and set URL_TO_OBSIDIAN_TARGET_DIR to an "
        "absolute path like /Users/you/Obsidian/URL Capture."
    )


def run_checked(cmd: List[str], env: Optional[Dict[str, str]] = None, input_text: Optional[str] = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=True, env=env, input=input_text, text=True, capture_output=False)


def ensure_dev_browser() -> None:
    if shutil.which("dev-browser"):
        return
    if not shutil.which("npm"):
        raise SystemExit("dev-browser is not installed, and npm is not available to install it automatically.")
    print("dev-browser not found. Installing it automatically with npm...")
    run_checked(["npm", "install", "-g", "dev-browser"])


def check_chrome_version(chrome_bin: str) -> None:
    if not Path(chrome_bin).exists():
        raise SystemExit(f"Google Chrome was not found at: {chrome_bin}")

    proc = subprocess.run([chrome_bin, "--version"], capture_output=True, text=True, check=False)
    version_output = (proc.stdout or proc.stderr or "").strip()
    match = re.search(r"(\d+)\.", version_output)
    if not match:
        raise SystemExit(f"Could not determine the installed Chrome version. Output was: {version_output}")

    major = int(match.group(1))
    if major < MIN_SUPPORTED_CHROME_MAJOR:
        raise SystemExit(
            f"Chrome {major} is too old for this skill's current-session remote-debugging flow.\n"
            f"This skill expects Chrome {MIN_SUPPORTED_CHROME_MAJOR}+ with chrome://inspect#remote-debugging "
            "support for active browser sessions."
        )


def build_endpoint(devtools_file: Path) -> str:
    if not devtools_file.exists():
        raise SystemExit(
            f"Chrome remote debugging is not enabled: {devtools_file} not found\n"
            "Open chrome://inspect#remote-debugging in Chrome and enable remote debugging first."
        )

    lines = devtools_file.read_text(encoding="utf-8").splitlines()
    port = lines[0].strip() if len(lines) >= 1 else ""
    ws_path = lines[1].strip() if len(lines) >= 2 else ""
    if not port or not ws_path:
        raise SystemExit("Invalid DevToolsActivePort contents")
    return f"ws://127.0.0.1:{port}{ws_path}"


def usage() -> str:
    script = Path(__file__).name
    return (
        f"Usage:\n"
        f"  python3 {script} <url-or-text>        # export + generate\n"
        f"  python3 {script} full <url-or-text>   # export + generate\n"
        f"  python3 {script} export <url-or-text> # export only\n"
        f"  python3 {script} generate             # generate only from existing JSON\n"
    )


def parse_mode_and_args(argv: List[str]) -> Tuple[str, List[str]]:
    if not argv:
        return "full", []
    mode = argv[0].strip().lower()
    if mode in {"full", "export", "generate"}:
        return mode, argv[1:]
    if mode in {"-h", "--help", "help"}:
        print(usage())
        raise SystemExit(0)
    return "full", argv


def collect_input(argv: List[str]) -> str:
    if argv:
        return " ".join(argv)
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("Pass a URL or paste text that contains one or more URLs.\n\n" + usage())


def extract_urls(raw_input: str, urls_json: Path) -> int:
    proc = subprocess.run(
        [sys.executable, str(EXTRACT_SCRIPT), raw_input],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = proc.stdout
    urls_json.parent.mkdir(parents=True, exist_ok=True)
    urls_json.write_text(payload if payload.endswith("\n") else payload + "\n", encoding="utf-8")
    try:
        data = json.loads(payload)
    except Exception:
        data = []
    return len(data) if isinstance(data, list) else 0


def main(argv: List[str]) -> int:
    mode, mode_args = parse_mode_and_args(argv)
    load_config()

    ensure_target_dir_configured()
    target_dir = env_path("URL_TO_OBSIDIAN_TARGET_DIR", default_target_dir())
    ensure_absolute_target_dir(target_dir)

    dev_browser_tmp = env_path("URL_TO_OBSIDIAN_DEV_BROWSER_TMP", common_home() / ".dev-browser" / "tmp")
    urls_json = env_path("URL_TO_OBSIDIAN_URLS_JSON", dev_browser_tmp / "url-to-obsidian-urls.json")
    source_json = env_path("URL_TO_OBSIDIAN_SOURCE_JSON", dev_browser_tmp / "url-to-obsidian-export.json")
    overrides_file = env_path("URL_TO_OBSIDIAN_LLM_OVERRIDES_FILE", dev_browser_tmp / "url-to-obsidian-llm-overrides.json")
    state_file = env_path("URL_TO_OBSIDIAN_STATE_FILE", target_dir / ".url_to_obsidian_state.json")

    os.environ["URL_TO_OBSIDIAN_TARGET_DIR"] = str(target_dir)
    os.environ["URL_TO_OBSIDIAN_STATE_FILE"] = str(state_file)
    os.environ["URL_TO_OBSIDIAN_SOURCE_JSON"] = str(source_json)
    os.environ["URL_TO_OBSIDIAN_LLM_OVERRIDES_FILE"] = str(overrides_file)

    run_export = mode in {"full", "export"} and not bool_env("URL_TO_OBSIDIAN_SKIP_EXPORT", "0")
    run_generate = mode in {"full", "generate"} and not bool_env("URL_TO_OBSIDIAN_SKIP_GENERATE", "0")
    if not run_export and not run_generate:
        raise SystemExit("Nothing to do: both export and generate are disabled.")

    child_env = os.environ.copy()
    url_count = 0

    if run_export:
        raw_input = collect_input(mode_args)
        url_count = extract_urls(raw_input, urls_json)
        if url_count == 0:
            raise SystemExit("No supported URLs were found in the provided text.")

        ensure_dev_browser()
        chrome_bin = resolve_chrome_bin()
        check_chrome_version(chrome_bin)
        endpoint = build_endpoint(resolve_devtools_file())
        child_env["URL_TO_OBSIDIAN_CHROME_BIN"] = chrome_bin

        run_checked(
            [
                "dev-browser",
                "--connect",
                endpoint,
                "--timeout",
                "900",
                "run",
                str(EXPORT_SCRIPT),
            ],
            env=child_env,
        )

    if run_generate:
        run_checked([sys.executable, str(GENERATE_SCRIPT)], env=child_env)

    if mode == "export" or (run_export and not run_generate):
        print(f"Exported {url_count} pages to {source_json}")
        print(f"Write agent overrides to {overrides_file}")
    elif mode == "generate" or (run_generate and not run_export):
        print(f"Generated URL notes into {target_dir}")
    else:
        print(f"Organized {url_count} link(s) into {target_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
