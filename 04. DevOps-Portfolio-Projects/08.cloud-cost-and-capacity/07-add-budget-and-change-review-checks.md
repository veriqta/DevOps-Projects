# 07. Add Budget and Change Review Checks

[← 06. Re-run the Same Workload and Cost Comparison](06-re-run-the-same-workload-and-cost-comparison.md) · [Project home](README.md) · [08. Evaluate Performance Cost and Reliability Tradeoffs →](08-evaluate-performance-cost-and-reliability-tradeoffs.md)

## Starting state and working directory

Complete chapter 06 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `08.cloud-cost-and-capacity` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 08.cloud-cost-and-capacity
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Budget review must fail closed on a missing estimate and must be combined with performance evidence. The sample checker reads the monthly estimate and compares it to an explicit budget. It does not stop provider spend, create an AWS budget or guarantee a future bill. A review record should include the candidate commit, estimate, performance report and approver’s reasoning.

## Work through the implementation

Store the two commands and their exit codes with the change proposal. To integrate them into your own CI, run them after generating fresh reports and require the status in branch protection. This guide does not include a fake precomputed price file that would pass forever while real prices or infrastructure change.

### Commands in execution order

```bash
python3 scripts/budget.py .lab/candidate-cost.json 30
python3 scripts/budget.py .lab/candidate-cost.json 0.01
# Expect the second check to fail for a nonzero estimate.
python3 scripts/compare.py .lab/baseline.json .lab/candidate.json
```

### Read the implementation: `scripts/budget.py`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```python
import json,sys
from pathlib import Path
report=json.loads(Path(sys.argv[1]).read_text());cost=report.get('totalMonthlyCost')
if cost is None:raise SystemExit('No estimate available: refusing to treat missing cost as zero')
limit=float(sys.argv[2]);actual=float(cost)
print(json.dumps({'estimated_monthly_usd':actual,'budget_usd':limit,'within_budget':actual<=limit}))
raise SystemExit(0 if actual<=limit else 1)
```

## Checkpoint — verify before continuing

The realistic budget check produces a visible decision; the deliberately tiny budget fails. A missing totalMonthlyCost also fails. Approve the candidate only if both budget and performance checks pass.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If the price exceeds 30 USD, the first check should fail too. Adjust a business budget only after reviewing requirements; do not increase it merely to make a demonstration pass.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [08. Evaluate Performance Cost and Reliability Tradeoffs](08-evaluate-performance-cost-and-reliability-tradeoffs.md). The next chapter assumes the state created here.
