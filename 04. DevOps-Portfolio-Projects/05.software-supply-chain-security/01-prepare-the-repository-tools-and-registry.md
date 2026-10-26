# 01. Prepare the Repository Tools and Registry

[← 00. Threat Model and Release Policy](00-threat-model-and-release-policy.md) · [Project home](README.md) · [02. Establish a Reproducible Baseline Build →](02-establish-a-reproducible-baseline-build.md)

## Starting state and working directory

Complete chapter 00 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `05.software-supply-chain-security` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 05.software-supply-chain-security
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Keep security evidence and keys in an ignored local directory. A registry token should have only the required package scope and should be entered through stdin rather than written into a shell command. The pinned tool baseline makes flags reproducible; vulnerability databases remain time-dependent and must be recorded separately.

## Work through the implementation

The downloaded tools come from their official release repositories. Inspect their corresponding release checksums/signatures before adopting them in a managed environment. In GitHub package settings make the dummy artifact public if you want anonymous verification; otherwise keep scoped registry login active for all commands. Do not place .lab or Cosign keys in a public repository.

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
case "$(uname -m)" in x86_64) ARCH=amd64; SYFT_ARCH=amd64; TRIVY_ARCH=64bit;; aarch64|arm64) ARCH=arm64; SYFT_ARCH=arm64; TRIVY_ARCH=ARM64;; *) exit 1;; esac
mkdir -p .lab/tools
curl -fsSL "https://github.com/sigstore/cosign/releases/download/v2.6.0/cosign-linux-${ARCH}" -o .lab/tools/cosign
sudo install .lab/tools/cosign /usr/local/bin/cosign
curl -fsSL "https://github.com/anchore/syft/releases/download/v1.30.0/syft_1.30.0_linux_${SYFT_ARCH}.tar.gz" -o .lab/tools/syft.tar.gz
tar -xzf .lab/tools/syft.tar.gz -C .lab/tools
sudo install .lab/tools/syft /usr/local/bin/syft
curl -fsSL "https://github.com/aquasecurity/trivy/releases/download/v0.76.1/trivy_0.76.1_Linux-${TRIVY_ARCH}.tar.gz" -o .lab/tools/trivy.tar.gz
tar -xzf .lab/tools/trivy.tar.gz -C .lab/tools
sudo install .lab/tools/trivy /usr/local/bin/trivy
cosign version
syft version
trivy --version

mkdir -p .lab
export GH_USER=REPLACE_WITH_YOUR_GITHUB_USERNAME
export REGISTRY_IMAGE=ghcr.io/REPLACE_USER/REPLACE_REPO/secure-orders
read -rsp "GHCR write token: " GHCR_TOKEN; echo
printf '%s' "$GHCR_TOKEN" | docker login ghcr.io -u "$GH_USER" --password-stdin
unset GHCR_TOKEN
```

## Checkpoint — verify before continuing

All tools report versions, Docker is functional and authentication succeeds. Ensure the registry path is lowercase and belongs to your account.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If Docker is missing, use the complete Docker installation steps in project 01 chapter 01 or Docker’s official Ubuntu instructions; Docker is an explicit prerequisite for this independent project. Do not use a company token with broader access than the lab needs.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [02. Establish a Reproducible Baseline Build](02-establish-a-reproducible-baseline-build.md). The next chapter assumes the state created here.
