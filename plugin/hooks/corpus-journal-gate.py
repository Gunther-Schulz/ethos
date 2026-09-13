#!/usr/bin/env python3
"""Pre-commit check — a corpus edit lands with its journal line.

OPT-IN, AND SILENT UNTIL CONFIGURED. Installing ethos does not wire
this: nothing runs it, and with no configuration it exits 0 without
printing. That is deliberate — the corpus ships as rules, and a gate
that fired on an adopter who never asked for it would be the
guard-fires-on-a-non-defect class, which trains the override reflex
that kills the guard.

WHAT IT ENFORCES. The maintenance doctrine's build-first rule: every
mint, sharpen or retire lands with its candidate-in-operation line in
the journal carrier, in the SAME commit as the corpus edit, because
that line is the fire-rate review's consumer anchor and without it the
chain there is torn.

THE DECLARED ASSUMPTION, which this gate cannot check for you: a
journal carrier exists and you have told this gate where it is. Point
`git config ethos.journalCarrier <path>` at it, in the corpus repo.

THE HONEST LIMIT, stated here rather than implied by the name. Where
the carrier lives in the SAME repository as the corpus, "staged in
this commit" is checkable and is what gets checked. Where the carrier
lives in a DIFFERENT repository — the arrangement that arises when the
corpus modules travel to a public home and the journal stays
private — there is no shared index, so no commit-time check can prove
the pair. The most this gate establishes there is that the carrier was
STAGED IN ITS OWN REPO at the moment the corpus commit was made. It
cannot prove that staged line is ever committed, nor that it describes
this edit. An assurance no wider than its predicate: a corpus edit
whose carrier was never touched is refused; one whose carrier was
staged and then abandoned is not caught, and the report says so.

WHAT COUNTS AS CORPUS is DERIVED, never restated: the module bodies
named by modules/ORDER, plus the maintenance doctrine beside them. A
restated list stays green while the source gains a member.

EXIT CODES: 0 clean or not configured or out of scope; 2 violation
(refuse the commit); 0 on any could-not-verify, with the reason on
stderr — a gate that cannot read its own inputs must not block a
commit on a guess, and silence with a reason is honest where a refusal
would not be.

WIRING (the adopter's one step; nothing does this for you):
    <plugin>/hooks/corpus-journal-gate.py --repo "$(git rev-parse --show-toplevel)"
called from your pre-commit, its exit status honoured.
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN_ROOT = os.path.normpath(os.path.join(HERE, ".."))

CONFIG_KEY = "ethos.journalCarrier"
GOVERNOR_BASENAME = "CLAUDE-maintenance.md"
ORDER_REL = os.path.join("modules", "ORDER")

_TIMEOUT = 10


def _git(args, cwd):
    """(returncode, stdout) — or (None, "") when git cannot be run at
    all, which callers map to could-not-verify, never to clean."""
    try:
        p = subprocess.run(["git"] + args, cwd=cwd, capture_output=True,
                           text=True, timeout=_TIMEOUT)
    except (OSError, subprocess.SubprocessError):
        return None, ""
    return p.returncode, p.stdout


def plugin_root_in(repo):
    """The directory inside `repo` holding modules/ORDER, or None.

    This is the SCOPE MARKER, the same role a corpus-repo marker plays
    anywhere: absent it, the repo is not a corpus checkout and the gate
    is silent. Searched rather than hardcoded so a repo that vendors the
    payload at a different depth still resolves."""
    for base, dirs, _files in os.walk(repo):
        # do not descend into version-control or dependency trees
        dirs[:] = [d for d in dirs
                   if d not in (".git", "node_modules", "__pycache__")]
        if os.path.isfile(os.path.join(base, ORDER_REL)):
            return base
    return None


def corpus_relpaths(repo, plugin_root):
    """Repo-relative paths of the corpus files, derived from ORDER.

    Returns None when ORDER is unreadable — could-not-verify, not an
    empty set read as "nothing is corpus"."""
    order_file = os.path.join(plugin_root, ORDER_REL)
    try:
        with open(order_file, encoding="utf-8") as f:
            names = [ln.strip() for ln in f if ln.strip()]
    except OSError:
        return None
    modules_dir = os.path.join(plugin_root, "modules")
    out = set()
    for name in names:
        out.add(os.path.relpath(os.path.join(modules_dir, name + ".md"),
                                repo))
    governor = os.path.join(plugin_root, GOVERNOR_BASENAME)
    if os.path.isfile(governor):
        out.add(os.path.relpath(governor, repo))
    return out


def carrier_setting(repo):
    """The configured carrier path, or None when unset (= opt-out)."""
    rc, out = _git(["config", "--get", CONFIG_KEY], cwd=repo)
    if rc is None or rc != 0:
        return None
    value = out.strip()
    return value or None


def carrier_is_staged(carrier_path):
    """(verdict, detail). verdict True/False, or None for
    could-not-verify. True iff the carrier shows as staged in the
    repository that contains it — which may be this repo or another."""
    carrier_abs = os.path.abspath(os.path.expanduser(carrier_path))
    carrier_dir = os.path.dirname(carrier_abs)
    if not os.path.isdir(carrier_dir):
        return None, "carrier directory does not exist: %s" % carrier_dir
    rc, out = _git(["rev-parse", "--show-toplevel"], cwd=carrier_dir)
    if rc is None or rc != 0:
        return None, "carrier is not inside a git repository: %s" % carrier_abs
    carrier_repo = out.strip()
    rel = os.path.relpath(carrier_abs, carrier_repo)
    rc, out = _git(["diff", "--cached", "--name-only"], cwd=carrier_repo)
    if rc is None or rc != 0:
        return None, "cannot read the staged set of %s" % carrier_repo
    staged = {ln.strip() for ln in out.splitlines() if ln.strip()}
    return (rel in staged), carrier_repo


def check(repo):
    """(exit code, [lines to print]) for a commit in `repo`."""
    plugin_root = plugin_root_in(repo)
    if plugin_root is None:
        return 0, []                      # not a corpus checkout
    carrier = carrier_setting(repo)
    if carrier is None:
        return 0, []                      # opt-in: unconfigured is silent

    corpus = corpus_relpaths(repo, plugin_root)
    if corpus is None:
        return 0, ["ethos corpus-journal-gate: could not verify — "
                   "modules/ORDER unreadable; the commit is NOT blocked"]

    rc, out = _git(["diff", "--cached", "--name-only"], cwd=repo)
    if rc is None or rc != 0:
        return 0, ["ethos corpus-journal-gate: could not verify — "
                   "cannot read the staged set; the commit is NOT blocked"]
    staged = {ln.strip() for ln in out.splitlines() if ln.strip()}
    touched = sorted(staged & corpus)
    if not touched:
        return 0, []

    verdict, detail = carrier_is_staged(carrier)
    if verdict is None:
        return 0, ["ethos corpus-journal-gate: could not verify — %s; "
                   "the commit is NOT blocked" % detail]
    if verdict:
        return 0, []

    same_repo = os.path.abspath(detail) == os.path.abspath(repo)
    lines = ["",
             "Corpus file(s) staged with no journal line:",
             ]
    lines += ["  - %s" % t for t in touched]
    lines += ["",
              "Every mint, sharpen or retire lands with its",
              "candidate-in-operation line in the journal carrier, in the",
              "same commit as the corpus edit — that line is the fire-rate",
              "review's consumer anchor.",
              "",
              "  carrier: %s" % carrier,
              "  -> write the journal line and stage it."]
    if not same_repo:
        lines += ["",
                  "NOTE, so this gate is not read as wider than it is: the",
                  "carrier lives in another repository (%s), so there is no"
                  % detail,
                  "shared index and no commit-time check can prove the pair.",
                  "All this gate establishes is that the carrier is staged",
                  "THERE right now — not that the line is ever committed,",
                  "nor that it describes this edit."]
    return 2, lines


def main(argv):
    repo = None
    if "--repo" in argv:
        i = argv.index("--repo")
        if i + 1 < len(argv):
            repo = argv[i + 1]
    if repo is None:
        rc, out = _git(["rev-parse", "--show-toplevel"], cwd=os.getcwd())
        if rc is None or rc != 0:
            return 0
        repo = out.strip()
    code, lines = check(repo)
    for ln in lines:
        print(ln, file=sys.stderr)
    return code


# ------------------------------------------------------------------
# Self-check
# ------------------------------------------------------------------

def _mkrepo(path):
    os.makedirs(path, exist_ok=True)
    subprocess.run(["git", "init", "-q", path], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", path, "config", "user.email", "t@example"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", path, "config", "user.name", "t"],
                   check=True, capture_output=True)


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _corpus_repo(root, modules=("grounding", "fixing")):
    _mkrepo(root)
    pr = os.path.join(root, "plugin")
    _write(os.path.join(pr, "modules", "ORDER"), "\n".join(modules) + "\n")
    for m in modules:
        _write(os.path.join(pr, "modules", m + ".md"), "# %s\n" % m)
    _write(os.path.join(pr, GOVERNOR_BASENAME), "# doctrine\n")
    subprocess.run(["git", "-C", root, "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", root, "commit", "-q", "-m", "seed",
                    "--no-verify"], check=True, capture_output=True)
    return pr


def _stage(repo, rel, text):
    _write(os.path.join(repo, rel), text)
    subprocess.run(["git", "-C", repo, "add", rel], check=True,
                   capture_output=True)


def _selftest_unconfigured_is_silent():
    """THE OPT-IN DEFAULT, and the row that matters most for an adopter
    who never asked for this gate: a corpus edit with NO configuration
    passes, silently."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = os.path.join(d, "corpus")
        _corpus_repo(root)
        _stage(root, "plugin/modules/grounding.md", "# grounding\nnew\n")
        code, lines = check(root)
        assert code == 0 and lines == [], (code, lines)


