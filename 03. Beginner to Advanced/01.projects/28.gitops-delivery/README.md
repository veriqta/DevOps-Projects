# 28. GitOps Delivery

[← All projects](../../README.md) · **Advanced** · Flux · Kubernetes

Reconcile a lab deployment from your own Git repository.

## Prerequisites

Project 27 image built, kind, kubectl, Flux, Git, and a writable GitHub account. Use a new dedicated GitOps repository.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Create a fresh lab cluster

```bash
kind create cluster --name gitops-lab
kind load docker-image devops-demo:lab --name gitops-lab
kubectl config current-context
flux check --pre
```

Expect kind-gitops-lab. In GitHub create a personal access token with repository permissions required by Flux bootstrap. Keep it out of files:

```bash
export GITHUB_USER=REPLACE_WITH_YOUR_USERNAME
read -rsp 'GitHub bootstrap token: ' GITHUB_TOKEN; echo
export GITHUB_TOKEN
flux bootstrap github --owner="$GITHUB_USER" --repository=devops-gitops-lab --branch=main --path=clusters/lab --personal
unset GITHUB_TOKEN
```

Bootstrap creates/configures the dedicated repository and deploy key. Use your own account, never the archived upstream.

### 2. Add the workload

From the DevOps-Projects root:

```bash
LAB_ROOT=$PWD
git clone "https://github.com/$GITHUB_USER/devops-gitops-lab.git" .lab/gitops
cd .lab/gitops
mkdir -p clusters/lab/demo
cp "$LAB_ROOT/02.examples/kubernetes.yml" clusters/lab/demo/deployment.yaml
printf 'resources:\n  - deployment.yaml\n' > clusters/lab/demo/kustomization.yaml
git add .
git commit -m "Reconcile demo service"
git push
flux reconcile source git flux-system
flux reconcile kustomization flux-system --with-source
kubectl rollout status deployment/demo --timeout=120s
```

Flux recursively finds the child kustomization from its generated root build.

### 3. Prove drift correction and rollback

```bash
kubectl scale deployment/demo --replicas=5
flux reconcile kustomization flux-system
kubectl get deployment demo
```

Expect two replicas again. Edit the committed manifest to replicas 3, commit/push and reconcile. Then `git revert HEAD`, push and reconcile to restore two.

## Verify completion

Flux reports Ready, Git changes affect replicas, manual drift is corrected and a revert rolls back the change.

## Troubleshooting

If Git cannot push over HTTPS, configure your own Git credential manager. Never embed the token in a remote URL or committed file.

## Cleanup

`kind delete cluster --name gitops-lab`. Delete the dedicated GitHub lab repository and revoke the bootstrap token/deploy key when finished.

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://fluxcd.io/flux/get-started/)

---

[← Previous: 27](../27.local-kubernetes-operations/README.md) · [All projects](../../README.md) · [Next: 29 →](../29.supply-chain-security/README.md)
