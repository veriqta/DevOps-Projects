# 08. Introduce a Failed Release and Roll Back

[← 07. Promote the Same Release With Approval](07-promote-the-same-release-with-approval.md) · [Project home](README.md) · [09. Capture Evidence and Remove Lab Resources →](09-capture-evidence-and-remove-lab-resources.md)

## Starting state and working directory

Complete chapter 07 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `01.production-delivery-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 01.production-delivery-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A useful release portfolio must demonstrate the negative path. BROKEN_RELEASE makes health fail before traffic is switched, so the script should return nonzero and leave the last healthy release serving. A rollback after a healthy but functionally wrong release is different: redeploy the saved earlier digest. Both cases matter; neither replaces testing database migration compatibility in a stateful application.

### Commands in execution order

```bash
BEFORE=$(cat $HOME/.local/state/orders-delivery/production/image)
BROKEN_RELEASE=1 bash deploy/release.sh production "$IMAGE"
# Expect the command above to fail. Continue with the checks below.
test "$(cat $HOME/.local/state/orders-delivery/production/image)" = "$BEFORE"
curl -fsS localhost:8082/health
bash deploy/release.sh production "$BEFORE"
curl -fsS localhost:8082/health
```

## Checkpoint — verify before continuing

The unhealthy candidate exits nonzero and production remains healthy. Record start/end timestamps and the old/new digest. To demonstrate a different-version rollback, publish a second commit, promote it, then redeploy the first saved digest.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Do not interpret an expected nonzero exit as a broken exercise. If active traffic changes during the rejected candidate, inspect the script order and fix it before continuing. Never remove the healthy proxy while diagnosing the inactive candidate.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [09. Capture Evidence and Remove Lab Resources](09-capture-evidence-and-remove-lab-resources.md). The next chapter assumes the state created here.
