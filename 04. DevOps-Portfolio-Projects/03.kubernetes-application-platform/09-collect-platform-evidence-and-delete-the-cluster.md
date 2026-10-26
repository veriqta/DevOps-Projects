# 09. Collect Platform Evidence and Delete the Cluster

[← 08. Diagnose a Failed Rollout and Demonstrate Recovery](08-diagnose-a-failed-rollout-and-demonstrate-recovery.md) · [Project home](README.md)

## Starting state and working directory

Complete chapter 08 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `03.kubernetes-application-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 03.kubernetes-application-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A platform handover needs to explain ownership, trust and recovery. Show the Service request path, the TLS verification command, the rendered chart, Git revision, reconciliation status and the failed-release recovery. Distinguish a local learning cluster from managed production Kubernetes and record the manual Secret/bootstrap boundaries.

## Work through the implementation

Prepare a short demo: explain request routing, show valid and invalid TLS checks, change replicas through Git, trigger an invalid image, and recover through a revert. A truthful résumé bullet might describe building a Helm/GitOps application platform with HTTPS and verified drift correction. Discuss how you would add workload identity, admission policy, managed certificates and multiple real failure domains without claiming those were implemented here.

### Commands in execution order

```bash
kind delete cluster --name orders-platform
kind get clusters
rm -rf .lab
# Remove or archive any lab-only public repository content you no longer need.
```

## Checkpoint — verify before continuing

orders-platform no longer appears in kind get clusters, and its Docker node containers are gone. The generated TLS private key has been removed. No cloud resources were created by the core path.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If cluster deletion fails, inspect kind node containers before manually removing anything. Do not delete another cluster or the whole Docker daemon state.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

The project is complete only after the acceptance checks pass and the lab resources are removed. Publish your sanitized implementation and evidence in your own portfolio repository.
