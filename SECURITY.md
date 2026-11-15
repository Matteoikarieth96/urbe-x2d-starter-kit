# Security

This kit adds three things to the two skills it carries: `install.sh`,
`scripts/sync_skills.py` and two GitHub Actions workflows. The skills' own threat
models are in [skills/3d-print-design/SECURITY.md](skills/3d-print-design/SECURITY.md)
and [skills/x2d-print/SECURITY.md](skills/x2d-print/SECURITY.md).

## What the kit runs

- **install.sh** creates symbolic links in `~/.claude/skills` and a Python virtual
  environment inside `skills/3d-print-design/.venv`, then installs that skill's
  `requirements.txt` from PyPI: versions pinned, prebuilt wheels only (no package code
  runs at install time), no hashes. It never deletes or overwrites an existing skill;
  the only thing it ever removes is its own `.venv`, when that is broken.
- **sync_skills.py** fetches each skill repository with `git`, copies only the files git
  tracks there (minus their `.github/` folder), refuses symbolic links, and prints every
  file it removes. `--check` compares `skills/` byte for byte, executable bits included,
  with the commits in `skills/SOURCES.json`; refuses a commit that is not on the
  upstream `main`; and refuses files committed under `skills/` that the upstream repo
  does not have (a `.venv` or `__pycache__` folder slipped in by hand, for example).
- **ci.yml** runs with read-only permissions and no stored credentials.
- **sync.yml** checks out without keeping credentials, so the upstream code it runs and
  tests cannot read the token. Only the last steps get it: they push the branch
  `sync/skills` (never `main`), open or update one pull request, or open an issue when
  the tests fail. A person reviews and merges. Its actions are pinned to commit hashes.
  On a pull request pushed with the workflow token, CI does not start by itself: the
  same tests already ran in the sync job; closing and reopening the pull request starts
  CI.
- **What a sync brings in**: whatever is on the skills' `main` branches. Review the
  pull request diff before merging, as you would any outside change.

## Reporting a problem

Open a private security advisory on this repository (Security tab, "Report a
vulnerability"), or on the skill's own repository if the problem is in a skill.
Please do not open a public issue for a vulnerability.
