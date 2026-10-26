# 04. Attribute Resource Consumption

[← 03. Estimate the Infrastructure Configuration](03-estimate-the-infrastructure-configuration.md) · [Project home](README.md) · [05. Change Capacity and Resource Requests →](05-change-capacity-and-resource-requests.md)

## Starting state and working directory

Complete chapter 03 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `08.cloud-cost-and-capacity` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 08.cloud-cost-and-capacity
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Attribute the observed resource use to the actual service and test interval. A process can be latency-bound on an external dependency while consuming little CPU, so low CPU alone does not prove overprovisioning. Memory and burst credits also matter in real instance sizing. Here Docker stats and the app’s metrics provide local workload context without pretending to be a cloud billing allocation system.

## Work through the implementation

In your report separate configured requests/limits, observed utilization and modeled cloud costs into three columns. For a real cluster, namespace allocation tools would add shared-resource accounting; that is an optional extension. This core exercise makes only the attribution it can actually measure.

### Commands in execution order

```bash
docker compose ps
docker stats --no-stream
curl -fsS localhost:8080/metrics > .lab/app-metrics.txt
cat .lab/baseline-resources.txt
```

## Checkpoint — verify before continuing

Record CPU and memory for the app, the request count and the observation time. State whether the sample was collected during or after load.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

A one-time snapshot can miss peaks. Repeat with a live sample during the next run. Do not assign shared Docker-host overhead to zero merely because it is outside the app container.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [05. Change Capacity and Resource Requests](05-change-capacity-and-resource-requests.md). The next chapter assumes the state created here.
