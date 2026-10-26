# 05. SSH Remote Server Setup

[← All projects](../README.md) · **Beginner** · Linux · OpenSSH

Create key-based access to a disposable Linux VM.

## Prerequisites

A disposable Ubuntu VM with a public address, a console or existing SSH login, and OpenSSH client.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

From the repository root, enter this project:

```bash
cd 05.ssh-remote-server-setup
```

Run the remaining commands here unless a step explicitly changes directories. This project uses the commands below; no starter files are required.

### 1. Create a dedicated key on your computer

```bash
ssh-keygen -t ed25519 -f ~/.ssh/devops_lab -C devops-projects
export LAB_HOST=REPLACE_WITH_VM_ADDRESS
export LAB_USER=ubuntu
```

Choose a passphrase. Confirm the server host-key fingerprint through the provider console before accepting it.

### 2. Install the public key

```bash
ssh-copy-id -i ~/.ssh/devops_lab.pub "$LAB_USER@$LAB_HOST"
ssh -i ~/.ssh/devops_lab "$LAB_USER@$LAB_HOST"
```

If the image accepts only a provider key, use that existing login to append the contents of `devops_lab.pub` to `~/.ssh/authorized_keys`; never copy the private key. Set `.ssh` mode 700 and `authorized_keys` mode 600.

### 3. Harden authentication — on the VM

Keep this session open:

```bash
printf 'PasswordAuthentication no\nPermitRootLogin no\n' | sudo tee /etc/ssh/sshd_config.d/00-devops-lab.conf
sudo sshd -t
sudo systemctl reload ssh
sudo sshd -T | grep -E 'passwordauthentication|permitrootlogin'
```

In a second local terminal, repeat the key login. Close the original session only after it succeeds.

## Verify completion

The second connection works. Effective config says `passwordauthentication no` and `permitrootlogin no`.

## Troubleshooting

Use the provider console if locked out. Ubuntu cloud images can already disable passwords; ssh-copy-id requires an existing way to authenticate.

## Cleanup

Delete the VM. Remove only the dedicated `~/.ssh/devops_lab` and `.pub` files after you no longer need them.

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented ssh remote server setup in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://www.openssh.com/manual.html)

---

[← Previous: 04](../04.github-pages-deployment/README.md) · [All projects](../README.md) · [Next: 06 →](../06.static-site-server/README.md)
