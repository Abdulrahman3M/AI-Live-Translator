#!/usr/bin/env python3
"""Build the minimal ChatGPT-installable distribution (stdlib only)."""
import json
import pathlib
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
FILES = ["LICENSE", "plugin.json", "README.md"]
DIRECTORIES = ["prompt", "skills/ai-live-translator", "skills/setup"]
EXCLUDE_PARTS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo"}
OUTPUT = ROOT / "dist" / f"AI-Live-Translator-ChatGPT-Plugin-v{VERSION}.zip"

def main():
    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    if manifest.get("version") != VERSION:
        raise SystemExit("Root plugin manifest and VERSION disagree")
    included = {path: ROOT / path for path in FILES}
    for directory in DIRECTORIES:
        for path in (ROOT / directory).rglob("*"):
            if path.is_file() and not (set(path.relative_to(ROOT).parts) & EXCLUDE_PARTS) and path.suffix not in EXCLUDE_SUFFIXES:
                included[path.relative_to(ROOT).as_posix()] = path
    required = ["plugin.json", "skills/setup/SKILL.md", "skills/ai-live-translator/SKILL.md"]
    for path in required:
        if path not in included or not included[path].is_file():
            raise SystemExit(f"Required plugin file missing: {path}")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as archive:
        for path, source in sorted(included.items()):
            archive.write(source, arcname=path)
    with zipfile.ZipFile(OUTPUT) as archive:
        assert archive.testzip() is None
        assert json.loads(archive.read("plugin.json"))["version"] == VERSION
    print(f"Created {OUTPUT} ({len(included)} files)")
if __name__ == "__main__":
    main()
