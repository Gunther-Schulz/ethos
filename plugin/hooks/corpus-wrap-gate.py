#!/usr/bin/env python3
"""Pre-commit check — corpus module lines stay within the 69-column wrap.

WHAT IT ENFORCES. This corpus's own stated wrap convention (the
environment module's grep bullet: "over hard-wrapped prose (this
corpus: 69 columns)") is a load-bearing premise, not a style
preference: the overlay-disjointness check's wrap-normalization
un-wraps paragraphs by rejoining hard-wrapped lines, and any
line-based phrase search over the corpus is blind across a wrap it
does not expect. A line that quietly drifts past 69 columns degrades
both silently — this gate makes the drift loud at commit time
instead.

SCOPE, DERIVED not restated. Exactly corpus-journal-gate's own
derivation — plugin/modules/*.md (named by modules/ORDER) plus
plugin/CLAUDE-maintenance.md — imported from that sibling module
rather than re-typed, so a corpus that gains or loses a module stays
in sync at one source (this corpus's own composition rule: "WHAT
COUNTS AS CORPUS is DERIVED, never restated").

EXIT CODES: 0 clean, not a corpus checkout, or could-not-verify
(reason on stderr, never blocking); 2 violation (refuse the commit) —
the same scheme as corpus-journal-gate.py.

WIRING (the adopter's one step; nothing does this for you):
    <plugin>/hooks/corpus-wrap-gate.py --repo "$(git rev-parse --show-toplevel)"
called from your pre-commit, its exit status honoured. This script is
runnable standalone with no wiring at all — invoke it directly against
any repo path via --repo.
"""

import importlib.util
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_CJG_PATH = os.path.join(HERE, "corpus-journal-gate.py")


