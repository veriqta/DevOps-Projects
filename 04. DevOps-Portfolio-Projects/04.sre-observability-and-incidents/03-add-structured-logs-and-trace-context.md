# 03. Add Structured Logs and Trace Context

[← 02. Instrument Request Metrics](02-instrument-request-metrics.md) · [Project home](README.md) · [04. Connect Metrics Logs and Traces to the Backends →](04-connect-metrics-logs-and-traces-to-the-backends.md)

## Starting state and working directory

Complete chapter 02 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `04.sre-observability-and-incidents` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 04.sre-observability-and-incidents
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A log line should be machine-readable and carry enough context to investigate a request without including payment or identity data. The app records service, route, status, duration, time and trace ID. OpenTelemetry creates the checkout span and exports it asynchronously to the collector. A trace identifier is useful for joining observations; it is not a user authentication token.

## Work through the implementation

The Python SDK is loaded only when the export endpoint is configured, so the same service can run dependency-free in earlier projects. This lab creates a span inside the request handler. Full inbound/outbound propagation across multiple services would require explicit context extraction and client instrumentation; that is an extension, not something this single-service trace proves.

### Commands in execution order

```bash
curl -fsS -H 'Content-Type: application/json' -d '{"item":"trace-check"}' localhost:8080/checkout
docker compose logs --tail=10 app
docker compose exec -T app tail -n 3 /logs/orders.json
```

### Read the implementation: `app/requirements.txt`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```text
opentelemetry-sdk==1.36.0
opentelemetry-exporter-otlp-proto-http==1.36.0
```

### Read the implementation: `app/Dockerfile`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```text
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd -u 10001 orders
COPY server.py .
USER orders
CMD ["python", "server.py"]
```

## Checkpoint — verify before continuing

The event is valid JSON and has a nonempty 32-character trace_id when telemetry is configured. Preserve one trace ID for the next chapter. No customer secret or authorization header is present.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

An empty trace ID means the app started without OTEL_EXPORTER_OTLP_ENDPOINT or the SDK was not installed. Export failures in app logs need collector connectivity and endpoint inspection, not retries of the business request alone.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [04. Connect Metrics Logs and Traces to the Backends](04-connect-metrics-logs-and-traces-to-the-backends.md). The next chapter assumes the state created here.
