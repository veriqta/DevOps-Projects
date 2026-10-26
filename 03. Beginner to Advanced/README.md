# DevOps Projects

**Build, ship, operate, and recover real systems.**

A follow-along path from your first Linux script to a complete DevOps portfolio.

[Beginner](#beginner) · [Intermediate](#intermediate) · [Advanced](#advanced) · [Getting started](#getting-started) · [Portfolio checklist](#portfolio-checklist)

## Start here

1. Read [Environment setup](SETUP.md).
2. Begin with [01. Server Performance Stats](01.server-performance-stats/README.md).
3. Continue through the numbered project folders. Each folder is one complete lab: open its README, enter that folder, run the steps, verify, clean up, and save your portfolio evidence. The supplied files stay beside their guide.

You do not need to visit separate examples, tools or test folders. A project only depends on another lab when its prerequisites explicitly say so.

## Getting started

Download this repository as a ZIP and extract it, or use a writable copy in your own account. Open a terminal at the repository root and run:

```bash
cd 01.server-performance-stats
python3 files/server_stats.py
```

Publishing exercises require a writable GitHub repository in your own account.

Start with project 01 on Linux or an Ubuntu VM. Each guide tells you which folder to enter, what tools you need, the exact steps, expected results, troubleshooting and cleanup. Uppercase placeholders require your own values.

Use Linux or a disposable Ubuntu VM for host administration. Local container labs need Docker Engine and Compose v2; Kubernetes labs also need kind and kubectl. Cloud projects need your own account and incur provider charges. Create a budget alert before provisioning and follow each cleanup section.

Each numbered folder contains its own walkthrough and the files used by that walkthrough. Optional extensions are labeled separately.

[Environment setup](SETUP.md)

## Beginner

| Project | Build with | Outcome |
| --- | --- | --- |
| [01. Server Performance Stats](01.server-performance-stats/README.md) | Linux · Python | Measure CPU load, memory, disk usage, and the busiest processes. |
| [02. Log Archive Tool](02.log-archive-tool/README.md) | CLI · Python | Create timestamped compressed archives without deleting source logs. |
| [03. Nginx Log Analyser](03.nginx-log-analyser/README.md) | Nginx · Python | Summarize status codes, client addresses, and requested paths in an access log. |
| [04. GitHub Pages Deployment](04.github-pages-deployment/README.md) | GitHub Actions | Deploy a small static site through an auditable workflow. |
| [05. SSH Remote Server Setup](05.ssh-remote-server-setup/README.md) | Linux · OpenSSH | Create key-based access to a disposable Linux VM. |
| [06. Static Site Server](06.static-site-server/README.md) | Linux · Nginx | Serve a static site from a disposable Ubuntu VM. |
| [07. Basic DNS Setup](07.basic-dns-setup/README.md) | DNS · dig | Map a lab subdomain to a server and inspect authoritative answers. |
| [08. Simple Monitoring](08.simple-monitoring/README.md) | Netdata | Observe a disposable VM and explain a change in its metrics. |
| [09. Dummy Systemd Service](09.dummy-systemd-service/README.md) | Linux · systemd | Run a restartable background process with logs in the journal. |
| [10. Basic Dockerfile](10.basic-dockerfile/README.md) | Docker | Package the demo HTTP service in an unprivileged container. |
| [11. EC2 Instance](11.ec2-instance/README.md) | AWS · SSH | Launch and inspect a disposable Linux instance. |

## Intermediate

| Project | Build with | Outcome |
| --- | --- | --- |
| [12. Pomodoro Timer](12.pomodoro-timer/README.md) | HTTP · Docker | Turn a small timer into a deployable, observable static application. |
| [13. Configuration Management](13.configuration-management/README.md) | Ansible | Idempotently install and configure Nginx on a disposable Ubuntu VM. |
| [14. IaC on DigitalOcean](14.iac-on-digitalocean/README.md) | Terraform · DigitalOcean | Provision one tagged Droplet with a declared SSH key. |
| [15. Node.js Service Deployment](15.node-js-service-deployment/README.md) | Node.js · GitHub Actions · SSH | Deploy the dependency-free service to a disposable VM through a release directory. |
| [16. Dockerized Service](16.dockerized-service/README.md) | Docker · GitHub Actions | Build and publish a versioned image and deploy it to a lab server. |
| [17. Multi-Container Application](17.multi-container-application/README.md) | Docker Compose · PostgreSQL | Operate an HTTP service and database with health checks and persistent storage. |
| [18. Automated DB Backups](18.automated-db-backups/README.md) | PostgreSQL · cron | Back up a lab database every 12 hours and prove restoration. |
| [19. Bastion Host](19.bastion-host/README.md) | SSH · Networking | Reach a private VM through a dedicated jump host. |
| [20. File Integrity Checker](20.file-integrity-checker/README.md) | Python · SHA-256 | Detect modified, missing and unexpected files against a baseline. |
| [21. Linux Server Setup](21.linux-server-setup/README.md) | Ubuntu · Linux | Prepare a disposable server with a non-root user, updates and a restrictive firewall. |
| [22. VPN Server Setup](22.vpn-server-setup/README.md) | WireGuard | Connect a client to a disposable private lab network. |
| [27. Local Kubernetes Operations](27.local-kubernetes-operations/README.md) | kind · kubectl · Kustomize | Deploy the demo to a local cluster and debug a failed rollout. |

## Advanced

| Project | Build with | Outcome |
| --- | --- | --- |
| [23. Blue-Green Deployment](23.blue-green-deployment/README.md) | Nginx · Docker | Switch traffic between two healthy application releases and roll back. |
| [24. Prometheus and Grafana](24.prometheus-and-grafana/README.md) | Prometheus · Grafana | Scrape the demo service and graph request counts. |
| [25. Multi-Service Application](25.multi-service-application/README.md) | Containers · Architecture | Build a gateway, API and worker with separate health and failure boundaries. |
| [26. Service Discovery](26.service-discovery/README.md) | Consul | Register a service and observe health-based discovery. |
| [28. GitOps Delivery](28.gitops-delivery/README.md) | Flux · Kubernetes | Reconcile a lab deployment from your own Git repository. |
| [29. Supply Chain Security](29.supply-chain-security/README.md) | Syft · Grype · Cosign | Produce an SBOM, evaluate vulnerabilities and verify an image signature. |
| [30. Load Testing and Resilience](30.load-testing-and-resilience/README.md) | k6 · Chaos Mesh | Measure latency under load and recovery after a controlled failure. |
| [31. Backup and Recovery Drill](31.backup-and-recovery-drill/README.md) | Restic · PostgreSQL · Velero | Prove recovery with a timed restore and a measurable recovery point. |
| [32. Cloud Secrets Integration](32.cloud-secrets-integration/README.md) | AWS · Azure · Google Cloud | Retrieve a lab secret at runtime using workload identity. |
| [33. Cloud Cost Management](33.cloud-cost-management/README.md) | Infracost · OpenCost | Estimate infrastructure changes and attribute local cluster costs. |
| [34. Production Readiness Capstone](34.production-readiness-capstone/README.md) | SRE · CI/CD · Kubernetes | Combine delivery, observability, security and recovery into one demonstrable system. |

## Suggested paths

- **Linux foundations:** 01 → 02 → 03 → 05 → 06 → 09 → 21.
- **Delivery engineer:** 04 → 10 → 12 → 15 → 16 → 17 → 23.
- **Cloud engineer:** 07 → 11 → 13 → 14 → 19 → 22 → 32 → 33.
- **Platform / SRE:** 08 → 18 → 24 → 25 → 26 → 27 → 28 → 29 → 30 → 31 → 34.

## Turn a completed lab into résumé evidence

1. Run every completion check and record what you actually observed.
2. Save a diagram, configuration, test output, failure diagnosis and recovery proof in your own repository.
3. Record a short demo and explain one design tradeoff.
4. Adapt the résumé bullet at the end of the guide with your measured results. Label the work as a lab or portfolio project.

## Portfolio checklist

For each completed project, add your architecture diagram, reproducible commands, test output, a failure you diagnosed, rollback or recovery evidence, and a short explanation of your design choices. Include a screenshot or short demo video, but remove tokens, private keys, account identifiers and personal data.

[Completion log](PROGRESS.md) · [Contributing](CONTRIBUTING.md) · [License](LICENSE)

Project titles overlap with common DevOps exercises, including the [roadmap.sh DevOps projects collection](https://roadmap.sh/devops/projects). The walkthroughs and supplied starter code here are original. This repository is independent of roadmap.sh.
