#!/usr/bin/env bash
set -euo pipefail
umask 077
repo=$(cd "$(dirname "$0")/.." && pwd)
dest=${1:?Usage: bash 03.tools/backup-db.sh /absolute/backup/directory}
case "$dest" in /*) ;; *) echo 'Use an absolute destination path' >&2; exit 2;; esac
mkdir -p "$dest"
file="$dest/lab-$(date -u +%Y%m%dT%H%M%S)-$$.sql"
trap 'rm -f "$file.partial"' EXIT
docker compose -f "$repo/02.examples/compose.yml" exec -T db pg_dump -U lab -d lab > "$file.partial"
test -s "$file.partial"
mv "$file.partial" "$file"
printf '%s\n' "$file"
