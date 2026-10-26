# 21. Linux Server Setup

[← All projects](../../README.md) · **Intermediate** · Ubuntu · Linux

Prepare a disposable server with a non-root user, updates and a restrictive firewall.

## Prerequisites

Disposable Ubuntu VM with console access and an initial sudo-capable SSH user.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Update and create a user — on the VM

```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo adduser devops
sudo usermod -aG sudo devops
sudo install -d -m 700 -o devops -g devops /home/devops/.ssh
sudo cp ~/.ssh/authorized_keys /home/devops/.ssh/authorized_keys
sudo chown devops:devops /home/devops/.ssh/authorized_keys
sudo chmod 600 /home/devops/.ssh/authorized_keys
```

From a second local terminal, log in as devops using the lab key and run `sudo -v`. Keep the original session until this succeeds.

### 2. Enable the host firewall — on the VM

```bash
sudo apt-get install -y ufw unattended-upgrades
sudo ufw allow OpenSSH
sudo ufw --force enable
sudo ufw status verbose
sudo dpkg-reconfigure -plow unattended-upgrades
sudo ss -tulpn
```

Choose Yes for automatic security updates. Before exposing a web service, explicitly allow its port.

### 3. Reboot and verify access

```bash
sudo reboot
```

Reconnect after the VM restarts. Inspect `systemctl --failed`, `uptime` and `sudo ufw status`. Apply project 05 authentication settings only after the new user works.

## Verify completion

The devops account can log in and use sudo, SSH survives reboot, and only intended inbound ports are allowed.

## Troubleshooting

If UFW blocks access, use the provider console to inspect rules. Do not close your working connection until a second login succeeds.

## Cleanup

Destroy the VM; verify provider disks/public IP allocations were removed.

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://documentation.ubuntu.com/server/how-to/security/)

---

[← Previous: 20](../20.file-integrity-checker/README.md) · [All projects](../../README.md) · [Next: 22 →](../22.vpn-server-setup/README.md)
