# 00. Data Loss Scenario and Recovery Objectives

[Project home](README.md) · [01. Start PostgreSQL and Create Known Test Data →](01-start-postgresql-and-create-known-test-data.md)

## Starting state and working directory

Read the project README and have a terminal open at the repository root.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `06.database-disaster-recovery` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 06.database-disaster-recovery
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Crash recovery and logical data recovery are different. PostgreSQL can restart cleanly after a DELETE because that DELETE was a valid committed transaction. A base backup gives a consistent starting point; archived WAL replays changes until the selected recovery target. The lab records the destructive transaction ID and excludes its commit so the recovery instance stops before the deletion.

## Work through the implementation

The source database remains available for comparison after the incident, while restoration uses a new volume. Do not restore in place over your only source. Backups and WAL are plain PostgreSQL files in local volumes here; keep them on an encrypted lab disk and treat them as sensitive even though the example records are dummy.

### Commands in execution order

```bash
find database scripts -maxdepth 2 -type f | sort
```

## Checkpoint — verify before continuing

Write the expected original data: orders 1/book and 2/keyboard. Define the lab RPO as recovery before the destructive transaction, and choose a recovery-time target you will measure rather than assume.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

A logical SQL dump alone cannot demonstrate arbitrary physical WAL replay. This exercise uses pg_basebackup and PostgreSQL recovery settings, not a claim that restarting a container is disaster recovery.

## What to record

Save the architecture and acceptance criteria in your own notes. You will compare the finished system with this contract in chapter 09.

## Continue

When this checkpoint passes, continue to [01. Start PostgreSQL and Create Known Test Data](01-start-postgresql-and-create-known-test-data.md). The next chapter assumes the state created here.
