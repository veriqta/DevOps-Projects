# 06. Deploy and Verify Staging

[← 05. Publish and Identify an Immutable Release](05-publish-and-identify-an-immutable-release.md) · [Project home](README.md) · [07. Promote the Same Release With Approval →](07-promote-the-same-release-with-approval.md)

## Starting state and working directory

Complete chapter 05 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `01.production-delivery-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 01.production-delivery-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

The release script creates an inactive blue/green candidate, checks it inside its container network, then rewrites the proxy only if it is healthy. The old color remains available until the next deployment replaces that inactive slot. This is a two-slot lab, not unlimited release history. Nginx sees the entire configuration directory as a bind mount so changing the file is visible inside the proxy.

## Work through the implementation

First run this manually on the Docker host from a copy of this project so you can inspect each resource. `docker network ls`, `docker ps --filter name=orders-staging` and `$HOME/.local/state/orders-delivery/staging/config/default.conf` show the implementation. Each script step either creates a missing resource, validates the candidate, or commits the traffic switch. No external application port is opened on the VM. Release state is stored under $HOME/.local/state/orders-delivery, outside the Git checkout, so checkout cleanup cannot erase an active proxy configuration.

### Commands in execution order

```bash
bash deploy/release.sh staging "$IMAGE"
curl -fsS localhost:8081/health
curl -fsS -H 'Content-Type: application/json' -d '{"item":"staging-check"}' localhost:8081/checkout
cat $HOME/.local/state/orders-delivery/staging/image
```

### Read the implementation: `deploy/release.sh`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```bash
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
```

## Checkpoint — verify before continuing

Staging health and checkout pass. The recorded image equals IMAGE and the container version contains the same sha256 digest. On a remote host run these commands there; forward local port 8081 with ssh -L 8081:127.0.0.1:8081 USER@HOST to inspect it from your workstation.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

A candidate health failure leaves the active proxy unchanged. Inspect docker logs orders-staging-blue or green. A proxy failure requires docker logs orders-staging-proxy and nginx -t, not opening extra firewall ports.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [07. Promote the Same Release With Approval](07-promote-the-same-release-with-approval.md). The next chapter assumes the state created here.
