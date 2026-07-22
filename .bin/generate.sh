#!/bin/bash
# GitHub Profile Page Generator — thin bridge to catalyst-repo.generator.
#
# The generator moved into catalyst-operator's ``catalyst-repo`` package
# so both TheBranchDriftCatalyst and any future profile-target repo share
# one implementation. This script just picks the target output + config
# and invokes the console script installed by that package.
#
# Editing the generator? Edit
#   packages/catalyst-repo/src/catalyst_repo/generator/_impl.py
# in catalyst-operator, then reinstall (``uv pip install -e ...``).

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_PATH="$SCRIPT_DIR/config.yml"
OUTPUT_PATH="$REPO_ROOT/README.md"

# Prefer the operator's shared venv (catalyst-repo lives there) — falls
# back to whatever ``catalyst-profile-generate`` resolves on PATH.
# TODO: fix this all up... probably resolved when we switch this to go and strangler fig the python out
CATALYST_OP_VENV="/Users/panda/catalyst-devspace/workspace/catalyst-operator/.venv/bin"
if [ -x "$CATALYST_OP_VENV/catalyst-profile-generate" ]; then
    GEN="$CATALYST_OP_VENV/catalyst-profile-generate"
elif command -v catalyst-profile-generate &> /dev/null; then
    GEN="catalyst-profile-generate"
else
    echo "Error: catalyst-profile-generate not found." >&2
    echo "Install with: uv pip install -e /Users/panda/catalyst-devspace/workspace/catalyst-operator/packages/catalyst-repo" >&2
    exit 1
fi

echo "🌊 GitHub Profile Page Generator"
echo "=================================="
echo ""
echo "  Config: $CONFIG_PATH"
echo "  Output: $OUTPUT_PATH"
echo ""

"$GEN" --config "$CONFIG_PATH" --output "$OUTPUT_PATH" "$@"

echo ""
echo "✓ Profile page generated successfully!"
