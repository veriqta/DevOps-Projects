# 09. Write the Recovery Runbook and Remove Lab Data

[← 08. Verify Data and Measure Recovery Objectives](08-verify-data-and-measure-recovery-objectives.md) · [Project home](README.md)

## Starting state and working directory

Complete chapter 08 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `06.database-disaster-recovery` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 06.database-disaster-recovery
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

The runbook should be usable by someone who did not write the backup script. Include the inputs, storage locations, target selection, restore command, verification queries, escalation criteria and abort conditions. Pair this with the tested result so a reviewer can distinguish documentation from an actual recovery exercise.

## Work through the implementation

A résumé bullet can describe verified PostgreSQL physical backups, WAL-based recovery before a destructive transaction and measured RTO/RPO. Use observed values. Prepare to explain backup age, WAL continuity, recovery targets, major-version compatibility, off-host storage and why replication is not a substitute for recovery from operator error.

### Commands in execution order

```bash
docker compose --profile restore down -v
rm -rf .lab
docker volume ls --filter name=portfolio-recovery
```

## Checkpoint — verify before continuing

The primary, archive, backup and restored volumes are removed after evidence is saved. Remove the cron entry first so it cannot recreate activity or emit misleading failures after cleanup.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

down -v permanently deletes this dummy lab data. Do not apply that cleanup pattern to a real database. If a volume remains attached, inspect the named container instead of deleting unrelated Docker resources.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

The project is complete only after the acceptance checks pass and the lab resources are removed. Publish your sanitized implementation and evidence in your own portfolio repository.
