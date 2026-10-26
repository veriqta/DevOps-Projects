# 01. Start PostgreSQL and Create Known Test Data

[← 00. Data Loss Scenario and Recovery Objectives](00-data-loss-scenario-and-recovery-objectives.md) · [Project home](README.md) · [02. Configure the Backup Repository and Credentials →](02-configure-the-backup-repository-and-credentials.md)

## Starting state and working directory

Complete chapter 00 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `06.database-disaster-recovery` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 06.database-disaster-recovery
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Initialize storage ownership before starting the database. Docker named volumes can begin owned by root, while PostgreSQL writes as postgres. The helper changes only the archive and backup volume ownership. The password is read from a Compose Secret backed by a local file, keeping it out of YAML and shell arguments.

## Work through the implementation

The default local socket access inside this disposable container allows the supplied admin commands. Do not equate that with a hardened database authentication design. The restore helper refuses to overwrite an already initialized recovery volume so a repeat attempt cannot silently destroy a previous recovery.

### Commands in execution order

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl git jq unzip python3 python3-venv openssl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
. /etc/os-release
printf 'deb [arch=%s signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu %s stable\n' "$(dpkg --print-architecture)" "$VERSION_CODENAME" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker "$USER"

```

Log out of the Ubuntu session and reconnect before continuing so Docker group membership is active. Verify `docker version` shows the server. Then run:

```bash
mkdir -p .lab
umask 077
openssl rand -base64 32 > .lab/db-password
bash database/prepare-volumes.sh
docker compose up -d --wait db
docker compose exec -T db psql -U postgres -d orders < database/seed.sql
docker compose exec -T db psql -U postgres -d orders -c 'TABLE orders;'
```

### Read the implementation: `compose.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
name: portfolio-recovery
services:
  db:
    image: postgres:17-alpine
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_DB: orders
    secrets: [db_password]
    command: ["postgres", "-c", "wal_level=replica", "-c", "archive_mode=on", "-c", "archive_command=(test -f /archive/%f && cmp -s %p /archive/%f) || (test ! -f /archive/%f && cp %p /archive/%f)", "-c", "archive_timeout=30s"]
    volumes:
      - data:/var/lib/postgresql/data
      - archive:/archive
      - backup:/backup
      - ./database/init.sh:/docker-entrypoint-initdb.d/10-init.sh:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d orders"]
      interval: 5s
      timeout: 3s
      retries: 20
  restore:
    image: postgres:17-alpine
    profiles: [restore]
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_DB: orders
    secrets: [db_password]
    volumes:
      - restored:/var/lib/postgresql/data
      - archive:/archive:ro
secrets:
  db_password:
    file: .lab/db-password
volumes:
  data: {}
  archive: {}
  backup: {}
  restored: {}
```

### Read the implementation: `database/prepare-volumes.sh`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```bash
#!/usr/bin/env bash
set -euo pipefail
docker compose run --rm --no-deps --user root --entrypoint sh db -c 'mkdir -p /archive /backup; chown postgres:postgres /archive /backup'
```

### Read the implementation: `database/init.sh`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```bash
#!/bin/sh
set -eu
mkdir -p /archive /backup
chown postgres:postgres /archive /backup
```

### Read the implementation: `database/seed.sql`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```sql
CREATE TABLE IF NOT EXISTS orders(id integer PRIMARY KEY, item text NOT NULL);
INSERT INTO orders VALUES (1,'book'),(2,'keyboard') ON CONFLICT DO NOTHING;
```

## Checkpoint — verify before continuing

The database becomes healthy and shows exactly the two known rows. No host database port is published. Preserve the output as the baseline for later recovery verification.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Permission denied under /archive means volume preparation did not run. A changed password file does not reset an already initialized PostgreSQL user; use a fresh lab volume or explicitly manage the database password.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [02. Configure the Backup Repository and Credentials](02-configure-the-backup-repository-and-credentials.md). The next chapter assumes the state created here.
