## Per-project accretion — conventions

- Before working in a project, its CLAUDE.md discipline sections,
  the ledger tail and the ready items are read (the session-start
  hook injects the latter two where deployed). An operator
  correction that generalizes is minted into the project
  CLAUDE.md as the general rule, not just the fix.
- On a direct conflict between a project convention and a global
  one, the project convention wins in that project.
- **File roles** — defaults a repo departs from only by a
  declaration in its CLAUDE.md. `CLAUDE.md`: discipline, pointers
  to every role file, the verify commands. `CLAUDE.local.md`: the
  untracked personal overlay; where the tracked CLAUDE.md is a
  foreign team's, the overlay takes the corrections and deviation
  declarations that would otherwise land in their file.
  `LEDGER.md`: the on-disk ledger. `BACKLOG.md` or the declared
  item carrier: work items (Backlog doctrine, below). `README.md`:
  humans, never the agent's operating knowledge. `tools/`:
  repo-owned checks — a probe used twice graduates there.
  `docs/directives/`: persisted briefs. `docs/runbooks/`: standing
  procedures (format: `runbook-format.md` beside the root
  CLAUDE.md). `dev-notes/*-OBSERVATIONS.md`: instrument lessons,
  kept in the owning instrument's repo, four slots per entry
  (incident + basis, class, pre-formulated fix, consumer + drain
  seam). `READINESS.json`: tier exclusions.
  `.claude/required-reading.json`: the reading roster. Everything
  persisted names its consumer at write time and sits on that
  consumer's read path. Every persisted artifact is ENGLISH
  (operator decision); exceptions are decided per string — quoted
  material, an untranslatable term, a fixture matching foreign
  text, text a person reads directly — and the check is a scan
  keyed on the language, never on its diacritics (JOURNAL, file
  roles, 2026-08-26).
- **Two exits**, no third: do it now or record its disposition; a
  change stated only in chat evaporates. A finding that blocks no
  named project goal is DROPPED by default — one ledger line,
  recoverable on recurrence; booking is the exception that argues
  itself, naming the goal or item that blocks on it. Boundaries at
  every grain: decision → ledger, work item → backlog, rule or
  discipline → project CLAUDE.md. A stated direction or planning
  assumption is decided the moment its sentence is composed and
  owes its carrier in the same reply. Done means done where the
  next occasion will READ it — a change living only in a running
  system is not done until its durable half lands. Which exit is
  decided by what the build needs that is absent NOW, and each
  named absence is graded real-now: an operator decision with the
  operator present is one question in this reply, a venue
  reachable by dispatch is a route line, a missing check that is
  part of the work is the work, and only what the session
  genuinely cannot reach AND a goal needs parks. A fix not yet
  DESIGNED is not a fix not yet DECIDABLE: gap → fix → designed
  now → built, booked or dropped. Recording a gap in a sibling
  carrier — an incident or journal entry — does not discharge the
  work item, and a proposal shipped with its recommendation is a
  work item at delivery. Dropping is legitimate; leaving no record
  never is (JOURNAL, two exits, 2026-08-26).
- **Backlog doctrine.** Items are graded by decision-completeness:
  READY (design decided, verifier named, done-criterion stated,
  realizing write boundary named as `Write-set:` with paths that
  resolve) or PARKED (its missing evidence or trigger named). An
  entry another party owns is graded by them. A drain orders by
  consequence and by who asked. Closure is TERMINAL — SHIPPED
  (built, verified, in its consumer's hands), DROPPED (one recorded
  line, recoverable on recurrence) or FROZEN (done as-is, its
  re-open condition named) — and MOVES the body to the one closure
  home. A foundation's implicit done, defect-free, is unreachable:
  its normal end is the FREEZE with its re-open condition named,
  not a backlog drained to zero. A closure is earned at the item's
  own size: pressure to clear an entry never makes a change larger,
  wider or less reversible than the entry asked for.
  Capture-dominated growth — booked far outrunning terminal
  closures, rough tripwire 3:1 over a +30%-line stretch — owes a
  retirement pass before new bookings. Where a
  repo declares the lifecycle plugin (`.claude/lifecycle.json`),
  its tool enforces these rules; elsewhere the ethic is the rule
  (JOURNAL, backlog doctrine, 2026-08-26).
- Operator verbs are made decisions, never ask-backs: "backlog
  it" → a decision-complete entry, no code; "park it" → an entry
  with its missing evidence; "ledger it" → the entry appended;
  "dispatch it" → a brief from the settled design; "certify it" →
  the tier-readiness pipeline for the named recurring procedure,
  its entry born eval-open; "commit" → commit AND push in the same
  turn, a self-initiated main-session commit included (a deliberate
  hold is stated, never asked); "close the session" → a clean
  close, the cutoff over owed-but-unstarted items asked as a
  numbered round before any wrap-up (JOURNAL, operator verbs,
  2026-08-26).
