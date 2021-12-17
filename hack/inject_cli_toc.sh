#!/bin/bash
#
# Regenerates the docs sidebar from the Cobra auto-generated docs (docs/cli/tilt.md)

set -eo pipefail

cd "$(dirname $(dirname "$0"))"
RESULT=$(python3 hack/gen_cli_toc_helper.py)
echo "$RESULT" > src/_data/docs.yml
