#!/usr/bin/env python3
"""Copy the two skills into skills/ from their own GitHub repos, or check that they match.

The skills are developed in their own repositories; this kit only carries copies.
    python3 scripts/sync_skills.py            # copy the latest main of both, update skills/SOURCES.json
    python3 scripts/sync_skills.py --check    # skills/ must equal the commits in SOURCES.json
Only files tracked by git upstream are copied, minus the upstream .github folder.
Standard library only; needs git on PATH.
"""
from __future__ import annotations

import argparse
import filecmp
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
SOURCES = SKILLS / "SOURCES.json"
UPSTREAM = {
    "3d-print-design": "https://github.com/Matteoikarieth96/3d-print-design-skill.git",
    "x2d-print": "https://github.com/Matteoikarieth96/x2d-print-skill.git",
}
SKIP_PREFIXES = (".github/",)
# local, never in git: the design skill's Python environment and caches survive a sync
LOCAL_ONLY = {".venv", "__pycache__", ".DS_Store"}


def git(*args: str, cwd: Path) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def fetch(url: str, ref: str, into: Path) -> str:
    """Shallow fetch of one commit or branch; returns the commit sha."""
    into.mkdir(parents=True)
    git("init", "-q", cwd=into)
    git("fetch", "-q", "--depth", "1", url, ref, cwd=into)
    git("-c", "advice.detachedHead=false", "checkout", "-q", "FETCH_HEAD", cwd=into)
    return git("rev-parse", "HEAD", cwd=into)


def tracked(repo: Path) -> list:
    files = git("ls-files", "-z", cwd=repo).split("\0")
    return sorted(f for f in files if f and not f.startswith(SKIP_PREFIXES))


def _local_files(dest: Path) -> set:
    if not dest.exists():
        return set()
    return {str(p.relative_to(dest)) for p in dest.rglob("*")
            if p.is_file() and not LOCAL_ONLY.intersection(p.relative_to(dest).parts)}


def copy(repo: Path, dest: Path) -> None:
    for rel in _local_files(dest) - set(tracked(repo)):
        (dest / rel).unlink()
    for rel in tracked(repo):
        src = repo / rel
        if src.is_symlink():
            raise SystemExit(f"refusing: {rel} is a symlink upstream")
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)


def differences(repo: Path, dest: Path) -> list:
    want = set(tracked(repo))
    have = _local_files(dest)
    out = [f"missing: {f}" for f in sorted(want - have)] + [f"extra: {f}" for f in sorted(have - want)]
    out += [f"changed: {f}" for f in sorted(want & have) if not filecmp.cmp(repo / f, dest / f, shallow=False)]
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="only check skills/ against SOURCES.json")
    ap.add_argument("--ref", default="main", help="branch or commit to copy (default main)")
    a = ap.parse_args(argv)
    sources = json.loads(SOURCES.read_text()) if SOURCES.is_file() else {}
    problems, changed = [], []
    with tempfile.TemporaryDirectory() as tmp:
        for name, url in UPSTREAM.items():
            work = Path(tmp) / name
            dest = SKILLS / name
            if a.check:
                commit = sources.get(name, {}).get("commit")
                if not commit:
                    problems.append(f"{name}: no commit recorded in skills/SOURCES.json")
                    continue
                fetch(url, commit, work)
                problems += [f"{name}: {d}" for d in differences(work, dest)]
                continue
            commit = fetch(url, a.ref, work)
            if differences(work, dest):
                copy(work, dest)
                changed.append(f"{name} {sources.get(name, {}).get('commit', 'none')[:7]} -> {commit[:7]}")
            sources[name] = {"repo": url.removesuffix(".git"), "commit": commit}
    if a.check:
        if problems:
            print("skills/ does not match its upstream repos. Change a skill in its own repo, then run "
                  "scripts/sync_skills.py (or the Sync skills action):\n  " + "\n  ".join(problems[:40]))
            return 1
        print("skills/ matches " + ", ".join(f"{n}@{s['commit'][:7]}" for n, s in sources.items()))
        return 0
    SOURCES.write_text(json.dumps(sources, indent=2) + "\n")
    print("updated: " + "; ".join(changed) if changed else "already up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
