# 07. Run a Complete Developer Onboarding Journey

[← 06. Enforce Naming Input and Access Rules](06-enforce-naming-input-and-access-rules.md) · [Project home](README.md) · [08. Test Failed Requests Retry and Rollback →](08-test-failed-requests-retry-and-rollback.md)

## Starting state and working directory

Complete chapter 06 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `07.developer-self-service-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 07.developer-self-service-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Use a second distinct service to demonstrate the full request contract from a clean name. Measure from request submission through successful generated tests and health, and separately measure repository/cluster integration. Combining all times into one number can hide waiting on authentication or external CI. Keep the same workload definition when comparing with your manual baseline.

## Work through the implementation

Use the same repository publishing and deployment sequence with the new service name only if you want a second external artifact. It is not required to create multiple charged resources just to collect a timing number. Save request input, generated commit, test result and health JSON as one traceable onboarding record.

### Commands in execution order

```bash
SECONDS=0
python3 automation/generate.py inventory-api --team platform
python3 -m unittest discover -s .generated/inventory-api -v
printf 'Request plus tests: %s seconds
' "$SECONDS"
PORT=8083 python3 .generated/inventory-api/server.py
```

## Checkpoint — verify before continuing

A second terminal request to localhost:8083/health identifies inventory-api/platform. Stop the process. Inspect the two independent generated directories and show that changing one service does not alter the template or the other service.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Do not interpret cached local generation speed as a full production onboarding time. Record the environment, included steps and whether CI/image downloads were warm.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [08. Test Failed Requests Retry and Rollback](08-test-failed-requests-retry-and-rollback.md). The next chapter assumes the state created here.
