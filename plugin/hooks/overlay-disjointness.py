#!/usr/bin/env python3
"""Overlap/drift check — an overlay clause that RESTATES its portable core.

WHAT IT ENFORCES. The overlay pattern's declared contract (this
corpus's composition rule, self-containment; each site overlay's own
header, once this check ships): a site overlay FILLS the portable
core's role-names with local artifacts and RESTATES NOTHING. Today
nothing mechanical holds that line — an overlay clause that drifts
into restating a core rule (in its own words, or copied and merely
rewrapped) degrades silently, the paraphrase-drift class.

WHAT IT CHECKS. Given a core text and an overlay text, each first
WRAP- AND CASE-NORMALIZED (hard-wrapped paragraphs rejoined into one
line per paragraph, then lowercased — this corpus's own stated search
bindings: a line-based phrase scan is blind across the wrap and to
case), the overlay is split into SENTENCES (clause-level units), and
each sentence at or above a minimum length is tested for exact
SUBSTRING membership in the normalized core blob. A hit is a finding:
the overlay states, verbatim after normalization, something the core
already states. This is the FLOOR, deliberately: exact substring
after normalization, nothing semantic — a paraphrase in different
words is not caught here, and is not claimed to be (composition rule,
self-containment: an assurance no wider than its predicate).

The minimum-length floor (MIN_CLAUSE_CHARS, normalized) is what keeps
a genuinely site-bound fact — a path, a version, a short instrument
name — from firing: such lines are short and specific, so they do not
happen to appear verbatim, at a length that matters, inside the
core's own prose. It is not a semantic carve-out; it is why the
must-not-fire control below passes.

TWO SHAPES, one check. An "instance" is (core region, overlay
region), each independently a whole file or a markdown SECTION of one
(a heading line through the next heading at the same-or-shallower
depth, or EOF) — so the same check covers a split-file pair
(--core FILE --overlay FILE) and a same-file split
(--core FILE --overlay FILE --overlay-heading "## Site overlay", core
and overlay the SAME path: the core region is then the file's text
with the sliced overlay section removed).

EXIT CODES: 0 clean (no restatements found); 1 findings (overlay
clauses restate the core — surfaced for disposition, never
auto-fixed); 2 unreadable (a path is missing, or a named heading is
not found in its file — could-not-verify, distinct from a clean
result).

WIRING: this is a standalone CLI, wiring-independent of any repo's
pre-commit — run it directly:
    overlay-disjointness.py --core <core-file> --overlay <overlay-file>
    overlay-disjointness.py --core <file> --overlay <file> \\
        --overlay-heading "## Site overlay"
"""

import os
import re
import sys

# Normalized-character floor for a candidate overlay clause. See the
# docstring: this is what keeps a short site-bound fact (a path, a
# version) from firing, without resorting to any semantic carve-out.
MIN_CLAUSE_CHARS = 60


# ------------------------------------------------------------------
# Heading-section slicing
# ------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#+)\s+(.*\S)\s*$")


def _heading_level(line):
    m = _HEADING_RE.match(line)
    return len(m.group(1)) if m else None


def slice_heading_section(text, heading_text):
    """(start, end) 0-based line indices [start, end) for the section
    opened by a line whose stripped text STARTS WITH `heading_text`
    (after stripping) — a prefix match, not exact equality, because a
    real heading routinely carries a trailing qualifier ("## Site
    overlay — this installation's bindings") that an exact match would
    miss — through the next heading at the same or shallower depth, or
    EOF. None if no such heading is found."""
    lines = text.splitlines()
    start = None
    level = None
    needle = heading_text.strip()
    for i, ln in enumerate(lines):
        stripped = ln.strip()
        if stripped.startswith(needle) and _heading_level(ln) is not None:
            start = i
            level = _heading_level(ln)
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        lv = _heading_level(lines[j])
        if lv is not None and lv <= level:
            end = j
            break
    return start, end


