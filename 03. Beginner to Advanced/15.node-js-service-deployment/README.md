# 15. Node.js Service Deployment

[← All projects](../README.md) · **Intermediate** · Node.js · GitHub Actions · SSH

Deploy the dependency-free service to a disposable VM through a release directory.

## Prerequisites

Project 05, disposable Ubuntu VM, Node.js installed on it, and a writable GitHub repository.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Files included

Everything below is inside this project’s `files/` folder.

| File or folder | Use |
| --- | --- |
| `app` | Demo HTTP service, Dockerfile and service unit. |
| `deploy-node.sh` | Activates a release with health checking and rollback. |
| `deploy-node.yml` | Configuration or starter code referenced in the steps below. |

## Walkthrough

From the repository root, enter this project:

```bash
cd 15.node-js-service-deployment
```

Run the remaining commands here unless a step explicitly changes directories. The `files/` folder contains the supplied code and configurations for this project.

### 1. Prepare the service account — on the VM

Clone/copy this repository onto the VM, enter `15.node-js-service-deployment`, then run:

```bash
sudo apt-get update
sudo apt-get install -y nodejs curl
sudo useradd --system --home /opt/devops-app --shell /usr/sbin/nologin devops-app
sudo mkdir -p /opt/devops-app/releases
sudo chown -R "$USER":devops-app /opt/devops-app
sudo chmod 755 /opt/devops-app /opt/devops-app/releases
sudo cp files/app/devops-app.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable devops-app
bash files/deploy-node.sh
curl -fsS http://127.0.0.1:8080/health
```

The script uses GNU mv and systemd, so run it on Ubuntu. It writes a release, checks JavaScript syntax, switches the current symlink, restarts and checks health. A failed activation restores the previous symlink.

### 2. Permit the dedicated deployment user to restart only this service

Still on the VM, replace the username below with your SSH login. Open `sudo visudo -f /etc/sudoers.d/devops-deploy` and add:

```text
YOUR_LAB_USER ALL=(root) NOPASSWD: /usr/bin/systemctl restart devops-app
```

Validate with `sudo visudo -cf /etc/sudoers.d/devops-deploy`. This deployment user can replace application code, so use a dedicated lab VM.

### 3. Configure GitHub deployment

On your computer, create a dedicated deployment key and authorize its public key for that VM user. Verify the VM host fingerprint through the provider console; then obtain its known_hosts line with `ssh-keyscan -H "$LAB_HOST"` and compare the fingerprint with `ssh-keygen -lf` before trusting it.

In your writable repository → Settings → Environments create `lab-server`. Add environment secrets `LAB_HOST`, `LAB_USER`, `SSH_KEY` (dedicated private key), and `SSH_KNOWN_HOSTS` (verified host entry).

```bash
mkdir -p ../.github/workflows
cp files/deploy-node.yml ../.github/workflows/deploy-node.yml
git add ../.github/workflows/deploy-node.yml
git commit -m "Add lab Node deployment"
git push
```

Open Actions → Deploy Node lab → Run workflow.

### 4. Prove rollback — on the VM

```bash
GOOD=$(readlink /opt/devops-app/current)
cp files/app/server.js /tmp/devops-good.js
printf 'throw new Error("lab failure");\n' > files/app/server.js
bash files/deploy-node.sh
# The previous command must exit nonzero after restoring the healthy release.
cp /tmp/devops-good.js files/app/server.js
test "$(readlink /opt/devops-app/current)" = "$GOOD"
curl -fsS http://127.0.0.1:8080/health
```

## Verify completion

The manual and Actions deployments pass. The deliberate runtime failure returns a nonzero exit code and leaves the old healthy release active.

## Troubleshooting

The service listens on VM loopback. Test through SSH or use `ssh -L 8080:127.0.0.1:8080 user@host`; a public curl is expected to fail until you add a reverse proxy.

## Cleanup

Disable/remove the workflow and revoke its key/secrets. On the VM disable devops-app, remove its unit and sudoers entry, then destroy the disposable VM.

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented node js service deployment in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)

---

[← Previous: 14](../14.iac-on-digitalocean/README.md) · [All projects](../README.md) · [Next: 16 →](../16.dockerized-service/README.md)
