# 31. Backup and Recovery Drill

[← All projects](../README.md) · **Advanced** · Restic · PostgreSQL · Velero

Prove recovery with a timed restore and a measurable recovery point.

## Prerequisites

Restic and Python. PostgreSQL extension requires project 18; the main restore drill runs entirely locally.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Files included

Everything below is inside this project’s `files/` folder.

| File or folder | Use |
| --- | --- |
| `app` | Demo HTTP service, Dockerfile and service unit. |
| `backup-db.sh` | Writes a database dump only after a successful backup. |
| `compose.yml` | Configuration or starter code referenced in the steps below. |

## Walkthrough

From the repository root, enter this project:

```bash
cd 31.backup-and-recovery-drill
```

Run the remaining commands here unless a step explicitly changes directories. The `files/` folder contains the supplied code and configurations for this project.

### 1. Create an encrypted local backup

```bash
mkdir -p .lab/recovery/source
printf 'recover this exact value\n' > .lab/recovery/source/proof.txt
export RESTIC_REPOSITORY="$PWD/.lab/recovery/repository"
read -rsp 'New lab repository password: ' RESTIC_PASSWORD; echo
export RESTIC_PASSWORD
restic init
restic backup .lab/recovery/source --tag devops-lab
restic snapshots
restic check
```

### 2. Simulate loss and time the restore

```bash
cp .lab/recovery/source/proof.txt .lab/recovery/expected.txt
rm .lab/recovery/source/proof.txt
SECONDS=0
restic restore latest --target .lab/recovery/restored
printf 'Restore duration: %s seconds\n' "$SECONDS"
find .lab/recovery/restored -name proof.txt -exec cmp .lab/recovery/expected.txt {} \;
```

Restic preserves the original directory path under the target, so find locates the restored file. Confirm it exists as well as checking cmp output:

```bash
test "$(find .lab/recovery/restored -name proof.txt | wc -l | tr -d ' ')" = 1
```

### 3. Restore application data

This folder includes the database configuration and backup script. Start a fresh lab database, seed one record, and restore its backup into a separate database:

```bash
docker compose -f files/compose.yml up -d --wait db
docker compose -f files/compose.yml exec -T db psql -U lab -d lab -c "CREATE TABLE IF NOT EXISTS proof(value text); INSERT INTO proof VALUES ('recovered');"
mkdir -p .lab/db-backups
DUMP=$(bash files/backup-db.sh "$PWD/.lab/db-backups")
restic backup "$DUMP" --tag database
restic snapshots --tag database
restic restore latest --tag database --target .lab/db-restored
RESTORED_DUMP=$(find .lab/db-restored -name "$(basename "$DUMP")")
test -n "$RESTORED_DUMP"
cmp "$DUMP" "$RESTORED_DUMP"
docker compose -f files/compose.yml exec -T db createdb -U lab restored
docker compose -f files/compose.yml exec -T db psql -v ON_ERROR_STOP=1 -U lab -d restored < "$RESTORED_DUMP"
docker compose -f files/compose.yml exec -T db psql -U lab -d restored -c 'TABLE proof;'
```

Expect a row containing recovered. Record backup age (RPO) separately from measured restore time (RTO).

The main lab covers file and logical-database recovery. Kubernetes volume recovery with Velero requires an object-storage and volume-backup setup appropriate to your cluster; it is a separate extension, not implied by a successful file restore.

## Verify completion

restic check passes, one restored proof file exactly matches expected.txt, and the restored database row matches the source.

## Troubleshooting

A wrong password cannot decrypt the repository. A backup catalog listing alone does not prove a usable restore; compare the restored bytes.

## Cleanup

After saving evidence, remove `.lab/recovery`, unset RESTIC_PASSWORD and RESTIC_REPOSITORY, and run `docker compose -f files/compose.yml down -v`.

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Performed encrypted backup and restore drills, verified recovered data and measured recovery time.”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://restic.readthedocs.io/en/stable/040_backup.html)

---

[← Previous: 30](../30.load-testing-and-resilience/README.md) · [All projects](../README.md) · [Next: 32 →](../32.cloud-secrets-integration/README.md)
