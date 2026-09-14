#!/usr/bin/env bash
# Grade the corpus modules against THIS corpus's declared register band.
#
# THE BAND IS THE DECLARATION, and it is the only thing this file owns:
#
#     45 words/sentence   30 em dashes per 1000 words
#
# Why these numbers and not the tool's defaults. register_lint ships a
# band derived from a sample of short imperative skills (7.9-18.7
# words/sentence, 0-5.34 dashes per 1000 words). This corpus is not
# written that way and the difference is deliberate: a rule here states
# its mechanism, its costume and its convention inside one clause,
# because a reader who takes the rule and drops the mechanism cannot
# check the rule at the next seam. Graded against the shipped default
# every module fails every line, which trains a reader to skip the
# checker — a check that fires on a non-defect is failing too.
#
# The band is a CEILING WITH HEADROOM, never a description of what the
# corpus currently measures. As of writing, the modules sit at
# 33.4-40.7 words/sentence and 20.5-27.5 dashes per 1000 words, so
# there is room above them and drift past it still fires. A band
# re-derived from the corpus each run would be no check at all: it
# would go green byte-identically to health, and the day a module slid
# to 60 words/sentence nothing would say so.
#
# Raising either number is a decision about how dense this corpus may
# get. It is the operator's, and it belongs in the commit that moves
# it, with what moved.
#
# WHAT THIS SCRIPT DOES NOT REACH, stated because a clean exit here
# otherwise reads as a verdict on a reader's whole always-loaded set:
# it grades the modules in THIS repo only. A consuming site may load
# site-bound modules of its own beside them — environment facts,
# routing decisions — which live in that site's repo and are invisible
# from here. A green below means the TRAVELING modules are inside the
# band and says nothing about the rest of any site's corpus.
#
# That is not hypothetical. The operator's site loads eight modules,
# six of them these; the first run of a site-side check found one of
# its own two at 50.6 words/sentence against this band's 45 — over,
# and unseen for as long as the only check ran here. A site that loads
# modules beyond this repo runs its own check over its own full set.
set -u

BAND_WORDS_PER_SENTENCE=45
BAND_EM_DASHES_PER_1000=30

here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
modules="$here/../plugin/modules"

# register_lint lives in the skill-craft plugin, whose install path is
# version-pinned and therefore moves on every release. Candidates are
# tried in order and the FIRST hit wins; absence is reported as
# could-not-verify and exits 2, never as a pass — a checker that cannot
# run is not a checker that found nothing.
lint=""
for cand in \
    "${REGISTER_LINT:-}" \
    "${CLAUDE_PLUGIN_ROOT:-}/tools/register_lint.py" \
    "$HOME/dev/Gunther-Schulz/skill-craft/plugin/tools/register_lint.py" \
    "$(ls -1d "$HOME"/.claude/plugins/cache/skill-craft-marketplace/skill-craft/*/tools/register_lint.py 2>/dev/null | sort -V | tail -1)"
do
    [ -n "$cand" ] && [ -f "$cand" ] && { lint="$cand"; break; }
done

if [ -z "$lint" ]; then
    echo "register-check: COULD NOT VERIFY — register_lint.py not found." >&2
    echo "  Set REGISTER_LINT=<path>, or install the skill-craft plugin." >&2
    echo "  Looked for it beside CLAUDE_PLUGIN_ROOT, in the ~/dev mirror," >&2
    echo "  and in the plugin cache. Nothing was graded." >&2
    exit 2
fi

fail=0
graded=0
for f in "$modules"/*.md; do
    [ -f "$f" ] || continue
    graded=$((graded + 1))
    python3 "$lint" "$f" \
        --band "$BAND_WORDS_PER_SENTENCE" "$BAND_EM_DASHES_PER_1000" \
        || fail=1
done

# A run over zero modules is the could-not-verify case wearing a clean
# exit: "0 files, no findings" reads exactly like "checked and clean".
if [ "$graded" -eq 0 ]; then
    echo "register-check: COULD NOT VERIFY — no modules under $modules" >&2
    exit 2
fi

if [ "$fail" -eq 0 ]; then
    echo "register-check: $graded module(s) inside the declared band" \
         "(${BAND_WORDS_PER_SENTENCE} w/s, ${BAND_EM_DASHES_PER_1000}/1000w)"
fi
exit "$fail"
