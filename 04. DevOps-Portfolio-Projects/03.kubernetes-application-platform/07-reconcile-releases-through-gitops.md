# 07. Reconcile Releases Through GitOps

[← 06. Add Configuration Secrets and Resource Controls](06-add-configuration-secrets-and-resource-controls.md) · [Project home](README.md) · [08. Diagnose a Failed Rollout and Demonstrate Recovery →](08-diagnose-a-failed-rollout-and-demonstrate-recovery.md)

## Starting state and working directory

Complete chapter 06 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `03.kubernetes-application-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 03.kubernetes-application-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Flux continuously reconciles a declared release from a Git revision. Install controllers into this disposable cluster, create a source pointing at your own public repository and let a Flux Kustomization manage the HelmRelease. The source URL is a literal file input you must replace before committing; placeholders are not valid repository addresses. Once Flux owns the release, make changes through Git rather than manual Helm commands.

## Work through the implementation

The GitRepository watches the branch; the Kustomization applies the GitOps directory; HelmRelease asks helm-controller to build the chart from that source. ReconcileStrategy Revision ensures a changed Git revision can rebuild the chart. Secret creation remains a documented manual bootstrap boundary, not something silently stored in Git.

### Commands in execution order

```bash
helm uninstall orders -n orders
curl -fsSL https://fluxcd.io/install.sh -o .lab/tools/install-flux.sh
# Read the downloaded official installer before executing it.
sudo bash .lab/tools/install-flux.sh
flux check --pre
flux install
# Edit gitops/release.yaml: replace REPLACE_USER and REPLACE_REPO.
git add gitops chart
git commit -m "Declare Orders GitOps release"
git push
kubectl apply -f gitops/release.yaml
kubectl apply -f platform/sync.yaml
flux reconcile source git portfolio
flux reconcile kustomization orders-platform --with-source
kubectl -n orders rollout status deployment/orders --timeout=180s
```

### Read the implementation: `gitops/release.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: portfolio
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/REPLACE_USER/REPLACE_REPO
  ref: {branch: main}
```

### Read the implementation: `gitops/helmrelease.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: orders
  namespace: orders
spec:
  interval: 1m
  chart:
    spec:
      chart: ./03.kubernetes-application-platform/chart
      sourceRef: {kind: GitRepository, name: portfolio, namespace: flux-system}
      reconcileStrategy: Revision
  values:
    image: orders:lab
    replicas: 2
    version: gitops-v1
    secretName: orders-runtime
```

### Read the implementation: `platform/sync.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: orders-platform
  namespace: flux-system
spec:
  interval: 1m
  path: ./03.kubernetes-application-platform/gitops
  prune: true
  sourceRef: {kind: GitRepository, name: portfolio}
```

### Read the implementation: `gitops/kustomization.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
resources:
  - release.yaml
  - helmrelease.yaml
```

## Checkpoint — verify before continuing

Flux source, Kustomization and HelmRelease report Ready. Commit replicas: 3 in gitops/helmrelease.yaml, push and reconcile; three pods appear. Manually scale to five, then reconcile and observe correction to three.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

A private Git repository needs a source Secret and is outside this public-source core path. A source Ready=False requires checking URL, branch and pushed file path before looking at Helm.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [08. Diagnose a Failed Rollout and Demonstrate Recovery](08-diagnose-a-failed-rollout-and-demonstrate-recovery.md). The next chapter assumes the state created here.
