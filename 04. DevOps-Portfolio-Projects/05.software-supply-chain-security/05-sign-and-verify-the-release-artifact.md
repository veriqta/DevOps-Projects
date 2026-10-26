# 05. Sign and Verify the Release Artifact

[← 04. Produce and Inspect the SBOM](04-produce-and-inspect-the-sbom.md) · [Project home](README.md) · [06. Enforce the Checks in CI →](06-enforce-the-checks-in-ci.md)

## Starting state and working directory

Complete chapter 04 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `05.software-supply-chain-security` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 05.software-supply-chain-security
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

The deployment verifier needs a trusted key and immutable subject. Cosign stores signature material alongside the registry artifact, while verification checks that material against the supplied public key. If an attacker can replace both the image and the verifier’s trusted key, a local signature check no longer establishes the intended identity boundary.

## Work through the implementation

Use `mkdir -p .lab/untrusted; (cd .lab/untrusted && cosign generate-key-pair)` for the negative test, then `cosign verify --key .lab/untrusted/cosign.pub "$IMAGE"`. Expect a nonzero exit. Never interpret a signature under an arbitrary key as proof of your release authority.

### Commands in execution order

```bash
cosign sign --key .lab/cosign.key "$IMAGE"
cosign verify --key .lab/cosign.pub "$IMAGE" > .lab/verified-image.json
python3 -m json.tool .lab/verified-image.json
```

## Checkpoint — verify before continuing

The signature payload identifies the same image digest as .lab/image.txt. Generate a second key in .lab/untrusted and verify that it cannot verify this image.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Registry authorization failures and signature failures are different. Confirm image access before debugging signing trust; do not disable identity or verification checks just to obtain output.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [06. Enforce the Checks in CI](06-enforce-the-checks-in-ci.md). The next chapter assumes the state created here.
