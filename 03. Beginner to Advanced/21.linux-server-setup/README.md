# 21. Linux Server Setup

[← All projects](../README.md) · **Intermediate** · Ubuntu · Linux

Prepare a disposable server with a non-root user, updates and a restrictive firewall.

## Prerequisites

Disposable Ubuntu VM with console access and an initial sudo-capable SSH user.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

From the repository root, enter this project:

```bash
cd 21.linux-server-setup
```

Run the remaining commands here unless a step explicitly changes directories. This project uses the commands below; no starter files are required.

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

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented linux server setup in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://documentation.ubuntu.com/server/how-to/security/)

---

[← Previous: 20](../20.file-integrity-checker/README.md) · [All projects](../README.md) · [Next: 22 →](../22.vpn-server-setup/README.md)
