# 01. Prepare the Workload and Cost Assumptions

[← 00. Business Budget and Performance Target](00-business-budget-and-performance-target.md) · [Project home](README.md) · [02. Measure the Baseline Under Repeatable Load →](02-measure-the-baseline-under-repeatable-load.md)

## Starting state and working directory

Complete chapter 00 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `08.cloud-cost-and-capacity` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 08.cloud-cost-and-capacity
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Keep the app image and test script fixed while comparing resource limits. Terraform is used only to describe a billable shape to Infracost; the invalid AMI and explicit precondition make apply unsuitable. A price estimate needs dated assumptions for region, purchase model, storage, traffic and usage, because those choices can dominate a nominal instance-size saving.

## Work through the implementation

Use the project’s fixed Docker image for both runs. The default local capacity is 0.25 CPU and 128 MiB, with a small simulated request delay. These are experiment inputs, not recommended EC2 sizing. Record Docker host CPU/memory and other running workloads so a reviewer can interpret noisy timing results.

### Commands in execution order

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl git jq unzip python3 python3-venv openssl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
. /etc/os-release
printf 'deb [arch=%s signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu %s stable\n' "$(dpkg --print-architecture)" "$VERSION_CODENAME" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker "$USER"

```

Log out of the Ubuntu session and reconnect before continuing so Docker group membership is active. Verify `docker version` shows the server. Then run:

```bash
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

python3 -m unittest discover -s app -v
python3 -m unittest discover -s scripts -v
mkdir -p .lab
docker compose config
docker compose up -d --build
curl -fsS localhost:8080/health
```

### Read the implementation: `compose.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
name: portfolio-capacity
services:
  app:
    build: ./app
    ports: ["127.0.0.1:8080:8080"]
    cpus: ${CPU_LIMIT:-0.25}
    mem_limit: ${MEMORY_LIMIT:-128m}
    environment:
      DELAY_MS: ${DELAY_MS:-100}
```

### Read the implementation: `terraform/main.tf`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```hcl
terraform {
  required_version = ">= 1.10, < 2.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 6.0" }
  }
}
provider "aws" { region = "us-east-1" }
variable "instance_type" {
  type    = string
  default = "t3.small"
}
resource "aws_instance" "estimate_only" {
  ami           = "ami-00000000000000000"
  instance_type = var.instance_type
  root_block_device { volume_size = 20 }
  lifecycle {
    precondition {
      condition     = var.instance_type == "DO-NOT-APPLY"
      error_message = "Estimate-only fixture: terraform apply is intentionally blocked."
    }
  }
}
```

## Checkpoint — verify before continuing

Application and comparison tests pass, the service is healthy and the rendered Compose limits are recorded. Do not run terraform apply in the estimate folder.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If Docker is unavailable, install it on the Ubuntu lab host before starting. Terraform validation does not validate a price, a budget or actual service performance.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [02. Measure the Baseline Under Repeatable Load](02-measure-the-baseline-under-repeatable-load.md). The next chapter assumes the state created here.
