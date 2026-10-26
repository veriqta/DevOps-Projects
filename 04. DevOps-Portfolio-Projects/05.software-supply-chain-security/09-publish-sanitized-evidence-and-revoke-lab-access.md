# 09. Publish Sanitized Evidence and Revoke Lab Access

[← 08. Prove Rejection Remediation and Exception Handling](08-prove-rejection-remediation-and-exception-handling.md) · [Project home](README.md)

## Starting state and working directory

Complete chapter 08 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `05.software-supply-chain-security` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 05.software-supply-chain-security
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A security portfolio should allow a reviewer to reconstruct the trust argument. Include the digest, SBOM summary, policy, scan decision and positive/negative verification output. Do not publish the private key, token or password. Explain both the strength of the digest verification and the bypass boundary of direct host access.

## Work through the implementation

A truthful résumé bullet can describe a digest-based security gate with SBOM generation, vulnerability policy, signing and demonstrated rejection. Include the date and evidence, not “zero vulnerabilities forever.” Prepare to explain trust roots, mutable tags, attestation binding, scanner freshness and why CI permissions differ for pull requests and releases.

### Commands in execution order

```bash
docker logout ghcr.io
rm -rf .lab
docker ps --filter name=verified-orders
```

## Checkpoint — verify before continuing

No lab container remains. Revoke the package token in GitHub, remove unneeded package versions/signatures and disable the copied workflow if the lab repository is being retired.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Removing local key files does not revoke a registry token or erase a public transparency-log entry. Rotate credentials through the provider and do not promise deletion of immutable public records.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

The project is complete only after the acceptance checks pass and the lab resources are removed. Publish your sanitized implementation and evidence in your own portfolio repository.
