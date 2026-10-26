# 05. Build and Explain the Dashboard

[← 04. Connect Metrics Logs and Traces to the Backends](04-connect-metrics-logs-and-traces-to-the-backends.md) · [Project home](README.md) · [06. Define an SLO and an Actionable Alert →](06-define-an-slo-and-an-actionable-alert.md)

## Starting state and working directory

Complete chapter 04 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `04.sre-observability-and-incidents` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 04.sre-observability-and-incidents
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

The supplied dashboard is provisioned so another learner sees the same queries instead of manually recreating an undocumented UI. Each panel has a different operational interpretation: throughput is workload, error ratio is customer failure, and p95 is the slower tail of latency. A request-rate decline can mean less traffic or inability to reach the service; interpret it together with availability and logs.

### Commands in execution order

```bash
curl -fsS localhost:9090/api/v1/targets > .lab/targets.json
python3 -m json.tool .lab/targets.json
```

### Read the implementation: `monitoring/datasources.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
apiVersion: 1
datasources:
  - {name: Prometheus, uid: prometheus, type: prometheus, access: proxy, url: "http://prometheus:9090", isDefault: true}
  - {name: Loki, uid: loki, type: loki, access: proxy, url: "http://loki:3100"}
  - {name: Tempo, uid: tempo, type: tempo, access: proxy, url: "http://tempo:3200"}
```

### Read the implementation: `monitoring/orders-dashboard.json`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```json
{
  "uid": "orders",
  "title": "Orders customer journey",
  "schemaVersion": 39,
  "version": 1,
  "panels": [
    {
      "id": 1,
      "title": "Checkout requests / second",
      "type": "timeseries",
      "datasource": {
        "type": "prometheus",
        "uid": "prometheus"
      },
      "gridPos": {
        "x": 0,
        "y": 0,
        "w": 24,
        "h": 8
      },
      "targets": [
        {
          "expr": "sum(rate(orders_requests_total[1m]))",
          "refId": "A"
        }
      ]
    },
    {
      "id": 2,
      "title": "Checkout failure ratio",
      "type": "timeseries",
      "datasource": {
        "type": "prometheus",
        "uid": "prometheus"
      },
      "gridPos": {
        "x": 0,
        "y": 8,
        "w": 24,
        "h": 8
      },
      "targets": [
        {
          "expr": "sum(rate(orders_requests_total{status=~\"5..\"}[1m])) / clamp_min(sum(rate(orders_requests_total[1m])),0.001)",
          "refId": "A"
        }
      ]
    },
    {
      "id": 3,
      "title": "Checkout p95 latency",
      "type": "timeseries",
      "datasource": {
        "type": "prometheus",
        "uid": "prometheus"
      },
      "gridPos": {
        "x": 0,
        "y": 16,
        "w": 24,
        "h": 8
      },
      "targets": [
        {
          "expr": "histogram_quantile(0.95,sum by(le)(rate(orders_duration_seconds_bucket[1m])))",
          "refId": "A"
        }
      ]
    }
  ],
  "time": {
    "from": "now-15m",
    "to": "now"
  },
  "refresh": "5s"
}
```

### Read the implementation: `monitoring/dashboards.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
apiVersion: 1
providers:
  - name: orders
    options: {path: /var/lib/grafana/dashboards}
```

## Checkpoint — verify before continuing

Open Dashboards → Orders customer journey in Grafana. Generate traffic, verify all three panels populate and inspect their PromQL. Export the dashboard through its UI into your own evidence if you customize it.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

No data can come from a wrong time range or insufficient scrapes. Check Prometheus directly before changing Grafana. A NaN ratio at zero traffic should not be reported as perfect availability.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [06. Define an SLO and an Actionable Alert](06-define-an-slo-and-an-actionable-alert.md). The next chapter assumes the state created here.
