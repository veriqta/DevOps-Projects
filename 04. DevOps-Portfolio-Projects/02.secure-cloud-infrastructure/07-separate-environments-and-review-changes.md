# 07. Separate Environments and Review Changes

[← 06. Provision the Application Compute Layer](06-provision-the-application-compute-layer.md) · [Project home](README.md) · [08. Demonstrate Drift Locking and Recovery →](08-demonstrate-drift-locking-and-recovery.md)

## Starting state and working directory

Complete chapter 06 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `02.secure-cloud-infrastructure` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 02.secure-cloud-infrastructure
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Environment isolation means independent state and inputs, not merely a different tag. The prod input uses a different name and CIDR. Reconfiguring one working directory to a different backend key changes the state it sees; it must not migrate dev resources into prod. Use separate working copies for simultaneous environments and verify the selected key before every mutation.

## Work through the implementation

Edit backend files with your editor and inspect them before init. The copied prod working directory has no .terraform directory or existing state, so init selects the new key without migration. Shared reusable modules can reduce duplication in a larger implementation; this guide keeps one readable root configuration and only copies it for the isolated preview.

### Commands in execution order

```bash
terraform -chdir=terraform plan -var-file=dev.tfvars
cp .lab/dev.backend.hcl .lab/prod.backend.hcl
# Edit only key in prod.backend.hcl to prod/terraform.tfstate.
# For this preview, use a separate temporary working copy.
mkdir -p .lab/prod-preview
cp terraform/*.tf terraform/prod.tfvars .lab/prod-preview/
terraform -chdir=.lab/prod-preview init -backend-config=../prod.backend.hcl
terraform -chdir=.lab/prod-preview plan -var-file=prod.tfvars
```

## Checkpoint — verify before continuing

Dev plan says No changes. Prod preview proposes a separate VPC and workload, not replacement of dev. Do not apply prod for this cost-bounded exercise unless you deliberately want a second charged environment.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If prod sees dev resources, stop and inspect its backend key. Do not accept an init prompt to migrate dev state into the prod key. State isolation and account isolation are different; separate accounts provide a stronger boundary.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [08. Demonstrate Drift Locking and Recovery](08-demonstrate-drift-locking-and-recovery.md). The next chapter assumes the state created here.
