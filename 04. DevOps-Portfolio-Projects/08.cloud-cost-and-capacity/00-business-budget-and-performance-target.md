# 00. Business Budget and Performance Target

[Project home](README.md) · [01. Prepare the Workload and Cost Assumptions →](01-prepare-the-workload-and-cost-assumptions.md)

## Starting state and working directory

Read the project README and have a terminal open at the repository root.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `08.cloud-cost-and-capacity` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 08.cloud-cost-and-capacity
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Optimization is a constrained decision: lower estimated cost is useful only when the service still meets the measured contract. Fix the workload and thresholds before changing resources. The lab uses 99% successful checkouts and p95 below 500 ms over a 60-second run. These short measurements are not a production capacity forecast and do not include every real customer dependency.

## Work through the implementation

The app simulates a small amount of service work and delay; it does not contain a real payment provider. Your conclusion can legitimately be “do not downsize” if the candidate violates the SLO. A portfolio that rejects an unsafe saving is stronger than one that fabricates a favorable percentage.

### Commands in execution order

```bash
find app terraform scripts -maxdepth 2 -type f | sort
```

## Checkpoint — verify before continuing

Write down the workload duration, virtual users, success/latency thresholds, estimate region and budget. Separate measured container behavior from modeled cloud pricing in your report.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If you change both traffic and capacity between runs, you cannot attribute the outcome to capacity alone. Reset the experiment and vary one parameter at a time.

## What to record

Save the architecture and acceptance criteria in your own notes. You will compare the finished system with this contract in chapter 09.

## Continue

When this checkpoint passes, continue to [01. Prepare the Workload and Cost Assumptions](01-prepare-the-workload-and-cost-assumptions.md). The next chapter assumes the state created here.
