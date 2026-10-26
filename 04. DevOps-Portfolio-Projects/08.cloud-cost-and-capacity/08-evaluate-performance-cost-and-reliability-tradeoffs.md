# 08. Evaluate Performance Cost and Reliability Tradeoffs

[← 07. Add Budget and Change Review Checks](07-add-budget-and-change-review-checks.md) · [Project home](README.md) · [09. Produce the Optimization Report and Remove Resources →](09-produce-the-optimization-report-and-remove-resources.md)

## Starting state and working directory

Complete chapter 07 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `08.cloud-cost-and-capacity` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 08.cloud-cost-and-capacity
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A final decision must say whether the evidence supports changing capacity, what uncertainty remains and how you would roll back. Include performance, modeled cost, load assumptions, host limits and reliability concerns such as burst credits or memory headroom. Do not equate an accepted local experiment with a production change approval.

## Work through the implementation

Use a report with baseline, candidate, fixed workload, repeated results, cost assumptions, decision and next validation step. Explain whether the estimated cloud-size change has enough CPU/memory/credit evidence to be plausible. Include an explicit rollback plan rather than a one-way optimization script.

### Commands in execution order

```bash
CPU_LIMIT=0.25 MEMORY_LIMIT=128m docker compose up -d --force-recreate app
curl -fsS localhost:8080/health
python3 -m json.tool .lab/comparison.json
```

## Checkpoint — verify before continuing

The baseline capacity is restored and healthy. Your written decision names accept/reject, the measured SLO result, modeled estimate delta and rollback condition.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

A cheaper configuration that breaks the SLO is rejected. A pass under an unrepresentative workload remains insufficient for a production rollout; state that limitation explicitly.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [09. Produce the Optimization Report and Remove Resources](09-produce-the-optimization-report-and-remove-resources.md). The next chapter assumes the state created here.
