# Security

This kit adds three things to the two skills it carries: `install.sh`,
`scripts/sync_skills.py` and two GitHub Actions workflows. The skills' own threat
models are in [skills/3d-print-design/SECURITY.md](skills/3d-print-design/SECURITY.md)
and [skills/x2d-print/SECURITY.md](skills/x2d-print/SECURITY.md).

## What the kit runs

- **install.sh** creates symbolic links in `~/.claude/skills` and a Python virtual
  environment inside `skills/3d-print-design/.venv`, then installs that skill's pinned
  `requirements.txt` from PyPI. It never deletes or overwrites an existing skill.
- **sync_skills.py** fetches one commit of each skill repository with `git`, copies
  only the files git tracks there (minus their `.github/` folder), and refuses
  symbolic links. `--check` compares `skills/` byte for byte with the commits in
  `skills/SOURCES.json`.
- **ci.yml** runs with read-only permissions and no stored credentials.
- **sync.yml** needs `contents: write` and `pull-requests: write` to push a branch and
  open a pull request. It never pushes to `main`: a person reviews and merges. It uses
  only the workflow's own token, and its actions are pinned to commit hashes.

## Reporting a problem

Open a private security advisory on this repository (Security tab, "Report a
vulnerability"), or on the skill's own repository if the problem is in a skill.
Please do not open a public issue for a vulnerability.
