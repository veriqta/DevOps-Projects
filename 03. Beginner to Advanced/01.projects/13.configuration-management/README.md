# 13. Configuration Management

[← All projects](../../README.md) · **Intermediate** · Ansible

Idempotently install and configure Nginx on a disposable Ubuntu VM.

## Prerequisites

Ansible installed using SETUP.md; disposable Ubuntu VM and working key-based SSH.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Create an inventory

```bash
mkdir -p .lab
cp 02.examples/inventory.ini .lab/inventory.ini
```

Edit `.lab/inventory.ini`: replace REPLACE_WITH_LAB_IP and set your username. If using the dedicated key, append `ansible_ssh_private_key_file=~/.ssh/devops_lab` to the host line. Connect once with SSH to verify its host key.

### 2. Inspect and apply

```bash
ansible -i .lab/inventory.ini web -m ping
ansible-playbook -i .lab/inventory.ini 02.examples/nginx.yml --check --diff
ansible-playbook -i .lab/inventory.ini 02.examples/nginx.yml
ansible-playbook -i .lab/inventory.ini 02.examples/nginx.yml
```

If your sudo configuration requires a password add `--ask-become-pass`. Dry-run on a fresh VM may report predicted changes; the real run performs installation.

### 3. Verify the page

```bash
export LAB_HOST=REPLACE_WITH_LAB_IP
curl -f "http://$LAB_HOST"
```

## Verify completion

The second apply reports changed=0. The page says Managed by Ansible. Modify the page manually on the VM, apply again and confirm Ansible restores it.

## Troubleshooting

UNREACHABLE indicates inventory/SSH issues. A sudo failure requires a sudo-capable lab user or --ask-become-pass.

## Cleanup

Delete the VM and `.lab/inventory.ini`.

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html)

---

[← Previous: 12](../12.pomodoro-timer/README.md) · [All projects](../../README.md) · [Next: 14 →](../14.iac-on-digitalocean/README.md)
