#!/usr/bin/env bash
set -euo pipefail
image=${1:?Usage: bash scripts/verify-release.sh image@sha256:digest public-key}
key=${2:?Public signing key required}
[[ "$image" =~ @sha256:[0-9a-f]{64}$ ]] || { echo 'Digest required' >&2;exit 2; }
cosign verify --key "$key" "$image" > /dev/null
trivy image --format json --output .lab/deployment-scan.json "$image"
python3 policy/evaluate.py .lab/deployment-scan.json
printf 'Verified signature and scan policy for %s\n' "$image"
