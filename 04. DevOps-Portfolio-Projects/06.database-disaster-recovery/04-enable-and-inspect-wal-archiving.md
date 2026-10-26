# 04. Enable and Inspect WAL Archiving

[← 03. Create and Verify the First Backup](03-create-and-verify-the-first-backup.md) · [Project home](README.md) · [05. Schedule Backups and Detect Backup Failures →](05-schedule-backups-and-detect-backup-failures.md)

## Starting state and working directory

Complete chapter 03 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `06.database-disaster-recovery` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 06.database-disaster-recovery
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

WAL archiving is enabled by the supplied startup flags from the first boot. A segment is archived after it is completed, not after every SQL statement. pg_switch_wal requests a segment switch so you can observe the archive during the lab. The archiver must not overwrite a different existing file; it treats an identical retry as success.

## Work through the implementation

The archive_timeout setting bounds the time before an active segment is switched during low activity, but it does not by itself establish an RPO guarantee. Archive transport, storage durability and monitoring still matter. This example uses local cp so the failure behavior is visible without requiring an external storage account.

### Commands in execution order

```bash
docker compose exec -T db psql -U postgres -d orders -c 'SHOW archive_mode; SHOW archive_command;'
docker compose exec -T db psql -U postgres -d orders -c 'SELECT pg_switch_wal();'
docker compose exec -T db psql -U postgres -d orders -c 'SELECT archived_count,failed_count,last_archived_wal,last_failed_wal FROM pg_stat_archiver;'
docker compose exec -T db ls /archive
```

## Checkpoint — verify before continuing

archive_mode is on and archived_count increases. At least one WAL segment exists in /archive. Investigate nonzero failed_count rather than assuming it is harmless.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

An archive command failure can fill the source disk because PostgreSQL retains required WAL. Check ownership, available space and the exact command. Never delete live pg_wal files to create space.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [05. Schedule Backups and Detect Backup Failures](05-schedule-backups-and-detect-backup-failures.md). The next chapter assumes the state created here.
