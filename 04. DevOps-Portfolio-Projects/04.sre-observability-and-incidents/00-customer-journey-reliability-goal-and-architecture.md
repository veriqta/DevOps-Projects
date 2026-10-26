# 00. Customer Journey Reliability Goal and Architecture

[Project home](README.md) · [01. Start the Application and Establish Normal Behavior →](01-start-the-application-and-establish-normal-behavior.md)

## Starting state and working directory

Read the project README and have a terminal open at the repository root.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `04.sre-observability-and-incidents` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 04.sre-observability-and-incidents
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

The meaningful customer action is an accepted checkout, not an HTTP health response. Define the lab availability SLI as successful checkout requests divided by all checkout attempts. The lab target is at least 99% success and p95 request latency below 500 ms during a stated test window. A short controlled lab run does not establish a monthly production SLO. Metrics locate the symptom, logs describe individual events and traces show a request’s timing context.

## Work through the implementation

This service emits one checkout span per request rather than a complete distributed trace across a payment provider. The payment fault is simulated inside the app. Correlation is still demonstrable because the JSON event records the same trace ID; describe that scope honestly. Alert evaluation is included, but notification delivery through Alertmanager is not part of the core stack.

### Commands in execution order

```bash
find app monitoring -maxdepth 2 -type f | sort
```

## Checkpoint — verify before continuing

Write the SLI numerator, denominator, latency threshold and observation window before generating traffic. Identify which telemetry source answers how many, what happened and how long.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Do not use process uptime as a substitute for checkout success. A healthy process can return 503 for every customer request.

## What to record

Save the architecture and acceptance criteria in your own notes. You will compare the finished system with this contract in chapter 09.

## Continue

When this checkpoint passes, continue to [01. Start the Application and Establish Normal Behavior](01-start-the-application-and-establish-normal-behavior.md). The next chapter assumes the state created here.
