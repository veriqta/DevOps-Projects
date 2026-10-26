# 05. Package the Application With Helm

[← 04. Configure Services Routing and HTTPS](04-configure-services-routing-and-https.md) · [Project home](README.md) · [06. Add Configuration Secrets and Resource Controls →](06-add-configuration-secrets-and-resource-controls.md)

## Starting state and working directory

Complete chapter 04 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `03.kubernetes-application-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 03.kubernetes-application-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

The initial resources were applied directly. Remove only those application objects before installing a Helm-managed release; Helm cannot safely adopt arbitrary unmanaged objects without ownership metadata. The gateway and Secrets remain. A values change should generate a traceable release revision, making it easier to inspect what changed and roll back.

## Work through the implementation

Chart version identifies the package while application version identifies the workload. Changing values does not require changing the app source. Compare helm get values and helm get manifest to distinguish user inputs from the final rendered objects. A Helm rollback creates a new revision; it does not erase the audit history.

### Commands in execution order

```bash
kubectl -n orders delete deployment/orders service/orders
helm lint chart
helm upgrade --install orders chart -n orders --wait --timeout=2m
helm list -n orders
helm upgrade orders chart -n orders --set version=helm-v2 --wait
helm history orders -n orders
helm rollback orders 1 -n orders --wait
```

### Read the implementation: `chart/Chart.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
apiVersion: v2
name: orders
version: 0.1.0
appVersion: "1.0.0"
description: Orders application portfolio chart
```

## Checkpoint — verify before continuing

Helm records the original release, an upgrade and a rollback revision. After each change, health reports the expected version via a port-forward.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Do not delete the namespace, gateway or Secret while switching ownership. If Helm reports existing-resource ownership conflicts, confirm you deleted only the earlier plain Deployment and Service.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [06. Add Configuration Secrets and Resource Controls](06-add-configuration-secrets-and-resource-controls.md). The next chapter assumes the state created here.
