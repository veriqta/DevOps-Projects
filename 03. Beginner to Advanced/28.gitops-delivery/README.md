# 28. GitOps Delivery

[← All projects](../README.md) · **Advanced** · Flux · Kubernetes

Reconcile a lab deployment from your own Git repository.

## Prerequisites

Project 27 image built, kind, kubectl, Flux, Git, and a writable GitHub account. Use a new dedicated GitOps repository.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Files included

Everything below is inside this project’s `files/` folder.

| File or folder | Use |
| --- | --- |
| `app` | Demo HTTP service, Dockerfile and service unit. |
| `kubernetes.yml` | Configuration or starter code referenced in the steps below. |

## Walkthrough

From the repository root, enter this project:

```bash
cd 28.gitops-delivery
```

Run the remaining commands here unless a step explicitly changes directories. The `files/` folder contains the supplied code and configurations for this project.

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

From this project folder:

```bash
LAB_ROOT=$PWD
mkdir -p .lab
git clone "https://github.com/$GITHUB_USER/devops-gitops-lab.git" .lab/gitops
cd .lab/gitops
mkdir -p clusters/lab/demo
cp "$LAB_ROOT/files/kubernetes.yml" clusters/lab/demo/deployment.yaml
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

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented gitops delivery in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://fluxcd.io/flux/get-started/)

---

[← Previous: 27](../27.local-kubernetes-operations/README.md) · [All projects](../README.md) · [Next: 29 →](../29.supply-chain-security/README.md)
