#!/usr/bin/env bash
# Requires authenticated GitHub CLI (gh) and git. PRIVATE by default.
set -euo pipefail
cd "$(dirname "$0")/../.."
OWNER="${1:-Abdulrahman3M}"
NAME="${2:-AI-Live-Translator}"
VISIBILITY="${3:---private}"
if [[ "$VISIBILITY" != "--private" && "$VISIBILITY" != "--public" ]]; then echo 'Visibility must be --private or --public' >&2; exit 2; fi
command -v gh >/dev/null || { echo 'Install gh first' >&2; exit 1; }
command -v git >/dev/null || { echo 'Install git first' >&2; exit 1; }
gh auth status
if gh repo view "$OWNER/$NAME" >/dev/null 2>&1; then echo 'Repository exists; refusing to overwrite' >&2; exit 1; fi
[[ -d .git ]] || git init -b main
git add .
if ! git diff --cached --quiet; then git commit -m 'feat: initial AI Live Translator v1.0.0'; fi
gh repo create "$OWNER/$NAME" "$VISIBILITY" --source . --remote origin --push
echo "Published https://github.com/$OWNER/$NAME"
