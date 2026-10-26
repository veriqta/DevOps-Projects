#!/usr/bin/env bash
set -euo pipefail
# Run as the deployment user from the repo root. sudo is used for the service only.
release="$(date -u +%Y%m%dT%H%M%S)-${GITHUB_SHA:-manual}-$$"
base=/opt/devops-app
mkdir -p "$base/releases/$release"
cp 02.examples/app/server.js "$base/releases/$release/server.js"
/usr/bin/node --check "$base/releases/$release/server.js"
previous=$(readlink "$base/current" || true)
ln -sfn "$base/releases/$release" "$base/next"
mv -Tf "$base/next" "$base/current"
sudo systemctl restart devops-app
for attempt in $(seq 1 15); do
  if curl -fsS http://127.0.0.1:8080/health; then
    printf '\nDeployed %s\n' "$release"
    exit 0
  fi
  sleep 1
done
printf 'Health check failed; restoring previous release\n' >&2
if [ -n "$previous" ]; then
  ln -sfn "$previous" "$base/next"
  mv -Tf "$base/next" "$base/current"
  sudo systemctl restart devops-app
fi
exit 1
