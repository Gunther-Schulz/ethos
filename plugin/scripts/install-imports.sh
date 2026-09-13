#!/bin/sh
# install-imports.sh — writes the ethos corpus's @-imports into a CLAUDE.md.
#
# Why this exists (see README, and dotfiles claude/records/
# corpus-portability-2026-09-13.md, "Injection redesign SETTLED"):
# Claude Code truncates oversized SessionStart hook stdout to a small
# preview plus a file pointer, and the six ethos modules run well past
# that threshold — so the corpus cannot travel as hook output at all.
# It travels instead as `@`-import lines resolved to absolute paths and
# written into the user's CLAUDE.md, which is the one channel proven to
# deliver content this size in full. This script is that one write; the
# plugin's SessionStart hook (verify-ethos.py) never writes anything —
# it only checks that this script's work is still in place.
#
# Idempotent: re-running replaces the existing marked block in place
# (same position in the file) rather than duplicating it — the intended
# upgrade path after a plugin version move changes the resolved paths.
# The replacement is atomic: built in a temp file in the target's own
# directory, then renamed over the target.
#
# Usage: install-imports.sh [target-CLAUDE.md-path]
#   Default target: $CLAUDE_CONFIG_DIR/CLAUDE.md, else ~/.claude/CLAUDE.md.
#   An explicit argument overrides the default (used by this repo's own
#   re-probe, against a scratch CLAUDE_CONFIG_DIR).
#
# Paths resolve from THIS SCRIPT's own location (symlinks followed), not
# from $CLAUDE_PLUGIN_ROOT or any other env var — so it works identically
# whether run from a marketplace-installed plugin cache or straight out
# of a checked-out ethos repo.

set -eu

# MODULE_ORDER is read from modules/ORDER (single source; see below).

BEGIN_MARKER='# >>> ethos imports (managed by ethos install-imports.sh) >>>'
END_MARKER='# <<< ethos imports <<<'

# --- resolve this script's own real, symlink-free directory -----------

script_path=$0
case "$script_path" in
    /*) : ;;
    *) script_path="$PWD/$script_path" ;;
esac
while [ -L "$script_path" ]; do
    link=$(readlink "$script_path")
    case "$link" in
        /*) script_path="$link" ;;
        *) script_path="$(dirname "$script_path")/$link" ;;
    esac
done
script_dir=$(cd "$(dirname "$script_path")" && pwd -P)
plugin_root=$(cd "$script_dir/.." && pwd -P)
modules_dir="$plugin_root/modules"

# --- module set: modules/ORDER is the single source of order AND
# --- membership; both directions fail loud (an unlisted module on
# --- disk would otherwise be silently never loaded)

if [ ! -f "$modules_dir/ORDER" ]; then
    echo "install-imports: ERROR: $modules_dir/ORDER missing — cannot determine the module set" >&2
    exit 1
fi
MODULE_ORDER=$(tr '\n' ' ' < "$modules_dir/ORDER")
for f in "$modules_dir"/*.md; do
    stem=$(basename "$f" .md)
    case " $MODULE_ORDER " in
        *" $stem "*) ;;
        *)
            echo "install-imports: ERROR: $f exists on disk but is not listed in modules/ORDER — it would be silently never loaded" >&2
            exit 1
            ;;
    esac
done
for m in $MODULE_ORDER; do
    if [ ! -f "$modules_dir/$m.md" ]; then
        echo "install-imports: ERROR: modules/ORDER lists '$m' but $modules_dir/$m.md does not exist" >&2
        exit 1
    fi
done

# --- resolve the install target ----------------------------------------

if [ "$#" -ge 1 ]; then
    target=$1
else
    config_dir=${CLAUDE_CONFIG_DIR:-"$HOME/.claude"}
    target="$config_dir/CLAUDE.md"
fi

# --- build the fresh block, failing loud on a missing module file ------

block_file=$(mktemp)
tmp_target=""
cleanup() {
    rm -f "$block_file"
    if [ -n "$tmp_target" ]; then rm -f "$tmp_target"; fi
}
trap cleanup EXIT INT TERM

{
    echo "$BEGIN_MARKER"
    for m in $MODULE_ORDER; do
        mod_path="$modules_dir/$m.md"
        if [ ! -f "$mod_path" ]; then
            echo "install-imports: missing module file: $mod_path" >&2
            exit 1
        fi
        echo "@$mod_path"
    done
    echo "$END_MARKER"
} > "$block_file"

# --- write the block into the target, in place if it already has one --

target_dir=$(dirname "$target")
mkdir -p "$target_dir"

tmp_target=$(mktemp "$target_dir/.ethos-imports.XXXXXX")

if [ -f "$target" ] && grep -qF "$BEGIN_MARKER" "$target"; then
    awk -v begin="$BEGIN_MARKER" -v end="$END_MARKER" -v blockfile="$block_file" '
        BEGIN {
            block = ""
            while ((getline line < blockfile) > 0) {
                block = block line "\n"
            }
        }
        $0 == begin { printf "%s", block; skip = 1; next }
        $0 == end   { skip = 0; next }
        !skip       { print }
    ' "$target" > "$tmp_target"
elif [ -f "$target" ]; then
    cp "$target" "$tmp_target"
    if [ -s "$tmp_target" ]; then
        printf '\n' >> "$tmp_target"
    fi
    cat "$block_file" >> "$tmp_target"
else
    cat "$block_file" > "$tmp_target"
fi

mv "$tmp_target" "$target"
tmp_target=""

# --- report what was written -------------------------------------------

echo "install-imports: plugin root: $plugin_root"
echo "install-imports: wrote ethos import block to: $target"
for m in $MODULE_ORDER; do
    echo "install-imports:   @$modules_dir/$m.md"
done
