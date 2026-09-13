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
accretion — injected into every session's context automatically, so
the discipline is present from the first turn rather than something
you have to remember to ask for.

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
3. (no manual step)
4. Verify: start a new Claude Code session and confirm a line
   beginning "ethos v0.1.0 — work-ethics corpus" appears in the
   session's context.
```

## Where this fits in the stack

**Core** (the daily working style): ethos + [lifecycle](https://github.com/Gunther-Schulz/lifecycle) (work-item tracking) + [dispatch-guards](https://github.com/Gunther-Schulz/dispatch-guards) (subagent dispatch discipline).

**Optional** (pick what fits your work): [statiker](https://github.com/Gunther-Schulz/statiker) (certified development runs), [skill-craft](https://github.com/Gunther-Schulz/skill-craft) (designing and reviewing skills), claude-worktime (time tracking).

ethos works standalone — the other plugins add capability on top of it, but none of them are required for ethos itself to be useful.

## License

Not yet decided for this repo — see the maintainer's own notes before relying on reuse terms.
