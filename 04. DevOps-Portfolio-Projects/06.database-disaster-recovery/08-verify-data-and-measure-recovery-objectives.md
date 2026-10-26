# 08. Verify Data and Measure Recovery Objectives

[← 07. Restore to the Selected Recovery Point](07-restore-to-the-selected-recovery-point.md) · [Project home](README.md) · [09. Write the Recovery Runbook and Remove Lab Data →](09-write-the-recovery-runbook-and-remove-lab-data.md)

## Starting state and working directory

Complete chapter 07 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `06.database-disaster-recovery` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 06.database-disaster-recovery
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

RTO is the observed time to restore and verify usable service, not just the time until a container exists. RPO describes how much committed data you can lose or intentionally exclude. This drill recovers the two original rows before a known destructive commit; it does not prove a long-term off-site recovery guarantee. Compare the restored result with the saved baseline, not merely a row count.

## Work through the implementation

Write down incident time, base-backup time, target transaction, last archived segment, restoration start, database promotion and application-verification time. Report which part your RTO includes. Explain why the source and restored instances must not both accept production writes without a planned cutover and conflict strategy.

### Commands in execution order

```bash
docker compose exec -T restore psql -At -U postgres -d orders -c 'SELECT id,item FROM orders ORDER BY id;'
docker compose exec -T restore psql -At -U postgres -d orders -c 'SELECT pg_is_in_recovery();'
docker compose exec -T db psql -At -U postgres -d orders -c 'SELECT count(*) FROM orders;'
```

## Checkpoint — verify before continuing

Restored rows are 1|book and 2|keyboard; recovery is false; the source still has zero rows. This shows the recovered data came from the independent recovery instance.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

A matching count with different records is not correctness. Compare actual values and, for a larger system, application invariants and sampled checksums. A replica of the deleted source would faithfully reproduce the deletion, not undo it.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [09. Write the Recovery Runbook and Remove Lab Data](09-write-the-recovery-runbook-and-remove-lab-data.md). The next chapter assumes the state created here.
