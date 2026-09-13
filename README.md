# ethos

The always-loaded work-ethics corpus for Claude Code sessions.

Most Claude Code guidance tells the model *what* to build. ethos is
about *how* to work while building it: check your claims against
evidence before stating them, fix problems at the place that actually
causes them instead of papering over the symptom, ask the right
questions before closing out a task, keep a paper trail so work
survives a restart, write reports the reader can act on, and keep a
project's own rules and backlog from silently rotting. It ships as six
short modules — grounding, fixing, calibration, insurance, reporting,
accretion — that a one-time install step wires into every session's
context via your CLAUDE.md (see Installation below for why it's a
step rather than something automatic), so the discipline is present
from the first turn rather than something you have to remember to ask
for. A SessionStart hook checks that wiring on every session and
speaks up loudly if it's ever missing or stale.

This is v1. It does **not** yet include the model-routing rules (which
model or tier to hand work to, when to delegate to a subagent) or any
machine-specific bindings (shell quirks, locale, permission settings)
— those stay local to the machine and stack they were written for.
What ships here is the portable half: rules about how to reason and
work that hold regardless of what machine or team you're on.

## What's inside

| Module | What it covers |
|---|---|
| Grounding | Basing claims and verdicts on evidence, not confidence; telling a decision from a factual claim |
| Fixing | Locating the real cause of a defect before patching it; verifying a fix by its own output, not by memory of having run it |
| Calibration | The questions to ask before skipping a check, before closing substantial work, and after an incident |
| Insurance | Mechanisms for work that outlives one session — on-disk records, fresh-context review, dispatched-work tracking |
| Reporting | How to recommend and report findings so the reader can act on them without re-deriving your reasoning |
| Accretion | Keeping a project's rules, backlog, and decisions from drifting or silently piling up over time |

## Installation

```
1. claude plugin marketplace add Gunther-Schulz/ethos
2. claude plugin install ethos@ethos-marketplace
3. Run the install script once — this is the one manual step, and
   here's why: Claude Code truncates oversized SessionStart hook
   output to a small preview plus a file pointer (measured on this
   stack), and the six ethos modules run well past that size. So the
   corpus can't travel as hook output at all — it travels instead as
   `@`-imports written into your CLAUDE.md, and writing them is the
   one thing a hook can't do on your behalf at install time. The
   plugin can tell you your install script's exact path (see step 4),
   or find it yourself under your plugin cache. Run it once:

       <path-to-install-imports.sh> [target-CLAUDE.md, default
       $CLAUDE_CONFIG_DIR/CLAUDE.md or ~/.claude/CLAUDE.md]

4. Verify: start a new Claude Code session. If step 3 worked, you'll
   see one line naming your installed version and confirming the
   module count: "ethos v<version>: corpus delivered via CLAUDE.md
   import block (6 modules verified)". If you skipped step 3 (or a
   later ethos update moved the install path), you'll instead see a
   WARNING naming exactly what's wrong plus the exact command to fix
   it — run that command. Its shape (verified against a scratch
   config in this build's own pre-release test run) is:

       ethos v<version> WARNING: <exactly what's wrong, and where>
       Fix: <your-plugin-install-path>/scripts/install-imports.sh <your-CLAUDE.md-path>

   Both paths are filled in with your own real locations — copying
   and running that `Fix:` line is exactly step 3, and it's the
   fastest way to find and run the script the first time, and again
   after any update that moves it.
```

Re-running the install script at any time is safe: an existing import
block is replaced in place, never duplicated, which is also how you
recover after an ethos version upgrade moves the install path out from
under an old block.

## The governance bundle (opt-in; nothing here is wired by default)

The corpus cites its own maintenance doctrine from inside the rules,
so shipping the rules without it would leave those citations
dangling. The doctrine therefore lives here too, in
[plugin/CLAUDE-maintenance.md](plugin/CLAUDE-maintenance.md) — the
rules for editing a rule corpus: what belongs in it, how a change is
grounded and vetted, and how it is reviewed and retired.

It is a coupled HOME, not a forced LOAD. Installing ethos does not
read it, wire it, or enforce it: the install step writes the six
module imports and nothing else, and a consume-only install enables
none of this. Read it only if you maintain a corpus of your own.

What it deliberately does NOT carry is anything bound to one site.
Real paths, journal and item carriers, tool names and enforcement
wiring live in the maintainer's own overlay, not here; this file
names the ROLES those artifacts fill and leaves a site to say what
fills them.

Its enforcement halves are separate from the doctrine and are NOT
shipped wired. Where a site wants them, each carries an assumption
it cannot check for you:

- a corpus-edit gate, which demands the doctrine be read in the
  same turn as a corpus edit — assumes an authoring skill is
  installed to vet against.
- a journal-coupling commit gate, which demands a corpus edit land
  with its journal line — assumes a journal carrier exists. This one
  SHIPS, in `plugin/hooks/corpus-journal-gate.py`, and is still not
  wired: with no configuration it exits silently, so installing
  ethos changes nothing. Two steps turn it on, both yours:

      git config ethos.journalCarrier /path/to/your/JOURNAL.md

  and a line in your own pre-commit whose exit status you honour:

      <plugin>/hooks/corpus-journal-gate.py --repo "$(git rev-parse --show-toplevel)"

  What it establishes is narrower than its name, and it says so in
  its own refusal text rather than leaving you to find out. Where
  corpus and carrier sit in the SAME repository, "staged in this
  commit" is checkable and is what it checks. Where they sit in
  DIFFERENT repositories — the arrangement you get when the corpus
  is public and the journal stays private — there is no shared
  index, so no commit-time check can prove the pair. It then
  establishes only that the carrier was staged in its own repo at
  that moment: not that the line is ever committed, nor that it
  describes this edit.

## Where this fits in the stack

**Core** (the daily working style): ethos + [lifecycle](https://github.com/Gunther-Schulz/lifecycle) (work-item tracking) + [dispatch-guards](https://github.com/Gunther-Schulz/dispatch-guards) (subagent dispatch discipline).

**Optional** (pick what fits your work): [statiker](https://github.com/Gunther-Schulz/statiker) (certified development runs), [skill-craft](https://github.com/Gunther-Schulz/skill-craft) (designing and reviewing skills), [claude-worktime](https://github.com/Gunther-Schulz/claude-worktime) (time tracking).

ethos works standalone — the other plugins add capability on top of it, but none of them are required for ethos itself to be useful.

## License

MIT — see [LICENSE](LICENSE).
