# Lab environment setup

[← Projects](README.md)

## Choose an environment

- **Projects 01–03 and 20:** Python 3.9+; project 01 needs Linux `/proc`.
- **Host administration:** disposable Ubuntu 24.04 VM with sudo and SSH. Keep a provider console available during SSH/firewall changes.
- **Containers:** Docker Engine with Compose v2, or Docker Desktop on macOS/Windows. Reserve at least 4 GB memory; 8 GB for Kubernetes and monitoring.
- **Kubernetes:** Docker, kind, kubectl. Helm and Flux are used in later projects.
- **Cloud:** AWS CLI v2 or Terraform and a provider account. Enable MFA and a budget alert. Lab resources can cost money even when idle.

## Ubuntu workstation / VM basics

```bash
sudo apt-get update
sudo apt-get install -y git curl jq python3 python3-venv openssh-client dnsutils nodejs npm
python3 --version
node --version
```

For Python-only labs no pip packages are needed. For Ansible create an isolated environment:

```bash
python3 -m venv .lab/ansible
. .lab/ansible/bin/activate
pip install 'ansible-core>=2.16,<2.20'
ansible --version
```

Install Docker from its [Ubuntu installation instructions](https://docs.docker.com/engine/install/ubuntu/) or [Docker Desktop](https://docs.docker.com/desktop/). Verify:

```bash
docker version
docker compose version
docker run --rm hello-world
```

Docker access is privileged; use a disposable environment for these labs. Do not use sudo randomly to work around a missing Docker daemon.

## Additional tools

Install the tools needed for the project you selected. Use the official instructions for your OS, then check the version:

| Tool | Install | Check |
| --- | --- | --- |
| Terraform | [Install](https://developer.hashicorp.com/terraform/install) | `terraform version` |
| AWS CLI v2 | [Install](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) | `aws --version` |
| kind | [Install](https://kind.sigs.k8s.io/docs/user/quick-start/#installation) | `kind version` |
| kubectl | [Install](https://kubernetes.io/docs/tasks/tools/) | `kubectl version --client` |
| Helm | [Install](https://helm.sh/docs/intro/install/) | `helm version` |
| Flux | [Install](https://fluxcd.io/flux/installation/) | `flux version --client` |
| Syft | [Install](https://github.com/anchore/syft#installation) | `syft version` |
| Grype | [Install](https://github.com/anchore/grype#installation) | `grype version` |
| Cosign | [Install](https://docs.sigstore.dev/cosign/system_config/installation/) | `cosign version` |
| k6 | [Install](https://grafana.com/docs/k6/latest/set-up/install-k6/) | `k6 version` |
| Restic | [Install](https://restic.readthedocs.io/en/stable/020_installation.html) | `restic version` |
| Infracost | [Install](https://www.infracost.io/docs/#quick-start) | `infracost --version` |

## Optional contributor checks

```bash
python3 -m unittest discover -s .github/checks -v
node --check 10.basic-dockerfile/files/app/server.js
```

Set `NODE_BIN` to an absolute Node executable path if `node` is not on PATH. The HTTP integration tests start temporary loopback servers and stop them automatically. Linux-only checks are skipped on other systems. The container smoke test is separate because it requires Docker:

```bash
bash .github/checks/container-smoke.sh
```

## Working from a ZIP

Extract the ZIP, open `README.md`, then begin with `01.server-performance-stats/README.md`. Contributor checks above are optional for learners. You do not need to clone the archived upstream repository. To publish your own copy, create an empty repository in your account, initialize Git here, and set its remote to your new repository.

## Keep labs separate

Use a dedicated cloud profile, a disposable VM and a dedicated Kubernetes context. Before any apply/delete command inspect `kubectl config current-context` or `aws sts get-caller-identity`. `.lab/` is ignored by Git and holds temporary local artifacts.
