# 18. Automated DB Backups

[← All projects](../../README.md) · **Intermediate** · PostgreSQL · cron

Back up a lab database every 12 hours and prove restoration.

## Prerequisites

Project 17, Docker Compose v2 and cron on a Linux lab host. Keep backups private.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Seed data and back up

```bash
docker compose -f 02.examples/compose.yml up -d --wait db
docker compose -f 02.examples/compose.yml exec -T db psql -U lab -d lab -c "CREATE TABLE IF NOT EXISTS notes (id integer PRIMARY KEY, message text); INSERT INTO notes VALUES (1,'backup proof') ON CONFLICT DO NOTHING;"
mkdir -p .lab/backups
BACKUP=$(bash 03.tools/backup-db.sh "$PWD/.lab/backups")
test -s "$BACKUP"
```

### 2. Restore to a separate database

```bash
docker compose -f 02.examples/compose.yml exec -T db createdb -U lab restored
docker compose -f 02.examples/compose.yml exec -T db psql -v ON_ERROR_STOP=1 -U lab -d restored < "$BACKUP"
docker compose -f 02.examples/compose.yml exec -T db psql -U lab -d restored -c 'TABLE notes;'
```

### 3. Schedule every 12 hours — on the Linux Docker host

Run `command -v docker` and `pwd`. Open `crontab -e` and add the following, replacing both `/absolute/path/DevOps-Projects` paths with your repository path:

```cron
PATH=/usr/local/bin:/usr/bin:/bin
0 */12 * * * /bin/bash /absolute/path/DevOps-Projects/03.tools/backup-db.sh /absolute/path/DevOps-Projects/.lab/backups >> /absolute/path/DevOps-Projects/.lab/backup.log 2>&1
```

Run the exact cron command manually first. Confirm the cron user can access Docker. This schedule runs at 00:00 and 12:00 in the host timezone; it does not guarantee a backup precisely 12 hours after every reboot.

### 4. Test failure and retention

Stop the db service, run backup-db.sh and expect a nonzero exit with no completed `.sql` file. Restart db. Review backups older than seven days before deleting them:

```bash
find .lab/backups -type f -name 'lab-*.sql' -mtime +7 -print
```

## Verify completion

The restored row matches the original. Failed dumps do not leave a completed backup. Record the scheduled timezone and prove at least one scheduled invocation.

## Troubleshooting

If restored already exists, drop only that lab database with dropdb before retrying. A cron failure is often PATH or Docker permissions.

## Cleanup

Remove your cron line using crontab -e, then `docker compose -f 02.examples/compose.yml down -v`. Remove `.lab/backups` after saving evidence.

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://www.postgresql.org/docs/current/backup-dump.html)

---

[← Previous: 17](../17.multi-container-application/README.md) · [All projects](../../README.md) · [Next: 19 →](../19.bastion-host/README.md)
