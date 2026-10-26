# 04. Connect Metrics Logs and Traces to the Backends

[← 03. Add Structured Logs and Trace Context](03-add-structured-logs-and-trace-context.md) · [Project home](README.md) · [05. Build and Explain the Dashboard →](05-build-and-explain-the-dashboard.md)

## Starting state and working directory

Complete chapter 03 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `04.sre-observability-and-incidents` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 04.sre-observability-and-incidents
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

The collector receives spans over OTLP HTTP and tails the shared JSON log file. Its traces pipeline sends to Tempo; its logs pipeline adds service.name and exports to Loki’s OTLP endpoint. A receiver defined in configuration does nothing unless a service pipeline references it. Loki’s structured metadata and TSDB schema support the OTLP log attributes used here.

## Work through the implementation

Select the Loki event and inspect its structured attributes, including trace_id. Copy that ID to Tempo rather than assuming a preconfigured clickable link exists. This manual correlation is the core demonstration. A production system also needs sampling, retention, ingestion limits, backend authentication and durable storage; the ephemeral local stack intentionally keeps those concerns out of the first incident drill.

### Commands in execution order

```bash
docker compose logs --tail=50 collector
docker compose logs --tail=30 loki tempo
curl -fsS -H 'Content-Type: application/json' -d '{"item":"correlation"}' localhost:8080/checkout
```

### Read the implementation: `monitoring/collector.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
receivers:
  otlp:
    protocols:
      http: {endpoint: "0.0.0.0:4318"}
  filelog:
    include: [/logs/orders.json]
    start_at: beginning
    operators:
      - type: json_parser
        parse_to: attributes
processors:
  resource:
    attributes:
      - {key: service.name, value: orders, action: upsert}
  batch: {}
exporters:
  otlphttp/tempo:
    endpoint: http://tempo:4318
  otlphttp/loki:
    endpoint: http://loki:3100/otlp
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlphttp/tempo]
    logs:
      receivers: [filelog]
      processors: [resource, batch]
      exporters: [otlphttp/loki]
```

### Read the implementation: `monitoring/loki.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
auth_enabled: false
server:
  http_listen_port: 3100
common:
  path_prefix: /tmp/loki
  replication_factor: 1
  ring:
    kvstore: {store: inmemory}
  storage:
    filesystem:
      chunks_directory: /tmp/loki/chunks
      rules_directory: /tmp/loki/rules
schema_config:
  configs:
    - from: 2024-04-01
      store: tsdb
      object_store: filesystem
      schema: v13
      index: {prefix: index_, period: 24h}
limits_config:
  allow_structured_metadata: true
```

### Read the implementation: `monitoring/tempo.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
server:
  http_listen_port: 3200
distributor:
  receivers:
    otlp:
      protocols:
        http: {endpoint: "0.0.0.0:4318"}
storage:
  trace:
    backend: local
    local: {path: /tmp/tempo/blocks}
    wal: {path: /tmp/tempo/wal}
```

## Checkpoint — verify before continuing

In Grafana Explore select Loki and query {service_name="orders"}. Select Tempo and search recent traces for service orders, or paste the captured trace ID. The span and JSON event must describe the same request.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If logs are absent, inspect /logs/orders.json in the app and collector mount before changing Loki. If traces are absent, inspect OTLP export errors and whether Tempo listens on 0.0.0.0:4318 inside the container.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [05. Build and Explain the Dashboard](05-build-and-explain-the-dashboard.md). The next chapter assumes the state created here.
