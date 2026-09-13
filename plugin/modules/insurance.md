## Insurance mechanisms — conventions, applied by trigger

- **On-disk ledger — trigger: context death risk** — work
  outliving the session that holds it (multi-session, resumed,
  compaction-survived, or handed to a successor session or
  desk). One line per entry, append-only, scannable: facts (with
  basis), decisions (with the why; rejected alternative when
  non-obvious), open questions — absence of an entry never reads
  as settled. Naming default and role boundaries: Per-project
  accretion, file roles. Rationale goes where future sessions
  look — ledger or commit message, never only the chat.
  Convention: a re-derivation of something possibly settled opens
  with a ledger read, the entry found or its absence named.
- **Fresh-context verification — trigger: self-blind checks.**
  Mechanical verifiers (tests, queries, renders — anything that
  runs and returns a verdict) gain no VERDICT value from a fresh
  context — the verdict is identical wherever it runs; where it
  runs is an ordinary routing question (Model routing). A fresh
  verifier earns its cost where self-blindness is the risk: own
  completeness claims ("all dependents updated"), surfaces whose
  wrongness is silent, statistical findings (briefed to refute),
  the session's own routing choices, and its own BOOKED verdicts
  when new work rests on them — a session re-reads its bookings
  as settled ground, and dispatches have overturned same-day
  bookings that inline continuation carried as premises. A
  verifier briefed with the dispatcher's reasoning inherits its
  blind spots — the brief is the artifact and the question,
  nothing else. Fresh context earns its value at the verdict,
  not at the design dialogue (Model routing: open judgment
  favors inline).
  - **Escalation past one-shot review.** Trigger, at intake or
    on first contact with the premise: work failing the skip
    gauge (Calibration) on both the silent-failure and
    blast-radius questions, resting on an unverified behavioral
    premise about an external system, spanning sessions.
    One-shot review misses two classes there: a premise whose
    basis was silently SUBSTITUTED between cycles (visible only
    against the ledger's record of the earlier basis — one-shot
    review has no record to compare), and a fix that OVERSHOOTS
    (visible only when a later round re-falsifies the fix —
    one-shot review books after one clean pass). That profile
    routes through iterated falsification: premises with their
    bases in the on-disk ledger, each round attacking both the
    design's fit to the stated intent and the factual bases it
    cites, re-run until a round returns zero delta — each round
    after the first under the re-entry seam's reason and trend
    questions (Calibration). A protocol
    skill covering this shape is a routing destination; the
    shape holds by hand.
- **Dispatched work — trigger: work another agent holds** (a
  delegated or parallel agent, or a whole item handed to a
  peer). Conduct forms — briefs, tails, one-writer, integration,
  silence-handling: the dispatch skill (`dispatch-guards:dispatch`;
  its load before any dispatch is hook-enforced, site overlay
  included). The wait carries an expected-return
  horizon, ARMED when it begins — the waiter schedules its own
  wake at it, because an unarmed horizon fires only if something
  else happens to wake the session, and permanent silence then
  reads as work. The instrument is a POLL (a Monitor-style loop
  with its own timeout) that WATCHES the artifact's every move
  and emits only at the horizon, at completion, or on a
  computable anomaly — movement re-arms it silently (the firing
  act, below): every emission re-invokes the waiting session and
  re-bills its prefix, so a per-move print is a paid wake with
  nothing to act on. Never a bare background `sleep`: a
  sleep-timer dies as silently as the lane it guards — measured
  2026-08-27, 4 of 9 killed on a shared machine, the kills
  clustering on another session's `pkill` to retire a spent timer,
  a dead-at-arming and a dead-at-disarm timer indistinguishable
  from the waiting end — while the poll held across every arm;
  a `killed` notice on any timer is a re-arm, never a no-op.
  Silence past the horizon is a finding, never more waiting
  (arming mechanics and mailbox
  binding: dispatch skill §4, canonical). Subagents commit
  unpushed by design (dispatch skill §4); the dispatcher's own
  commit verb: Per-project accretion, operator verbs.
  - **Horizon sizing and firing.** The horizon is a dead-lane
    DETECTOR, not a deadline, and is sized for detection: a
    horizon set to a comfortable multiple of the estimate buys
    a lane dead at minute two that whole excess read as
    working. Where the lane's artifact is observable (files,
    commits in a shared copy), the cheap form is a RECURRING
    short horizon — roughly half the expected remaining
    duration, floored near 10 min (below that the cadence is
    babysitting) and capped near 45 min so every wake lands
    inside the prompt-cache TTL with margin (1h, as of
    2026-08-20); ~30 min is the open-ended default. A peer's
    ANNOUNCED immediate action re-keys the horizon to MINUTES:
    the announcement is the estimate, and a turn that ENDS on
    the announcement has STOPPED — nothing re-invokes a stopped
    session, so "doing it now" with no first tool call is
    already the stall (JOURNAL, horizon sizing, 2026-08-26); the
    waiting side's timer is the robust seam, the receiver's prose
    is not (Calibration, the incoming demand). The horizon's firing
    act is an artifact LOOK: a changing artifact re-arms
    silently at zero interruption; on a SESSION lane the look
    reads the peer's live status too (ListAgents) —
    waiting/idle beneath an announced-unstarted action confirms
    the stall and skips straight to the demand; a static one
    escalates to the status demand — which resumes the lane and
    can cross an in-flight report (measured), so it is the
    second rung, never the first — then stop-or-redispatch. A
    wait that ENDS disarms its timer in the same turn: a spent
    timer left running fires a stale wake. On a SESSION lane the
    wait has a second instrument beside the timer: a one-shot
    idle subscription (`notify_when_idle`, armable only from a
    main session — as of 2026-08-26) fires when the peer next
    goes idle or exits, which catches a stop that produced no
    report in seconds rather than at the horizon. It is spent
    after one firing and re-arms only by being asked again, and
    it can expire having observed nothing — so it shortens the
    good case and never replaces the timer, which stays the
    instrument that fires when the peer produces no event at
    all.
