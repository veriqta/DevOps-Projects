# 17. Multi-Container Application

[← All projects](../../README.md) · **Intermediate** · Docker Compose · PostgreSQL

Operate an HTTP service and database with health checks and persistent storage.

## Prerequisites

Docker Compose v2. Stop other labs on port 8080.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Start the stack

```bash
docker compose -f 02.examples/compose.yml config
docker compose -f 02.examples/compose.yml up -d --build --wait
curl -fsS localhost:8080/health
```

The HTTP demo and PostgreSQL are separate services. The HTTP demo does not query the database; use psql to practice storage independently.

### 2. Create persistent data

```bash
docker compose -f 02.examples/compose.yml exec -T db psql -U lab -d lab -c "CREATE TABLE IF NOT EXISTS notes (id integer PRIMARY KEY, message text); INSERT INTO notes VALUES (1,'survives restart') ON CONFLICT DO NOTHING;"
docker compose -f 02.examples/compose.yml up -d --force-recreate db
docker compose -f 02.examples/compose.yml exec -T db psql -U lab -d lab -c 'TABLE notes;'
```

### 3. Inspect isolation

```bash
docker compose -f 02.examples/compose.yml ps
docker compose -f 02.examples/compose.yml logs --tail 20 db
```

Only the HTTP port is published on loopback. PostgreSQL uses a named volume; its supplied password is for this isolated local lab only.

## Verify completion

The notes row remains after database-container recreation. The database has no published host port.

## Troubleshooting

PostgreSQL may still be starting after recreation. Check health in compose ps and retry psql when healthy.

## Cleanup

`docker compose -f 02.examples/compose.yml down -v` deletes the lab data.

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://docs.docker.com/compose/intro/compose-application-model/)

---

[← Previous: 16](../16.dockerized-service/README.md) · [All projects](../../README.md) · [Next: 18 →](../18.automated-db-backups/README.md)
