# 29. Supply Chain Security

[← All projects](../../README.md) · **Advanced** · Syft · Grype · Cosign

Produce an SBOM, evaluate vulnerabilities and verify an image signature.

## Prerequisites

Docker, Syft, Grype, Cosign and an internet connection. Use only the public demo artifact; signing can write artifact hashes to a public transparency log.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Create and scan an SBOM

```bash
mkdir -p .lab/supply-chain
docker build -t devops-demo:lab 02.examples/app
syft devops-demo:lab -o cyclonedx-json > .lab/supply-chain/sbom.json
grype sbom:.lab/supply-chain/sbom.json -o table
```

Save the scan timestamp and database version from `grype db status`. Findings change as vulnerability databases update. Review fixed versions rather than blindly suppressing findings.

### 2. Sign the SBOM

```bash
cd .lab/supply-chain
cosign generate-key-pair
cosign sign-blob --key cosign.key --bundle sbom.bundle.json sbom.json
cosign verify-blob --key cosign.pub --bundle sbom.bundle.json sbom.json
```

Choose a private-key password when prompted. Inspect and accept any transparency-log consent only for this public lab artifact.

### 3. Prove tamper detection

```bash
cp sbom.json tampered.json
printf '\n ' >> tampered.json
cosign verify-blob --key cosign.pub --bundle sbom.bundle.json tampered.json
```

The final command must fail because the bytes changed.

### 4. Sign an image digest

Complete project 16, authenticate to your registry, then use its exact public lab digest:

```bash
export IMAGE=REPLACE_WITH_GHCR_IMAGE_AT_SHA256_DIGEST
cosign sign --key cosign.key "$IMAGE"
cosign verify --key cosign.pub "$IMAGE"
```

A valid signature proves who controlled the signing key, not that the image is vulnerability-free. Keep the public key through a separate trusted channel.

## Verify completion

The original SBOM and image verify, the modified SBOM fails verification, and the scan report records a dated decision about findings.

## Troubleshooting

A signature failure can mean a changed blob, wrong key or incompatible bundle tooling. Use the same current Cosign version for signing and verification.

## Cleanup

Remove `.lab/supply-chain` after saving public evidence; destroy the lab signing key. Delete the lab registry artifact and associated signatures if no longer needed.

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://docs.sigstore.dev/cosign/signing/overview/)

---

[← Previous: 28](../28.gitops-delivery/README.md) · [All projects](../../README.md) · [Next: 30 →](../30.load-testing-and-resilience/README.md)
