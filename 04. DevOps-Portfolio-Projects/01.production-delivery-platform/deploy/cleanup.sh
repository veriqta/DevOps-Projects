#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
for env in staging production;do
 for name in blue green proxy;do docker rm -f "orders-$env-$name" 2>/dev/null || true;done
 docker network rm "orders-$env" 2>/dev/null || true
done
rm -rf "${ORDERS_RUNTIME_DIR:-$HOME/.local/state/orders-delivery}"
