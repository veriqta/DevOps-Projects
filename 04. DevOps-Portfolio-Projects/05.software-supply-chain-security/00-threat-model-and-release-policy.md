# 00. Threat Model and Release Policy

[Project home](README.md) · [01. Prepare the Repository Tools and Registry →](01-prepare-the-repository-tools-and-registry.md)

## Starting state and working directory

Read the project README and have a terminal open at the repository root.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `05.software-supply-chain-security` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 05.software-supply-chain-security
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Scanning and signing answer different questions. A vulnerability scan reports known issues at a point in time; a signature proves that the holder of a key signed a particular digest. Neither proves safe behavior. The lab blocks fixed HIGH and CRITICAL vulnerabilities, reports unfixed findings for review and requires a signature from the expected lab key. An empty or malformed scan must not be mistaken for a clean image.

## Work through the implementation

The adversarial cases are a substituted tag, unsigned image, wrong signing key, changed SBOM and a scan finding that should block promotion. This is defensive verification of artifacts you own. The deployment wrapper is bypassable by someone with direct Docker access, so the lab also requires a written access-boundary discussion. A real cluster admission controller is an optional future strengthening, not a hidden guarantee here.

### Commands in execution order

```bash
find app policy scripts workflows -maxdepth 2 -type f | sort
```

## Checkpoint — verify before continuing

Write the policy in plain language, identify the trusted public key and explain why tags alone cannot identify an approved release.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If a policy statement says “secure image,” make it more specific: name the scanner decision, key identity, artifact digest and verification time.

## What to record

Save the architecture and acceptance criteria in your own notes. You will compare the finished system with this contract in chapter 09.

## Continue

When this checkpoint passes, continue to [01. Prepare the Repository Tools and Registry](01-prepare-the-repository-tools-and-registry.md). The next chapter assumes the state created here.
