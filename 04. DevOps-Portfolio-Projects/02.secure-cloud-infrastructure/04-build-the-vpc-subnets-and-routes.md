# 04. Build the VPC Subnets and Routes

[← 03. Bootstrap Protected Remote State](03-bootstrap-protected-remote-state.md) · [Project home](README.md) · [05. Configure Access and Security Boundaries →](05-configure-access-and-security-boundaries.md)

## Starting state and working directory

Complete chapter 03 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `02.secure-cloud-infrastructure` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 02.secure-cloud-infrastructure
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Each subnet gets an explicit route-table association, avoiding dependence on the VPC default table. Public routes use the internet gateway; private routes use the NAT gateway. The application has no SSH access and no public IP. Creating two private subnets does not remove the single NAT failure domain; distinguish workload distribution from egress resilience in your design explanation.

## Work through the implementation

cidrsubnet adds eight subnet bits to the VPC CIDR. Public indices 0–1 and private indices 10–11 create distinct ranges. The NAT’s dependency on the internet gateway expresses the required egress foundation. Explain why the private instances still need outbound access to install Nginx, and which costs would change with per-AZ NAT or VPC endpoints.

### Commands in execution order

```bash
export TF_VAR_allowed_cidr=REPLACE_WITH_YOUR_PUBLIC_IPV4/32
terraform -chdir=terraform fmt -check
terraform -chdir=terraform validate
terraform -chdir=terraform plan -var-file=dev.tfvars -out=dev.plan
```

### Read the implementation: `terraform/network.tf`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```hcl
resource "aws_vpc" "main" {
  cidr_block           = var.cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags                 = { Name = local.name }
}
resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.cidr, 8, count.index)
  availability_zone = local.azs[count.index]
}
resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.cidr, 8, 10 + count.index)
  availability_zone = local.azs[count.index]
}
resource "aws_internet_gateway" "main" { vpc_id = aws_vpc.main.id }
resource "aws_eip" "nat" { domain = "vpc" }
resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id
  depends_on    = [aws_internet_gateway.main]
}
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main.id
  }
}
resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}
resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}
```

## Checkpoint — verify before continuing

The plan shows exactly one VPC, two public subnets, two private subnets and one NAT gateway. It must not contain changes to unrelated existing resources. Do not apply until the next chapter’s boundary review passes.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

A /32 validation error means you supplied a network range or malformed address. If the account lacks two available AZs, choose a supported region and rebuild backend inputs consistently before creation.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [05. Configure Access and Security Boundaries](05-configure-access-and-security-boundaries.md). The next chapter assumes the state created here.
