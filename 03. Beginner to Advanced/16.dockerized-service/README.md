# 16. Dockerized Service

[← All projects](../README.md) · **Intermediate** · Docker · GitHub Actions

Build and publish a versioned image and deploy it to a lab server.

## Prerequisites

Docker, a writable GitHub repository with Actions and GHCR enabled, and a disposable Docker VM for the deployment step.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Files included

Everything below is inside this project’s `files/` folder.

| File or folder | Use |
| --- | --- |
| `app` | Demo HTTP service, Dockerfile and service unit. |
| `publish-image.yml` | Configuration or starter code referenced in the steps below. |

## Walkthrough

From the repository root, enter this project:

```bash
cd 16.dockerized-service
```

Run the remaining commands here unless a step explicitly changes directories. The `files/` folder contains the supplied code and configurations for this project.

### 1. Build and test locally

```bash
docker build -t devops-demo:lab files/app
docker run -d --name image-test -p 127.0.0.1:8080:8080 devops-demo:lab
curl -fsS localhost:8080/health
docker rm -f image-test
```

### 2. Publish an immutable release

```bash
mkdir -p ../.github/workflows
cp files/publish-image.yml ../.github/workflows/publish-image.yml
git add ../.github/workflows/publish-image.yml
git commit -m "Publish lab image"
git push
```

Run **Publish demo image** in Actions. Copy the image reference including `@sha256:…` from its job summary. Under your profile/organization → Packages, set this lab package public if you want anonymous pulls. Keep private packages private if they contain anything sensitive; use a scoped registry read credential instead.

### 3. Deploy — on the Docker VM

```bash
export IMAGE=REPLACE_WITH_FULL_GHCR_IMAGE_AT_SHA256_DIGEST
docker pull "$IMAGE"
docker run -d --name deployed-demo -p 127.0.0.1:8080:8080 "$IMAGE"
curl -fsS localhost:8080/health
docker inspect --format '{{.Image}}' deployed-demo
```

Save the digest before any replacement. For a second release, stop/remove the lab container and repeat with the next digest; repeat with the saved digest to roll back. This basic deployment has downtime; project 23 removes the single-instance switch.

## Verify completion

The workflow publishes a SHA-tagged image, the deployment uses a digest, health succeeds and rollback runs the previous digest.

## Troubleshooting

A registry 403 often means package visibility or token permissions. Ensure the image path is lowercase and use the exact digest from the build summary.

## Cleanup

On the VM run `docker rm -f deployed-demo`. Remove lab images and package versions through GHCR; disable/remove the workflow and destroy the VM.

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented dockerized service in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://docs.github.com/en/actions/tutorials/publish-packages/publish-docker-images)

---

[← Previous: 15](../15.node-js-service-deployment/README.md) · [All projects](../README.md) · [Next: 17 →](../17.multi-container-application/README.md)
