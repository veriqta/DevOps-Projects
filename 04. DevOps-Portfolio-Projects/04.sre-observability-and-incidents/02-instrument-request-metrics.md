# 02. Instrument Request Metrics

[← 01. Start the Application and Establish Normal Behavior](01-start-the-application-and-establish-normal-behavior.md) · [Project home](README.md) · [03. Add Structured Logs and Trace Context →](03-add-structured-logs-and-trace-context.md)

## Starting state and working directory

Complete chapter 01 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `04.sre-observability-and-incidents` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 04.sre-observability-and-incidents
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Counters represent accumulated events while histograms represent an observation distribution. orders_requests_total is labeled by HTTP status; summing rates over status codes gives throughput and filtering 5xx gives failed customer attempts. The histogram buckets must be interpreted as cumulative counts. Percentile estimates from buckets are approximate, and they need enough observations to become useful.

## Work through the implementation

Only checkout attempts contribute to the customer metrics. Health and scrape requests are excluded so operational polling does not inflate the success ratio. The app is a demonstration metric implementation, not a replacement for a mature client library under high traffic. The test workload is intentionally bounded.

### Commands in execution order

```bash
for i in $(seq 1 20);do curl -fsS -H 'Content-Type: application/json' -d '{"item":"metric-check"}' localhost:8080/checkout > /dev/null;done
curl -fsS localhost:8080/metrics
```

### Read the implementation: `monitoring/prometheus.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
global:
  scrape_interval: 5s
rule_files: [/etc/prometheus/alerts.yaml]
scrape_configs:
  - job_name: orders
    static_configs: [{targets: ["app:8080"]}]
```

## Checkpoint — verify before continuing

The 201 counter increases by twenty and the histogram count increases accordingly. In Prometheus at localhost:9090/targets, orders becomes UP. Query sum(rate(orders_requests_total[1m])) after at least two scrapes.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

An empty rate with a new process often means insufficient samples. A counter resetting after container restart is normal; rate handles resets, while subtracting raw counter values manually may not.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [03. Add Structured Logs and Trace Context](03-add-structured-logs-and-trace-context.md). The next chapter assumes the state created here.
