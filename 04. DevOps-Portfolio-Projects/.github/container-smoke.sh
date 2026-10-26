#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
root=$PWD
cleanup() {
  (cd "$root/01.production-delivery-platform" && bash deploy/cleanup.sh) >/dev/null 2>&1 || true
  for folder in 04.sre-observability-and-incidents 06.database-disaster-recovery 08.cloud-cost-and-capacity;do
    (cd "$root/$folder" && docker compose --profile restore down -v) >/dev/null 2>&1 || true
  done
  docker rm -f portfolio-test-registry >/dev/null 2>&1 || true
}
trap cleanup EXIT
retry() { for i in $(seq 1 40);do if "$@";then return 0;fi;sleep 2;done;return 1; }
# Digest-based delivery and rejected candidate; the registry exists only on loopback.
docker run -d --name portfolio-test-registry -p 127.0.0.1:5000:5000 registry:2
retry curl -fsS http://127.0.0.1:5000/v2/
cd "$root/01.production-delivery-platform"
docker build -t 127.0.0.1:5000/orders:lab app
docker push 127.0.0.1:5000/orders:lab
image=$(docker image inspect --format '{{index .RepoDigests 0}}' 127.0.0.1:5000/orders:lab)
bash deploy/release.sh staging "$image"
bash deploy/release.sh production "$image"
if BROKEN_RELEASE=1 bash deploy/release.sh production "$image";then echo 'Unhealthy release was accepted' >&2;exit 1;fi
curl -fsS localhost:8082/health
bash deploy/cleanup.sh
# Real database backup, delete, independent PITR restore and promotion check.
cd "$root/06.database-disaster-recovery"
mkdir -p .lab
printf 'disposable-test-password' > .lab/db-password
bash database/prepare-volumes.sh
docker compose up -d --wait db
docker compose exec -T db psql -v ON_ERROR_STOP=1 -U postgres -d orders < database/seed.sql
bash scripts/backup.sh
xid=$(docker compose exec -T db psql -At -U postgres -d orders -c 'WITH removed AS (DELETE FROM orders RETURNING *) SELECT txid_current();')
segment=$(docker compose exec -T db psql -At -U postgres -d orders -c 'SELECT pg_walfile_name(pg_current_wal_lsn());')
docker compose exec -T db psql -U postgres -d orders -c 'SELECT pg_switch_wal();'
retry docker compose exec -T db test -f "/archive/$segment"
bash scripts/restore.sh "$xid"
bash scripts/verify.sh
docker compose --profile restore down -v
# Observability stack accepts telemetry, not just configuration text.
cd "$root/04.sre-observability-and-incidents"
docker compose up -d --build
retry curl -fsS localhost:8080/health
curl -fsS -H 'Content-Type: application/json' -d '{"item":"smoke"}' localhost:8080/checkout
docker compose exec -T prometheus promtool check config /etc/prometheus/prometheus.yml
trace_available() {
  docker compose exec -T app python -c 'import json,urllib.request; e=json.loads(open("/logs/orders.json").readlines()[-1]); r=urllib.request.urlopen("http://tempo:3200/api/traces/"+e["trace_id"]);assert r.status==200'
}
retry trace_available
logs_available() {
  docker compose exec -T app python -c 'import json,urllib.request; r=json.load(urllib.request.urlopen("http://loki:3100/loki/api/v1/query_range?query=%7Bservice_name%3D%22orders%22%7D&limit=20"));assert r["data"]["result"]'
}
retry logs_available
docker compose down -v
# Capacity fixture starts with the declared constraints.
cd "$root/08.cloud-cost-and-capacity"
docker compose up -d --build
retry curl -fsS localhost:8080/health
curl -fsS -H 'Content-Type: application/json' -d '{"item":"capacity"}' localhost:8080/checkout
docker compose down
printf 'Container smoke checks passed\n'
