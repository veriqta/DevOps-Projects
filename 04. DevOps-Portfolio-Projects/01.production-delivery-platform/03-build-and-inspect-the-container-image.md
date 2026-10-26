# 03. Build and Inspect the Container Image

[← 02. Run and Test the Application Locally](02-run-and-test-the-application-locally.md) · [Project home](README.md) · [04. Create Pull Request Checks →](04-create-pull-request-checks.md)

## Starting state and working directory

Complete chapter 02 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `01.production-delivery-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 01.production-delivery-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A container packages the interpreter and application into a versioned filesystem. USER orders prevents the application from running as root. A tag such as orders:v1 is mutable; it is useful locally, but the registry digest in chapter 05 becomes the durable release identity. Record the resolved base-image digest if you need to repeat the exact build later.

### Commands in execution order

```bash
docker build -t orders:v1 app
docker run -d --name orders-local -p 127.0.0.1:8080:8080 -e VERSION=v1 orders:v1
curl -fsS localhost:8080/health
docker exec orders-local id
docker inspect --format '{{.Image}}' orders-local
docker rm -f orders-local
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

The process has UID 10001, health reports v1 and the image ID is recorded. Submit one checkout before removing the container to prove business behavior inside the image.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If the image builds but exits immediately, inspect docker logs orders-local before removing it. EXPOSE documents a port; it does not publish it, which is why -p is needed.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [04. Create Pull Request Checks](04-create-pull-request-checks.md). The next chapter assumes the state created here.
