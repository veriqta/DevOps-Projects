# 08. Simple Monitoring

[← All projects](../README.md) · **Beginner** · Netdata

Observe a disposable VM and explain a change in its metrics.

## Prerequisites

Docker and a web browser. The minimal container shows container metrics, not all host metrics.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

From the repository root, enter this project:

```bash
cd 08.simple-monitoring
```

Run the remaining commands here unless a step explicitly changes directories. This project uses the commands below; no starter files are required.

### 1. Start Netdata locally

```bash
docker run -d --name netdata-lab -p 127.0.0.1:19999:19999 netdata/netdata:stable
curl -I http://127.0.0.1:19999
```

Open `http://127.0.0.1:19999` and use the local dashboard; no cloud signup is required for this lab. Find CPU and memory charts.

### 2. Generate load in the monitored container

```bash
docker exec -d netdata-lab sh -c 'end=$(( $(date +%s) + 15 )); while [ "$(date +%s)" -lt "$end" ]; do :; done'
docker stats --no-stream netdata-lab
```

Watch the charts during and after the 15-second workload. Compare with `docker stats`.

### 3. Inspect logs

```bash
docker logs --tail 30 netdata-lab
```

## Verify completion

The dashboard loads, the CPU chart changes during the workload and settles afterward. Document the visibility limits of running without host mounts.

## Troubleshooting

If the dashboard is blank, inspect logs and wait for initialization. Avoid adding host privileges just to make extra charts appear.

## Cleanup

`docker rm -f netdata-lab`

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented simple monitoring in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://learn.netdata.cloud/docs/netdata-agent/installation/docker)

---

[← Previous: 07](../07.basic-dns-setup/README.md) · [All projects](../README.md) · [Next: 09 →](../09.dummy-systemd-service/README.md)
