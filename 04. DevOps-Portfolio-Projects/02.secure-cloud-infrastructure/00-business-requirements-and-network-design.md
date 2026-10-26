# 00. Business Requirements and Network Design

[Project home](README.md) · [01. Prepare AWS Access Budget and Tooling →](01-prepare-aws-access-budget-and-tooling.md)

## Starting state and working directory

Read the project README and have a terminal open at the repository root.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `02.secure-cloud-infrastructure` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 02.secure-cloud-infrastructure
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Public and private describe routing and addressing, not just subnet names. The ALB needs public subnets in two availability zones; application instances remain in private subnets without public IPs. Their package installation uses NAT egress. Security groups are stateful: the application permits port 80 only from the ALB group, while response packets do not need a matching inbound ephemeral-port rule. Terraform’s remote backend is a separate control-plane dependency that must exist before the workload is initialized.

## Work through the implementation

Use dev first. Reserve a region, an unused VPC CIDR and your current public IPv4 /32. The supplied dev/prod CIDRs do not overlap. List all chargeable resources and decide when you will destroy them. The prod input represents a second lab environment, not an instruction to create actual company production infrastructure.

### Commands in execution order

```bash
find bootstrap terraform scripts -maxdepth 2 -type f | sort
```

## Checkpoint — verify before continuing

Draw internet → ALB → private instance and private instance → NAT → package repositories. Identify the state bucket as separate from application networking.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If you cannot explain both traffic directions, review routes and security-group rules before applying. A private subnet with an internet-gateway route does not automatically give a private-only instance public access.

## What to record

Save the architecture and acceptance criteria in your own notes. You will compare the finished system with this contract in chapter 09.

## Continue

When this checkpoint passes, continue to [01. Prepare AWS Access Budget and Tooling](01-prepare-aws-access-budget-and-tooling.md). The next chapter assumes the state created here.
