#!/usr/bin/env python3
"""SessionStart hook — verifies the ethos corpus's @-import delivery.

Supersedes inject-ethos.py (this plugin's v1 build). Measured after that
build shipped (dotfiles claude/records/corpus-portability-2026-09-13.md,
"Phase-1 verdict"): the harness truncates oversized SessionStart hook
stdout to a small preview plus a file pointer, and the six ethos modules
run to ~83KB — well past that threshold — so injecting them as hook
output never delivered the corpus at all, whatever this hook's own
stdout claimed. The corpus instead travels as `@`-import lines that
`scripts/install-imports.sh` resolves to absolute paths and writes into
the user's CLAUDE.md at install time (the one channel proven, on this
stack, to deliver content this size in full — the daily corpus loads
through it). This hook's only job is to VERIFY that delivery still
holds. It never injects the corpus itself, and its own output stays
comfortably under the same truncation threshold that made injection
unworkable in the first place — a verifier whose own warning got
truncated would be the same defect one level down, so this script's
longest possible output (six missing-module lines, the worst case) is
nowhere near 2000 bytes and there is no cap logic here to get wrong.

Healthy: the marked import block
(`# >>> ethos imports (managed by ethos install-imports.sh) >>>` …
`# <<< ethos imports <<<`) is present in the target CLAUDE.md, names
exactly the six modules in the corpus's own table order, each resolved
path exists on disk, and each resolves to THIS hook's own plugin root's
modules/ directory. That last check is what catches a version upgrade
that moved the plugin's install path out from under an import block
written for the old version — a stale block would otherwise degrade
silently, since the paths it names go on existing (they still point at
SOME installed version's modules) while ceasing to be what this running
hook itself was shipped with.

Unhealthy (any one of): the target CLAUDE.md is missing (counted as
block-missing, not a crash), the block is missing or malformed, the
block doesn't name exactly the six expected modules in order, an
imported path does not exist on disk, or an imported path resolves
outside this plugin's own modules/ directory. One short warning naming
exactly what is wrong, plus the verbatim fix command — the absolute
path to install-imports.sh and the target CLAUDE.md path, both resolved
by this hook itself, so the printed command is directly runnable with
no substitution needed.

Exit 0 always — a verifier must never be able to block a session from
starting.
"""

import json
import os
import sys

VERSION = "0.1.0"

MODULE_ORDER = [
    "grounding",
    "fixing",
    "calibration",
    "insurance",
    "reporting",
    "accretion",
]

BEGIN_MARKER = "# >>> ethos imports (managed by ethos install-imports.sh) >>>"
END_MARKER = "# <<< ethos imports <<<"

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN_ROOT = os.path.normpath(os.path.join(HERE, ".."))
MODULES_DIR = os.path.join(PLUGIN_ROOT, "modules")
INSTALL_SCRIPT = os.path.join(PLUGIN_ROOT, "scripts", "install-imports.sh")


# Rebound by the self-test only (_run_main), never in production use:
# lets the battery point at a fixture directory instead of the real
# ~/.claude without touching the CLAUDE_CONFIG_DIR env var itself.
_CONFIG_DIR_OVERRIDE = None


def config_dir():
    if _CONFIG_DIR_OVERRIDE is not None:
        return _CONFIG_DIR_OVERRIDE
    env = os.environ.get("CLAUDE_CONFIG_DIR")
    if env:
        return env
    return os.path.join(os.path.expanduser("~"), ".claude")


def target_claude_md():
    return os.path.join(config_dir(), "CLAUDE.md")


def extract_block(text):
    """[@-line path strings] between the markers, or None when the block
    is absent or malformed (out of order, nested, unbalanced) — a
    corrupted block is not a delivered corpus either, so it is graded
    the same as no block at all."""
    lines = text.splitlines()
    start = None
    end = None
    for i, ln in enumerate(lines):
        stripped = ln.strip()
        if stripped == BEGIN_MARKER:
            if start is not None:
                return None
            start = i
        elif stripped == END_MARKER:
            if start is None or end is not None:
                return None
            end = i
    if start is None or end is None or end <= start:
        return None
    body = [ln.strip() for ln in lines[start + 1:end]]
    paths = [ln[1:].strip() for ln in body if ln.startswith("@")]
    non_at = [ln for ln in body if ln and not ln.startswith("@")]
    if non_at:
        return None
    return paths


