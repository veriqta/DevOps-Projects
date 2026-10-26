# 34. Production Readiness Capstone

[← All projects](../README.md) · **Advanced** · SRE · CI/CD · Kubernetes

Combine delivery, observability, security and recovery into one demonstrable system.

## Prerequisites

Complete projects 23, 24, 27, 29, 30 and 31. Docker, Python, Node, kind, kubectl, k6 and the security tools.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

From the repository root, enter this project:

```bash
cd 34.production-readiness-capstone
```

Run the remaining commands here unless a step explicitly changes directories. This project uses the commands below; no starter files are required.

### 1. Establish your baseline

Complete the verification section in each prerequisite project before starting. Each lab keeps its own files and commands together.

```bash
mkdir -p .lab/capstone
```

Create `.lab/capstone/report.md` using this structure:

```markdown
# Readiness evidence
## Architecture and tool versions
## Release commit and immutable image digest
## SLO and load-test result
## Alert trigger and recovery timestamps
## Failed release and rollback
## SBOM, scan decisions and signature verification
## Backup age and measured restore time
## Cost assumptions
## Cleanup evidence
## Follow-up improvements
```

### 2. Run the release drill

Follow project 23 to move blue → green → blue and capture every health result. Use project 16’s digest-published image if you have a registry; record the exact digest rather than a mutable tag.

### 3. Run the operations drill

Complete project 24’s target-down alert and recovery. Run project 30’s baseline and failure load tests. Write a measurable lab SLO such as 99% successful requests over the 30-second test; report the observed result, including any deliberate failure.

### 4. Run security and recovery checks

Complete project 29’s SBOM tamper test and project 31’s actual restore. Attach the public verification outputs and measured RTO/RPO. The presence of configuration files alone does not count as passing these checks.

### 5. Rehearse an incident

Start a 30-minute timer, stop one lab service, note detection time, identify the failure using metrics/logs, recover and verify. Write a short timeline: trigger → detected → diagnosed → restored → verified. Add one concrete improvement with an owner and target date.

### 6. Publish your evidence

Copy sanitized evidence into a new branch of your own portfolio repository. Include the architecture, reproducible commands and observed limits. Review for secrets before pushing.

## Verify completion

Every report section includes actual output or a linked artifact, all temporary resources are cleaned up, and another person can reproduce your chosen deployment path from the report.

## Troubleshooting

If a prerequisite failed, resolve it before marking the capstone complete. Separate observations from assumptions and label any unexecuted provider-specific extension.

## Cleanup

Follow cleanup in each prerequisite lab. Run docker compose ls and kind get clusters, inspect cloud consoles and billing, and remove only resources created for these labs.

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented production readiness capstone in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://sre.google/workbook/table-of-contents/)

---

[← Previous: 33](../33.cloud-cost-management/README.md) · [All projects](../README.md)
