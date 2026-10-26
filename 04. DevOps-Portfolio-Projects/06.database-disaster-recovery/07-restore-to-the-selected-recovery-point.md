# 07. Restore to the Selected Recovery Point

[← 06. Introduce a Controlled Data Loss Event](06-introduce-a-controlled-data-loss-event.md) · [Project home](README.md) · [08. Verify Data and Measure Recovery Objectives →](08-verify-data-and-measure-recovery-objectives.md)

## Starting state and working directory

Complete chapter 06 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `06.database-disaster-recovery` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 06.database-disaster-recovery
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Restoration copies the verified base backup into a new volume and configures restore_command to fetch archived segments. recovery_target_xid names the delete transaction; recovery_target_inclusive=false stops before that transaction commits. recovery_target_action=promote makes the result writable after the target is reached. The source data volume remains untouched.

## Work through the implementation

Inspect docker compose logs restore for the selected transaction target and timeline messages. PostgreSQL physical backups are version-sensitive: the restore image matches the primary major version. A valid manifest plus readable data is still not enough for a real application; also test application queries, constraints and user permissions in a production recovery plan.

### Commands in execution order

```bash
SECONDS=0
bash scripts/restore.sh "$(cat .lab/delete-xid)"
bash scripts/verify.sh
printf 'Observed restore and verification time: %s seconds
' "$SECONDS"
docker compose exec -T restore psql -U postgres -d orders -c 'SELECT pg_is_in_recovery();'
```

### Read the implementation: `scripts/restore.sh`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```bash
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
```

### Read the implementation: `scripts/verify.sh`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```bash
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
```

## Checkpoint — verify before continuing

Both rows reappear and pg_is_in_recovery is false. Record elapsed restore/verification time; do not call the exercise successful if the instance is still waiting for unavailable WAL.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

A restore volume with PG_VERSION already present is deliberately refused. For another attempt preserve diagnostics, stop restore and remove only portfolio-recovery_restored before retrying. Never remove the source data or archive volume.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [08. Verify Data and Measure Recovery Objectives](08-verify-data-and-measure-recovery-objectives.md). The next chapter assumes the state created here.
