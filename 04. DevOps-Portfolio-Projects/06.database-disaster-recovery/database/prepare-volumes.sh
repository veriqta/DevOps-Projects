#!/usr/bin/env bash
set -euo pipefail
docker compose run --rm --no-deps --user root --entrypoint sh db -c 'mkdir -p /archive /backup; chown postgres:postgres /archive /backup'
