# 06. Provision the Application Compute Layer

[← 05. Configure Access and Security Boundaries](05-configure-access-and-security-boundaries.md) · [Project home](README.md) · [07. Separate Environments and Review Changes →](07-separate-environments-and-review-changes.md)

## Starting state and working directory

Complete chapter 05 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `02.secure-cloud-infrastructure` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 02.secure-cloud-infrastructure
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Apply the reviewed plan, then verify the service from outside and inspect target health inside AWS. Auto Scaling and the launch template provide replacement, while cloud-init installs Nginx on each new machine. A created instance is not the same as a ready target: the package installation, web server and ALB health checks must all succeed.

### Commands in execution order

```bash
terraform -chdir=terraform apply dev.plan
terraform -chdir=terraform output
bash scripts/check.sh
TG=$(terraform -chdir=terraform output -raw target_group_arn)
aws elbv2 describe-target-health --target-group-arn "$TG" --output table
```

### Read the implementation: `scripts/check.sh`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../terraform"
url=$(terraform output -raw url)
for attempt in $(seq 1 60);do
 if curl -fsS --connect-timeout 5 "$url" | grep -q 'Orders foundation';then echo 'Application verified through ALB';exit 0;fi
 sleep 10
done
exit 1
```

## Checkpoint — verify before continuing

The page contains Orders foundation and dev. Both ALB targets become healthy. In EC2 verify their public IPv4 field is empty and their subnets are the private pair.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If targets stay unhealthy, inspect their cloud-init logs through SSM Session Manager, check NAT routes and package downloads, then check port-80 group references. A client timeout with healthy targets can mean your public IP changed.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [07. Separate Environments and Review Changes](07-separate-environments-and-review-changes.md). The next chapter assumes the state created here.
