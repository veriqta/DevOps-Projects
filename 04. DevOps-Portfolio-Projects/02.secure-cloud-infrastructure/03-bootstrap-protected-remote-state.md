# 03. Bootstrap Protected Remote State

[← 02. Inspect the Resources Before Automating](02-inspect-the-resources-before-automating.md) · [Project home](README.md) · [04. Build the VPC Subnets and Routes →](04-build-the-vpc-subnets-and-routes.md)

## Starting state and working directory

Complete chapter 02 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `02.secure-cloud-infrastructure` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 02.secure-cloud-infrastructure
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

The backend cannot create its own S3 bucket during init. Bootstrap uses local state to create a versioned, encrypted bucket with public access blocked. Its prevent_destroy lifecycle stops an accidental ordinary destroy, but does not make the bucket indestructible or replace IAM controls. Keep bootstrap state private; it is the record needed to manage this foundation.

## Work through the implementation

Review the saved plan before applying; its sensitive contents belong outside Git. Do not delete local bootstrap state after the bucket appears. This is not a migration from an existing workload state: the workload has not yet been applied. If migrating an existing deployment, use init -migrate-state with backups and compare state lineage rather than reconfiguring blindly.

### Commands in execution order

```bash
export TF_VAR_region=us-east-1
export TF_VAR_bucket_name=REPLACE_WITH_GLOBALLY_UNIQUE_LAB_BUCKET
terraform -chdir=bootstrap plan -out=bootstrap.plan
terraform -chdir=bootstrap apply bootstrap.plan
mkdir -p .lab
printf 'bucket = "%s"
key = "dev/terraform.tfstate"
region = "%s"
encrypt = true
use_lockfile = true
' "$TF_VAR_bucket_name" "$TF_VAR_region" > .lab/dev.backend.hcl
terraform -chdir=terraform init -backend-config=../.lab/dev.backend.hcl
```

### Read the implementation: `bootstrap/main.tf`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```hcl
terraform {
  required_version = ">= 1.10, < 2.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 6.0" }
  }
}
provider "aws" { region = var.region }
variable "region" { type = string }
variable "bucket_name" { type = string }
resource "aws_s3_bucket" "state" {
  bucket = var.bucket_name
  lifecycle { prevent_destroy = true }
}
resource "aws_s3_bucket_versioning" "state" {
  bucket = aws_s3_bucket.state.id
  versioning_configuration { status = "Enabled" }
}
resource "aws_s3_bucket_server_side_encryption_configuration" "state" {
  bucket = aws_s3_bucket.state.id
  rule {
    apply_server_side_encryption_by_default { sse_algorithm = "AES256" }
  }
}
resource "aws_s3_bucket_public_access_block" "state" {
  bucket                  = aws_s3_bucket.state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
output "bucket" { value = aws_s3_bucket.state.id }
```

## Checkpoint — verify before continuing

The S3 bucket shows versioning Enabled, default encryption and all public-access blocks enabled. Workload init reports the S3 backend. The role needs GetObject/PutObject on the state key and GetObject/PutObject/DeleteObject on its .tflock key, plus scoped bucket listing.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

BucketAlreadyExists requires another globally unique name. Do not delete or overwrite a bucket you do not own. Lock permission failures need the .tflock object permissions, not a DynamoDB table in this native-locking setup.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [04. Build the VPC Subnets and Routes](04-build-the-vpc-subnets-and-routes.md). The next chapter assumes the state created here.
