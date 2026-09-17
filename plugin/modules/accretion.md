## Per-project accretion — convention

- Read the project CLAUDE.md discipline sections before working in
  it, and scan the ledger tail and the backlog's ready items — the
  ledger closes re-derivation, the ready items are what is
  dispatchable without further design (where the session-start
  hook is deployed it performs that scan; the reads stay the
  session's where it is not). An
  operator correction that generalizes gets minted into the
  project CLAUDE.md or standards doc — the general rule, not just
  the fix.
- On a direct conflict between a project convention and a global
  one, the project convention wins in that project — the global
  corpus carries defaults, project files the deliberate
  exceptions.
- Project file roles — defaults a repo deviates from only by a
  declaration in its CLAUDE.md (the pointer is the contract, the
  filename the default; no retrofit of existing repos). `CLAUDE.md`:
  discipline, pointers to every role file, and a verify section
  naming the exact commands that make work in the repo trustworthy.
  `CLAUDE.local.md`: the personal, untracked overlay beside a
  CLAUDE.md — machine-local operating knowledge; where the tracked
  CLAUDE.md is a foreign team's, the overlay carries the operating
  knowledge, says so, and takes the corrections and deviation
  declarations that would otherwise land in the foreign file.
  `LEDGER.md` at root: the on-disk ledger (form and trigger:
  Insurance). `BACKLOG.md` at root: work items graded by
  decision-completeness — the full grading-and-drainage doctrine
  is its own bullet below (Backlog doctrine).
  `README.md`: humans and the public, never the agent's operating
  knowledge. `tools/`: repo-owned checks — a probe used twice,
  script or inline one-liner, graduates there or dies (the
  re-pasted one-liner is where a latent variant bug rides
  unexamined). `docs/directives/`: persisted briefs and
  specs of substantial dispatched work. `docs/runbooks/`: standing
  procedures written for a fresh context — each a permanently
  existing decision-complete brief (Model routing) — in two kinds,
  told apart by what enters them: intent workflows a session sets
  out to run, and EVENT LANES entered because something fired,
  which end at a named terminal disposition and are found through
  an always-loaded router declared in the repo's reading roster.
  Format, `Trigger:` syntax, router and mint/retire rules:
  `runbook-format.md`, beside the root CLAUDE.md.
  `dev-notes/*-OBSERVATIONS.md` (or a repo's declared
  equivalent): the instrument-lesson carrier — process or tool
  weaknesses observed while USING an instrument land in the
  OWNING instrument's repo, never a pooled cross-instrument list.
  An entry carries four slots:
  incident + basis · class · the PRE-FORMULATED rule/fix text ·
  consumer + drain seam; same class merges into the existing
  entry, never a sibling. The carrier drains by the retirement
  quota and its pass applies the pre-formulated text or discards
  with a one-line reason — both are exits (Backlog doctrine).
  (Slot template: dispatch-guards
  `dev-notes/OBSERVATIONS-FORM.md`, provenance.)
  `READINESS.json`
  at root: the repo's tier-readiness EXCLUSIONS and deviations —
  procedures that must never run on a cheaper tier here
  (silent-failure + outward-facing) and departures from class
  certifications; certification itself is class-level and global
  (mechanism, schema, register: dispatch skill §6).
  `.claude/required-reading.json` at the repo root: the reading
  roster — a list of repo-relative files a fresh context reads
  before working in the repo, additive to this section's standing
  reads, never replacing them; where the mechanism is deployed it
  injects the roster at session start and gates the first write,
  and without one the roster is still honored by hand. The roles
  above
  are consumer assignments as much as homes — everything persisted
  needs its consumer named at write time: the moment or mechanism
  that will re-encounter it — and the carrier must sit on that
  consumer's read path: a fresh context loads its own brief,
  handoff, or tracker, never a sibling repo's ledger, so an entry
  that consumer must act on travels there too; a named reader who
  never loads the carrier makes the naming decorative. Role
  contents inherit the role's; session-local scratch is exempt —
  it is not persistence.
  "Who reads this, and when?" is answered before the file exists.
  The consumer also fixes the artifact's LANGUAGE — the same
  question one axis over, and the one never asked, because prose
  arrives in whatever language its author was thinking in.
  Operator decision (2026-08-27): every persisted artifact is
  ENGLISH — hooks, guards, carriers, records, registers, the text a
  guard injects — whatever its consumer; the consumer question
  decides only the register, no longer the language (the earlier
  agent-English / person-their-language split is superseded; what
  survives of it is the exception list below). The
  cost is recurring rather than aesthetic: a guard's own text is
  INJECTED into the reader it governs, so the choice is re-billed
  on every fire. Bilingual is not the compromise — two bodies for
  one fact is paraphrase-drift (Grounding) with divergence
  guaranteed; an artifact with both consumers splits into two,
  never one text said twice. The exceptions, narrow and decided
  per string: quoted material, a term of art with no faithful
  rendering, a fixture that must match real foreign text, and text
  a person reads directly (CLI output, notifications). The check
  is a scan keyed on the language, never on its diacritics — an
  umlaut sweep read "no German remains" over a dozen surviving
  strings (measured 2026-08-27; dotfiles `tools/german-scan.py`,
  both controls in its own test).
  (JOURNAL, file roles, 2026-08-26; fire-rate data, 2026-08-27.)
- Two exits, no third: the work is done now or booked; a change
  stated only in chat has no carrier and evaporates. The exits grade
  the EFFECT's home, not the act: done now means done where the next
  occasion will READ it. A change living only in a running system — a
  value applied to a live machine, an instrument started by hand, an
  authored copy while a deployed one executes, a setting a running
  program serves from memory and writes out only at exit — is the
  do-branch's form of that evaporating change, and it hides better:
  it is correct, verified at the effect site, and working when
  checked, so nothing in its own output raises the question. The
  consumer question (file roles, above) is the test, asked of applied
  state rather than of files: name what will next READ this — the
  next start, the next fresh context — and check the change is in
  THAT. Where it is not, the work is not done; the durable half is
  its own exit, taken now or booked, and where it needs an authority
  this session lacks, that is the booking's named absence, never a
  silent completion. Boundaries, at
  every grain: decision → ledger, work item → backlog, rule or
  discipline → project CLAUDE.md. WHICH exit is decided by what
  the build needs that is absent NOW, and the booking names it:
  the realizing write sits at another desk, repo, or held
  working copy; evidence or an operator decision is outstanding;
  the work needs a tier or fresh context this session is not; or
  its blast radius exceeds the session's remaining attention.
  Each named absence is graded REAL-NOW before it parks anything
  — naming absences feels like compliance, which is exactly how
  the rule is escaped: an absence this session can dissolve is
  the next step in an absence's costume, not a parking basis. An
  operator decision with the operator LIVE in the conversation is
  one numbered question in the same reply; a missing check that
  is itself part of the work is the work; a venue reachable by
  dispatch from here is a route line, not a blocker. Only what
  the session genuinely cannot reach — operator away, evidence
  external, a write boundary another desk holds — parks. A fix
  not yet DESIGNED is not a fix not yet DECIDABLE: "review with
  evidence later" defers the design step available now; the flow
  is gap → fix → designed now → built or booked, and book-or-do
  is routing, never an argument against the design. No
  absence named means DO — and the entry that took about as long
  to write as the fix would have is the deferral refuting itself
  in its own arithmetic. The trigger is the
  missing carrier, never the
  phrasing — an enumerated tell catches its listed wording and
  misses the next variant, and the variants that last wear the
  costume above: prudence rather than postponement, so declining
  to act reads as judgment. Declining IS a legitimate call; not
  booking never is. Naming a gap feels like delivering
  it — and so does recording it in a SIBLING carrier: an incident
  or journal entry, however complete, does not discharge the work
  item, whose home is the backlog; a proposal shipped with its
  recommendation is a work item at delivery. The check is against
  the work-item carrier's record, never against that feeling.
  (JOURNAL, two exits, 2026-08-26.)
- **Backlog doctrine** (the BACKLOG.md role's full rules —
  grading, vocabulary, drainage, retirement — and the rules of
  every carrier that captures and drains, the instrument-lesson
  carrier above included):
  `BACKLOG.md` at root: future work graded by
  DECISION-COMPLETENESS, never by intent to build — parked (carries
  its named missing evidence or trigger) and ready (design decided,
  verifier named, done-criterion stated, realizing write-boundary
  named — slot token `Write-set:`, one spelling: a slot concept
  taught under one name while a carrier's checker demands another
  mints non-conforming entries that read green to their author —
  the artifact the change lands in, a desk or operator
  decision, or another venue — dispatchable by construction, singly
  or bundled). The boundary slot is what makes merging, batching and
  parallel dispatch a mechanical join over entries instead of a
  judgment pass over their prose — the pass that grows with the
  queue and binds the strongest reader available; an entry naming
  only what is wrong, not where the fix lands, hides its collisions
  until brief time. The slot's paths RESOLVE at booking — each
  names a file that exists or one the entry itself creates —
  because the join consumes them unchecked: a phantom path
  collides with nothing by construction, so the join's worst
  misread presents as its cleanest answer, a tidy standalone lane
  (measured 2026-09-14: four existing files booked under a wrong
  prefix graded "shares no file with any schedulable item"). A
  boundary genuinely unknown is written as unknown and DEMOTES
  the entry to parked — never invented into paths, which satisfy
  the parse and hand the join a confident wrong clustering in the
  same stroke. Ready promises that a fresh
  context could execute the entry; it is not a queue position and
  not a commitment. WHOSE promise it is matters once more than one
  party writes the carrier: a grade asserts something about work,
  and where the work is another party's in-flight draft, only they
  can say it is done being changed. Reading their artifact tells
  you its content and never that they have stopped; a grade
  applied on their behalf publishes a readiness they never
  claimed, and the next reader executes it. So an entry another
  party owns is graded by them — what a reader may add is
  evidence beside it, or the observation that it looks ready, and
  the promotion waits for its owner
  (JOURNAL, another party's grade, 2026-09-14).
  Those coincide while the ready set is small and
  part company when it outgrows what the repo will ever schedule:
  the grade then asserts an intent nobody holds, and a label
  nobody believes carries no information — the head of the list
  becomes indistinguishable from its tail. Past
  that point the repo declares a THIRD grade in its CLAUDE.md and
  reserves ready for the scheduled head — same bodies, same
  verifiers, nothing dropped and booking still cheap. The split
  owes a trigger BOTH
  ways or the third grade is a sink: outgrowing the schedule is what
  DEMOTES, and what RETURNS entries is the head draining faster
  than it fills — scheduled out against booked in, over the window
  the retirement ratio already uses — computable from the
  carrier's own record, never a
  re-derivation someone remembers. No size cap stands behind
  either: the number has no honest source, and a grade whose only
  re-entry is somebody noticing is this section's
  decorative-reader failure one level up.
  Below it the two grades
  stand: a third grade over a queue the repo can actually drain is
  ceremony.
  Grade words and slot tokens are a CLOSED vocabulary the carrier
  itself declares (default grades READY/PARKED/DONE/DROPPED; extras
  are declared beside them, never improvised), because an open one
  decays invisibly on two measured lines. A counter folds what it
  does not recognize into the open queue, so closure synonyms graded
  in place inflate exactly the numbers the drain triggers read — a
  counter over a carrier has THREE answers: open, closed, and
  unknown grade words listed with their counts. And a checker
  matching the vocabulary by word-presence over free prose fires on
  entries that merely DISCUSS a grade and is silenced by ordinary
  sentences carrying one — carrier checkers anchor on the slot's
  position, never on a word occurring anywhere. A closure vocabulary
  sprouting synonyms is the tell that the MOVE is what costs, not
  that finer semantics are wanted: mechanize the move and the
  synonyms stop minting. A closure is earned at the item's own
  size: the pressure to clear a tracked entry is not a reason to
  make a change larger, wider or less reversible than the entry
  asked for, and that pressure runs the opposite way to this
  section's build-default — there the cost of doing equals the
  cost of booking, here the act has grown past what was booked.
  The tell is a change whose scope is argued from the QUEUE
  rather than from the work: closing this out, while we are in
  here, it would be odd to leave half done. An item that cannot
  be closed at its own size is two items or a drop, both recorded
  exits (JOURNAL, completion pressure, 2026-09-14). Items
  leave by commit ref or by a deliberate one-line drop — an exit of
  equal standing, not a failure: the role's goal is lose nothing
  SILENTLY, which a recorded drop satisfies completely, and a queue
  that never drops is accreting, not succeeding — the closure home
  is exactly ONE: the repo's chronological
  carrier (journal or ledger) where one records closures, else a
  `## Done` section in the backlog itself — never both, one fact
  one home; which carrier a repo uses is the repo's own declared
  truth, and the declaration chooses the HOME, never whether
  closures leave: leaving means the body MOVES there at closure
  time. A strike-through or in-place DONE grade left sitting in
  the live sections is a closure without an exit — the carrier
  grows without bound while formally compliant —
  and
  the role carries a retirement TRIGGER: when growth since the
  last retirement pass is
  capture-dominated (booked far outrunning shipped-plus-dropped;
  rough tripwire 3:1 over a +30%-line stretch), the next session
  working the repo owes a retirement pass before new bookings —
  re-check stale-risk entries against the world, drop the
  overtaken, merge duplicates (mechanism: lifecycle plugin,
  wave 2). The ratio is computed by the
  session-start backlog banner where deployed (it prints
  "retirement pass owed" — binding, as of 2026-08-11), by hand at
  session start where not: an unread ratio fires nothing. The
  trigger reads the ratio, never
  the size: a large backlog draining steadily owes nothing, and
  every investigation spawning several findings while closing one
  is the mechanism that makes capture outrun any ordering rubric.
  The ratio's blind axis is POPULATION: it reads the whole
  carrier, so one category ballooning inside a healthy-draining
  carrier fires nothing. A carrier declared in
  categories gets the ratio question per category; a population
  sharing one expensive default disposition is its own carrier
  for this trigger's purpose.
  Where a repo declares the lifecycle plugin
  (`.claude/lifecycle.json`), the grading, vocabulary and closure
  rules above are refusals its tool enforces, the two-exits cost
  test included; elsewhere the ethic beside them is the rule.
  (JOURNAL, backlog doctrine, 2026-08-26.)
- Operator verbs at the settle moment — the cheap trigger at the
  design-settlement seam, their absence forbidding nothing; each
  is a made decision, never
  an ask-back: "backlog it" → decision-complete entry, no code;
  "park it" → entry with its named missing evidence; "ledger it" →
  append the entry; "dispatch it" → brief from the settled design
  (Model routing); "certify it" → the tier-readiness pipeline for
  the named recurring procedure (dispatch skill §6), entry born
  eval-open; "commit" → commit-and-push in the same turn — the
  same-turn push binds a SELF-INITIATED main-session commit too,
  not only the verb — never split to ask "shall I push?" (that ask
  is the drift the unpushed-reminder Stop-hook catches); a
  deliberate hold (WIP series, operator hold) is stated in one
  line, never asked; "close the session" → CLEAN close, never
  stop-this-second: the made decision is the target state — work in
  flight is finished or backed out, never left mid-state, then the
  repo's close lane where one exists. What stays the operator's is
  the CUTOFF over owed-but-unstarted items: intent, so it travels
  as a numbered finish-vs-hand-off round with a recommendation each
  (the book-or-do absences, read at close), delivered BEFORE any
  wrap-up prose is written — a session that unilaterally books what
  it could cleanly finish inside the horizon the operator just
  opened has answered the round for them.
  (JOURNAL, operator verbs, 2026-08-26.)