def read_text(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def region_text(path, heading=None, exclude_heading_of=None):
    """The text of `path`, optionally sliced to the section opened by
    `heading`, or with that section's slice from `exclude_heading_of`
    REMOVED (used for a same-file core: everything but the overlay
    section). None on an unreadable path or an unresolved heading —
    could-not-verify, never treated as empty-and-clean."""
    text = read_text(path)
    if text is None:
        return None
    lines = text.splitlines()
    if heading is not None:
        bounds = slice_heading_section(text, heading)
        if bounds is None:
            return None
        return "\n".join(lines[bounds[0]:bounds[1]])
    if exclude_heading_of is not None:
        bounds = slice_heading_section(text, exclude_heading_of)
        if bounds is None:
            return None
        return "\n".join(lines[:bounds[0]] + lines[bounds[1]:])
    return text


def load_core_and_overlay(core_path, overlay_path, overlay_heading):
    """((core_text, overlay_text), None) or (None, reason)."""
    if overlay_heading is not None:
        overlay_text = region_text(overlay_path, heading=overlay_heading)
        if overlay_text is None:
            return None, ("overlay heading %r not found in %s (or the "
                          "file is unreadable)" % (overlay_heading, overlay_path))
        same_file = os.path.abspath(core_path) == os.path.abspath(overlay_path)
        if same_file:
            core_text = region_text(core_path, exclude_heading_of=overlay_heading)
        else:
            core_text = read_text(core_path)
    else:
        overlay_text = read_text(overlay_path)
        core_text = read_text(core_path)
    if core_text is None:
        return None, "core unreadable: %s" % core_path
    if overlay_text is None:
        return None, "overlay unreadable: %s" % overlay_path
    return (core_text, overlay_text), None


# ------------------------------------------------------------------
# Wrap/case normalization and clause splitting
# ------------------------------------------------------------------

def _paragraphs(text):
    """[(first_line_no, joined_text)] — blank-line-delimited
    paragraphs, each block's lines rejoined with a single space
    (undoing the hard wrap). 1-based first line number, kept for
    reporting."""
    lines = text.splitlines()
    out = []
    buf = []
    buf_start = None
    for i, ln in enumerate(lines, start=1):
        if ln.strip() == "":
            if buf:
                out.append((buf_start, " ".join(buf)))
                buf = []
                buf_start = None
            continue
        if buf_start is None:
            buf_start = i
        buf.append(ln.strip())
    if buf:
        out.append((buf_start, " ".join(buf)))
    return out


_WS_RE = re.compile(r"\s+")


def normalize(s):
    """Case- and whitespace-normalized: lowercased, runs of
    whitespace collapsed to one space. The wrap half is done by
    _paragraphs() joining hard-wrapped lines BEFORE this runs; this
    handles the residual (list-marker indentation, doubled spaces)."""
    return _WS_RE.sub(" ", s.strip().lower())


_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?;])\s+")


def clauses(text):
    """[(line_no, normalized_clause)] for every sentence/clause-level
    unit in `text`'s paragraphs, normalized for wrap and case."""
    out = []
    for line_no, para in _paragraphs(text):
        norm_para = normalize(para)
        for part in _SENTENCE_SPLIT_RE.split(norm_para):
            part = part.strip()
            if part:
                out.append((line_no, part))
    return out


def find_restatements(core_text, overlay_text, min_chars=MIN_CLAUSE_CHARS):
    """[(line_no, clause)] — overlay clauses at/above `min_chars`
    (normalized) that appear verbatim in the normalized core blob."""
    core_blob = normalize(" ".join(p for _, p in _paragraphs(core_text)))
    out = []
    for line_no, clause in clauses(overlay_text):
        if len(clause) < min_chars:
            continue
        if clause in core_blob:
            out.append((line_no, clause))
    return out


def check(core_path, overlay_path, overlay_heading=None,
          min_chars=MIN_CLAUSE_CHARS):
    """(exit code, [lines to print])."""
    loaded, err = load_core_and_overlay(core_path, overlay_path, overlay_heading)
    if loaded is None:
        return 2, ["overlay-disjointness: could not verify — %s" % err]
    core_text, overlay_text = loaded
    findings = find_restatements(core_text, overlay_text, min_chars)
    if not findings:
        return 0, []
    lines = ["",
             "Overlay clauses that RESTATE the portable core (%s):" % overlay_path,
             ""]
    for line_no, clause in findings:
        shown = clause if len(clause) <= 160 else clause[:157] + "..."
        lines.append("  line ~%d: %s" % (line_no, shown))
    lines += ["",
              "A site overlay fills the core's role-names; it never",
              "restates a core clause. Amend the overlay (name the",
              "artifact, drop the restated rule) or, if the rule truly",
              "belongs in both, source-label it explicitly in each home",
              "(corpus composition rule, Corpus-wide amendment audit)."]
    return 1, lines


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

def _arg(argv, name):
    if name in argv:
        i = argv.index(name)
        if i + 1 < len(argv):
            return argv[i + 1]
    return None


def main(argv):
    core = _arg(argv, "--core")
    overlay = _arg(argv, "--overlay")
    overlay_heading = _arg(argv, "--overlay-heading")
    min_chars_raw = _arg(argv, "--min-chars")
    if core is None or overlay is None:
        print("usage: overlay-disjointness.py --core FILE --overlay FILE "
              "[--overlay-heading HEADING] [--min-chars N]", file=sys.stderr)
        return 2
    kwargs = {}
    if overlay_heading is not None:
        kwargs["overlay_heading"] = overlay_heading
    if min_chars_raw is not None:
        try:
            kwargs["min_chars"] = int(min_chars_raw)
        except ValueError:
            print("overlay-disjointness: --min-chars must be an integer",
                  file=sys.stderr)
            return 2
    code, lines = check(core, overlay, **kwargs)
    for ln in lines:
        print(ln)
    return code


# ------------------------------------------------------------------
# Self-check
# ------------------------------------------------------------------

