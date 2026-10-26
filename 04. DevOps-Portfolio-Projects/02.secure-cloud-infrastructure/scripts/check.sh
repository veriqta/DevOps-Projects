#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../terraform"
url=$(terraform output -raw url)
for attempt in $(seq 1 60);do
 if curl -fsS --connect-timeout 5 "$url" | grep -q 'Orders foundation';then echo 'Application verified through ALB';exit 0;fi
 sleep 10
done
exit 1
