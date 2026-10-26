# 06. Enforce Naming Input and Access Rules

[← 05. Produce the Service Deployment Configuration](05-produce-the-service-deployment-configuration.md) · [Project home](README.md) · [07. Run a Complete Developer Onboarding Journey →](07-run-a-complete-developer-onboarding-journey.md)

## Starting state and working directory

Complete chapter 05 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `07.developer-self-service-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 07.developer-self-service-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A platform contract must reject requests it cannot safely fulfill. Exercise invalid input, unknown ownership and duplicates, then explain which layer actually controls access. The allowlist prevents arbitrary ownership labels but does not prevent another local OS user with filesystem access from modifying it. CI and GitHub repository permissions remain separate from generator validation.

## Work through the implementation

In your design notes identify the caller identity, permitted teams, allowed templates, registry rights and cluster privileges that a real hosted portal would enforce. This CLI runs under the user’s existing access and does not implement those identity systems. A good interview explanation states that boundary rather than equating a JSON allowlist with enterprise authorization.

### Commands in execution order

```bash
python3 automation/generate.py ../../escape --team payments
python3 automation/generate.py payments-api --team unknown
python3 automation/generate.py orders-api --team payments
# All three commands above should fail without replacing a service.
python3 -m unittest discover -s automation -v
```

## Checkpoint — verify before continuing

Each invalid request exits nonzero and the valid existing service remains runnable. Compare its health and Git diff after the negative tests.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If a validation failure creates a final service directory, fix the validation order before claiming atomic generation. A dry-run may create the destination parent, but it must not publish the named service.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [07. Run a Complete Developer Onboarding Journey](07-run-a-complete-developer-onboarding-journey.md). The next chapter assumes the state created here.
