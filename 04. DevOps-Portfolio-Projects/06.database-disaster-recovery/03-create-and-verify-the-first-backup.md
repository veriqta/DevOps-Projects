# 03. Create and Verify the First Backup

[← 02. Configure the Backup Repository and Credentials](02-configure-the-backup-repository-and-credentials.md) · [Project home](README.md) · [04. Enable and Inspect WAL Archiving →](04-enable-and-inspect-wal-archiving.md)

## Starting state and working directory

Complete chapter 02 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `06.database-disaster-recovery` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 06.database-disaster-recovery
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

pg_basebackup copies a consistent physical cluster while PostgreSQL is running. -X stream includes the WAL required to make the backup consistent; it does not remove the need for later WAL archiving for PITR. pg_verifybackup checks the backup manifest and files. A successful copy is not yet proof of a successful application restore.

## Work through the implementation

The script runs as postgres and uses the local replication connection. Each successful run creates a new physical backup; no retention deletion runs automatically. Record its completion time and manifest verification. Deleting older backups before a tested replacement can make an apparently healthy backup schedule unrecoverable.

### Commands in execution order

```bash
bash scripts/backup.sh
docker compose exec -T --user postgres db sh -c 'readlink /backup/latest; pg_verifybackup /backup/latest'
```

### Read the implementation: `scripts/backup.sh`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```bash
#!/usr/bin/env bash
set -euo pipefail
docker compose exec -T --user postgres db sh -eu -c 'name=base-$(date -u +%Y%m%dT%H%M%S)-$$; pg_basebackup -U postgres -h /var/run/postgresql -D "/backup/$name" -X stream -c fast; pg_verifybackup "/backup/$name"; ln -sfn "$name" /backup/latest'
docker compose exec -T db psql -U postgres -d orders -c 'SELECT pg_switch_wal();'
```

## Checkpoint — verify before continuing

The backup helper exits zero and pg_verifybackup reports success. The latest symlink refers to a timestamped base backup, allowing scheduled runs without overwriting the preceding backup.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If a backup fails, do not point latest at the incomplete directory. The script updates latest only after pg_verifybackup passes. Inspect the failed directory and disk space before retrying.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [04. Enable and Inspect WAL Archiving](04-enable-and-inspect-wal-archiving.md). The next chapter assumes the state created here.
