# 07. Enforce the Deployment Verification Policy

[← 06. Enforce the Checks in CI](06-enforce-the-checks-in-ci.md) · [Project home](README.md) · [08. Prove Rejection Remediation and Exception Handling →](08-prove-rejection-remediation-and-exception-handling.md)

## Starting state and working directory

Complete chapter 06 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `05.software-supply-chain-security` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 05.software-supply-chain-security
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

The wrapper is the release entry point. It rejects a non-digest input, verifies the signature, scans that exact digest again and applies the vulnerability policy. Only after it exits successfully should deployment continue. The wrapper is a process control, not an admission controller: direct Docker privileges bypass it, so access to the host remains an explicit trust boundary.

## Work through the implementation

Run the verification and deployment with && for the actual recorded demonstration. The separated lines above let you inspect each stage, but you must stop if verification fails. An unsigned digest must not be deployed through this entry point. A future policy-controller integration can enforce the boundary inside Kubernetes rather than relying on host operator discipline.

### Commands in execution order

```bash
bash scripts/verify-release.sh "$IMAGE" .lab/cosign.pub && docker run -d --name verified-orders -p 127.0.0.1:8080:8080 "$IMAGE"
curl -fsS localhost:8080/health
docker rm -f verified-orders
```

### Read the implementation: `scripts/verify-release.sh`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```bash
#!/usr/bin/env bash
set -euo pipefail
image=${1:?Usage: bash scripts/verify-release.sh image@sha256:digest public-key}
key=${2:?Public signing key required}
[[ "$image" =~ @sha256:[0-9a-f]{64}$ ]] || { echo 'Digest required' >&2;exit 2; }
cosign verify --key "$key" "$image" > /dev/null
trivy image --format json --output .lab/deployment-scan.json "$image"
python3 policy/evaluate.py .lab/deployment-scan.json
printf 'Verified signature and scan policy for %s\n' "$image"
```

## Checkpoint — verify before continuing

The wrapper passes for the trusted signed digest only when its current scan meets policy. Health works after deployment. Repeat using the unrelated key and confirm the wrapper exits before any deployment command is reached.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Shell commands on separate lines do not automatically enforce sequencing after a failure in an interactive shell. In your own automation use `bash scripts/verify-release.sh ... && docker run ...` or a script with set -e.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [08. Prove Rejection Remediation and Exception Handling](08-prove-rejection-remediation-and-exception-handling.md). The next chapter assumes the state created here.
