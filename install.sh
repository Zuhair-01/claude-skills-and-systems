#!/usr/bin/env bash
# install.sh — one-command setup for claude-skills-and-systems
#   ./install.sh                          symlink everything into Claude Code (~/.claude/skills)
#   ./install.sh --copy                   copy instead of symlink
#   ./install.sh --pack frontend          install one pack (see packs/, --list-packs)
#   ./install.sh --opencode               target OpenCode (~/.config/opencode/skills)
#   ./install.sh --target DIR             custom target directory
set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"
MODE="link"; PACK=""; TARGET=""
while [ $# -gt 0 ]; do
  case "$1" in
    --copy) MODE="copy" ;;
    --pack) PACK="$2"; shift ;;
    --opencode) TARGET="$HOME/.config/opencode/skills" ;;
    --target) TARGET="$2"; shift ;;
    --list-packs) ls "$REPO/packs" | sed 's/\.txt$//'; exit 0 ;;
    --list) ls "$REPO/skills"; exit 0 ;;
    *) echo "unknown flag: $1 (see ROUTING.md)"; exit 1 ;;
  esac
  shift
done
[ -z "$TARGET" ] && TARGET="$HOME/.claude/skills"
mkdir -p "$TARGET"
if [ -n "$PACK" ]; then
  [ -f "$REPO/packs/$PACK.txt" ] || { echo "no such pack: $PACK"; exit 1; }
  WANT=$(grep -v '^#' "$REPO/packs/$PACK.txt" | grep -v '^$' || true)
else
  WANT=$(ls "$REPO/skills")
fi
n=0; skip=0
for s in $WANT; do
  [ -d "$REPO/skills/$s" ] || { echo "  skip (not in repo): $s"; skip=$((skip+1)); continue; }
  if [ "$MODE" = "link" ]; then
    [ -e "$TARGET/$s" ] || ln -s "$REPO/skills/$s" "$TARGET/$s"
  else
    [ -e "$TARGET/$s" ] || cp -r "$REPO/skills/$s" "$TARGET/$s"
  fi
  n=$((n+1))
done
echo "installed $n skills -> $TARGET ($MODE, skipped $skip)"
echo "next: read ROUTING.md to make your agent fire skill-router automatically."
