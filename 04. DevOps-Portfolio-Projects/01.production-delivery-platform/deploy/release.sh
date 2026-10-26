#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
env=${1:?Usage: bash deploy/release.sh staging|production image@sha256:digest}
image=${2:?Supply an immutable image digest}
case "$env" in staging) port=8081;; production) port=8082;; *) exit 2;; esac
[[ "$image" =~ @sha256:[0-9a-f]{64}$ ]] || { echo 'An immutable sha256 image reference is required' >&2;exit 2; }
state="${ORDERS_RUNTIME_DIR:-$HOME/.local/state/orders-delivery}/$env";mkdir -p "$state/config"
old=$(cat "$state/active" 2>/dev/null || echo green)
if [ "$old" = blue ];then next=green;else next=blue;fi
network="orders-$env";name="orders-$env-$next";proxy="orders-$env-proxy"
docker network inspect "$network" >/dev/null 2>&1 || docker network create "$network" >/dev/null
docker pull "$image"
docker rm -f "$name" >/dev/null 2>&1 || true
docker run -d --name "$name" --network "$network" -e VERSION="${image##*@}" -e BROKEN_RELEASE="${BROKEN_RELEASE:-0}" "$image"
healthy=0
for attempt in $(seq 1 20);do
 if docker exec "$name" python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8080/health')" >/dev/null 2>&1;then healthy=1;break;fi
 sleep 1
done
if [ "$healthy" != 1 ];then docker rm -f "$name";echo 'Candidate unhealthy; active traffic unchanged' >&2;exit 1;fi
cp "$state/config/default.conf" "$state/previous.conf" 2>/dev/null || true
printf 'server { listen 80; location / { proxy_pass http://%s:8080; } }\n' "$name" > "$state/config/default.conf"
if docker inspect "$proxy" >/dev/null 2>&1;then
 if ! docker exec "$proxy" nginx -t || ! docker exec "$proxy" nginx -s reload;then
  if [ -f "$state/previous.conf" ];then cp "$state/previous.conf" "$state/config/default.conf";docker exec "$proxy" nginx -s reload;fi
  exit 1
 fi
else
 docker run -d --name "$proxy" --network "$network" -p "127.0.0.1:$port:80" -v "$state/config:/etc/nginx/conf.d:ro" nginx:stable-alpine
fi
for attempt in $(seq 1 15);do
 if curl -fsS "http://127.0.0.1:$port/health";then
  printf '%s\n' "$next" > "$state/active";printf '%s\n' "$image" > "$state/image";exit 0
 fi
 sleep 1
done
if [ -f "$state/previous.conf" ];then cp "$state/previous.conf" "$state/config/default.conf";docker exec "$proxy" nginx -s reload;fi
echo 'Proxy verification failed; previous configuration restored where available' >&2
exit 1
