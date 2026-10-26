#!/usr/bin/env bash
set -euo pipefail
for i in $(seq 1 60);do
  if docker compose exec -T restore pg_isready -U postgres -d orders >/dev/null 2>&1;then
    recovery=$(docker compose exec -T restore psql -At -U postgres -d orders -c 'SELECT pg_is_in_recovery();' 2>/dev/null || true)
    actual=$(docker compose exec -T restore psql -At -U postgres -d orders -c 'SELECT count(*) FROM orders;' 2>/dev/null || true)
    if [ "$recovery" = f ] && [ "$actual" = 2 ];then
      docker compose exec -T restore psql -U postgres -d orders -c 'TABLE orders;'
      echo 'Both original orders recovered and database promoted'
      exit 0
    fi
  fi
  sleep 2
done
docker compose logs --tail=60 restore
exit 1
