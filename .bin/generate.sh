#!/bin/bash
# GitHub Profile Page Generator
# Generates a synthwave-style profile README from workspace repositories

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🌊 GitHub Profile Page Generator"
echo "=================================="
echo ""

# Check if Poetry is available
if ! command -v poetry &> /dev/null; then
    echo "Error: poetry is required but not found"
    echo "Install with: curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "Installing dependencies with Poetry..."
    poetry install --directory "$SCRIPT_DIR"
fi

# Run the generator with Poetry
echo "Running generator..."
cd "$SCRIPT_DIR"
poetry run python generate.py

echo ""
echo "✓ Profile page generated successfully!"
echo "  Output: $REPO_ROOT/README.md"