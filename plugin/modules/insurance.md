## Insurance mechanisms — conventions, applied by trigger

- **On-disk ledger — trigger: context death risk** — work
  outliving the session that holds it (multi-session, resumed,
  compacted, handed to a successor). One line per entry,
  append-only: facts with their basis, decisions with their why,
  open questions. The absence of an entry never reads as settled.
  Rationale goes where future sessions look — the ledger or the
  commit message, never only the chat. Convention: a re-derivation
  of something possibly settled opens with a ledger read, the
  entry found or its absence named.
- **Fresh-context verification — trigger: self-blind checks.**
  Mechanical verifiers gain no verdict value from a fresh context.
  A fresh verifier earns its cost where self-blindness is the
  risk: own completeness claims, surfaces whose failure is silent,
  statistical findings (briefed to refute), the session's own
  routing, and its own booked verdicts when new work rests on
  them. Its brief is the artifact and the question, nothing else.
  - **Escalation past one-shot review.** Work failing the skip
    gauge on both silent failure and blast radius, resting on an
    unverified behavioural premise about an external system, and
    spanning sessions routes through iterated falsification:
    premises and their bases in the ledger, each round attacking
    the design's fit to intent and the facts it cites. One-shot
    review misses a premise whose basis was silently substituted
    between cycles and a fix that overshoots. Protocol: statiker
    where invoked; the shape holds by hand.
- **Dispatched work — trigger: work another agent holds.** Brief,
  report and integration forms: the dispatch skill. Subagents
  commit unpushed by design. The wait carries an expected-return
  horizon ARMED when it begins — the waiter schedules its own
  wake, since nothing else is certain to. Silence past the horizon
  is a finding, never more waiting. **Horizon sizing:** the
  horizon is a dead-lane detector, not a deadline — short and
  recurring where the lane's artifact is observable, minutes where
  a peer has announced an immediate action (JOURNAL, horizon
  sizing, 2026-08-26). The instrument is a POLL that watches the
  artifact, never a bare background `sleep`, which dies as
  silently as the lane it guards. Every emission re-invokes and
  re-bills the waiting session, so the poll emits only at the
  horizon, at completion, or on a computable anomaly. A wait
  resolves its anchor inside each pass and keys its condition to a
  DELTA from a baseline taken when it began, the baseline shown at
  arming — a condition read off cumulative state fires instantly
  on what predates the wait. A spent timer is retired by PID or a
  literal match, never an unescaped pattern. On a session lane, a
  one-shot idle subscription armed at the driving send catches a
  stopped peer in seconds; it never replaces the timer.
