#!/bin/sh
# Install bs-webctl git hooks (Agent-SE-SPEC §4 gate).
# Run once after clone. core.hooksPath must be absolute — git resolves relative
# paths against $GIT_DIR (.git/), not the worktree, so in-worktree hooks need
# an absolute pointer.
set -e
ROOT="$(git rev-parse --show-toplevel)"
git config core.hooksPath "$ROOT/scripts/hooks"
echo "hooks → $(git config core.hooksPath)"
