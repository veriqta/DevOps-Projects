# 14. IaC on DigitalOcean

[← All projects](../README.md) · **Intermediate** · Terraform · DigitalOcean

Provision one tagged Droplet with a declared SSH key.

## Prerequisites

Terraform, DigitalOcean account with billing, API token scoped to create/delete lab Droplets, and an uploaded SSH public key.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Files included

Everything below is inside this project’s `files/` folder.

| File or folder | Use |
| --- | --- |
| `terraform-digitalocean` | Configuration used by this project. |

## Walkthrough

From the repository root, enter this project:

```bash
cd 14.iac-on-digitalocean
```

Run the remaining commands here unless a step explicitly changes directories. The `files/` folder contains the supplied code and configurations for this project.

### 1. Set private inputs

```bash
read -rsp 'DigitalOcean token: ' TF_VAR_do_token; echo
export TF_VAR_do_token
export TF_VAR_ssh_key_fingerprint=REPLACE_WITH_UPLOADED_KEY_FINGERPRINT
cd files/terraform-digitalocean
terraform init
terraform fmt -check
terraform validate
```

The key fingerprint is available under DigitalOcean Settings → Security → SSH keys. The lab defaults are nyc3, Ubuntu 24.04 and s-1vcpu-1gb; confirm availability and pricing before applying.

### 2. Review and provision

```bash
terraform plan -out=lab.plan
terraform apply lab.plan
terraform output address
terraform plan
```

The Droplet is publicly addressed. Before using it beyond this lab, create a provider firewall permitting SSH from your own address only. Do not run unrelated workloads on it.

### 3. Connect

```bash
ssh -i ~/.ssh/devops_lab root@"$(terraform output -raw address)"
```

## Verify completion

The address matches the console, SSH succeeds and the second plan says No changes. Keep the generated provider lock file; do not commit state or the saved plan.

## Troubleshooting

If apply partially fails, inspect terraform state list and the console, then destroy tracked resources. Do not delete state before cleanup.

## Cleanup

```bash
terraform destroy
# Confirm destruction in the console before deleting local state.
rm -f lab.plan terraform.tfstate terraform.tfstate.backup
unset TF_VAR_do_token TF_VAR_ssh_key_fingerprint
```

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented iac on digitalocean in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://registry.terraform.io/providers/digitalocean/digitalocean/latest/docs/resources/droplet)

---

[← Previous: 13](../13.configuration-management/README.md) · [All projects](../README.md) · [Next: 15 →](../15.node-js-service-deployment/README.md)
