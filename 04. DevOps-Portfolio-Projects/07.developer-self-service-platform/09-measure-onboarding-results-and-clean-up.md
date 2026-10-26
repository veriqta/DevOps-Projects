# 09. Measure Onboarding Results and Clean Up

[← 08. Test Failed Requests Retry and Rollback](08-test-failed-requests-retry-and-rollback.md) · [Project home](README.md)

## Starting state and working directory

Complete chapter 08 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `07.developer-self-service-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 07.developer-self-service-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

The useful portfolio result is a developer journey with input validation, executable generated output, CI and failure handling. Include the measured subset of onboarding time, not an invented percentage reduction. Explain why generation is atomic locally and where distributed rollback or authentication would be needed for a hosted system.

## Work through the implementation

A résumé bullet can describe a self-service generator producing tested services, CI and Kubernetes manifests with validated inputs and atomic failure recovery. Include measured onboarding time only with its exact scope. Demonstrate one successful request, one invalid request, a failed render and a recovered request. Discuss identity, template versioning, safe updates and remote side-effect compensation in an interview.

### Commands in execution order

```bash
kind delete cluster --name self-service
# Stop any foreground generated servers before removing their files.
rm -rf .generated
gh auth status
```

## Checkpoint — verify before continuing

The lab cluster and generated local copies are removed after evidence is saved. Review GitHub repositories and delete or retain only the lab repositories you intentionally created; revoke unnecessary CLI/token access.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Deleting .generated does not delete GitHub repositories or remote access grants. Make each external cleanup explicit and inspect its destination before acting.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

The project is complete only after the acceptance checks pass and the lab resources are removed. Publish your sanitized implementation and evidence in your own portfolio repository.
