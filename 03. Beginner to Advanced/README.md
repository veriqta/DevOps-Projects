# DevOps Projects

**Build, ship, operate, and recover real systems.**

A follow-along path from your first Linux script to a complete DevOps portfolio.

[Beginner](#beginner) · [Intermediate](#intermediate) · [Advanced](#advanced) · [Getting started](#getting-started) · [Portfolio checklist](#portfolio-checklist)

## Start here

1. Read [Environment setup](SETUP.md).
2. Begin with [01. Server Performance Stats](01.projects/01.server-performance-stats/README.md).
3. Continue through the numbered folders. Each guide links to the previous and next project. Use the suggested paths below if you want to focus on one specialty.

## Folder guide

| Folder | Purpose |
| --- | --- |
| **01.projects** | **Begin here.** Open `README.md`, then project `01.server-performance-stats`. |
| 02.examples | Application code and configurations used in the walkthroughs. |
| 03.tools | Scripts used by the projects. |
| 04.tests | Automated checks and container smoke tests. |
| 05.fixtures | Sample log files and test data. |
| 06.site | Static website for the GitHub Pages project. |

## Getting started

Download this repository as a ZIP and extract it, or use a writable copy in your own account. Open a terminal at the repository root and run:

```bash
python3 -m unittest discover -s 04.tests -v
```

Publishing exercises require a writable GitHub repository in your own account.

Start with project 01. Each guide lists its prerequisites, walkthrough, completion checks, cleanup, and extensions. Run commands from the repository root unless a guide changes directories. Commands containing uppercase placeholders require your own values.

Use Linux or a disposable Ubuntu VM for host administration. Local container labs need Docker Engine and Compose v2; Kubernetes labs also need kind and kubectl. Cloud projects need your own account and incur provider charges. Create a budget alert before provisioning and follow each cleanup section.

The `02.examples/` directory contains the configurations and code used by the walkthroughs. Each project has a complete core path; optional provider and scaling extensions are labeled separately.

[Environment setup](SETUP.md) · [Run the checks](TESTING.md)

## Beginner

| Project | Build with | Outcome |
| --- | --- | --- |
| [01. Server Performance Stats](01.projects/01.server-performance-stats/README.md) | Linux · Python | Measure CPU load, memory, disk usage, and the busiest processes. |
| [02. Log Archive Tool](01.projects/02.log-archive-tool/README.md) | CLI · Python | Create timestamped compressed archives without deleting source logs. |
| [03. Nginx Log Analyser](01.projects/03.nginx-log-analyser/README.md) | Nginx · Python | Summarize status codes, client addresses, and requested paths in an access log. |
| [04. GitHub Pages Deployment](01.projects/04.github-pages-deployment/README.md) | GitHub Actions | Deploy a small static site through an auditable workflow. |
| [05. SSH Remote Server Setup](01.projects/05.ssh-remote-server-setup/README.md) | Linux · OpenSSH | Create key-based access to a disposable Linux VM. |
| [06. Static Site Server](01.projects/06.static-site-server/README.md) | Linux · Nginx | Serve a static site from a disposable Ubuntu VM. |
| [07. Basic DNS Setup](01.projects/07.basic-dns-setup/README.md) | DNS · dig | Map a lab subdomain to a server and inspect authoritative answers. |
| [08. Simple Monitoring](01.projects/08.simple-monitoring/README.md) | Netdata | Observe a disposable VM and explain a change in its metrics. |
| [09. Dummy Systemd Service](01.projects/09.dummy-systemd-service/README.md) | Linux · systemd | Run a restartable background process with logs in the journal. |
| [10. Basic Dockerfile](01.projects/10.basic-dockerfile/README.md) | Docker | Package the demo HTTP service in an unprivileged container. |
| [11. EC2 Instance](01.projects/11.ec2-instance/README.md) | AWS · SSH | Launch and inspect a disposable Linux instance. |

## Intermediate

| Project | Build with | Outcome |
| --- | --- | --- |
| [12. Pomodoro Timer](01.projects/12.pomodoro-timer/README.md) | HTTP · Docker | Turn a small timer into a deployable, observable static application. |
| [13. Configuration Management](01.projects/13.configuration-management/README.md) | Ansible | Idempotently install and configure Nginx on a disposable Ubuntu VM. |
| [14. IaC on DigitalOcean](01.projects/14.iac-on-digitalocean/README.md) | Terraform · DigitalOcean | Provision one tagged Droplet with a declared SSH key. |
| [15. Node.js Service Deployment](01.projects/15.node-js-service-deployment/README.md) | Node.js · GitHub Actions · SSH | Deploy the dependency-free service to a disposable VM through a release directory. |
| [16. Dockerized Service](01.projects/16.dockerized-service/README.md) | Docker · GitHub Actions | Build and publish a versioned image and deploy it to a lab server. |
| [17. Multi-Container Application](01.projects/17.multi-container-application/README.md) | Docker Compose · PostgreSQL | Operate an HTTP service and database with health checks and persistent storage. |
| [18. Automated DB Backups](01.projects/18.automated-db-backups/README.md) | PostgreSQL · cron | Back up a lab database every 12 hours and prove restoration. |
| [19. Bastion Host](01.projects/19.bastion-host/README.md) | SSH · Networking | Reach a private VM through a dedicated jump host. |
| [20. File Integrity Checker](01.projects/20.file-integrity-checker/README.md) | Python · SHA-256 | Detect modified, missing and unexpected files against a baseline. |
| [21. Linux Server Setup](01.projects/21.linux-server-setup/README.md) | Ubuntu · Linux | Prepare a disposable server with a non-root user, updates and a restrictive firewall. |
| [22. VPN Server Setup](01.projects/22.vpn-server-setup/README.md) | WireGuard | Connect a client to a disposable private lab network. |
| [27. Local Kubernetes Operations](01.projects/27.local-kubernetes-operations/README.md) | kind · kubectl · Kustomize | Deploy the demo to a local cluster and debug a failed rollout. |

## Advanced

| Project | Build with | Outcome |
| --- | --- | --- |
| [23. Blue-Green Deployment](01.projects/23.blue-green-deployment/README.md) | Nginx · Docker | Switch traffic between two healthy application releases and roll back. |
| [24. Prometheus and Grafana](01.projects/24.prometheus-and-grafana/README.md) | Prometheus · Grafana | Scrape the demo service and graph request counts. |
| [25. Multi-Service Application](01.projects/25.multi-service-application/README.md) | Containers · Architecture | Build a gateway, API and worker with separate health and failure boundaries. |
| [26. Service Discovery](01.projects/26.service-discovery/README.md) | Consul | Register a service and observe health-based discovery. |
| [28. GitOps Delivery](01.projects/28.gitops-delivery/README.md) | Flux · Kubernetes | Reconcile a lab deployment from your own Git repository. |
| [29. Supply Chain Security](01.projects/29.supply-chain-security/README.md) | Syft · Grype · Cosign | Produce an SBOM, evaluate vulnerabilities and verify an image signature. |
| [30. Load Testing and Resilience](01.projects/30.load-testing-and-resilience/README.md) | k6 · Chaos Mesh | Measure latency under load and recovery after a controlled failure. |
| [31. Backup and Recovery Drill](01.projects/31.backup-and-recovery-drill/README.md) | Restic · PostgreSQL · Velero | Prove recovery with a timed restore and a measurable recovery point. |
| [32. Cloud Secrets Integration](01.projects/32.cloud-secrets-integration/README.md) | AWS · Azure · Google Cloud | Retrieve a lab secret at runtime using workload identity. |
| [33. Cloud Cost Management](01.projects/33.cloud-cost-management/README.md) | Infracost · OpenCost | Estimate infrastructure changes and attribute local cluster costs. |
| [34. Production Readiness Capstone](01.projects/34.production-readiness-capstone/README.md) | SRE · CI/CD · Kubernetes | Combine delivery, observability, security and recovery into one demonstrable system. |

## Suggested paths

- **Linux foundations:** 01 → 02 → 03 → 05 → 06 → 09 → 21.
- **Delivery engineer:** 04 → 10 → 12 → 15 → 16 → 17 → 23.
- **Cloud engineer:** 07 → 11 → 13 → 14 → 19 → 22 → 32 → 33.
- **Platform / SRE:** 08 → 18 → 24 → 25 → 26 → 27 → 28 → 29 → 30 → 31 → 34.

## Portfolio checklist

For each completed project, add your architecture diagram, reproducible commands, test output, a failure you diagnosed, rollback or recovery evidence, and a short explanation of your design choices. Include a screenshot or short demo video, but remove tokens, private keys, account identifiers and personal data.

[Completion log](PROGRESS.md) · [Contributing](CONTRIBUTING.md) · [License](LICENSE)

Project titles overlap with common DevOps exercises, including the [roadmap.sh DevOps projects collection](https://roadmap.sh/devops/projects). The walkthroughs and supplied starter code here are original. This repository is independent of roadmap.sh.
