# 04. Add the Delivery Workflow and Repository Integration

[← 03. Generate and Test the First Service](03-generate-and-test-the-first-service.md) · [Project home](README.md) · [05. Produce the Service Deployment Configuration →](05-produce-the-service-deployment-configuration.md)

## Starting state and working directory

Complete chapter 03 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `07.developer-self-service-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 07.developer-self-service-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

The generated service is intended to become its own repository. Its CI file is already at that generated repository’s .github/workflows path. GitHub creation must target your own account and avoid silently replacing a repository with the same name. A local rollback cannot undo an externally published repository, so the guide treats publishing as an explicit user action.

## Work through the implementation

If Git asks for an author identity, set your own name/email for this generated repository before committing. GitHub CLI login permissions should match the publishing action you intend; do not paste a broad token into template files. The source portfolio repository ignores .generated so it does not accidentally commit nested repository data.

### Commands in execution order

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null
printf 'deb [arch=%s signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main
' "$(dpkg --print-architecture)" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt-get update && sudo apt-get install -y gh
gh auth login
cd .generated/orders-api
git init -b main
git add .
git commit -m "Generate Orders API from platform template"
# Replace YOUR_USER; inspect the destination before publishing.
gh repo create YOUR_USER/orders-api --public --source=. --remote=origin --push
cd ../..
```

### Read the implementation: `template/.github/workflows/check.yml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
name: Check generated service
on: [push, pull_request, workflow_dispatch]
permissions: {contents: read}
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - run: python3 -m unittest discover -v
      - run: docker build -t generated-service:test .
```

## Checkpoint — verify before continuing

The new repository contains only the generated service, and its Check generated service workflow runs tests and builds the image. Preserve the repository/run URL.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If the repository already exists, stop and choose a new validated service name. Do not add a force push or delete an unrelated repository to make the example work.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [05. Produce the Service Deployment Configuration](05-produce-the-service-deployment-configuration.md). The next chapter assumes the state created here.
