# 00. Developer Request and Platform Contract

[Project home](README.md) · [01. Run the Platform Locally →](01-run-the-platform-locally.md)

## Starting state and working directory

Read the project README and have a terminal open at the repository root.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `07.developer-self-service-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 07.developer-self-service-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Self-service means the developer supplies a small, validated request and receives a useful outcome without editing a dozen platform files. It does not mean hiding all implementation details. The service contract here includes an owner, health response, behavioral test, Docker image definition, CI and Kubernetes deployment. A generated folder alone is not success; the service must run and its tests must execute.

## Work through the implementation

Record a manual setup baseline if you want to compare onboarding time. Use the same service requirements for both approaches. A single-person local test does not establish a company-wide productivity gain, but it can demonstrate a repeatable developer workflow and its error handling.

### Commands in execution order

```bash
find portal automation template -maxdepth 4 -type f | sort
```

## Checkpoint — verify before continuing

List the request inputs and generated outputs. Define the successful onboarding checkpoint as tests plus a working health response, not merely generator exit 0.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If a proposed template needs manual edits before it can start, those inputs belong in the request contract or must be explicit later deployment values.

## What to record

Save the architecture and acceptance criteria in your own notes. You will compare the finished system with this contract in chapter 09.

## Continue

When this checkpoint passes, continue to [01. Run the Platform Locally](01-run-the-platform-locally.md). The next chapter assumes the state created here.
