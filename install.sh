#!/bin/sh
# Install the two skills of this kit for Claude Code on this computer.
# It links skills/3d-print-design and skills/x2d-print into ~/.claude/skills
# (so `git pull` in this folder updates them) and creates the Python
# environment the design skill needs. It never overwrites a skill you already
# have: if one is there, it says so and leaves it alone.
set -eu
KIT="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/skills"
mkdir -p "$DEST"
for name in 3d-print-design x2d-print; do
  src="$KIT/skills/$name"
  if [ -L "$DEST/$name" ] && [ "$(readlink "$DEST/$name")" = "$src" ]; then
    echo "ok: $name is already linked to this kit"
  elif [ -e "$DEST/$name" ] || [ -L "$DEST/$name" ]; then
    echo "skipped: $DEST/$name already exists (another copy of the skill). Move it away and run this again to use the kit's copy."
  else
    ln -s "$src" "$DEST/$name"
    echo "installed: $name -> $src"
  fi
done
PY="${PYTHON:-python3}"
if ! "$PY" -c 'import sys; sys.exit(sys.version_info < (3, 9))' 2>/dev/null; then
  echo "Python 3.9 or newer is needed: install it from python.org, then run this again." >&2
  exit 1
fi
VENV="$KIT/skills/3d-print-design/.venv"
if [ ! -x "$VENV/bin/python" ]; then
  echo "creating the design skill's Python environment (a minute or two)..."
  "$PY" -m venv "$VENV"
  "$VENV/bin/python" -m pip install --quiet -r "$KIT/skills/3d-print-design/requirements.txt"
fi
echo "done. Next: install Bambu Studio (bambulab.com), open Claude Code and say what you want to print."
