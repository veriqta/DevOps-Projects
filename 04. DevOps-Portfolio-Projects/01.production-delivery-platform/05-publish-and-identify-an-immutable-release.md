# 05. Publish and Identify an Immutable Release

[← 04. Create Pull Request Checks](04-create-pull-request-checks.md) · [Project home](README.md) · [06. Deploy and Verify Staging →](06-deploy-and-verify-staging.md)

## Starting state and working directory

Complete chapter 04 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `01.production-delivery-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 01.production-delivery-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A SHA tag links an artifact to source, while the content digest identifies what the registry actually stores. Build once, then pass that digest to both environments. Rebuilding for production would produce a second artifact and weaken the claim that staging tested the production release. The publishing token is GitHub’s job-scoped GITHUB_TOKEN rather than a long-lived personal credential.

## Work through the implementation

Open the completed build summary and preserve both the source commit SHA and digest. Set `export IMAGE=ghcr.io/YOUR_USER/YOUR_REPO/orders@sha256:YOUR_DIGEST` using the actual lowercase path. On the deployment VM, run `docker pull "$IMAGE"` to verify access before configuring CI. A private package needs an authenticated pull on that VM; do not assume the workflow login is inherited remotely. The workflow builds amd64 and arm64 variants. Its release digest identifies the multi-platform index; Docker selects the matching platform manifest, so record both the index identity and the deployment host architecture when explaining the release.

### Commands in execution order

```bash
cp workflows/publish.yml ../.github/workflows/orders-publish.yml
git add ../.github/workflows/orders-publish.yml
git commit -m "Publish immutable Orders releases"
git push
```

### Read the implementation: `workflows/publish.yml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
name: Publish Orders release
on: {workflow_dispatch: {}}
permissions: {contents: read, packages: write}
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - id: image
        run: echo "name=ghcr.io/${GITHUB_REPOSITORY,,}/orders" >> "$GITHUB_OUTPUT"
      - uses: docker/setup-qemu-action@v3
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        id: build
        with:
          context: 01.production-delivery-platform/app
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.image.outputs.name }}:${{ github.sha }}
      - run: echo '${{ steps.image.outputs.name }}@${{ steps.build.outputs.digest }}' >> "$GITHUB_STEP_SUMMARY"
```

## Checkpoint — verify before continuing

Run Publish Orders release from Actions. Copy its ghcr.io/.../orders@sha256:... summary into your notes and export IMAGE with that value in the terminal used below. The digest suffix must contain 64 hexadecimal characters.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

A registry 403 usually means package permissions or owner settings. Under the created package settings, make this demonstration package public for anonymous pulls. Never publish an image containing credentials or private business code.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [06. Deploy and Verify Staging](06-deploy-and-verify-staging.md). The next chapter assumes the state created here.
