# 05. Change Capacity and Resource Requests

[← 04. Attribute Resource Consumption](04-attribute-resource-consumption.md) · [Project home](README.md) · [06. Re-run the Same Workload and Cost Comparison →](06-re-run-the-same-workload-and-cost-comparison.md)

## Starting state and working directory

Complete chapter 04 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `08.cloud-cost-and-capacity` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 08.cloud-cost-and-capacity
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Change one resource constraint at a time and keep the application image, artificial delay, traffic and host environment constant. A candidate may pass at low load and fail at peak load, so repeat a range of request rates before making a production sizing claim. This lab provides a first bounded experiment rather than a full seasonal capacity model.

## Work through the implementation

The candidate keeps memory unchanged, so this run isolates CPU quota. A second separately documented experiment can vary memory. If the workload remains delay-bound, explain why CPU downsizing had little observed effect and why more representative CPU-heavy traffic is needed before a real infrastructure recommendation.

### Commands in execution order

```bash
CPU_LIMIT=0.10 MEMORY_LIMIT=128m docker compose up -d --force-recreate app
curl -fsS localhost:8080/health
docker run --rm --user "$(id -u):$(id -g)" --network host -v "$PWD:/work" -w /work grafana/k6:1.2.3 run --summary-export .lab/candidate.json load-test.js
docker stats --no-stream > .lab/candidate-resources.txt
```

## Checkpoint — verify before continuing

The candidate summary was collected using the same load-test.js and duration as baseline. Record whether thresholds passed; either a pass or an explained rejection is valid experiment evidence.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Do not lower VUS or increase latency thresholds to hide a candidate failure. Check Compose’s rendered CPU limit and confirm the container was recreated with the changed environment inputs.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [06. Re-run the Same Workload and Cost Comparison](06-re-run-the-same-workload-and-cost-comparison.md). The next chapter assumes the state created here.
