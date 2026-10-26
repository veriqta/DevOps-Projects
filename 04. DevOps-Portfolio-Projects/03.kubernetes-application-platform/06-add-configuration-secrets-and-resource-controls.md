# 06. Add Configuration Secrets and Resource Controls

[← 05. Package the Application With Helm](05-package-the-application-with-helm.md) · [Project home](README.md) · [07. Reconcile Releases Through GitOps →](07-reconcile-releases-through-gitops.md)

## Starting state and working directory

Complete chapter 05 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `03.kubernetes-application-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 03.kubernetes-application-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Configuration should be explicit and reviewable. The chart injects a welcome message, a release version and a reference to a pre-existing Secret. Changing a Secret’s value does not automatically restart pods that read it into environment variables. Explain the operational difference between updating a resource and refreshing the process that consumes it.

## Work through the implementation

The welcome variable is an example of runtime injection; the current HTTP API does not display it. Inspect the pod spec to prove injection rather than claiming it changes business behavior. Before production, replace the dummy token with a real workload identity or secret integration and enforce restricted RBAC for Secret reads.

### Commands in execution order

```bash
helm upgrade orders chart -n orders --set message="Portfolio checkout" --set cpuRequest=150m --wait
kubectl -n orders describe deployment orders
kubectl -n orders get secret orders-runtime -o jsonpath='{.metadata.name}'
kubectl -n orders rollout restart deployment/orders
kubectl -n orders rollout status deployment/orders --timeout=120s
```

## Checkpoint — verify before continuing

Resource requests reflect the chosen values and the application still passes checkout. The Secret value does not appear in the chart or Git history. Record why the limits are lab baselines rather than measured capacity recommendations.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

An insufficient CPU request and a hard CPU limit are different concepts. Pending pods need scheduler events; OOMKilled pods need memory investigation. Do not solve either by removing every resource control.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [07. Reconcile Releases Through GitOps](07-reconcile-releases-through-gitops.md). The next chapter assumes the state created here.
