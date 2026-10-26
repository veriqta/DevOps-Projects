# 03. Estimate the Infrastructure Configuration

[← 02. Measure the Baseline Under Repeatable Load](02-measure-the-baseline-under-repeatable-load.md) · [Project home](README.md) · [04. Attribute Resource Consumption →](04-attribute-resource-consumption.md)

## Starting state and working directory

Complete chapter 02 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `08.cloud-cost-and-capacity` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 08.cloud-cost-and-capacity
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

An estimate is a model, not an invoice. Infracost reads the supported AWS resource shape without provisioning a real instance. The template AMI is deliberately invalid and the Terraform precondition blocks apply; neither prevents static estimate generation. Do not substitute a real AMI merely to make the cost fixture deployable.

## Work through the implementation

Before sharing reports, review them for account metadata. A local CPU limit is not an EC2 SKU, and container load does not prove which burstable instance will meet sustained production traffic. Use this chapter to demonstrate disciplined cost modeling and the explicit limits of your conclusion, not to promise an actual bill reduction.

### Commands in execution order

```bash
case "$(uname -m)" in x86_64) ARCH=amd64;; aarch64|arm64) ARCH=arm64;; *) exit 1;; esac
curl -fsSL "https://github.com/infracost/infracost/releases/download/v0.10.43/infracost-linux-${ARCH}.tar.gz" -o .lab/infracost.tar.gz
tar -xzf .lab/infracost.tar.gz -C .lab
sudo install ".lab/infracost-linux-${ARCH}" /usr/local/bin/infracost
infracost auth login
infracost breakdown --path terraform --format json --out-file .lab/base-cost.json
infracost breakdown --path terraform --terraform-var 'instance_type=t3.micro' --format json --out-file .lab/candidate-cost.json
infracost diff --path terraform --terraform-var 'instance_type=t3.micro' --compare-to .lab/base-cost.json
```

## Checkpoint — verify before continuing

Both JSON estimates have a non-null totalMonthlyCost. Record the instance types, region, storage size, timestamp and any resources/usage not priced.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Authentication errors or unsupported resources are not zero-cost outcomes. Preserve the warning and correct the model. The estimate does not include an ALB, NAT, database, egress or support unless those are modeled explicitly.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [04. Attribute Resource Consumption](04-attribute-resource-consumption.md). The next chapter assumes the state created here.
