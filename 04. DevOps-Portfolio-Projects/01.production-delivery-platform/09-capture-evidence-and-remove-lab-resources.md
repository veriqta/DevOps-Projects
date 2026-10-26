# 09. Capture Evidence and Remove Lab Resources

[← 08. Introduce a Failed Release and Roll Back](08-introduce-a-failed-release-and-roll-back.md) · [Project home](README.md)

## Starting state and working directory

Complete chapter 08 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `01.production-delivery-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 01.production-delivery-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

The finished artifact is the system plus evidence that it behaves as claimed. Capture a release record tying source commit, test run, image digest, approval and verification together. Report the measured recovery duration from your own drill. A professional handover also explains limitations: one lab host, HTTP behind loopback, an in-memory order list and a manually provisioned Docker daemon.

## Work through the implementation

Create a short portfolio report with: architecture; commit and digest; failed and corrected CI runs; reviewer wait; successful checkout; rejected candidate; earlier-version rollback; recovery time; and cleanup proof. A résumé example after completion is “Built a digest-based delivery pipeline with staging, approval and health-gated rollout; demonstrated recovery in [measured time].” Be ready to explain why a green health check is not enough, what changes for a database migration, and how you would separate production hosts. Replace the measurement and describe the work as a portfolio lab.

### Commands in execution order

```bash
bash deploy/cleanup.sh
docker ps --filter name=orders-
docker network ls --filter name=orders-
```

### Read the implementation: `deploy/cleanup.sh`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
for env in staging production;do
 for name in blue green proxy;do docker rm -f "orders-$env-$name" 2>/dev/null || true;done
 docker network rm "orders-$env" 2>/dev/null || true
done
rm -rf "${ORDERS_RUNTIME_DIR:-$HOME/.local/state/orders-delivery}"
```

## Checkpoint — verify before continuing

No project containers or networks remain. Stop/remove the dedicated runner service with sudo ./svc.sh stop and sudo ./svc.sh uninstall from ~/actions-runner. Remove the runner in GitHub Settings → Actions → Runners; use the displayed removal token if ./config.sh remove is needed. Disable the copied deployment workflows, revoke unneeded lab keys and remove unneeded GHCR versions. Delete the charged lab VM and inspect its provider disks/public-IP allocations.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If a network is still attached, inspect docker network inspect before removing anything. Delete only this project’s containers. Stopping a VM does not necessarily remove disks or public-IP charges.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

The project is complete only after the acceptance checks pass and the lab resources are removed. Publish your sanitized implementation and evidence in your own portfolio repository.
