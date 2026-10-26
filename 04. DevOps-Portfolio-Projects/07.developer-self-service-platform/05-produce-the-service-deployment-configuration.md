# 05. Produce the Service Deployment Configuration

[← 04. Add the Delivery Workflow and Repository Integration](04-add-the-delivery-workflow-and-repository-integration.md) · [Project home](README.md) · [06. Enforce Naming Input and Access Rules →](06-enforce-naming-input-and-access-rules.md)

## Starting state and working directory

Complete chapter 04 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `07.developer-self-service-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 07.developer-self-service-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Generated deployment files must be executable, not merely plausible YAML. The image tag in deployment.yaml matches the generated service name. Load that image into the named local kind cluster, apply the manifest and verify readiness before forwarding the Service. This is a local platform contract; registry publication is a separate integration for a remote cluster.

## Work through the implementation

On a fresh Ubuntu host, Docker must be installed and usable by the current user before kind starts. The versioned tool installation used in this course is:

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

```

If Docker is not installed, use the official Docker Ubuntu installation block in project 01 chapter 01. Docker itself is an explicit prerequisite of this deployment chapter, not a file shared between projects. The generated workload has two replicas and resource requests; it is not autoscaled or publicly exposed.

### Commands in execution order

```bash
docker build -t orders-api:lab .generated/orders-api
kind create cluster --name self-service
kind load docker-image orders-api:lab --name self-service
kubectl config current-context
kubectl apply -f .generated/orders-api/deployment.yaml
kubectl rollout status deployment/orders-api --timeout=120s
kubectl port-forward service/orders-api 8080:80
```

## Checkpoint — verify before continuing

In a second terminal request localhost:8080/health and expect orders-api/payments. The active context must be kind-self-service. Stop port-forward with Ctrl+C.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If Docker/kind/kubectl are missing, install them before this chapter using the complete tool block below. An image pull failure means the tag was not loaded into this cluster or the manifest names a different service.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [06. Enforce Naming Input and Access Rules](06-enforce-naming-input-and-access-rules.md). The next chapter assumes the state created here.
