# 05. Schedule Backups and Detect Backup Failures

[← 04. Enable and Inspect WAL Archiving](04-enable-and-inspect-wal-archiving.md) · [Project home](README.md) · [06. Introduce a Controlled Data Loss Event →](06-introduce-a-controlled-data-loss-event.md)

## Starting state and working directory

Complete chapter 04 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `06.database-disaster-recovery` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 06.database-disaster-recovery
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A backup schedule needs an observable failure path and a retention decision. Cron must use an absolute working directory and a Docker-capable user. The helper creates a new timestamped backup on every successful run, so scheduled executions do not overwrite the only recovery point. In this local lab, first prove the failure exit before enabling the schedule.

## Work through the implementation

On the Ubuntu Docker host open crontab -e. Add PATH=/usr/local/bin:/usr/bin:/bin, then a line `0 */12 * * * cd /ABSOLUTE/PATH/06.database-disaster-recovery && /bin/bash scripts/backup.sh >> .lab/backup.log 2>&1`. Replace the path and run that command manually before waiting for the schedule. It runs at midnight/noon in the host timezone. Monitor nonzero exits through your scheduler or log alerting; cron output alone is not a notification system. List backup ages and define retention only after the restore drill passes.

### Commands in execution order

```bash
docker compose stop db
bash scripts/backup.sh
# Expect nonzero: a stopped database cannot produce a new backup.
docker compose up -d --wait db
bash scripts/backup.sh
```

## Checkpoint — verify before continuing

The stopped-database attempt fails and does not move /backup/latest. The restarted attempt succeeds. Record both outputs and compare the latest target.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Cron often fails because PATH or Docker permissions differ from an interactive shell. Run the exact cron command as the same user first. A log file with only old success messages is not proof of recent backups.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [06. Introduce a Controlled Data Loss Event](06-introduce-a-controlled-data-loss-event.md). The next chapter assumes the state created here.
