# 09. Produce the Optimization Report and Remove Resources

[← 08. Evaluate Performance Cost and Reliability Tradeoffs](08-evaluate-performance-cost-and-reliability-tradeoffs.md) · [Project home](README.md)

## Starting state and working directory

Complete chapter 08 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `08.cloud-cost-and-capacity` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 08.cloud-cost-and-capacity
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

The portfolio should show disciplined engineering judgment rather than a guaranteed savings percentage. Link the raw k6 summaries, comparison decision, dated cost estimates and resource observations. Explain any rejected candidate and what workload or billing evidence would be needed next. Clean up local containers and credentials without ever applying the estimate fixture.

## Work through the implementation

A résumé bullet can describe a repeatable cost/performance experiment with SLO and budget gates, adding actual measured/estimated values only when supported by the reports. Be prepared to explain utilization versus allocation versus billing, why load equivalence matters, how a failed candidate changes the decision, and why a static estimate is not a cloud invoice.

### Commands in execution order

```bash
docker compose down
rm -rf .lab
docker compose ps
```

## Checkpoint — verify before continuing

No local app container remains. No AWS resource was created by the Terraform estimate folder. Revoke an unnecessary Infracost API key through its account settings; deleting files alone does not revoke service access.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If you accidentally applied another infrastructure configuration, clean it up through its own tracked state. The intentionally blocked estimate folder is not a cleanup mechanism for unrelated cloud resources.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

The project is complete only after the acceptance checks pass and the lab resources are removed. Publish your sanitized implementation and evidence in your own portfolio repository.
