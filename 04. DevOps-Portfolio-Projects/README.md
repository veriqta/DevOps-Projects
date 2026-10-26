# DevOps Portfolio Projects

Eight substantial, step-by-step projects for building, delivering, securing and operating applications.

**Start with [01. Production Delivery Platform](01.production-delivery-platform/README.md).** Open its README, follow chapters 00–09 in order, verify each checkpoint, then complete the recovery and cleanup exercises.

Each numbered folder is a complete project. Its chapters and implementation files stay together; no shared examples folder is required. The primary command path uses a disposable Ubuntu 24.04 workstation or VM. Cloud and registry chapters require your own accounts and can incur charges.

| Project | Finished result |
| --- | --- |
| [01. Production Delivery Platform](01.production-delivery-platform/README.md) | A tested Orders API is published to GHCR, deployed to staging, promoted by digest through approval, and recovered safely after an unhealthy candidate. |
| [02. Secure Cloud Infrastructure Platform](02.secure-cloud-infrastructure/README.md) | A scoped AWS VPC with public load balancer, private application instances, native S3 state locking, separate environment keys and a tested cleanup procedure. |
| [03. Kubernetes Application Platform](03.kubernetes-application-platform/README.md) | An Orders Helm release runs in a local multi-node kind cluster, serves trusted lab HTTPS, and is reconciled from Git with a demonstrated failed rollout and recovery. |
| [04. SRE Observability and Incident Response](04.sre-observability-and-incidents/README.md) | Checkout metrics, JSON logs and OpenTelemetry traces reach local backends; a customer-error alert fires during an injected fault and resolves after recovery. |
| [05. Software Supply Chain Security](05.software-supply-chain-security/README.md) | A scan-and-sign workflow produces an SBOM and proves both successful verification and rejection; a release wrapper enforces signature and vulnerability checks before deployment. |
| [06. Database Reliability and Disaster Recovery](06.database-disaster-recovery/README.md) | A PostgreSQL 17 database produces verified physical backups and archived WAL; a separate recovery instance restores both original orders before a known delete transaction. |
| [07. Developer Self-Service Platform](07.developer-self-service-platform/README.md) | A CLI portal creates a complete named service atomically, validates team/name inputs, runs generated tests, publishes to the learner’s repository and deploys to a local cluster. |
| [08. Cloud Cost and Capacity Optimization](08.cloud-cost-and-capacity/README.md) | Repeatable load results and estimate-only Terraform inputs support a cost/performance decision, with a budget check that rejects missing or excessive estimates. |

## Build a portfolio you can explain

Complete the implementation, record the observed results, deliberately introduce the documented failure, recover, and remove the resources. Each final chapter helps turn this evidence into a demonstration and an honest résumé bullet. Fill measurements with your own results; do not claim production experience from a lab.

Start one project at a time. Local applications often use port 8080, and cloud resources remain chargeable until destroyed. Optional extensions are labeled; the core walkthrough does not depend on them.

[Contributing](CONTRIBUTING.md) · [License](LICENSE)
