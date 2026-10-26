#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# Run on a disposable Docker host: this script removes its own named lab volumes.
files=(02.examples/compose.yml 02.examples/observability.yml 02.examples/multiservice/compose.yml 02.examples/consul/compose.yml 02.examples/bluegreen/compose.yml)
cleanup() {
  for file in "${files[@]}"; do docker compose -f "$file" down -v --remove-orphans >/dev/null 2>&1 || true; done
  rm -rf 02.examples/bluegreen/config
}
trap cleanup EXIT
for file in "${files[@]}"; do docker compose -f "$file" config --quiet; done
retry() { for i in $(seq 1 60); do if "$@"; then return 0; fi; sleep 2; done; return 1; }
health() { curl -fsS http://127.0.0.1:8080/health >/dev/null; }
docker compose -f 02.examples/compose.yml up -d --build --wait
retry health
docker compose -f 02.examples/compose.yml exec -T db psql -v ON_ERROR_STOP=1 -U lab -d lab -c "CREATE TABLE smoke_proof(value text); INSERT INTO smoke_proof VALUES ('restored-exactly');"
latest=$(bash 03.tools/backup-db.sh "$PWD/.lab/smoke-backups")
docker compose -f 02.examples/compose.yml exec -T db createdb -U lab restored
docker compose -f 02.examples/compose.yml exec -T db psql -v ON_ERROR_STOP=1 -U lab -d restored < "$latest"
test "$(docker compose -f 02.examples/compose.yml exec -T db psql -At -U lab -d restored -c 'SELECT value FROM smoke_proof')" = restored-exactly
docker compose -f 02.examples/compose.yml down -v
docker compose -f 02.examples/observability.yml up -d --build
retry health
retry curl -fsS http://127.0.0.1:9090/-/ready
docker compose -f 02.examples/observability.yml exec -T prometheus promtool check config /etc/prometheus/prometheus.yml
docker compose -f 02.examples/observability.yml down -v
docker compose -f 02.examples/multiservice/compose.yml up -d --build
retry health
id=$(curl -fsS -H 'Content-Type: application/json' -d '{"value":"hello"}' localhost:8080/jobs | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])')
job_done() { curl -fsS "localhost:8080/jobs/$id" | python3 -c 'import json,sys; assert json.load(sys.stdin)["result"]=="HELLO"'; }
retry job_done
docker compose -f 02.examples/multiservice/compose.yml down -v
docker compose -f 02.examples/consul/compose.yml up -d --build
consul_count() { curl -fsS 'localhost:8500/v1/health/service/demo?passing=true' | python3 -c "import json,sys; assert len(json.load(sys.stdin))==$1"; }
retry consul_count 1
docker compose -f 02.examples/consul/compose.yml stop app
retry consul_count 0
docker compose -f 02.examples/consul/compose.yml down -v
mkdir -p 02.examples/bluegreen/config
cp 02.examples/bluegreen/blue.conf 02.examples/bluegreen/config/default.conf
docker compose -f 02.examples/bluegreen/compose.yml up -d --build
retry health
version() { curl -fsS localhost:8080/health | python3 -c "import json,sys; assert json.load(sys.stdin)['version']=='$1'"; }
retry version blue
for color in green blue; do
  cp "02.examples/bluegreen/$color.conf" 02.examples/bluegreen/config/default.conf
  docker compose -f 02.examples/bluegreen/compose.yml exec -T proxy nginx -t
  docker compose -f 02.examples/bluegreen/compose.yml exec -T proxy nginx -s reload
  retry version "$color"
done
printf 'All container smoke checks passed\n'