def _selftest_non_corpus_repo_is_silent():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = os.path.join(d, "plain")
        _mkrepo(root)
        _write(os.path.join(root, "a.md"), "x\n")
        subprocess.run(["git", "-C", root, "add", "a.md"], check=True,
                       capture_output=True)
        code, lines = check(root)
        assert code == 0 and lines == [], (code, lines)


def _selftest_same_repo_pair():
    """Carrier in the SAME repo: unstaged -> refused, staged -> clean.
    The two arms must DIFFER, or neither proves anything."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = os.path.join(d, "corpus")
        _corpus_repo(root)
        _write(os.path.join(root, "JOURNAL.md"), "log\n")
        subprocess.run(["git", "-C", root, "add", "JOURNAL.md"], check=True,
                       capture_output=True)
        subprocess.run(["git", "-C", root, "commit", "-q", "-m", "j",
                        "--no-verify"], check=True, capture_output=True)
        subprocess.run(["git", "-C", root, "config", CONFIG_KEY,
                        os.path.join(root, "JOURNAL.md")], check=True,
                       capture_output=True)

        _stage(root, "plugin/modules/grounding.md", "# grounding\nnew\n")
        red, red_lines = check(root)
        assert red == 2, (red, red_lines)
        assert any("no journal line" in ln for ln in red_lines), red_lines
        assert not any("another repository" in ln for ln in red_lines), \
            "same-repo case must not print the cross-repo limit"

        _stage(root, "JOURNAL.md", "log\nnew line\n")
        green, green_lines = check(root)
        assert green == 0 and green_lines == [], (green, green_lines)
        assert red != green, "the two arms must differ"


def _selftest_cross_repo_limit_is_stated():
    """Carrier in ANOTHER repo: still refused when untouched, and the
    refusal SAYS what it cannot prove."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = os.path.join(d, "corpus")
        _corpus_repo(root)
        side = os.path.join(d, "private")
        _mkrepo(side)
        _write(os.path.join(side, "JOURNAL.md"), "log\n")
        subprocess.run(["git", "-C", side, "add", "JOURNAL.md"], check=True,
                       capture_output=True)
        subprocess.run(["git", "-C", side, "commit", "-q", "-m", "j",
                        "--no-verify"], check=True, capture_output=True)
        subprocess.run(["git", "-C", root, "config", CONFIG_KEY,
                        os.path.join(side, "JOURNAL.md")], check=True,
                       capture_output=True)

        _stage(root, "plugin/modules/fixing.md", "# fixing\nnew\n")
        code, lines = check(root)
        assert code == 2, (code, lines)
        assert any("another repository" in ln for ln in lines), lines
        assert any("not that the line is ever committed" in ln
                   for ln in lines), lines

        _stage(side, "JOURNAL.md", "log\nnew\n")
        code2, lines2 = check(root)
        assert code2 == 0 and lines2 == [], (code2, lines2)


