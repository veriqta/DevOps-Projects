# 00. Business Scenario and Architecture

[Project home](README.md) · [01. Prepare the Workstation and Repository →](01-prepare-the-workstation-and-repository.md)

## Starting state and working directory

Read the project README and have a terminal open at the repository root.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `01.production-delivery-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 01.production-delivery-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A deployment is a change to a running service, not just a successful build. Separate artifact identity from environment identity: one digest should move between staging and the production-like lab. The two environments use distinct Docker networks and proxies, so a staging switch cannot accidentally redirect the production proxy. They share one lab host to control cost; that is not host-level fault isolation. The Orders API stores demonstration orders in memory, so it is deliberately stateless for release exercises and unsuitable as an order database. Project 06 addresses persistent data recovery.

## Work through the implementation

Define the release contract in your notes: valid checkouts return HTTP 201; health returns 200; a candidate returning 503 must never receive active traffic. Choose a reviewer for production-like promotion. A second person provides independent approval; a solo learner can leave self-review enabled and document that reduced separation. Record these lab limitations before building.

### Commands in execution order

```bash
pwd
find app deploy workflows -maxdepth 2 -type f | sort
```

## Checkpoint — verify before continuing

Identify the application, release script and three workflow files. Draw the request path from port 8081 to the active color and explain where approval occurs.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If the directories do not exist, you are at the wrong level. Enter this numbered project, rather than the repository root.

## What to record

Save the architecture and acceptance criteria in your own notes. You will compare the finished system with this contract in chapter 09.

## Continue

When this checkpoint passes, continue to [01. Prepare the Workstation and Repository](01-prepare-the-workstation-and-repository.md). The next chapter assumes the state created here.
