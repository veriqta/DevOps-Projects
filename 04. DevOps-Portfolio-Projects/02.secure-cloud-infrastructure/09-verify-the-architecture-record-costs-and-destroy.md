# 09. Verify the Architecture Record Costs and Destroy

[← 08. Demonstrate Drift Locking and Recovery](08-demonstrate-drift-locking-and-recovery.md) · [Project home](README.md)

## Starting state and working directory

Complete chapter 08 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `02.secure-cloud-infrastructure` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 02.secure-cloud-infrastructure
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Complete the ownership cycle by deleting the workload before the backend. Remote state is the record Terraform needs to destroy the resources. The bucket is intentionally retained by default, because deleting it and its historical versions is a separate consequential decision. Do not use force_destroy just to silence a failed cleanup.

## Work through the implementation

Publish a diagram, restricted-rule proof, private-instance inventory, backend policy description, drift/replacement evidence and cost assumptions. A résumé bullet can describe a Terraform-managed private application foundation with remote locking and verified recovery; use actual results. To remove the backend after confirming all workload environments are destroyed: export/retain any state records you need, remove prevent_destroy in bootstrap/main.tf, inspect all versions/delete markers with aws s3api list-object-versions, explicitly delete only this disposable bucket’s versions in the S3 console, then run terraform -chdir=bootstrap destroy with the original variables. This permanently deletes state history, so do it only after review. Include remaining S3 storage in cleanup evidence if you retain it.

### Commands in execution order

```bash
terraform -chdir=terraform plan -destroy -var-file=dev.tfvars
terraform -chdir=terraform destroy -var-file=dev.tfvars
aws ec2 describe-nat-gateways --filter Name=state,Values=available --output table
aws elbv2 describe-load-balancers --output table
```

## Checkpoint — verify before continuing

The workload state contains no managed resources after destroy. Confirm the project ALB, ASG, NAT gateway and EIP are gone in the console, and inspect costs after billing data catches up. The private/versioned state bucket remains intentionally unless you complete the explicit deletion process below.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If destruction fails, keep state and fix the dependency or permission issue. A retained VPC can indicate a service-created network interface still exists; inspect it before deleting anything unrelated.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

The project is complete only after the acceptance checks pass and the lab resources are removed. Publish your sanitized implementation and evidence in your own portfolio repository.