def _selftest_governor_is_corpus():
    """The doctrine beside the modules is coupled too — it is the file
    that SETS UP the requirement, so it is not exempt from it."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = os.path.join(d, "corpus")
        _corpus_repo(root)
        _write(os.path.join(root, "JOURNAL.md"), "log\n")
        subprocess.run(["git", "-C", root, "add", "JOURNAL.md"], check=True,
                       capture_output=True)
        subprocess.run(["git", "-C", root, "commit", "-q", "-m", "j",
                        "--no-verify"], check=True, capture_output=True)
        subprocess.run(["git", "-C", root, "config", CONFIG_KEY,
                        os.path.join(root, "JOURNAL.md")], check=True,
                       capture_output=True)
        _stage(root, "plugin/" + GOVERNOR_BASENAME, "# doctrine\nnew\n")
        code, lines = check(root)
        assert code == 2, (code, lines)


def _selftest_membership_derived_not_restated():
    """A module ADDED to ORDER is coupled immediately, with no edit
    here — the property a restated list would lose."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = os.path.join(d, "corpus")
        pr = _corpus_repo(root)
        _write(os.path.join(pr, "modules", "ORDER"),
               "grounding\nfixing\nseventh\n")
        _write(os.path.join(pr, "modules", "seventh.md"), "# seventh\n")
        rels = corpus_relpaths(root, pr)
        assert os.path.join("plugin", "modules", "seventh.md") in rels, rels


