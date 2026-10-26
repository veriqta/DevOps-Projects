# 24. Prometheus and Grafana

[← All projects](../README.md) · **Advanced** · Prometheus · Grafana

Scrape the demo service and graph request counts.

## Prerequisites

Docker Compose v2 and a browser.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Files included

Everything below is inside this project’s `files/` folder.

| File or folder | Use |
| --- | --- |
| `alerts.yml` | Configuration or starter code referenced in the steps below. |
| `app` | Demo HTTP service, Dockerfile and service unit. |
| `observability.yml` | Configuration or starter code referenced in the steps below. |
| `prometheus.yml` | Configuration or starter code referenced in the steps below. |

## Walkthrough

From the repository root, enter this project:

```bash
cd 24.prometheus-and-grafana
```

Run the remaining commands here unless a step explicitly changes directories. The `files/` folder contains the supplied code and configurations for this project.

### 1. Start the stack

```bash
docker compose -f files/observability.yml up -d --build
curl -fsS localhost:8080/health
curl -fsS localhost:8080/metrics
```

Open `http://localhost:9090/targets`; wait for the demo target to show UP.

### 2. Build the dashboard

Open `http://localhost:3000`. Sign in with the lab default admin/admin and change the password. Connections → Data sources → Add → Prometheus → URL `http://prometheus:9090` → Save & test. Create a dashboard, add a visualization with query `demo_requests_total`, then another with `rate(demo_requests_total[1m])`.

Generate requests:

```bash
for i in $(seq 1 20); do curl -fsS localhost:8080/health > /dev/null; sleep 1; done
```

### 3. Trigger an alert

```bash
docker compose -f files/observability.yml stop app
```

Open `http://localhost:9090/alerts`. After the next scrape and 15-second pending period, DemoUnavailable should fire. This lab evaluates an alert but does not send notifications; an Alertmanager receiver is a separate integration.

```bash
docker compose -f files/observability.yml start app
```

## Verify completion

The target is UP, the request counter increases, the alert fires during downtime and resolves after restart. Save/export your Grafana dashboard before cleanup.

## Troubleshooting

The Grafana data-source address uses the Compose service name, not localhost. A counter rate needs multiple scrapes before it has useful data.

## Cleanup

`docker compose -f files/observability.yml down -v`

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented prometheus and grafana in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://prometheus.io/docs/introduction/first_steps/)

---

[← Previous: 23](../23.blue-green-deployment/README.md) · [All projects](../README.md) · [Next: 25 →](../25.multi-service-application/README.md)
