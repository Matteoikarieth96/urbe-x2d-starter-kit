#!/bin/sh
# Install the two skills of this kit for Claude Code on this computer.
# Installa le due skill del kit per Claude Code su questo computer.
#
# It links skills/3d-print-design and skills/x2d-print into ~/.claude/skills
# (so `git pull` in this folder updates them) and creates the Python
# environment the design skill needs. It never overwrites a skill you already
# have: if one is there, it says so and leaves it alone. Run it again at any
# time: it repairs a half-finished environment.
set -eu
KIT="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/skills"
REQ="$KIT/skills/3d-print-design/requirements.txt"
VENV="$KIT/skills/3d-print-design/.venv"

say() { printf '%s\n%s\n' "$1" "   $2"; }

mkdir -p "$DEST"
for name in 3d-print-design x2d-print; do
  src="$KIT/skills/$name"
  if [ -L "$DEST/$name" ] && [ "$(readlink "$DEST/$name")" = "$src" ]; then
    say "ok: $name is already linked to this kit" "ok: $name è già collegata a questo kit"
  elif [ -e "$DEST/$name" ] || [ -L "$DEST/$name" ]; then
    say "skipped: $DEST/$name already exists (another copy of the skill). Move it away and run this again to use the kit's copy." \
        "saltata: $DEST/$name esiste già (un'altra copia della skill). Spostala altrove e rilancia questo script per usare quella del kit."
  else
    ln -s "$src" "$DEST/$name"
    say "installed: $name -> $src" "installata: $name"
  fi
done

# The design skill's pinned packages (numpy 2.4.6 and friends) need Python 3.11 to 3.14.
# The python3 that comes with macOS is 3.9 and will not work.
ok_python() { "$1" -c 'import sys; sys.exit(not ((3, 11) <= sys.version_info[:2] <= (3, 14)))' 2>/dev/null; }
PY=""
if [ -n "${PYTHON:-}" ]; then
  if ok_python "$PYTHON"; then PY="$PYTHON"; fi
else
  for cand in python3.13 python3.12 python3.14 python3.11 python3; do
    if command -v "$cand" >/dev/null 2>&1 && ok_python "$cand"; then PY="$cand"; break; fi
  done
fi
if [ -z "$PY" ]; then
  say "Python 3.11 to 3.14 is needed (the python3 built into macOS is too old). Install Python 3.13 from https://www.python.org/downloads/macos/ (pick the latest 3.13.x installer, not 3.15: its packages are not ready yet), close and reopen the terminal, then run ./install.sh again." \
      "Serve Python dalla 3.11 alla 3.14 (quello già presente su macOS è troppo vecchio). Installa Python 3.13 da https://www.python.org/downloads/macos/ (scegli l'ultimo installer 3.13.x, non la 3.15: i suoi pacchetti non sono ancora pronti), chiudi e riapri il terminale, poi rilancia ./install.sh." >&2
  exit 1
fi

ready() { "$VENV/bin/python" -c 'import numpy, trimesh, manifold3d, shapely' 2>/dev/null; }
if [ -x "$VENV/bin/python" ] && ok_python "$VENV/bin/python" && ready; then
  say "ok: the design skill's Python environment is ready" "ok: l'ambiente Python della skill di design è pronto"
else
  if [ -e "$VENV" ]; then
    say "repairing the design skill's Python environment..." "riparo l'ambiente Python della skill di design..."
    rm -rf "$VENV"
  fi
  say "creating the design skill's Python environment with $PY (a minute or two, needs internet)..." \
      "creo l'ambiente Python della skill di design con $PY (un paio di minuti, serve internet)..."
  "$PY" -m venv "$VENV"
  if ! "$VENV/bin/python" -m pip install --quiet --disable-pip-version-check --only-binary=:all: -r "$REQ" || ! ready; then
    rm -rf "$VENV"
    say "the Python packages did not install with $PY. Check the internet connection and run ./install.sh again (or choose another Python: PYTHON=python3.13 ./install.sh); if it fails again, copy the error into Claude Code and ask for help." \
        "i pacchetti Python non si sono installati con $PY. Controlla la connessione e rilancia ./install.sh (oppure scegli un altro Python: PYTHON=python3.13 ./install.sh); se fallisce di nuovo, incolla l'errore in Claude Code e chiedi aiuto." >&2
    exit 1
  fi
fi
say "done. Next: install Bambu Studio (bambulab.com), open Claude Code and say what you want to print." \
    "fatto. Ora: installa Bambu Studio (bambulab.com), apri Claude Code e scrivi cosa vuoi stampare."