def _load_cjg():
    """corpus-journal-gate.py, loaded by path (its filename is not a
    valid module identifier) for its plugin_root_in/corpus_relpaths —
    and, self-test only, its tiny repo-fixture helpers."""
    spec = importlib.util.spec_from_file_location(
        "_ethos_corpus_journal_gate", _CJG_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_cjg = _load_cjg()
plugin_root_in = _cjg.plugin_root_in
corpus_relpaths = _cjg.corpus_relpaths

WRAP_LIMIT = 69
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


def staged_text(repo, rel):
    """Staged (index) content of `rel`, or None if unreadable or
    deleted from the index."""
    rc, out = _git(["show", ":%s" % rel], cwd=repo)
    if rc is None or rc != 0:
        return None
    return out


def wide_lines(text, limit=WRAP_LIMIT):
    """[(line_no, line)] for lines over `limit` columns."""
    return [(i, ln) for i, ln in enumerate(text.splitlines(), start=1)
            if len(ln) > limit]


def check(repo, limit=WRAP_LIMIT):
    """(exit code, [lines to print]) for a commit in `repo`."""
    plugin_root = plugin_root_in(repo)
    if plugin_root is None:
        return 0, []                      # not a corpus checkout
    corpus = corpus_relpaths(repo, plugin_root)
    if corpus is None:
        return 0, ["ethos corpus-wrap-gate: could not verify — "
                   "modules/ORDER unreadable; the commit is NOT blocked"]

    rc, out = _git(["diff", "--cached", "--name-only"], cwd=repo)
    if rc is None or rc != 0:
        return 0, ["ethos corpus-wrap-gate: could not verify — "
                   "cannot read the staged set; the commit is NOT blocked"]
    staged = {ln.strip() for ln in out.splitlines() if ln.strip()}
    touched = sorted(staged & corpus)

    violations = []
    for rel in touched:
        text = staged_text(repo, rel)
        if text is None:
            continue
        wide = wide_lines(text, limit)
        if wide:
            violations.append((rel, wide))
    if not violations:
        return 0, []

    lines = ["", "Corpus line(s) over the %d-column wrap:" % limit, ""]
    for rel, wide in violations:
        for i, ln in wide:
            shown = ln if len(ln) <= 100 else ln[:97] + "..."
            lines.append("  %s:%d (%d cols): %s" % (rel, i, len(ln), shown))
    lines += ["",
              "The corpus's own hard-wrap convention (69 columns) is",
              "what the overlay-disjointness check's wrap-normalization",
              "— and any line-based phrase search over the corpus —",
              "assumes. Re-wrap the line(s) above before committing."]
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

def _selftest_non_corpus_repo_is_silent():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = os.path.join(d, "plain")
        _cjg._mkrepo(root)
        _cjg._write(os.path.join(root, "a.md"), "x" * 200 + "\n")
        subprocess.run(["git", "-C", root, "add", "a.md"], check=True,
                       capture_output=True)
        code, lines = check(root)
        assert code == 0 and lines == [], (code, lines)


def _selftest_wide_line_in_corpus_module_fires():
    """RED-FIRST — a planted wide line in a staged corpus module."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = os.path.join(d, "corpus")
        _cjg._corpus_repo(root)
        wide = "x" * 90
        _cjg._stage(root, "plugin/modules/grounding.md",
                    "# grounding\n" + wide + "\n")
        code, lines = check(root)
        assert code == 2, (code, lines)
        assert any("90 cols" in ln for ln in lines), lines
        assert any("plugin/modules/grounding.md:2" in ln for ln in lines), lines


def _selftest_non_corpus_file_in_corpus_repo_is_silent():
    """MUST-NOT-FIRE control, paired against the red case above: the
    same repo, the same wide line, staged in a file the corpus does
    NOT claim — a gate that simply refused every commit would score
    identically to a correct one without this row."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = os.path.join(d, "corpus")
        _cjg._corpus_repo(root)
        wide = "x" * 90
        _cjg._stage(root, "README.md", wide + "\n")
        code, lines = check(root)
        assert code == 0 and lines == [], (code, lines)


def _selftest_within_limit_is_clean():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = os.path.join(d, "corpus")
        _cjg._corpus_repo(root)
        _cjg._stage(root, "plugin/modules/grounding.md",
                    "# grounding\n" + ("x" * WRAP_LIMIT) + "\n")
        code, lines = check(root)
        assert code == 0 and lines == [], (code, lines)


def _selftest_governor_is_scoped_too():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = os.path.join(d, "corpus")
        _cjg._corpus_repo(root)
        wide = "y" * 80
        _cjg._stage(root, "plugin/" + _cjg.GOVERNOR_BASENAME,
                    "# doctrine\n" + wide + "\n")
        code, lines = check(root)
        assert code == 2, (code, lines)


def _selftest_missing_order_is_could_not_verify():
    """plugin_root_in() only checks os.path.isfile(ORDER) (the scope
    marker), so ORDER must EXIST and be a regular file to resolve a
    plugin root at all; corpus_relpaths() then separately opens it for
    content. Un-readable (not merely absent) is what isolates that
    second failure: chmod 000 leaves isfile() true and open() raising
    OSError, caught by corpus_relpaths' own could-not-verify path."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = os.path.join(d, "corpus")
        pr = os.path.join(root, "plugin")
        _cjg._mkrepo(root)
        order_path = os.path.join(pr, "modules", "ORDER")
        _cjg._write(order_path, "grounding\n")
        _cjg._write(os.path.join(pr, "modules", "grounding.md"), "# g\n")
        subprocess.run(["git", "-C", root, "add", "-A"], check=True,
                       capture_output=True)
        os.chmod(order_path, 0o000)
        try:
            code, lines = check(root)
        finally:
            os.chmod(order_path, 0o644)
        assert code == 0, (code, lines)
        assert any("could not verify" in ln for ln in lines), lines


def _selftest():
    _selftest_non_corpus_repo_is_silent()
    _selftest_wide_line_in_corpus_module_fires()
    _selftest_non_corpus_file_in_corpus_repo_is_silent()
    _selftest_within_limit_is_clean()
    _selftest_governor_is_scoped_too()
    _selftest_missing_order_is_could_not_verify()
    print("corpus-wrap-gate: all tests passed")


if __name__ == "__main__":
    if "--test" in sys.argv:
        _selftest()
        sys.exit(0)
    sys.exit(main(sys.argv[1:]))
