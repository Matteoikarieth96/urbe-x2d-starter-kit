# Urbe X2D starter kit

From an idea to a print on the Bambu Lab X2D, with Claude Code, even if you have
never used a 3D printer. Two Claude Code skills work one after the other:

1. **[3d-print-design](skills/3d-print-design)** asks what you want to make, designs
   the part in code, checks that it can be printed, and shows it in your browser.
   Before you print anything it shows you **versions to choose from** (light,
   standard, strong, or smaller, fewer colours), each with its **filament in grams
   and its print time**.
2. **[x2d-print](skills/x2d-print)** turns the chosen version into a Bambu Studio
   project (`.3mf`) with every colour on the right spool and nozzle, slices it on
   your computer to check the real time and filament, and writes a step-by-step
   guide for your first print.

You open the `.3mf` in Bambu Studio (**File > Open project**, never by
double-clicking it), check the preview and press Print. Nothing in this kit talks
to the printer: sending the print stays your step.

Made for the maker lab of [Urbe](https://github.com/urbe-hub), a community hub in
Rome with a Bambu Lab X2D, and for anyone else with the same printer.

> **In italiano, in breve.** Questo kit porta da un'idea a una stampa sulla Bambu Lab X2D,
> anche per chi non ha mai stampato. Installi il kit, apri Claude Code e scrivi cosa vuoi
> stampare ("disegnami un gancio per lo zaino"). Claude ti fa qualche domanda,
> disegna il pezzo, ti mostra 2 o 3 versioni con grammi di filamento e tempo di stampa,
> poi prepara il file `.3mf` da aprire in Bambu Studio (File > Apri progetto, mai con
> doppio clic) e una guida passo passo in italiano.
>
> **Cosa ti serve**: un Mac con [Claude Code](https://claude.com/claude-code); Python
> dalla 3.11 alla 3.14 da [python.org](https://www.python.org/downloads/) (quello già
> presente su macOS è troppo vecchio); [Bambu Studio](https://bambulab.com/it/download/studio);
> una X2D con PLA caricato. Se la stampante è del Lab, chiedi a chi la gestisce come
> collegarti: non cambiare le sue impostazioni di rete o di account.
>
> **Installazione**: apri il Terminale e incolla, una riga alla volta:
>
> ```
> git clone https://github.com/Matteoikarieth96/urbe-x2d-starter-kit.git
> cd urbe-x2d-starter-kit
> ./install.sh
> ```
>
> Se si ferma con un errore, leggi il messaggio (è anche in italiano), sistema e
> rilancia `./install.sh`: ripara da solo un'installazione a metà. Quando Claude Code
> ti chiede il permesso di eseguire un comando, leggi cosa fa: le due skill lanciano
> solo Python e Bambu Studio sul tuo computer, nella cartella del progetto.

## What you need

- A computer with [Claude Code](https://claude.com/claude-code). Tested on macOS only;
  Linux should work, Windows only through WSL (not tested).
- Python 3.11 to 3.14 (macOS: from [python.org](https://www.python.org/downloads/); the
  python3 that comes with macOS is 3.9 and is too old for the design skill's packages).
- [Bambu Studio](https://bambulab.com/en/download/studio), the free slicer for Bambu Lab
  printers, connected to the printer through your Bambu account, LAN or a USB stick (the
  x2d-print guide shows each way). If the printer is shared (a lab's X2D), ask the
  person who manages it how to connect: do not change its network or account settings.
- A Bambu Lab X2D with PLA loaded. The design skill also works for other printers: you
  get STL files and a print sheet for your own slicer, and the estimates are rougher.

## Install

```
git clone https://github.com/Matteoikarieth96/urbe-x2d-starter-kit.git
cd urbe-x2d-starter-kit
./install.sh
```

`install.sh` links both skills into `~/.claude/skills` and creates the Python
environment the design skill needs. It never replaces a skill you already have. To
update later: `git pull` in this folder, then `./install.sh` again.

**If the install stops**: read the message, fix what it says (usually Python missing or
too old, or no internet) and run `./install.sh` again; it repairs a half-finished
environment by itself. If a skill was "skipped", you already have another copy of it in
`~/.claude/skills`: keep that one, or move it away to use the kit's.

**Permission prompts**: Claude Code asks before it runs a command. The two skills run
Python scripts and Bambu Studio's command line on your computer, inside the project
folder; nothing is sent to the printer. Read each prompt and say yes only to what you
understand.

## Your first print, step by step

1. Open Claude Code and say what you want, in your own words: *"I've never 3D printed.
   Design me a hook for my backpack, to print on the X2D."*
2. Answer a few questions (what it is for, sizes, which filament and colours you have).
   Every term is explained the first time it comes up.
3. Claude builds the part, checks it (closed solid, flat on the plate, nothing hanging
   in the air, fits the printer) and shows a table like this one, for the two-colour
   coaster example (estimates before slicing; the real Bambu Studio slice of the
   standard version took 38 min and 19.7 g):

   | Version | What changes | Filament | Print time | vs standard |
   |---|---|---|---|---|
   | standard | 3 walls, 15% infill | ~19.8 g PLA | ~36 min (30 to 55 min) | |
   | light | 2 walls, 10% infill | ~18.5 g PLA | ~34 min (25 to 55 min) | -2 min, -1.3 g |
   | strong | 4 walls, 40% infill | ~24.2 g PLA | ~41 min (30 min to 1 h 05) | +5 min, +4.4 g |

   About 6 or 7 of those minutes are the printer getting ready (heating, levelling), so
   a small part never takes less than that. On a small part like this one the versions
   differ little; on a bigger or solid part the light version saves much more.

   It also suggests bigger savings in the design itself, when there are any (a
   smaller part, colours only on the top layers), and which nozzle plan is faster:
   here both colours on the left nozzle (~36 min) beat black on the right one (~41 min).
4. You look at it in the browser and pick a version.
5. Claude moves to x2d-print: it tells you which spool goes in the AMS and which on the
   external holder, helps you save a settings template from your own Bambu Studio, and
   builds the `.3mf`. It slices every version on your computer, so you see the **real**
   minutes and grams before you print.
6. Open the `.3mf` in Bambu Studio with **File > Open project**, follow the guide, stay
   by the printer for the first layer.

## How the estimates are made

Before slicing, the design skill estimates filament from the part's shape and the
version's walls and infill, and time from a model fitted on real Bambu Studio slices on
the X2D. Its accuracy is measured, and the data is published in
[estimate-calibration.csv](skills/3d-print-design/references/estimate-calibration.csv)
([how it was made](skills/3d-print-design/references/estimate-calibration.md)):

| Slices | Time, worst | Time, mean | Grams, worst |
|---|---|---|---|
| 34 used to fit the model | 12.6 % | 3.3 % | 9.8 % |
| 18 new parts never used to fit it (holdout) | 32 % | 8 % | 16 % |

So the range it shows is wide on purpose: -15 % to +50 % on time and -15 % to +10 % on
grams, and every slice above falls inside it. That holds only in the measured field
(X2D, PLA, 0.4 mm nozzle, 0.2 mm layers, no supports, infill up to 40 %). Anything
else (another material, nozzle or layer height, supports, another printer) gets a wider
range marked "rough: outside the measured range, trust the slicer".

A colour change on the same nozzle costs about 2 minutes and 0.7 g each. On the X2D a
second colour on the other nozzle saves those changes but costs about 10 minutes once,
to heat and prime the second nozzle, so with few colour layers one nozzle is faster: the
design skill compares both plans and suggests the quicker one. x2d-print then slices
on your computer for closer figures.

## How this repository stays up to date

The skills are developed in their own repositories, and this kit carries copies:

| Skill | Source repository |
|---|---|
| 3d-print-design | https://github.com/Matteoikarieth96/3d-print-design-skill |
| x2d-print | https://github.com/Matteoikarieth96/x2d-print-skill |

- `skills/SOURCES.json` records the exact commit of each copy.
- The **Sync skills** action (nightly, or by hand from the Actions tab) copies the
  latest version of both, runs both test suites and the hand-off test in `tests/`, and
  opens a pull request on the branch `sync/skills` (or updates the one already open).
- CI refuses any change to `skills/` that does not match the source repositories: fix a
  skill in its own repository, then sync. `python3 scripts/sync_skills.py --check` runs
  the same check locally.
- After merging a sync, run `git pull` (and `./install.sh` if `requirements.txt`
  changed) in your clone: your installed skills are links into it.
- If the copy or the tests fail, the action opens an issue "Sync skills failed" instead
  of a pull request; the next green run closes it.
- CI on the sync pull request waits for your approval ("Approve workflows to run" on
  the pull request): the sync run tested on Ubuntu only, CI adds macOS and the other
  Python versions.
- GitHub switches scheduled actions off after 60 days without activity in a public repo.
  After changing a skill, run the sync by hand: `gh workflow enable sync.yml` (if it was
  switched off), then `gh workflow run sync.yml`.

What belongs here: this README, `install.sh`, the hand-off test and, later, Urbe Lab
material (printer settings, example projects).

## Safety

- The printer gets hot (nozzle up to 300 C, bed over 100 C). Stay nearby during the
  first layers and never leave a print running unattended for long.
- Let the plate cool before taking the part off. PLA is fine indoors; ventilate for
  ABS or ASA.
- Printed parts are not for anything where a failure could hurt someone.

Security details for each skill: [3d-print-design](skills/3d-print-design/SECURITY.md),
[x2d-print](skills/x2d-print/SECURITY.md), and [SECURITY.md](SECURITY.md) for this kit.

## Not affiliated

Not affiliated with or endorsed by Bambu Lab. "Bambu Lab", "Bambu Studio" and "X2D" are
names of their owner, used only to say which printer and software this kit works with.

## Licence

MIT, see [LICENSE](LICENSE). Each skill keeps its own MIT licence in its folder.
