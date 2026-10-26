#!/usr/bin/env bash
set -euo pipefail
target=${1:?Supply the recovery target transaction ID saved before the DELETE}
[[ "$target" =~ ^[0-9]+$ ]] || exit 2
docker compose --profile restore stop restore
docker compose --profile restore run --rm --no-deps --user root --entrypoint sh -v portfolio-recovery_backup:/backup:ro restore -eu -c '
  test -f /backup/latest/PG_VERSION
  test ! -f /var/lib/postgresql/data/PG_VERSION
  cp -a /backup/latest/. /var/lib/postgresql/data/
  printf "restore_command = '\''cp /archive/%%f %%p'\''\nrecovery_target_xid = '\''%s'\''\nrecovery_target_inclusive = false\nrecovery_target_action = '\''promote'\''\n" "$1" >> /var/lib/postgresql/data/postgresql.auto.conf
  touch /var/lib/postgresql/data/recovery.signal
  chown -R postgres:postgres /var/lib/postgresql/data
  chmod 700 /var/lib/postgresql/data
' sh "$target"
docker compose --profile restore up -d restore
