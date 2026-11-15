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
- **sync.yml** runs in two jobs so that the skills' own code (their tests and the
  packages they install) never runs next to a write token. The `test` job has a
  read-only token: it copies the skills, checks them and runs every test. The `publish`
  job gets `contents`, `pull-requests` and `issues` write, but runs only this kit's code:
  it copies the same commits again with `sync_skills.py --pinned` (each must be on the
  skill's `main`), checks them, pushes the branch `sync/skills` (never `main`) and opens
  or updates one pull request. A person reviews and merges. If a job fails, a third job
  with only `issues: write` opens an issue. Checkouts keep no credentials, actions are
  pinned to commit hashes, and every `run` step uses `bash -eo pipefail`.
- **What a sync brings in**: whatever is on the skills' `main` branches. Review the
  pull request diff before merging, as you would any outside change.

## Reporting a problem

Open a private security advisory on this repository (Security tab, "Report a
vulnerability"), or on the skill's own repository if the problem is in a skill.
Please do not open a public issue for a vulnerability.
