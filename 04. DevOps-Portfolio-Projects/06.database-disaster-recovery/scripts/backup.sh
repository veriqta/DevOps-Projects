#!/usr/bin/env bash
set -euo pipefail
docker compose exec -T --user postgres db sh -eu -c 'name=base-$(date -u +%Y%m%dT%H%M%S)-$$; pg_basebackup -U postgres -h /var/run/postgresql -D "/backup/$name" -X stream -c fast; pg_verifybackup "/backup/$name"; ln -sfn "$name" /backup/latest'
docker compose exec -T db psql -U postgres -d orders -c 'SELECT pg_switch_wal();'
