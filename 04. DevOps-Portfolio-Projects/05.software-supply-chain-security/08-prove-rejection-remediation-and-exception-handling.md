# 08. Prove Rejection Remediation and Exception Handling

[← 07. Enforce the Deployment Verification Policy](07-enforce-the-deployment-verification-policy.md) · [Project home](README.md) · [09. Publish Sanitized Evidence and Revoke Lab Access →](09-publish-sanitized-evidence-and-revoke-lab-access.md)

## Starting state and working directory

Complete chapter 07 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `05.software-supply-chain-security` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 05.software-supply-chain-security
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Collect negative-path evidence deliberately. Byte changes to the SBOM should break its blob signature; a wrong key should reject the image; a policy fixture containing a fixed high-severity finding should block. Remediation means changing the artifact or policy through review and producing new evidence, not editing the output file. Exceptions must identify a scope, owner, rationale and expiry.

## Work through the implementation

Write an exception record with artifact digest, vulnerability ID, impact review, compensating control, owner and expiration. This is a review exercise, not an implemented allowlist. Discuss how a production system would verify and enforce signed exceptions. The core acceptance remains the explicit strict policy in evaluate.py.

### Commands in execution order

```bash
cp .lab/sbom.json .lab/tampered.json
printf '\n ' >> .lab/tampered.json
cosign verify-blob --key .lab/cosign.pub --bundle .lab/sbom.bundle.json .lab/tampered.json
# Expect verification failure; then run the independent policy tests.
python3 -m unittest discover -s policy -v
```

## Checkpoint — verify before continuing

Capture the failed tamper verification and passing positive/negative policy tests. If a real scan blocks, rebuild after a base-image fix and show the changed digest and rerun result.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Do not add an all-CVE exclusion to make the example pass. For this strict core implementation there is no automated exception bypass; document a proposed exception separately rather than pretending the gate consumed it.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [09. Publish Sanitized Evidence and Revoke Lab Access](09-publish-sanitized-evidence-and-revoke-lab-access.md). The next chapter assumes the state created here.
