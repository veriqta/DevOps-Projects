# 06. Static Site Server

[← All projects](../README.md) · **Beginner** · Linux · Nginx

Serve a static site from a disposable Ubuntu VM.

## Prerequisites

A disposable Ubuntu VM, SSH access (project 05), and inbound TCP 80 permitted for the lab.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

From the repository root, enter this project:

```bash
cd 06.static-site-server
```

Run the remaining commands here unless a step explicitly changes directories. This project uses the commands below; no starter files are required.

### 1. Install and configure — on the VM

```bash
sudo apt-get update
sudo apt-get install -y nginx
printf '<h1>DevOps Projects</h1>\n' | sudo tee /var/www/html/index.html
sudo nginx -t
sudo systemctl enable --now nginx
curl -fsS http://127.0.0.1
```

### 2. Test from your computer

```bash
export LAB_HOST=REPLACE_WITH_VM_ADDRESS
curl -f "http://$LAB_HOST"
```

If using UFW, allow TCP 80 on the VM with `sudo ufw allow 80/tcp`. Also allow it in the cloud firewall/security group.

### 3. Read the request logs — on the VM

```bash
sudo tail -n 10 /var/log/nginx/access.log
sudo tail -n 10 /var/log/nginx/error.log
```

## Verify completion

The response contains DevOps Projects. A new access-log entry appears for your external request.

## Troubleshooting

Local success plus remote timeout usually means the cloud firewall or UFW blocks port 80. Use `sudo ss -ltnp` to check the listener.

## Cleanup

Delete the disposable VM and its lab security-group/firewall rules.

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented static site server in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://nginx.org/en/docs/beginners_guide.html)

---

[← Previous: 05](../05.ssh-remote-server-setup/README.md) · [All projects](../README.md) · [Next: 07 →](../07.basic-dns-setup/README.md)
