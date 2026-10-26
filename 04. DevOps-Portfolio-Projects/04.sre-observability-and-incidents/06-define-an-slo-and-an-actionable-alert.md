# 06. Define an SLO and an Actionable Alert

[← 05. Build and Explain the Dashboard](05-build-and-explain-the-dashboard.md) · [Project home](README.md) · [07. Generate Load and Introduce a Controlled Failure →](07-generate-load-and-introduce-a-controlled-failure.md)

## Starting state and working directory

Complete chapter 05 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `04.sre-observability-and-incidents` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 04.sre-observability-and-incidents
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

An alert must identify an actionable condition and the time window in which it is evaluated. The error-ratio rule fires above 1% for 30 seconds using one-minute rates; this is a short lab demonstration, not a full multi-window burn-rate implementation for a monthly budget. The target-down rule detects scrape loss separately, because a ratio cannot describe requests that never reach an unavailable process.

## Work through the implementation

Write a response note beside the alert in your portfolio: first inspect the checkout failure ratio, then recent error logs and trace durations, then check the payment-fault control and deployment history. An alert that only says “something is wrong” without a diagnostic path adds noise. Notification routing is an optional next integration; do not claim an email/page was sent merely because Prometheus shows firing.

### Commands in execution order

```bash
docker compose exec -T prometheus promtool check config /etc/prometheus/prometheus.yml
docker compose exec -T prometheus promtool check rules /etc/prometheus/alerts.yaml
```

### Read the implementation: `monitoring/alerts.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
groups:
  - name: orders
    rules:
      - alert: CheckoutErrorBudgetBurn
        expr: sum(rate(orders_requests_total{status=~"5.."}[1m])) / clamp_min(sum(rate(orders_requests_total[1m])), 0.001) > 0.01
        for: 30s
        annotations:
          summary: More than one percent of checkout attempts fail
      - alert: OrdersTargetDown
        expr: up{job="orders"} == 0
        for: 15s
```

## Checkpoint — verify before continuing

Both promtool checks pass. Open localhost:9090/alerts and find CheckoutErrorBudgetBurn and OrdersTargetDown. They should be inactive during healthy traffic.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

An inactive alert with no traffic is expected. To test an error ratio, keep sending checkout attempts through the fault window; a single failed request may be diluted by previous successes.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [07. Generate Load and Introduce a Controlled Failure](07-generate-load-and-introduce-a-controlled-failure.md). The next chapter assumes the state created here.