def diagnose():
    """(healthy, detail) — detail is empty on healthy, else the one
    warning reason."""
    target = target_claude_md()
    if not os.path.isfile(target):
        return False, "CLAUDE.md not found at %s" % target
    try:
        with open(target, encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError as exc:
        return False, "cannot read %s: %s" % (target, exc)

    paths = extract_block(text)
    if paths is None:
        return False, "ethos import block missing or malformed in %s" % target
    if len(paths) != len(MODULE_ORDER):
        return False, (
            "ethos import block in %s has %d import line(s), expected %d"
            % (target, len(paths), len(MODULE_ORDER)))

    expected_dir = os.path.realpath(MODULES_DIR)
    for name, path in zip(MODULE_ORDER, paths):
        want_base = name + ".md"
        if os.path.basename(path) != want_base:
            return False, (
                "ethos import block in %s is out of order or missing %s"
                % (target, want_base))
        if not os.path.isfile(path):
            return False, "imported module missing on disk: %s" % path
        got_dir = os.path.realpath(os.path.dirname(path))
        if got_dir != expected_dir:
            return False, (
                "imported path %s resolves outside this plugin's own "
                "modules/ (stale path after a plugin update?)" % path)
    return True, ""


def main():
    # Read and discard stdin so the harness never sees a broken pipe;
    # the target is the user's CLAUDE.md, never the session's cwd, so
    # the hook payload itself carries nothing this check needs.
    try:
        json.load(sys.stdin)
    except (ValueError, OSError):
        pass

    healthy, detail = diagnose()
    if healthy:
        print("ethos v%s: corpus delivered via CLAUDE.md import block "
              "(%d modules verified)" % (VERSION, len(MODULE_ORDER)))
        return 0

    print("ethos v%s WARNING: %s" % (VERSION, detail))
    print("Fix: %s %s" % (INSTALL_SCRIPT, target_claude_md()))
    return 0


# ------------------------------------------------------------------
# Self-check
# ------------------------------------------------------------------

def _run_main(payload, config_dir_override):
    """(exit code, stdout) from main() with CONFIG_DIR rebound to a
    fixture and stdin fed `payload` (a dict, JSON-encoded)."""
    import contextlib
    import io

    global _CONFIG_DIR_OVERRIDE
    old_override = _CONFIG_DIR_OVERRIDE
    _CONFIG_DIR_OVERRIDE = config_dir_override
    old_stdin = sys.stdin
    out = io.StringIO()
    try:
        sys.stdin = io.StringIO(json.dumps(payload))
        with contextlib.redirect_stdout(out):
            ret = main()
    finally:
        sys.stdin = old_stdin
        _CONFIG_DIR_OVERRIDE = old_override
    return ret, out.getvalue()


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _valid_block(modules_dir):
    lines = [BEGIN_MARKER]
    for name in MODULE_ORDER:
        lines.append("@" + os.path.join(modules_dir, name + ".md"))
    lines.append(END_MARKER)
    return "\n".join(lines) + "\n"


def _selftest_healthy_line_under_2000_bytes():
    """BITE — a correctly-installed block yields exactly one confirmation
    line, well under the 2000-byte budget this hook is built never to
    need a cap for."""
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        cfg = os.path.join(d, "claude-config")
        _write(os.path.join(cfg, "CLAUDE.md"),
               "# prose before\n\n" + _valid_block(MODULES_DIR)
               + "\n# prose after\n")
        ret, out = _run_main({"cwd": d}, cfg)
        assert ret == 0, (ret, out)
        assert out.startswith("ethos v%s: corpus delivered" % VERSION), out
        assert "6 modules verified" in out, out
        assert len(out.encode("utf-8")) < 2000, len(out.encode("utf-8"))


def _selftest_missing_claude_md_is_block_missing_not_crash():
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        cfg = os.path.join(d, "nope")
        ret, out = _run_main({"cwd": d}, cfg)
        assert ret == 0, (ret, out)
        assert "WARNING" in out, out
        assert "CLAUDE.md not found" in out, out
        assert ("Fix: %s" % INSTALL_SCRIPT) in out, out


def _selftest_block_missing_in_existing_file():
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        cfg = os.path.join(d, "claude-config")
        _write(os.path.join(cfg, "CLAUDE.md"), "# just some prose\n")
        ret, out = _run_main({"cwd": d}, cfg)
        assert ret == 0 and "WARNING" in out, out
        assert "import block missing or malformed" in out, out


def _selftest_malformed_markers_read_as_missing():
    """Unbalanced or out-of-order markers grade the same as no block —
    a corrupted block is not a delivered corpus."""
    import tempfile

    cases = [
        BEGIN_MARKER + "\n@x/grounding.md\n",           # no end marker
        END_MARKER + "\n" + BEGIN_MARKER + "\n",          # end before start
        BEGIN_MARKER + "\n" + BEGIN_MARKER + "\n" + END_MARKER + "\n",
    ]
    with tempfile.TemporaryDirectory() as d:
        for i, body in enumerate(cases):
            cfg = os.path.join(d, "c%d" % i)
            _write(os.path.join(cfg, "CLAUDE.md"), body)
            ret, out = _run_main({"cwd": d}, cfg)
            assert ret == 0, (body, ret, out)
            assert "import block missing or malformed" in out, (body, out)


def _selftest_dead_path_is_unhealthy():
    """BITE — a module file that does not exist on disk (deleted,
    truncated block, wrong path) is caught even though the block itself
    parses fine."""
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        cfg = os.path.join(d, "claude-config")
        missing_dir = os.path.join(d, "deleted-modules-dir")
        lines = [BEGIN_MARKER]
        for name in MODULE_ORDER:
            if name == "insurance":
                # correct basename (so the order/name check passes), but a
                # directory that does not exist — isolates the "on disk"
                # check from the "named right" check above it.
                lines.append("@" + os.path.join(missing_dir, "insurance.md"))
            else:
                lines.append("@" + os.path.join(MODULES_DIR, name + ".md"))
        lines.append(END_MARKER)
        _write(os.path.join(cfg, "CLAUDE.md"), "\n".join(lines) + "\n")
        ret, out = _run_main({"cwd": d}, cfg)
        assert ret == 0 and "WARNING" in out, out
        assert "imported module missing on disk" in out, out
        assert os.path.join(missing_dir, "insurance.md") in out, out


def _selftest_stale_prefix_after_version_move_is_unhealthy():
    """BITE — the exact defect this check exists for: an import block
    written for a DIFFERENT install of the plugin (an old version's
    cache path) — every named file still exists (it is a real,
    installed, OTHER version's modules/ directory), so only the
    resolved-prefix comparison against THIS hook's own plugin root
    catches it. Paired against a control where the prefix matches, so
    the failure is the comparison firing and not every path simply
    being treated as dead."""
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        other_version_modules = os.path.join(d, "ethos", "0.0.9", "modules")
        for name in MODULE_ORDER:
            _write(os.path.join(other_version_modules, name + ".md"),
                   "# " + name + "\n")

        cfg = os.path.join(d, "claude-config")
        _write(os.path.join(cfg, "CLAUDE.md"), _valid_block(other_version_modules))
        ret, out = _run_main({"cwd": d}, cfg)
        assert ret == 0 and "WARNING" in out, out
        assert "resolves outside this plugin's own modules/" in out, out
        assert "stale path after a plugin update" in out, out

        # control: same fixture shape, correct prefix -> healthy
        cfg2 = os.path.join(d, "claude-config-2")
        _write(os.path.join(cfg2, "CLAUDE.md"), _valid_block(MODULES_DIR))
        ret2, out2 = _run_main({"cwd": d}, cfg2)
        assert ret2 == 0 and "WARNING" not in out2, out2


def _selftest_wrong_count_or_order_is_unhealthy():
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        # too few
        cfg = os.path.join(d, "few")
        lines = [BEGIN_MARKER]
        for name in MODULE_ORDER[:3]:
            lines.append("@" + os.path.join(MODULES_DIR, name + ".md"))
        lines.append(END_MARKER)
        _write(os.path.join(cfg, "CLAUDE.md"), "\n".join(lines) + "\n")
        ret, out = _run_main({"cwd": d}, cfg)
        assert ret == 0 and "3 import line(s), expected 6" in out, out

        # swapped order
        cfg2 = os.path.join(d, "swapped")
        swapped = [MODULE_ORDER[1], MODULE_ORDER[0]] + MODULE_ORDER[2:]
        lines = [BEGIN_MARKER]
        for name in swapped:
            lines.append("@" + os.path.join(MODULES_DIR, name + ".md"))
        lines.append(END_MARKER)
        _write(os.path.join(cfg2, "CLAUDE.md"), "\n".join(lines) + "\n")
        ret2, out2 = _run_main({"cwd": d}, cfg2)
        assert ret2 == 0 and "out of order or missing" in out2, out2


def _selftest_config_dir_env_precedence():
    """CLAUDE_CONFIG_DIR, when set, decides the target — not ~/.claude —
    matching install-imports.sh's own default resolution exactly."""
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        cfg = os.path.join(d, "custom-config")
        _write(os.path.join(cfg, "CLAUDE.md"), _valid_block(MODULES_DIR))
        old = os.environ.get("CLAUDE_CONFIG_DIR")
        os.environ["CLAUDE_CONFIG_DIR"] = cfg
        try:
            assert target_claude_md() == os.path.join(cfg, "CLAUDE.md")
        finally:
            if old is None:
                os.environ.pop("CLAUDE_CONFIG_DIR", None)
            else:
                os.environ["CLAUDE_CONFIG_DIR"] = old


def _selftest():
    _selftest_healthy_line_under_2000_bytes()
    _selftest_missing_claude_md_is_block_missing_not_crash()
    _selftest_block_missing_in_existing_file()
    _selftest_malformed_markers_read_as_missing()
    _selftest_dead_path_is_unhealthy()
    _selftest_stale_prefix_after_version_move_is_unhealthy()
    _selftest_wrong_count_or_order_is_unhealthy()
    _selftest_config_dir_env_precedence()
    print("verify-ethos: all tests passed")


if __name__ == "__main__":
    if "--test" in sys.argv:
        _selftest()
        sys.exit(0)
    sys.exit(main())
