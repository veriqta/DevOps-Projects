# 09. Dummy Systemd Service

[← All projects](../README.md) · **Beginner** · Linux · systemd

Run a restartable background process with logs in the journal.

## Prerequisites

A disposable Ubuntu VM with systemd; clone or copy this repository onto that VM.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Files included

Everything below is inside this project’s `files/` folder.

| File or folder | Use |
| --- | --- |
| `devops-demo.service` | Configuration or starter code referenced in the steps below. |

## Walkthrough

From the repository root, enter this project:

```bash
cd 09.dummy-systemd-service
```

Run the remaining commands here unless a step explicitly changes directories. The `files/` folder contains the supplied code and configurations for this project.

### 1. Install the supplied unit — on the VM, in this project folder

```bash
sudo cp files/devops-demo.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now devops-demo
systemctl is-active devops-demo
journalctl -u devops-demo -n 10 --no-pager
```

### 2. Prove automatic restart

```bash
OLD_PID=$(systemctl show devops-demo -p MainPID --value)
sudo systemctl kill --kill-whom=all --signal=SIGKILL devops-demo
sleep 4
NEW_PID=$(systemctl show devops-demo -p MainPID --value)
printf 'old=%s new=%s\n' "$OLD_PID" "$NEW_PID"
systemctl is-active devops-demo
```

## Verify completion

Expect `active`, a new nonzero PID and timestamp messages in the journal. Logs are managed by journald rather than an unbounded custom log file.

## Troubleshooting

`System has not been booted with systemd` means this is a container or unsupported environment; use a full VM.

## Cleanup

```bash
sudo systemctl disable --now devops-demo
sudo rm /etc/systemd/system/devops-demo.service
sudo systemctl daemon-reload
```

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented dummy systemd service in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html)

---

[← Previous: 08](../08.simple-monitoring/README.md) · [All projects](../README.md) · [Next: 10 →](../10.basic-dockerfile/README.md)
