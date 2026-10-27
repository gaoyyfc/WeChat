"""从已保存的提示词调用 api-image；凭据仅在内存和子进程环境中使用。"""

import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tomllib
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BACKEND = Path.home() / ".codex/skills/api-image/scripts/generate_image.py"


def resolve_provider():
    codex_root = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    config = tomllib.loads((codex_root / "config.toml").read_text())
    auth = json.loads((codex_root / "auth.json").read_text())
    active = config.get("model_provider", "openai")
    base = config.get("model_providers", {}).get(active, {}).get("base_url")
    key = auth.get("OPENAI_API_KEY")
    if base and urlparse(base).hostname in ("localhost", "127.0.0.1", "::1"):
        database = Path.home() / ".cc-switch/cc-switch.db"
        with sqlite3.connect(f"file:{database}?mode=ro", uri=True) as conn:
            row = conn.execute(
                "SELECT settings_config FROM providers "
                "WHERE app_type='codex' AND is_current=1 LIMIT 1"
            ).fetchone()
        if row is None:
            raise RuntimeError("当前 CCSwitch 上游配置不存在")
        selected = json.loads(row[0])
        upstream = tomllib.loads(selected["config"])
        active = upstream.get("model_provider", "openai")
        base = upstream.get("model_providers", {}).get(active, {}).get("base_url")
        base = base or upstream.get("base_url")
        key = selected.get("auth", {}).get("OPENAI_API_KEY")
    if not base or not key:
        raise RuntimeError("当前图片上游地址或密钥缺失")
    base = base.rstrip("/")
    if not base.endswith("/v1"):
        base += "/v1"
    return base, key


def render(name, base, key):
    prompt_file = HERE / "prompts" / f"{name}.md"
    output_file = HERE / "generated" / f"{name}.png"
    if output_file.exists():
        print(f"SKIP {name}: 已有图片", flush=True)
        return True
    if not prompt_file.exists():
        print(f"FAIL {name}: 缺少已保存提示词", flush=True)
        return False
    reference = (HERE / "references" / "已确认黄蓝生活漫画风.png"
                 if name == "01-cover" else HERE / "generated" / "01-cover.png")
    if not reference.exists():
        print(f"FAIL {name}: 封面或风格参考缺失", flush=True)
        return False
    prompt = prompt_file.read_text().split("---", 2)[2].strip()
    env = os.environ.copy()
    env["API_IMAGE_API_KEY"] = key
    cmd = [
        sys.executable, str(BACKEND), "--base-url", base,
        "--api-key-env", "API_IMAGE_API_KEY", "--model", "gpt-image-2",
        "--prompt", prompt, "--image", str(reference),
        "--image-role", "style and palette reference approved by the user; do not copy its text, numbers, props, scene, or layout",
        "--size", "1152x1536", "--quality", "high", "--timeout", "1800",
        "--out", str(output_file),
    ]
    print(f"START {name}", flush=True)
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    ok = output_file.exists() and output_file.stat().st_size > 10000
    if ok:
        print(f"OK {name}", flush=True)
    else:
        detail = (result.stdout + result.stderr).replace(key, "[redacted]")
        detail = detail.replace(base, "[provider]")
        print(f"FAIL {name}: {detail[-1000:]}", flush=True)
    return ok


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("names", nargs="+")
    parser.add_argument("--jobs", type=int, default=1)
    args = parser.parse_args()
    provider_base, provider_key = resolve_provider()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
        results = list(executor.map(
            lambda name: render(name, provider_base, provider_key), args.names
        ))
    sys.exit(0 if all(results) else 1)
