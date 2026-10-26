# 02. Configure the Backup Repository and Credentials

[← 01. Start PostgreSQL and Create Known Test Data](01-start-postgresql-and-create-known-test-data.md) · [Project home](README.md) · [03. Create and Verify the First Backup →](03-create-and-verify-the-first-backup.md)

## Starting state and working directory

Complete chapter 01 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `06.database-disaster-recovery` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 06.database-disaster-recovery
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

The backup volume is separate from the live data volume, and WAL has a separate archive volume. This lets you remove or inspect one component without confusing the source with its recovery copy. Separation on one Docker host does not survive host loss; that limit must be explicit in the portfolio. Read the mounted Secret’s path, not its content, when collecting configuration evidence.

## Work through the implementation

For a production design add off-host/object storage, independent access controls, encryption/key recovery, retention and tested cross-host restores. Those features should not be represented by an empty folder named backup. This local chapter establishes a real, inspectable physical repository and explains exactly what failure domain it covers.

### Commands in execution order

```bash
docker compose exec -T db psql -U postgres -d orders -c 'SHOW data_directory;'
docker compose exec -T db sh -c 'ls -ld /backup /archive; test -s /run/secrets/db_password'
docker volume ls --filter name=portfolio-recovery
```

## Checkpoint — verify before continuing

The live data, backup and archive volumes have distinct names. The password file exists with restrictive host permissions and is ignored by Git.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If no backup/archive directories exist, inspect Compose mounts before writing into the container filesystem. Files stored only in the container writable layer disappear when it is replaced.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [03. Create and Verify the First Backup](03-create-and-verify-the-first-backup.md). The next chapter assumes the state created here.