def _selftest_non_corpus_edit_passes():
    """A NON-corpus file in a configured corpus repo is not coupled —
    the must-NOT-fire row. Without it, a gate that simply refuses every
    commit would score identically to a correct one."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = os.path.join(d, "corpus")
        _corpus_repo(root)
        _write(os.path.join(root, "JOURNAL.md"), "log\n")
        subprocess.run(["git", "-C", root, "add", "JOURNAL.md"], check=True,
                       capture_output=True)
        subprocess.run(["git", "-C", root, "commit", "-q", "-m", "j",
                        "--no-verify"], check=True, capture_output=True)
        subprocess.run(["git", "-C", root, "config", CONFIG_KEY,
                        os.path.join(root, "JOURNAL.md")], check=True,
                       capture_output=True)
        _stage(root, "README.md", "# readme\n")
        code, lines = check(root)
        assert code == 0 and lines == [], (code, lines)


def _selftest_missing_carrier_is_could_not_verify():
    """A configured carrier that does not exist must NOT block: a gate
    that cannot read its inputs refuses nothing and says why."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = os.path.join(d, "corpus")
        _corpus_repo(root)
        subprocess.run(["git", "-C", root, "config", CONFIG_KEY,
                        os.path.join(d, "nowhere", "JOURNAL.md")],
                       check=True, capture_output=True)
        _stage(root, "plugin/modules/grounding.md", "# grounding\nnew\n")
        code, lines = check(root)
        assert code == 0, (code, lines)
        assert any("could not verify" in ln for ln in lines), lines


def _selftest():
    _selftest_unconfigured_is_silent()
    _selftest_non_corpus_repo_is_silent()
    _selftest_same_repo_pair()
    _selftest_cross_repo_limit_is_stated()
    _selftest_governor_is_corpus()
    _selftest_membership_derived_not_restated()
    _selftest_non_corpus_edit_passes()
    _selftest_missing_carrier_is_could_not_verify()
    print("corpus-journal-gate: all tests passed")


if __name__ == "__main__":
    if "--test" in sys.argv:
        _selftest()
        sys.exit(0)
    sys.exit(main(sys.argv[1:]))
