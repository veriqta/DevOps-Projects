# 00. Platform Requirements and Request Flow

[Project home](README.md) · [01. Install Tools and Create the Lab Cluster →](01-install-tools-and-create-the-lab-cluster.md)

## Starting state and working directory

Read the project README and have a terminal open at the repository root.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `03.kubernetes-application-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 03.kubernetes-application-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Kubernetes separates desired state from individual processes. A Deployment maintains replicas, a Service selects ready endpoints, and the TLS gateway terminates the client connection before forwarding HTTP inside the isolated lab cluster. Helm renders application resources; Flux later owns their reconciliation. Mixing manual Helm changes with a GitOps owner creates competing control loops, so the guide explicitly hands ownership over.

## Work through the implementation

The completion contract includes behavior, not just Running pods: HTTPS validates, checkout returns 201, a failed release does not become ready, and the Git reconciliation restores the desired configuration. A lab-only Kubernetes Secret demonstrates runtime injection; it is not a complete cloud secret-management system. Keep its value out of Git.

### Commands in execution order

```bash
find app platform chart gitops -maxdepth 3 -type f | sort
```

## Checkpoint — verify before continuing

Explain the browser → TLS gateway → Service → pod path and the independent Git → Flux → Helm control path. Identify which parts remain single points of failure in this local lab.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

A multi-node kind cluster still shares the Docker host. Do not label it multi-host high availability in a portfolio report.

## What to record

Save the architecture and acceptance criteria in your own notes. You will compare the finished system with this contract in chapter 09.

## Continue

When this checkpoint passes, continue to [01. Install Tools and Create the Lab Cluster](01-install-tools-and-create-the-lab-cluster.md). The next chapter assumes the state created here.
