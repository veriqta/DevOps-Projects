# Run the checks

[← Projects](README.md) · [Environment setup](SETUP.md)

## Scripts and applications

```bash
python3 -m unittest discover -s 04.tests -v
node --check 02.examples/app/server.js
node 04.tests/test_timer.cjs
bash -n 03.tools/deploy-node.sh 03.tools/backup-db.sh 04.tests/container-smoke.sh
```

The tests exercise archives, malformed log lines, integrity-check exit codes, backup success/failure through a fake Docker command, real HTTP requests, durable job recovery after an API restart, and timer controls with a simulated clock. The backup mocks validate error handling; they do not prove a PostgreSQL restore. The Linux stats test runs only on Linux.

## Containers

On a disposable Docker host with Compose v2, curl and Python:

```bash
bash 04.tests/container-smoke.sh
```

This builds and starts the supplied stacks sequentially, checks HTTP, dumps/restores PostgreSQL, validates Prometheus configuration, processes a durable job, checks Consul health filtering and switches blue → green → blue. It removes its named lab containers and volumes on exit. Do not use it against existing lab data you want to keep.

## Terraform

```bash
terraform fmt -check -recursive 02.examples
terraform -chdir=02.examples/terraform-digitalocean init -backend=false
terraform -chdir=02.examples/terraform-digitalocean validate
terraform -chdir=02.examples/terraform-cost init -backend=false
terraform -chdir=02.examples/terraform-cost validate
```

These checks require provider downloads but do not create resources. An infrastructure apply and destroy must be verified separately in your own account.

## Ansible and Kubernetes

```bash
ansible-playbook -i 02.examples/inventory.ini 02.examples/nginx.yml --syntax-check
kubectl kustomize 02.examples/kustomize/overlays/lab
```

Project 13 verifies real Ansible idempotence on your VM. Project 27 verifies a real Kubernetes rollout. The included GitHub Actions workflow executes unit, container, Terraform and kind checks on a writable repository after you push it. A workflow file is not evidence that it has already passed.