def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _selftest_split_files_red_first():
    """RED-FIRST, instance shape 1 (split files): a planted overlay
    sentence that restates a core sentence, wrapped differently AND
    case-shifted, must fire."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        core = os.path.join(d, "core.md")
        overlay = os.path.join(d, "overlay.md")
        _write(core, "# Core\n\n"
               "A site overlay fills the portable core's role-names "
               "with local artifacts and restates nothing from it.\n")
        _write(overlay, "# Overlay\n\n"
               "A SITE OVERLAY fills the portable core's\n"
               "role-names with local artifacts and restates nothing\n"
               "from it.\n")
        code, lines = check(core, overlay)
        assert code == 1, (code, lines)
        assert any("site overlay fills the portable core" in ln
                   for ln in lines), lines


def _selftest_same_file_section_red_first():
    """RED-FIRST, instance shape 2 (same file, heading-split): a
    "## Site overlay" section restating a portable-core sentence
    above it, wrapped and case-shifted, must fire — and the core
    region must exclude the overlay's own text (else the overlay
    would trivially "restate" itself)."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "routing.md")
        _write(path,
               "# Tier routing\n\n"
               "Brief-covered execution and discovery default to the "
               "cheapest daily tier in every installation.\n\n"
               "## Site overlay\n\n"
               "BRIEF-COVERED EXECUTION AND DISCOVERY\n"
               "DEFAULT TO THE CHEAPEST DAILY TIER in every\n"
               "installation. The cheapest daily tier here is sonnet.\n")
        code, lines = check(path, path, overlay_heading="## Site overlay")
        assert code == 1, (code, lines)
        assert any("brief-covered execution and discovery default" in ln
                   for ln in lines), lines


def _selftest_must_not_fire_site_bound_control():
    """MUST-NOT-FIRE control, paired against the two red cases above:
    a legitimately site-bound line (a path, a version) states a fact
    the core never states verbatim, and must not fire — the same
    substring test, on content that genuinely does not restate."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        core = os.path.join(d, "core.md")
        overlay = os.path.join(d, "overlay.md")
        _write(core, "# Core\n\n"
               "The journal carrier lives beside the overlay; name "
               "it in the overlay, never here.\n")
        _write(overlay, "# Overlay\n\n"
               "The journal carrier is claude/JOURNAL.md, version\n"
               "0.2.89.\n")
        code, lines = check(core, overlay)
        assert code == 0 and lines == [], (code, lines)


def _selftest_paraphrase_not_semantically_matched():
    """The stated floor: exact substring after normalization, nothing
    semantic. A same-MEANING, different-WORDING overlay clause must
    NOT fire — this is the deliberate limit, not a defect."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        core = os.path.join(d, "core.md")
        overlay = os.path.join(d, "overlay.md")
        _write(core, "# Core\n\n"
               "A site overlay fills the portable core's role-names "
               "with local artifacts and restates nothing from it.\n")
        _write(overlay, "# Overlay\n\n"
               "This file supplies the concrete paths and instruments "
               "that the shared doctrine leaves as named roles.\n")
        code, lines = check(core, overlay)
        assert code == 0 and lines == [], (code, lines)


def _selftest_short_clause_below_floor_does_not_fire():
    """A short shared phrase, present verbatim in both but under
    MIN_CLAUSE_CHARS, must not fire — isolates the length floor from
    the substring test."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        core = os.path.join(d, "core.md")
        overlay = os.path.join(d, "overlay.md")
        _write(core, "# Core\n\nThe corpus is the corpus.\n")
        _write(overlay, "# Overlay\n\nSee the corpus.\n")
        code, lines = check(core, overlay)
        assert code == 0 and lines == [], (code, lines)


def _selftest_clean_pair_no_restatement():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        core = os.path.join(d, "core.md")
        overlay = os.path.join(d, "overlay.md")
        _write(core, "# Core\n\n"
               "Every mint or amendment reads its home section's "
               "neighbors and tests for contradiction on a concrete "
               "case.\n")
        _write(overlay, "# Overlay\n\n"
               "The neighbor-collision instrument at this site is "
               "tools/neighbor-check.py, run over the staged diff.\n")
        code, lines = check(core, overlay)
        assert code == 0 and lines == [], (code, lines)


def _selftest_unreadable_path_is_could_not_verify():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        core = os.path.join(d, "core.md")
        _write(core, "# Core\n")
        code, lines = check(core, os.path.join(d, "nowhere.md"))
        assert code == 2, (code, lines)
        assert any("could not verify" in ln for ln in lines), lines


def _selftest_missing_heading_is_could_not_verify():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "routing.md")
        _write(path, "# Tier routing\n\nBody text, no site section.\n")
        code, lines = check(path, path, overlay_heading="## Site overlay")
        assert code == 2, (code, lines)
        assert any("could not verify" in ln for ln in lines), lines


def _selftest():
    _selftest_split_files_red_first()
    _selftest_same_file_section_red_first()
    _selftest_must_not_fire_site_bound_control()
    _selftest_paraphrase_not_semantically_matched()
    _selftest_short_clause_below_floor_does_not_fire()
    _selftest_clean_pair_no_restatement()
    _selftest_unreadable_path_is_could_not_verify()
    _selftest_missing_heading_is_could_not_verify()
    print("overlay-disjointness: all tests passed")


if __name__ == "__main__":
    if "--test" in sys.argv:
        _selftest()
        sys.exit(0)
    sys.exit(main(sys.argv[1:]))
