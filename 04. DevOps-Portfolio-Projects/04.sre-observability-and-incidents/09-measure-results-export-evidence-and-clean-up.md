# 09. Measure Results Export Evidence and Clean Up

[← 08. Investigate Recover and Write the Incident Timeline](08-investigate-recover-and-write-the-incident-timeline.md) · [Project home](README.md)

## Starting state and working directory

Complete chapter 08 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `04.sre-observability-and-incidents` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 04.sre-observability-and-incidents
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A useful SRE portfolio distinguishes an experiment from sustained operational history. Report the test duration, traffic rate, injected-failure period and measured detection/recovery times. Preserve the dashboard and incident narrative before deleting ephemeral backends. Explain why the lab SLO window and single-service trace are narrower than a real production service.

## Work through the implementation

A résumé bullet after completion can say “Instrumented a checkout service with metrics, logs and traces; built SLO-focused dashboards and rehearsed detection/recovery with [observed timings].” Prepare to explain sampling, cardinality, alert windows, why health differs from success, and how backend retention/authentication would change in a production adaptation.

### Commands in execution order

```bash
docker compose down -v
docker compose ps
rm -rf .lab
```

## Checkpoint — verify before continuing

All stack containers stop and the project log volume is removed. Any exported evidence contains dummy payloads only. No Prometheus/Tempo/Loki endpoint remains published.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Do not delete evidence before exporting it. Grafana changes not encoded in provisioning files can be lost when the container disappears.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

The project is complete only after the acceptance checks pass and the lab resources are removed. Publish your sanitized implementation and evidence in your own portfolio repository.
