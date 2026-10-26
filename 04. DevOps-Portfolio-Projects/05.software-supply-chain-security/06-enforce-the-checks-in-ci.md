# 06. Enforce the Checks in CI

[← 05. Sign and Verify the Release Artifact](05-sign-and-verify-the-release-artifact.md) · [Project home](README.md) · [07. Enforce the Deployment Verification Policy →](07-enforce-the-deployment-verification-policy.md)

## Starting state and working directory

Complete chapter 05 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `05.software-supply-chain-security` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 05.software-supply-chain-security
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A check is enforceable only when the protected branch or deployment path requires it. The workflow creates a scan report, evaluates it and uploads the evidence even if the gate fails. Its read-only token cannot publish packages, and pull-request code is not granted a signing secret. Signing is intentionally separate from untrusted pull-request execution.

## Work through the implementation

Configure Settings → Rules → Rulesets for main after the first run exposes the exact check name. For a deterministic failure demonstration, temporarily change the policy’s threshold test to fail in a branch, observe the rejected check, then restore it. Real CVE findings depend on the live database, so record them without assuming a particular CVE will always remain present.

### Commands in execution order

```bash
mkdir -p ../.github/workflows
cp workflows/security.yml ../.github/workflows/orders-security.yml
git add ../.github/workflows/orders-security.yml
git commit -m "Require Orders scan policy"
git push
```

### Read the implementation: `workflows/security.yml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
name: Release security gate
on: [pull_request, workflow_dispatch]
permissions: {contents: read}
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - run: python3 -m unittest discover -s 05.software-supply-chain-security/policy -v
      - run: docker build -t orders:security 05.software-supply-chain-security/app
      - uses: aquasecurity/trivy-action@v0.36.0
        with:
          version: v0.76.1
          image-ref: orders:security
          format: json
          output: scan.json
          exit-code: '0'
      - run: python3 05.software-supply-chain-security/policy/evaluate.py scan.json
      - uses: actions/upload-artifact@v4
        if: always()
        with: {name: security-scan, path: scan.json}
```

## Checkpoint — verify before continuing

Open a pull request and inspect the policy test, scan and evaluation steps. Download the security-scan artifact from both a passing or failing run. Require the gate status in the main branch ruleset.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

A passing job without a branch rule is informational. Do not change the workflow event to pull_request_target while checking out untrusted code and giving it secrets.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [07. Enforce the Deployment Verification Policy](07-enforce-the-deployment-verification-policy.md). The next chapter assumes the state created here.
