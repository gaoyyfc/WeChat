"""Render saved prompts with api-image; credentials stay in process memory."""

import argparse
import concurrent.futures
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
BACKEND = Path.home() / ".codex/skills/api-image/scripts/generate_image.py"
PROVIDER_HELPER = HERE.parent / "别人说话让你不舒服贴图-20261111/generate.py"


def resolve_provider():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("image_provider_helper", PROVIDER_HELPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.resolve_provider()


def render(task, base, key):
    topic_name, name = task.split(":", 1)
    folder = HERE / topic_name
    topic = json.loads((folder / "制作内容.json").read_text())
    output = folder / "generated" / f"{name}.png"
    prompt_file = folder / "prompts" / f"{name}.md"
    if output.exists():
        print(f"SKIP {task}: image exists", flush=True)
        return True
    if name == "01-cover":
        references = [folder / "references" / ref for ref in topic["references"]]
        roles = [
            "Typography hierarchy reference ONLY; ignore reference topic, colors, UI, words and exact layout.",
            "Material and composition research reference ONLY: notebook spacing or photographic mood or checklist hierarchy; ignore topic, words, watermarks, exact scene, palette and UI.",
        ]
    else:
        references = [folder / "references/00-本组封面.png", folder / "references" / topic["references"][-1]]
        roles = [
            "PRIMARY SERIES REFERENCE: approved cover. Preserve this series typography, palette, photo treatment and visual texture, but use the new layout, scene and Chinese words.",
            "SECONDARY STRUCTURE/MATERIAL REFERENCE ONLY: spacing of note rows, photographic mood or checklist hierarchy; do not copy words, topic, palette, people, exact scene or UI.",
        ]
    if not prompt_file.exists() or any(not ref.exists() for ref in references):
        print(f"FAIL {task}: prompt or approved reference missing", flush=True)
        return False
    prompt = prompt_file.read_text().split("---", 2)[2].strip()
    env = os.environ.copy()
    env["API_IMAGE_API_KEY"] = key
    cmd = [sys.executable, str(BACKEND), "--base-url", base,
           "--api-key-env", "API_IMAGE_API_KEY", "--model", "gpt-image-2",
           "--prompt", prompt, "--size", "1152x1536", "--quality", "high",
           "--timeout", "1800", "--out", str(output)]
    for reference, role in zip(references, roles):
        cmd.extend(["--image", str(reference), "--image-role", role])
    for attempt in range(2):
        print(f"START {task} attempt={attempt+1}", flush=True)
        result = subprocess.run(cmd, env=env, text=True, capture_output=True)
        if result.returncode == 0 and output.exists() and output.stat().st_size > 10000:
            print(f"OK {task}", flush=True)
            return True
        detail = (result.stdout + result.stderr).replace(key, "[redacted]").replace(base, "[provider]")
        print(f"FAIL {task}: {detail[-900:]}", flush=True)
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tasks", nargs="+")
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    if not 1 <= args.jobs <= 4:
        parser.error("Use 1–4 concurrent image tasks")
    base_url, api_key = resolve_provider()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
        results = list(executor.map(lambda task: render(task, base_url, api_key), args.tasks))
    sys.exit(0 if all(results) else 1)
