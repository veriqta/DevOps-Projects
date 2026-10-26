# 04. Produce and Inspect the SBOM

[← 03. Scan Dependencies and Container Contents](03-scan-dependencies-and-container-contents.md) · [Project home](README.md) · [05. Sign and Verify the Release Artifact →](05-sign-and-verify-the-release-artifact.md)

## Starting state and working directory

Complete chapter 03 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `05.software-supply-chain-security` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 05.software-supply-chain-security
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

An SBOM inventories components; it is not a vulnerability verdict or proof that every runtime dependency is covered. Sign its bytes separately to demonstrate tamper detection. Signing the image and signing its SBOM are two separate operations here; without an attestation binding the SBOM to the image digest, do not claim that the image signature authenticates the SBOM relationship.

## Work through the implementation

Open the CycloneDX metadata and components sections and identify the interpreter plus operating-system packages. Save the image digest beside the SBOM in your report. The public key can be shared; the encrypted private key and its password cannot. A production signing design should describe custody, rotation and CI identity rather than checking a personal key into the workflow.

### Commands in execution order

```bash
syft "$IMAGE" -o cyclonedx-json > .lab/sbom.json
python3 -m json.tool .lab/sbom.json > /dev/null
cd .lab
cosign generate-key-pair
cosign sign-blob --key cosign.key --bundle sbom.bundle.json sbom.json
cosign verify-blob --key cosign.pub --bundle sbom.bundle.json sbom.json
cd ..
```

## Checkpoint — verify before continuing

The SBOM parses, lists components and verifies against the generated public key. Record the key fingerprint and keep its trusted copy separate from the artifact being verified.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If Cosign asks for a transparency-log consent, inspect it and use only this public lab artifact. Protect the generated private-key password. A bundle from a different file or key must fail verification.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [05. Sign and Verify the Release Artifact](05-sign-and-verify-the-release-artifact.md). The next chapter assumes the state created here.
