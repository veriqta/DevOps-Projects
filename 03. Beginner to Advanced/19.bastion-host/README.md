# 19. Bastion Host

[← All projects](../README.md) · **Intermediate** · SSH · Networking

Reach a private VM through a dedicated jump host.

## Prerequisites

AWS CLI v2, jq, a dedicated AWS lab account/profile, a key pair, and project 11. This creates two charged instances.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Files included

Everything below is inside this project’s `files/` folder.

| File or folder | Use |
| --- | --- |
| `terraform-bastion` | Configuration used by this project. |

## Walkthrough

From the repository root, enter this project:

```bash
cd 19.bastion-host
```

Run the remaining commands here unless a step explicitly changes directories. The `files/` folder contains the supplied code and configurations for this project.

### 1. Provision the isolated network and two instances

The supplied Terraform creates a VPC, public/private subnets, a bastion restricted to your /32, and a private instance accepting SSH only from the bastion security group. It creates no NAT gateway. Use a dedicated AWS account/profile and confirm pricing first.

```bash
aws sts get-caller-identity
export TF_VAR_my_ip_cidr=REPLACE_WITH_YOUR_PUBLIC_IP/32
export TF_VAR_key_name=REPLACE_WITH_AWS_KEY_PAIR_NAME
terraform -chdir=files/terraform-bastion init
terraform -chdir=files/terraform-bastion validate
terraform -chdir=files/terraform-bastion plan -out=lab.plan
terraform -chdir=files/terraform-bastion apply lab.plan
export BASTION_IP=$(terraform -chdir=files/terraform-bastion output -raw bastion_ip)
export PRIVATE_IP=$(terraform -chdir=files/terraform-bastion output -raw private_ip)
mkdir -p .lab
```

Use a key pair matching your local `~/.ssh/devops_lab` key. If not already uploaded, import its public key with `aws ec2 import-key-pair --key-name devops-lab --public-key-material fileb://$HOME/.ssh/devops_lab.pub` and set TF_VAR_key_name=devops-lab before planning. Wait for instance status checks in the console.

### 2. Connect from your computer

Add this to a dedicated SSH config file `.lab/ssh-config`, replacing both addresses with the Terraform outputs above. The config ensures the jump connection also uses the correct key:

```sshconfig
Host bastion-lab
  HostName REPLACE_WITH_PUBLIC_BASTION_IP
  User ubuntu
  IdentityFile ~/.ssh/devops_lab
  IdentitiesOnly yes
Host private-lab
  HostName REPLACE_WITH_PRIVATE_INSTANCE_IP
  User ubuntu
  IdentityFile ~/.ssh/devops_lab
  IdentitiesOnly yes
  ProxyJump bastion-lab
```

```bash
ssh -F .lab/ssh-config private-lab
```

Verify both host keys using their provider consoles when first connecting.

### 3. Check the access boundary

From your computer, `ssh -o ConnectTimeout=5 ubuntu@"$PRIVATE_IP"` should fail. Through ProxyJump, run `hostname` and `ip -brief address` and compare with the private instance in the console.

## Verify completion

Only the bastion has a public address; the private security group references the bastion security group; ProxyJump succeeds while direct internet access does not.

## Troubleshooting

If jump authentication uses the wrong key, use the supplied SSH config and `ssh -vv -F .lab/ssh-config private-lab`. Do not enable agent forwarding to fix it.

## Cleanup

Run `terraform -chdir=files/terraform-bastion destroy` with the same inputs. Confirm both instances and the VPC are gone before removing state. Delete the imported key pair only if you created it for this lab.

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented bastion host in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://man.openbsd.org/ssh_config#ProxyJump)

---

[← Previous: 18](../18.automated-db-backups/README.md) · [All projects](../README.md) · [Next: 20 →](../20.file-integrity-checker/README.md)
