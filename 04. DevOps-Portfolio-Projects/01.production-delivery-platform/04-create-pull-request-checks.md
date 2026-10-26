# 04. Create Pull Request Checks

[← 03. Build and Inspect the Container Image](03-build-and-inspect-the-container-image.md) · [Project home](README.md) · [05. Publish and Identify an Immutable Release →](05-publish-and-identify-an-immutable-release.md)

## Starting state and working directory

Complete chapter 03 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `01.production-delivery-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 01.production-delivery-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

CI should run on a proposed change before it is merged. The workflow grants read-only repository access and builds an image only after behavioral tests pass. Installing workflow YAML inside this project directory does not activate it: GitHub reads workflows from the repository-root .github/workflows directory. Branch protection then decides whether a failing check blocks merge.

## Work through the implementation

In GitHub open Settings → Rules → Rulesets, create a branch ruleset targeting main, require a pull request and the test status check. Choose the check after its first run so the name is correct. Record a failed run URL and the corrected run URL. Do not merge the deliberate failing assertion.

### Commands in execution order

```bash
mkdir -p ../.github/workflows
cp workflows/checks.yml ../.github/workflows/orders-checks.yml
git add ../.github/workflows/orders-checks.yml
git commit -m "Add Orders pull request checks"
git push
```

### Read the implementation: `workflows/checks.yml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
name: Orders pull request checks
on: [pull_request, workflow_dispatch]
permissions: {contents: read}
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v5
        with: {python-version: '3.12'}
      - run: python -m unittest discover -s 01.production-delivery-platform/app -v
      - run: docker build -t orders:test 01.production-delivery-platform/app
```

## Checkpoint — verify before continuing

Open a branch and pull request in your repository. Confirm the test job passes. Temporarily change an assertion in app/test_server.py, commit and confirm it fails; restore the assertion before merging. Configure a ruleset for main requiring the observed check name.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

No workflow run means the file is not at the repository root, Actions is disabled, or no pull request event occurred. A green run does not block merges until the branch rule requires it.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [05. Publish and Identify an Immutable Release](05-publish-and-identify-an-immutable-release.md). The next chapter assumes the state created here.
