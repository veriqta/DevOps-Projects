# 01. Prepare the Workstation and Repository

[← 00. Business Scenario and Architecture](00-business-scenario-and-architecture.md) · [Project home](README.md) · [02. Run and Test the Application Locally →](02-run-and-test-the-application-locally.md)

## Starting state and working directory

Complete chapter 00 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `01.production-delivery-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 01.production-delivery-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A reproducible delivery exercise starts with a known shell, Docker daemon and writable source repository. The Docker client alone is insufficient: release.sh needs a daemon to create networks and containers. The Docker group grants privileged host access, so use a disposable lab host rather than adding unrelated users to an important machine.

## Work through the implementation

Download/extract the repository or clone your own writable copy. In GitHub create an empty repository under your account. From the repository root run `git init -b main`, set your own Git identity if prompted, add/commit the files, add that repository as origin, and push. Do not clone the old archived upstream expecting these new files. Keep SSH private keys outside Git. For the dedicated runner VM: in your own AWS account, create a budget alert, open EC2 → Launch instance, choose Ubuntu Server 24.04 LTS, a suitable paid instance type (for example t3.small), a dedicated key pair and inbound SSH from My IP only. Review storage and hourly charges before launch. On your workstation set chmod 400 /path/to/key.pem, then connect using ssh -i /path/to/key.pem ubuntu@PUBLIC_IP after verifying its host fingerprint through the console. Copy or clone your writable repository onto that VM, enter this numbered project, and repeat the Docker installation and group-login check there. Leave application ports closed; the runner connects outbound to GitHub. A local Ubuntu VM with outbound internet can be used instead when you do not need a cloud VM.

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

## Checkpoint — verify before continuing

After installation, log out of the Ubuntu session and reconnect so the group change applies. Run docker version, docker compose version and docker run --rm hello-world; the server section and successful hello-world output must appear.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

A permission error means the new group is not active. A missing server section means Docker is not running: inspect sudo systemctl status docker.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [02. Run and Test the Application Locally](02-run-and-test-the-application-locally.md). The next chapter assumes the state created here.
