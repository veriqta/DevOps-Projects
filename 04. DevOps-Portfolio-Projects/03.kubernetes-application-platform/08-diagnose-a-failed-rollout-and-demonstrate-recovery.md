# 08. Diagnose a Failed Rollout and Demonstrate Recovery

[← 07. Reconcile Releases Through GitOps](07-reconcile-releases-through-gitops.md) · [Project home](README.md) · [09. Collect Platform Evidence and Delete the Cluster →](09-collect-platform-evidence-and-delete-the-cluster.md)

## Starting state and working directory

Complete chapter 07 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `03.kubernetes-application-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 03.kubernetes-application-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A bad image should surface as failed readiness and controller status, not a mysterious website failure. Change the image through Git to orders:missing, wait for reconciliation and inspect the resulting events. Recovery is a Git revert so desired state and actual state agree again. A direct kubectl fix can be overwritten by the next reconciliation.

## Work through the implementation

Use git log to identify the deliberate bad-image commit, then run git revert THAT_COMMIT_SHA and git push from this repository. Run the reconciliation commands again. Watch flux get helmreleases -A and kubectl rollout status; a controller timeout may take longer than the readiness of the restored pods. Preserve both status and customer-request evidence.

### Commands in execution order

```bash
kubectl -n orders get helmrelease
kubectl -n orders get pods
kubectl -n orders get events --sort-by=.metadata.creationTimestamp
# After committing and pushing image: orders:missing, inspect the failure.
flux reconcile source git portfolio
flux reconcile kustomization orders-platform --with-source
kubectl -n orders describe deployment orders
```

## Checkpoint — verify before continuing

Record the failing revision and ImagePullBackOff events. Revert that specific Git commit, push, reconcile source and Kustomization, then wait until HelmRelease Ready and the Orders deployment is healthy again. Retest HTTPS checkout.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Helm may retain old healthy pods during an upgrade failure, so customer impact can differ from deployment failure. Record what you actually observed. Do not claim an outage merely because the candidate failed.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [09. Collect Platform Evidence and Delete the Cluster](09-collect-platform-evidence-and-delete-the-cluster.md). The next chapter assumes the state created here.
