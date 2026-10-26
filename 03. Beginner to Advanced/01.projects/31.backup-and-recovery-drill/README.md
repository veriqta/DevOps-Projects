# 31. Backup and Recovery Drill

[← All projects](../../README.md) · **Advanced** · Restic · PostgreSQL · Velero

Prove recovery with a timed restore and a measurable recovery point.

## Prerequisites

Restic and Python. PostgreSQL extension requires project 18; the main restore drill runs entirely locally.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

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

Complete project 18, back up its completed SQL dump with Restic, remove the local dump copy, restore it into a separate directory and run project 18’s createdb/psql restore steps. Compare the table row before and after. Record backup age (RPO) separately from measured restore time (RTO).

The main lab covers file and logical-database recovery. Kubernetes volume recovery with Velero requires an object-storage and volume-backup setup appropriate to your cluster; it is a separate extension, not implied by a successful file restore.

## Verify completion

restic check passes, one restored proof file exactly matches expected.txt, and the restored database row matches the source.

## Troubleshooting

A wrong password cannot decrypt the repository. A backup catalog listing alone does not prove a usable restore; compare the restored bytes.

## Cleanup

After saving evidence, remove `.lab/recovery`, unset RESTIC_PASSWORD and RESTIC_REPOSITORY, and clean up the Compose database with down -v.

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://restic.readthedocs.io/en/stable/040_backup.html)

---

[← Previous: 30](../30.load-testing-and-resilience/README.md) · [All projects](../../README.md) · [Next: 32 →](../32.cloud-secrets-integration/README.md)
