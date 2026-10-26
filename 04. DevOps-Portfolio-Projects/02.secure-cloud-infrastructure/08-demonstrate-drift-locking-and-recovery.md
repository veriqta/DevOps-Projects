# 08. Demonstrate Drift Locking and Recovery

[← 07. Separate Environments and Review Changes](07-separate-environments-and-review-changes.md) · [Project home](README.md) · [09. Verify the Architecture Record Costs and Destroy →](09-verify-the-architecture-record-costs-and-destroy.md)

## Starting state and working directory

Complete chapter 07 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `02.secure-cloud-infrastructure` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 02.secure-cloud-infrastructure
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Terraform detects differences between its configuration and actual resources, while Auto Scaling handles instance replacement. These are separate control loops. Demonstrate a reversible console tag drift rather than weakening security rules. Then show that concurrent Terraform operations on the same backend contend for a state lock. Never force-unlock a live operation simply to make the exercise pass.

## Work through the implementation

For replacement evidence, locate one instance in the lab ASG, note its ID, and use EC2 → Instance state → Terminate. Do not decrement desired capacity. Watch Auto Scaling Activities and ALB target health until a replacement becomes healthy. Record customer impact by repeatedly requesting the ALB during the event. This demonstrates recovery from one instance loss, not a whole-AZ or NAT outage.

### Commands in execution order

```bash
VPC=$(terraform -chdir=terraform output -raw vpc_id)
aws ec2 create-tags --resources "$VPC" --tags Key=Name,Value=manual-drift
terraform -chdir=terraform plan -var-file=dev.tfvars
terraform -chdir=terraform apply -var-file=dev.tfvars
```

## Checkpoint — verify before continuing

The plan proposes restoring the Name tag to orders-dev. During an apply, a second terminal using the same AWS inputs and backend should either wait for a lock or report lock contention; short applies may finish too quickly, so an unobserved collision is not proof of failure.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If a lock persists after a crashed process, verify no operation is active, inspect the .tflock owner and use the documented force-unlock procedure only for your abandoned lab lock. Never delete a lock while another person is applying.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [09. Verify the Architecture Record Costs and Destroy](09-verify-the-architecture-record-costs-and-destroy.md). The next chapter assumes the state created here.
