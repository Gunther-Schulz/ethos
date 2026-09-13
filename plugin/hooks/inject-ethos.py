#!/usr/bin/env python3
"""SessionStart hook — injects the ethos work-ethics corpus verbatim.

Emits one header line naming ethos and its shipped version, then the six
module bodies in the corpus' own table order (grounding, fixing,
calibration, insurance, reporting, accretion), each under its own
existing `## ` heading (the module files carry that heading as their
first line already — nothing is added or rewritten).

Modules ship INSIDE this plugin's payload at ../modules/<name>.md,
relative to this script's own location (CLAUDE_PLUGIN_ROOT-independent,
so the script works under any install path). A missing module file is
FAIL-LOUD: non-zero exit, one stderr line naming the missing file, and
nothing is emitted to stdout for that run — never a silent partial
corpus. This is deliberately the opposite of a context-injector's usual
"nothing to add is a silent no-op" convention (see the dotfiles sibling
required-reading-inject.py): here the six modules are the plugin's whole
declared payload, so a missing one means the install is broken, not that
there is honestly nothing to inject.

KNOWN OPEN QUESTION, not resolved by this script (see the ethos build
report): the six module bodies concatenate to ~83KB. Claude Code's
SessionStart hook output has been measured elsewhere in this stack to
truncate to a small preview plus a file pointer beyond some threshold
(dotfiles claude/hooks/required-reading-inject.py, which self-caps at
8192 bytes for exactly this reason). This script applies NO cap and NO
truncation handling — that is a design decision for whoever mints the
next version, not this build's to improvise. Whether the harness
delivers all ~83KB to the model or silently previews it is unverified
here.
"""

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

HERE = os.path.dirname(os.path.abspath(__file__))
MODULES_DIR = os.path.normpath(os.path.join(HERE, "..", "modules"))


def main():
    bodies = []
    for name in MODULE_ORDER:
        path = os.path.join(MODULES_DIR, name + ".md")
        if not os.path.isfile(path):
            sys.stderr.write(
                "inject-ethos: missing module file: %s\n" % path
            )
            return 1
        try:
            with open(path, "r", encoding="utf-8") as f:
                body = f.read()
        except OSError as exc:
            sys.stderr.write(
                "inject-ethos: cannot read module file %s: %s\n"
                % (path, exc)
            )
            return 1
        bodies.append(body.rstrip("\n"))

    out = []
    out.append("ethos v%s — work-ethics corpus (injected at session start)" % VERSION)
    out.append("")
    out.append("\n\n".join(bodies))
    sys.stdout.write("\n".join(out) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
