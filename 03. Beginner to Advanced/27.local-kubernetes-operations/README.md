# 27. Local Kubernetes Operations

[← All projects](../README.md) · **Intermediate** · kind · kubectl · Kustomize

Deploy the demo to a local cluster and debug a failed rollout.

## Prerequisites

Docker, kind and kubectl. At least 4 GB available memory.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Files included

Everything below is inside this project’s `files/` folder.

| File or folder | Use |
| --- | --- |
| `app` | Demo HTTP service, Dockerfile and service unit. |
| `kubernetes.yml` | Configuration or starter code referenced in the steps below. |
| `kustomize` | Kubernetes base and lab overlay. |

## Walkthrough

From the repository root, enter this project:

```bash
cd 27.local-kubernetes-operations
```

Run the remaining commands here unless a step explicitly changes directories. The `files/` folder contains the supplied code and configurations for this project.

### 1. Create an isolated cluster and load the image

```bash
kind create cluster --name devops-lab
kubectl config current-context
docker build -t devops-demo:lab files/app
kind load docker-image devops-demo:lab --name devops-lab
kubectl create namespace devops-lab
kubectl kustomize files/kustomize/overlays/lab
kubectl apply -k files/kustomize/overlays/lab
kubectl -n devops-lab rollout status deployment/demo --timeout=120s
kubectl -n devops-lab port-forward service/demo 8080:80
```

The context must be kind-devops-lab. Leave port-forward running; in another terminal request `curl -fsS localhost:8080/health`. Stop port-forward with Ctrl+C.

### 2. Diagnose a failed rollout

```bash
kubectl -n devops-lab set image deployment/demo demo=devops-demo:missing
kubectl -n devops-lab rollout status deployment/demo --timeout=30s
kubectl -n devops-lab get pods
kubectl -n devops-lab get events --sort-by=.metadata.creationTimestamp
kubectl -n devops-lab rollout undo deployment/demo
kubectl -n devops-lab rollout status deployment/demo --timeout=120s
```

The rollout-status timeout is expected. Inspect an affected pod with kubectl describe before undoing.

## Verify completion

The overlay renders three replicas in devops-lab, all become ready, an invalid image triggers ImagePullBackOff and undo restores readiness.

## Troubleshooting

A missing local image requires kind load after building. Check current-context before every mutation; avoid operating on an unrelated cluster.

## Cleanup

`kind delete cluster --name devops-lab`

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented local kubernetes operations in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://kind.sigs.k8s.io/docs/user/quick-start/)

---

[← Previous: 26](../26.service-discovery/README.md) · [All projects](../README.md) · [Next: 28 →](../28.gitops-delivery/README.md)
