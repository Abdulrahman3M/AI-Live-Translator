#!/usr/bin/env python3
"""Build reproducible Codex, Claude Code, Agent Skill, and source ZIPs."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
OUTPUT_DIR = ROOT / "dist"
EXCLUDED_PARTS = {
    ".git",
    ".idea",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".superpowers",
    ".venv",
    "__pycache__",
    "dist",
    "node_modules",
    "venv",
}
EXCLUDED_SUFFIXES = {".bak", ".pyc", ".pyo", ".swp", ".swo", ".temp", ".tmp"}
ZIP_TIMESTAMP = (2020, 1, 1, 0, 0, 0)


def _is_package_file(path: pathlib.Path, *, exclude_tests: bool = False) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDED_PARTS or path.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    return not (exclude_tests and "tests" in parts)


def _collect_paths(paths: tuple[str, ...], *, exclude_tests: bool = False) -> dict[str, pathlib.Path]:
    collected: dict[str, pathlib.Path] = {}
    for relative in paths:
        source = ROOT / relative
        if source.is_file():
            if _is_package_file(pathlib.Path(relative), exclude_tests=exclude_tests):
                collected[pathlib.Path(relative).as_posix()] = source
            continue
        if not source.is_dir():
            raise FileNotFoundError(f"Required package path is missing: {relative}")
        for file_path in source.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(ROOT)
                if _is_package_file(relative_path, exclude_tests=exclude_tests):
                    collected[relative_path.as_posix()] = file_path
    return collected


def _write_archive(output_path: pathlib.Path, files: dict[str, pathlib.Path], *, prefix: str = "") -> None:
    if not files:
        raise ValueError(f"Refusing to create an empty archive: {output_path.name}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative, source in sorted(files.items()):
            info = zipfile.ZipInfo(f"{prefix}{relative}", date_time=ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes())


def _verify_archive(
    archive_path: pathlib.Path,
    *,
    required: tuple[str, ...],
    manifest_path: str | None = None,
    root_prefix: str = "",
) -> None:
    with zipfile.ZipFile(archive_path) as archive:
        if archive.testzip() is not None:
            raise ValueError(f"Archive integrity check failed: {archive_path.name}")
        names = set(archive.namelist())
        for relative in required:
            expected = f"{root_prefix}{relative}"
            if expected not in names:
                raise ValueError(f"Archive {archive_path.name} is missing {expected}")
        if manifest_path:
            manifest = json.loads(archive.read(f"{root_prefix}{manifest_path}"))
            if manifest.get("version") != VERSION:
                raise ValueError(f"Archive {archive_path.name} has a mismatched manifest version")
            interface = manifest.get("interface", {})
            for field in ("composerIcon", "logo"):
                asset = interface.get(field)
                if isinstance(asset, str) and asset.startswith("./") and asset[2:] not in names:
                    raise ValueError(f"Archive {archive_path.name} is missing declared asset {asset}")


def _source_files() -> dict[str, pathlib.Path]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        check=True,
        capture_output=True,
    )
    files: dict[str, pathlib.Path] = {}
    for item in result.stdout.decode("utf-8").split("\0"):
        if not item:
            continue
        relative = pathlib.Path(item)
        source = ROOT / relative
        if source.is_file() and _is_package_file(relative):
            files[relative.as_posix()] = source
    return files


def build_archives(output_dir: pathlib.Path = OUTPUT_DIR) -> dict[str, pathlib.Path]:
    """Build and verify the four non-ChatGPT release ZIPs."""
    output_dir = pathlib.Path(output_dir)
    manifests = {
        ".codex-plugin/plugin.json": (".codex-plugin/plugin.json", "skills/setup/SKILL.md", "skills/ai-live-translator/SKILL.md", "plugin/commands/start.md", "plugin/commands/help.md"),
        ".claude-plugin/plugin.json": (".claude-plugin/plugin.json", "plugin/commands/start.md", "plugin/commands/help.md", "skills/ai-live-translator/SKILL.md"),
    }
    archives: dict[str, pathlib.Path] = {}

    codex_files = _collect_paths((".codex-plugin/plugin.json", "LICENSE", "VERSION", "assets", "skills", "plugin/commands", "prompt"))
    codex_path = output_dir / f"AI-Live-Translator-Codex-Plugin-v{VERSION}.zip"
    _write_archive(codex_path, codex_files)
    _verify_archive(codex_path, required=manifests[".codex-plugin/plugin.json"], manifest_path=".codex-plugin/plugin.json")
    archives["codex"] = codex_path

    claude_files = _collect_paths((".claude-plugin/plugin.json", "LICENSE", "VERSION", "plugin/commands", "skills/ai-live-translator", "prompt"), exclude_tests=True)
    claude_path = output_dir / f"AI-Live-Translator-Claude-Code-Plugin-v{VERSION}.zip"
    _write_archive(claude_path, claude_files)
    _verify_archive(claude_path, required=manifests[".claude-plugin/plugin.json"], manifest_path=".claude-plugin/plugin.json")
    archives["claude_code"] = claude_path

    skill_files = {
        pathlib.Path(relative).relative_to("skills/ai-live-translator").as_posix(): source
        for relative, source in _collect_paths(("skills/ai-live-translator",), exclude_tests=True).items()
    }
    skill_path = output_dir / f"AI-Live-Translator-Agent-Skill-v{VERSION}.zip"
    _write_archive(skill_path, skill_files, prefix="ai-live-translator/")
    _verify_archive(
        skill_path,
        required=("SKILL.md", "agents/openai.yaml", "rules/translation-contract.md", "examples/en-ar.jsonl", "references/activation.md", "scripts/router.py", "assets/ai-live-translator-icon-64.png"),
        root_prefix="ai-live-translator/",
    )
    archives["agent_skill"] = skill_path

    source_files = _source_files()
    source_root = f"AI-Live-Translator-v{VERSION}/"
    source_path = output_dir / f"AI-Live-Translator-Source-v{VERSION}.zip"
    _write_archive(source_path, source_files, prefix=source_root)
    _verify_archive(
        source_path,
        required=("VERSION", "plugin.json", "assets/ai-live-translator-hero.png", "skills/ai-live-translator/SKILL.md"),
        root_prefix=source_root,
    )
    archives["source"] = source_path
    return archives


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=pathlib.Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    for name, path in build_archives(args.output_dir).items():
        print(f"Created {name}: {path}")


if __name__ == "__main__":
    main()
