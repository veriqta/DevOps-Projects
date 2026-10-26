# 02. Inspect the Resources Before Automating

[← 01. Prepare AWS Access Budget and Tooling](01-prepare-aws-access-budget-and-tooling.md) · [Project home](README.md) · [03. Bootstrap Protected Remote State →](03-bootstrap-protected-remote-state.md)

## Starting state and working directory

Complete chapter 01 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `02.secure-cloud-infrastructure` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 02.secure-cloud-infrastructure
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Read the inventory before creating it. Infrastructure code can create IAM roles, public endpoints and hourly-billed resources; terraform validate checks structure, not your intended architecture. Inspect the account’s VPC, instance and NAT inventory now so later cleanup can distinguish this project from pre-existing systems. AWS API describe commands are read-only.

## Work through the implementation

The provider default tags identify workload ownership. `environment` validates dev/prod, `allowed_cidr` requires an IPv4 /32, and the AMI is resolved from Canonical’s public SSM parameter in the selected region. This introduces version drift as that parameter moves: record the actual AMI ID in evidence and pin it when reproducibility requires an unchanged operating-system image.

### Commands in execution order

```bash
aws ec2 describe-vpcs --query 'Vpcs[].{Id:VpcId,CIDR:CidrBlock}' --output table
aws ec2 describe-nat-gateways --query 'NatGateways[].{Id:NatGatewayId,State:State}' --output table
aws ec2 describe-instances --query 'Reservations[].Instances[].{Id:InstanceId,State:State.Name}' --output table
terraform -chdir=bootstrap init
terraform -chdir=bootstrap validate
```

### Read the implementation: `terraform/versions.tf`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```hcl
terraform {
  required_version = ">= 1.10, < 2.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 6.0" }
  }
  backend "s3" {}
}
provider "aws" {
  region = var.region
  default_tags { tags = { Project = "orders-foundation", Environment = var.environment, ManagedBy = "Terraform" } }
}
variable "region" { type = string }
variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "prod"], var.environment)
    error_message = "Use dev or prod."
  }
}
variable "allowed_cidr" {
  type = string
  validation {
    condition     = can(cidrnetmask(var.allowed_cidr)) && endswith(var.allowed_cidr, "/32")
    error_message = "Use your public IPv4 /32."
  }
}
variable "cidr" { type = string }
data "aws_availability_zones" "available" { state = "available" }
data "aws_ssm_parameter" "ubuntu" { name = "/aws/service/canonical/ubuntu/server/24.04/stable/current/amd64/hvm/ebs-gp3/ami-id" }
locals {
  name = "orders-${var.environment}"
  azs  = slice(data.aws_availability_zones.available.names, 0, 2)
}
```

## Checkpoint — verify before continuing

Record the existing inventory and read every planned resource type. No resources have been created by init or validate.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

AccessDenied on describe calls is an identity/permission problem. Do not switch accounts casually to bypass it. Confirm AWS_PROFILE and caller identity first.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [03. Bootstrap Protected Remote State](03-bootstrap-protected-remote-state.md). The next chapter assumes the state created here.
