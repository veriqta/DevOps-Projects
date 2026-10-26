# 01. Prepare AWS Access Budget and Tooling

[← 00. Business Requirements and Network Design](00-business-requirements-and-network-design.md) · [Project home](README.md) · [02. Inspect the Resources Before Automating →](02-inspect-the-resources-before-automating.md)

## Starting state and working directory

Complete chapter 00 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `02.secure-cloud-infrastructure` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 02.secure-cloud-infrastructure
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A plan is meaningful only when you know which account and region it targets. Temporary SSO credentials avoid saving long-lived access keys in project files. Provider access and backend access are separate operations; both use your AWS identity, but the backend must also write and delete its lock object. Native S3 locking in this lab requires the supplied Terraform 1.13 baseline.

## Work through the implementation

For a standalone account without IAM Identity Center, the AWS console’s CloudShell can supply temporary credentials and Terraform can be installed there, but it changes the workstation assumptions. Keep one primary local Ubuntu path when recording results. Confirm sufficient permissions with your account administrator rather than attaching broad policies to a production identity. Official AWS CLI installer instructions: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html.

### Commands in execution order

```bash
sudo apt-get update
sudo apt-get install -y curl jq unzip python3
case "$(uname -m)" in x86_64) ARCH=amd64;; aarch64|arm64) ARCH=arm64;; *) echo 'Unsupported CPU'; exit 1;; esac
mkdir -p .lab/tools
curl -fsSL "https://releases.hashicorp.com/terraform/1.13.4/terraform_1.13.4_linux_${ARCH}.zip" -o .lab/tools/terraform.zip
curl -fsSL https://releases.hashicorp.com/terraform/1.13.4/terraform_1.13.4_SHA256SUMS -o .lab/tools/SHA256SUMS
EXPECTED=$(awk -v name="terraform_1.13.4_linux_${ARCH}.zip" '$2==name {print $1}' .lab/tools/SHA256SUMS)
test -n "$EXPECTED"
printf '%s  %s\n' "$EXPECTED" .lab/tools/terraform.zip | sha256sum -c -
unzip -o .lab/tools/terraform.zip -d .lab/tools
sudo install .lab/tools/terraform /usr/local/bin/terraform
terraform version

case "$(uname -m)" in x86_64) AWS_ARCH=x86_64;; aarch64|arm64) AWS_ARCH=aarch64;; esac
curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-${AWS_ARCH}.zip" -o .lab/tools/aws.zip
unzip -o .lab/tools/aws.zip -d .lab/tools
sudo .lab/tools/aws/install --update
aws --version
aws configure sso
aws sso login --profile portfolio
export AWS_PROFILE=portfolio
aws sts get-caller-identity
```

## Checkpoint — verify before continuing

The caller ARN and account are the intended lab identity. In AWS Billing → Budgets create a monthly cost budget with an email alert before provisioning. A budget alert is not an automatic spending cap.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If aws is missing, install AWS CLI v2: download awscli-exe-linux-x86_64.zip or awscli-exe-linux-aarch64.zip from awscli.amazonaws.com for your architecture, unzip it and run sudo ./aws/install. If SSO is unavailable, use your organization’s approved temporary-credential method; never paste credentials into tfvars.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [02. Inspect the Resources Before Automating](02-inspect-the-resources-before-automating.md). The next chapter assumes the state created here.
