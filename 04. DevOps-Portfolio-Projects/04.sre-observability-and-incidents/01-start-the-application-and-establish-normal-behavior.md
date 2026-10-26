# 01. Start the Application and Establish Normal Behavior

[← 00. Customer Journey Reliability Goal and Architecture](00-customer-journey-reliability-goal-and-architecture.md) · [Project home](README.md) · [02. Instrument Request Metrics →](02-instrument-request-metrics.md)

## Starting state and working directory

Complete chapter 00 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `04.sre-observability-and-incidents` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 04.sre-observability-and-incidents
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Start with a known healthy request before investigating telemetry. The Compose stack wires services through internal DNS names; Grafana’s datasource URL must refer to prometheus, loki or tempo rather than its own localhost. Port publishing is separate and restricted to the workstation loopback. First startup downloads images and may take time before all backends are ready.

## Work through the implementation

Install Docker only if it is not already functional. After the group change reconnect before running Docker as the current user. Do not send real customer payloads through this stack. The root user override exists to write a shared local log volume; a hardened deployment would initialize ownership and run the app under its image’s UID.

### Commands in execution order

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl git jq unzip python3 python3-venv openssl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
. /etc/os-release
printf 'deb [arch=%s signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu %s stable\n' "$(dpkg --print-architecture)" "$VERSION_CODENAME" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker "$USER"

```

Log out of the Ubuntu session and reconnect before continuing so Docker group membership is active. Verify `docker version` shows the server. Then run:

```bash
mkdir -p .lab
docker compose config
docker compose up -d --build
curl -fsS localhost:8080/health
curl -fsS -H 'Content-Type: application/json' -d '{"item":"baseline"}' localhost:8080/checkout
```

### Read the implementation: `compose.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
name: portfolio-sre
services:
  app:
    build: ./app
    environment:
      OTEL_EXPORTER_OTLP_ENDPOINT: http://collector:4318
      OTEL_EXPORTER_OTLP_PROTOCOL: http/protobuf
      LOG_FILE: /logs/orders.json
    ports: ["127.0.0.1:8080:8080"]
    volumes: ["logs:/logs"]
    user: "0:0" # Local log-volume convenience; harden ownership before a production adaptation.
  collector:
    image: otel/opentelemetry-collector-contrib:0.131.0
    command: ["--config=/etc/otelcol/config.yaml"]
    volumes:
      - ./monitoring/collector.yaml:/etc/otelcol/config.yaml:ro
      - logs:/logs:ro
  prometheus:
    image: prom/prometheus:v3.5.0
    ports: ["127.0.0.1:9090:9090"]
    volumes:
      - ./monitoring/prometheus.yaml:/etc/prometheus/prometheus.yml:ro
      - ./monitoring/alerts.yaml:/etc/prometheus/alerts.yaml:ro
  loki:
    image: grafana/loki:3.5.3
    command: ["-config.file=/etc/loki/config.yaml"]
    volumes: ["./monitoring/loki.yaml:/etc/loki/config.yaml:ro"]
  tempo:
    image: grafana/tempo:2.8.2
    command: ["-config.file=/etc/tempo.yaml"]
    volumes: ["./monitoring/tempo.yaml:/etc/tempo.yaml:ro"]
  grafana:
    image: grafana/grafana:12.1.0
    ports: ["127.0.0.1:3000:3000"]
    volumes:
      - ./monitoring/datasources.yaml:/etc/grafana/provisioning/datasources/sources.yaml:ro
      - ./monitoring/dashboards.yaml:/etc/grafana/provisioning/dashboards/default.yaml:ro
      - ./monitoring/orders-dashboard.json:/var/lib/grafana/dashboards/orders.json:ro
volumes:
  logs: {}
```

## Checkpoint — verify before continuing

Health is ok, checkout returns 201, and docker compose ps shows the stack running. Open localhost:3000, sign in with the lab default admin/admin and change the password.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

A startup connection refusal is not necessarily a configuration error. Inspect docker compose logs --tail=50 and distinguish an image pull, process crash and backend initialization.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [02. Instrument Request Metrics](02-instrument-request-metrics.md). The next chapter assumes the state created here.
