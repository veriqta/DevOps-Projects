# 02. Build and Load the Application Image

[← 01. Install Tools and Create the Lab Cluster](01-install-tools-and-create-the-lab-cluster.md) · [Project home](README.md) · [03. Deploy the Workload and Understand Each Manifest →](03-deploy-the-workload-and-understand-each-manifest.md)

## Starting state and working directory

Complete chapter 01 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `03.kubernetes-application-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 03.kubernetes-application-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A local Docker image is not automatically available in the kind node’s container runtime. Loading it bridges that gap without requiring a registry. IfNotPresent prevents needless pulls of the local lab tag; a production adaptation should use a registry digest. Tests run before packaging so a failed business contract is caught earlier than a cluster rollout.

## Work through the implementation

The token is a dummy runtime input to demonstrate Secret references. The HTTP app does not authenticate checkouts with it; do not claim application authentication. The real operational outcome is that a missing Secret blocks pod startup and that no secret value is committed to a chart. Strengthen the identity boundary before handling real requests.

### Commands in execution order

```bash
python3 -m unittest discover -s app -v
docker build -t orders:lab app
kind load docker-image orders:lab --name orders-platform
kubectl create namespace orders
kubectl -n orders create secret generic orders-runtime --from-literal=token=lab-only-value
```

### Read the implementation: `app/Dockerfile`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```text
FROM python:3.12-alpine
WORKDIR /app
COPY server.py .
RUN adduser -D -u 10001 orders
USER orders
EXPOSE 8080
CMD ["python", "server.py"]
```

## Checkpoint — verify before continuing

Application tests pass, the image load succeeds and the orders-runtime Secret exists in orders. Inspect only its key names, not its decoded value in published evidence.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

ImagePullBackOff in the next chapter often means you loaded a different tag or used a different kind cluster. Confirm the Docker image name and active context.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [03. Deploy the Workload and Understand Each Manifest](03-deploy-the-workload-and-understand-each-manifest.md). The next chapter assumes the state created here.
