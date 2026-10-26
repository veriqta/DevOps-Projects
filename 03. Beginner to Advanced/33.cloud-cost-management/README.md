# 33. Cloud Cost Management

[← All projects](../README.md) · **Advanced** · Infracost · OpenCost

Estimate infrastructure changes and attribute local cluster costs.

## Prerequisites

Infracost account/API key, Terraform; for allocation analysis Docker, kind, kubectl and Helm. The Terraform sample is estimate-only and must not be applied.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Files included

Everything below is inside this project’s `files/` folder.

| File or folder | Use |
| --- | --- |
| `opencost-values.yml` | Configuration or starter code referenced in the steps below. |
| `prometheus-values.yml` | Configuration or starter code referenced in the steps below. |
| `terraform-cost` | Configuration used by this project. |

## Walkthrough

From the repository root, enter this project:

```bash
cd 33.cloud-cost-management
```

Run the remaining commands here unless a step explicitly changes directories. The `files/` folder contains the supplied code and configurations for this project.

### 1. Estimate without provisioning

```bash
infracost auth login
mkdir -p .lab/cost
infracost breakdown --path files/terraform-cost --format json --out-file .lab/cost/base.json
infracost diff --path files/terraform-cost --terraform-var 'instance_type=t3.small' --compare-to .lab/cost/base.json
```

Record the monthly estimate and the delta. The sample AMI is deliberately invalid because pricing does not require creating a VM. Never run terraform apply in this sample folder. Estimates exclude many usage-dependent costs unless you supply usage data.

### 2. Install metrics and OpenCost in a disposable cluster

```bash
kind create cluster --name costs-lab
kubectl config current-context
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add opencost-charts https://opencost.github.io/opencost-helm-chart
helm repo update
helm upgrade --install metrics prometheus-community/prometheus --version 29.38.2 -n monitoring --create-namespace -f files/prometheus-values.yml --wait --timeout=5m
helm upgrade --install opencost opencost-charts/opencost --version 2.5.33 -n opencost --create-namespace -f files/opencost-values.yml --wait --timeout=5m
kubectl -n opencost port-forward service/opencost 9003:9003 9090:9090
```

Leave the forward open. In a second terminal:

```bash
curl -fsS 'http://localhost:9003/allocation/compute?window=30m&aggregate=namespace'
```

Open `http://localhost:9090`. Let metrics accumulate, then compare namespaces. A local kind cluster uses modeled allocation/pricing, not an actual cloud bill. Save the installed chart versions using helm list -A.

## Verify completion

The larger instance estimate costs more; OpenCost returns namespace allocations after metrics collection. State estimate assumptions and distinguish allocation from invoiced cost.

## Troubleshooting

Empty allocations often mean insufficient scrape history or a wrong Prometheus service URL. Confirm metrics-server exists in monitoring and inspect OpenCost logs.

## Cleanup

Stop port-forward, run `kind delete cluster --name costs-lab`, and remove `.lab/cost`. No AWS resources are created by the estimate step.

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented cloud cost management in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://www.infracost.io/docs/)

---

[← Previous: 32](../32.cloud-secrets-integration/README.md) · [All projects](../README.md) · [Next: 34 →](../34.production-readiness-capstone/README.md)
