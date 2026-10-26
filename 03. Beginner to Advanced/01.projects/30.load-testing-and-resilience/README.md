# 30. Load Testing and Resilience

[← All projects](../../README.md) · **Advanced** · k6 · Chaos Mesh

Measure latency under load and recovery after a controlled failure.

## Prerequisites

Docker, k6; for the second exercise project 27 plus Helm and a disposable kind cluster.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Establish a baseline

```bash
docker build -t devops-demo:lab 02.examples/app
docker run -d --name load-demo -p 127.0.0.1:8080:8080 devops-demo:lab
mkdir -p .lab
k6 run --summary-export .lab/k6-baseline.json 02.examples/load.js
```

Expect failure rate below 1% and p95 below 500 ms on an otherwise idle local system. Threshold failures return nonzero; record the result rather than weakening thresholds to hide failures.

### 2. Measure a restart

Run k6 again. In a second terminal run `docker restart load-demo`. Compare errors and p95 with baseline; short failures are expected for this single-instance app.

```bash
docker rm -f load-demo
```

### 3. Inject a Kubernetes failure

Complete project 27 and confirm kind-devops-lab is the current context:

```bash
kubectl config current-context
helm repo add chaos-mesh https://charts.chaos-mesh.org
helm repo update
helm upgrade --install chaos-mesh chaos-mesh/chaos-mesh --version 2.8.5 --namespace chaos-mesh --create-namespace --set chaosDaemon.runtime=containerd --set chaosDaemon.socketPath=/run/containerd/containerd.sock --set dashboard.create=false --wait --timeout=5m
kubectl apply -f 02.examples/chaos.yml
kubectl -n devops-lab describe podchaos demo-failure
kubectl -n devops-lab get pods -w
```

The selector confines a 20-second experiment to one demo pod in devops-lab. Stop watching with Ctrl+C. Observe events and readiness before, during and after the experiment.

## Verify completion

Save the baseline and restart results. Confirm the chaos experiment completes and all three demo replicas become ready again.

## Troubleshooting

Chaos Mesh needs privileged cluster components. Run only in the disposable cluster. If installation fails, inspect its pods/events before running the experiment.

## Cleanup

```bash
kubectl delete -f 02.examples/chaos.yml --ignore-not-found
helm uninstall chaos-mesh -n chaos-mesh
kind delete cluster --name devops-lab
```

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://grafana.com/docs/k6/latest/get-started/running-k6/)

---

[← Previous: 29](../29.supply-chain-security/README.md) · [All projects](../../README.md) · [Next: 31 →](../31.backup-and-recovery-drill/README.md)
