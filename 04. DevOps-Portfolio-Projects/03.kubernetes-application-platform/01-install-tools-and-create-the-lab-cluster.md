# 01. Install Tools and Create the Lab Cluster

[← 00. Platform Requirements and Request Flow](00-platform-requirements-and-request-flow.md) · [Project home](README.md) · [02. Build and Load the Application Image →](02-build-and-load-the-application-image.md)

## Starting state and working directory

Complete chapter 00 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `03.kubernetes-application-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 03.kubernetes-application-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

kubectl speaks to the cluster API; kind creates the local cluster; Helm renders and manages a release. Check the active context before mutations so a personal workstation does not accidentally target an unrelated cluster. The guide uses a versioned client baseline and named cluster rather than relying on whatever tools were previously installed.

## Work through the implementation

Run the Docker installation only on a fresh Ubuntu lab host; if Docker already works, start at the version checks. Downloaded tools are placed under .lab/tools before installation. For a real team, pin and verify all release checksums/signatures through your approved tool-distribution process. The kubectl binary checksum is checked explicitly here.

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

Log out and reconnect so Docker group membership is active. Confirm `docker version`, then continue:

```bash
case "$(uname -m)" in x86_64) ARCH=amd64;; aarch64|arm64) ARCH=arm64;; *) exit 1;; esac
mkdir -p .lab/tools
curl -fsSL "https://dl.k8s.io/release/v1.34.1/bin/linux/${ARCH}/kubectl" -o .lab/tools/kubectl
curl -fsSL "https://dl.k8s.io/release/v1.34.1/bin/linux/${ARCH}/kubectl.sha256" -o .lab/tools/kubectl.sha256
printf '%s  %s\n' "$(cat .lab/tools/kubectl.sha256)" .lab/tools/kubectl | sha256sum -c -
sudo install .lab/tools/kubectl /usr/local/bin/kubectl
curl -fsSL "https://kind.sigs.k8s.io/dl/v0.30.0/kind-linux-${ARCH}" -o .lab/tools/kind
sudo install .lab/tools/kind /usr/local/bin/kind
curl -fsSL "https://get.helm.sh/helm-v3.19.0-linux-${ARCH}.tar.gz" -o .lab/tools/helm.tar.gz
tar -xzf .lab/tools/helm.tar.gz -C .lab/tools
sudo install ".lab/tools/linux-${ARCH}/helm" /usr/local/bin/helm
kubectl version --client
kind version
helm version

kind create cluster --name orders-platform --config platform/kind.yaml
kubectl config current-context
kubectl get nodes
```

### Read the implementation: `platform/kind.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
```

## Checkpoint — verify before continuing

The context is kind-orders-platform and three nodes become Ready. The Kubernetes API and node versions are recorded. Docker must be running before kind creation.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If kind cannot schedule, check Docker memory and docker logs for the node containers. If the context is not kind-orders-platform, select it explicitly before any apply or delete.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [02. Build and Load the Application Image](02-build-and-load-the-application-image.md). The next chapter assumes the state created here.
