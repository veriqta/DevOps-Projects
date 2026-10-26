# 02. Establish a Reproducible Baseline Build

[← 01. Prepare the Repository Tools and Registry](01-prepare-the-repository-tools-and-registry.md) · [Project home](README.md) · [03. Scan Dependencies and Container Contents →](03-scan-dependencies-and-container-contents.md)

## Starting state and working directory

Complete chapter 01 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `05.software-supply-chain-security` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 05.software-supply-chain-security
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Begin with behavior tests, then package and publish the same application. The base image tag can move, so record its resolved digest if claiming exact rebuild reproducibility. The registry digest is the release subject even when the source is unchanged. A signature or scan attached only to a human-readable tag can be misleading after that tag moves.

## Work through the implementation

Inspect the final image user and layers with docker inspect and docker history. Secrets should not appear in Dockerfile instructions, build arguments or copied files. This app has no third-party Python dependencies, but the operating-system and interpreter components still need scanning.

### Commands in execution order

```bash
python3 -m unittest discover -s app -v
docker build -t orders:security app
docker tag orders:security "$REGISTRY_IMAGE:lab"
docker push "$REGISTRY_IMAGE:lab"
docker pull "$REGISTRY_IMAGE:lab"
IMAGE=$(docker image inspect --format '{{index .RepoDigests 0}}' "$REGISTRY_IMAGE:lab")
printf '%s
' "$IMAGE" > .lab/image.txt
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

Tests pass and IMAGE has the expected registry path plus @sha256: followed by 64 hex characters. Compare with the digest printed by docker push.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

An unexpected RepoDigests entry requires inspecting docker image inspect and choosing the digest for your exact registry path. Do not continue signing a different repository or merely the local image ID.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [03. Scan Dependencies and Container Contents](03-scan-dependencies-and-container-contents.md). The next chapter assumes the state created here.
