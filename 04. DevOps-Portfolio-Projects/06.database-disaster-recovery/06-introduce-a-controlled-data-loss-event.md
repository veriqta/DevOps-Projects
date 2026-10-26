# 06. Introduce a Controlled Data Loss Event

[← 05. Schedule Backups and Detect Backup Failures](05-schedule-backups-and-detect-backup-failures.md) · [Project home](README.md) · [07. Restore to the Selected Recovery Point →](07-restore-to-the-selected-recovery-point.md)

## Starting state and working directory

Complete chapter 05 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `06.database-disaster-recovery` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 06.database-disaster-recovery
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Save the exact destructive transaction identifier, then force and verify archival of the containing WAL segment. Restoring before a guessed wall-clock time can hide timezone or ordering mistakes; this transaction-targeted drill is deterministic. Keep the source running long enough to archive the required segment and record the event before starting restoration.

## Work through the implementation

Run this only against the named lab database. The command deletes dummy orders intentionally and does not take a new base backup afterward. Taking a new backup after the deletion and expecting it to contain old rows would misunderstand the recovery model. Later successful backups may still be useful, but this drill must restore from a backup preceding the destructive transaction.

### Commands in execution order

```bash
DELETE_XID=$(docker compose exec -T db psql -At -U postgres -d orders -c 'WITH removed AS (DELETE FROM orders RETURNING *) SELECT txid_current();')
printf '%s
' "$DELETE_XID" > .lab/delete-xid
docker compose exec -T db psql -U postgres -d orders -c 'SELECT count(*) FROM orders;'
SEGMENT=$(docker compose exec -T db psql -At -U postgres -d orders -c 'SELECT pg_walfile_name(pg_current_wal_lsn());')
docker compose exec -T db psql -U postgres -d orders -c 'SELECT pg_switch_wal();'
for i in $(seq 1 30);do docker compose exec -T db test -f "/archive/$SEGMENT" && break; sleep 2;done
docker compose exec -T db test -f "/archive/$SEGMENT"
```

## Checkpoint — verify before continuing

The source count is zero, .lab/delete-xid contains only a numeric transaction ID and the selected WAL segment is present in /archive. Preserve baseline and loss output side by side.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If the transaction ID is empty or includes command tags, stop and inspect psql output before restoring. If the WAL segment never arrives, diagnose archiving before assuming the recovery point is available.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [07. Restore to the Selected Recovery Point](07-restore-to-the-selected-recovery-point.md). The next chapter assumes the state created here.
