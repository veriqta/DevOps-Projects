# 10. Basic Dockerfile

[← All projects](../README.md) · **Beginner** · Docker

Package the demo HTTP service in an unprivileged container.

## Prerequisites

Docker. Port 8080 must be available.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Files included

Everything below is inside this project’s `files/` folder.

| File or folder | Use |
| --- | --- |
| `app` | Demo HTTP service, Dockerfile and service unit. |

## Walkthrough

From the repository root, enter this project:

```bash
cd 10.basic-dockerfile
```

Run the remaining commands here unless a step explicitly changes directories. The `files/` folder contains the supplied code and configurations for this project.

### 1. Build and run

```bash
docker build -t devops-demo:lab files/app
docker run -d --name demo-lab -p 127.0.0.1:8080:8080 devops-demo:lab
curl -fsS http://127.0.0.1:8080/health
```

### 2. Inspect the container

```bash
docker exec demo-lab id
docker inspect --format '{{.Config.User}}' demo-lab
docker logs demo-lab
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8080/missing
```

### 3. Change the version

```bash
docker rm -f demo-lab
docker run -d --name demo-lab -e VERSION=v2 -p 127.0.0.1:8080:8080 devops-demo:lab
curl -fsS http://127.0.0.1:8080/health
```

## Verify completion

Health returns status ok, version changes to v2, missing routes return 404, and the process user is node rather than root.

## Troubleshooting

If Docker cannot connect, start its daemon/Desktop. An occupied port requires stopping the previous lab first.

## Cleanup

```bash
docker rm -f demo-lab
docker image rm devops-demo:lab
```

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented basic dockerfile in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://docs.docker.com/build/concepts/dockerfile/)

---

[← Previous: 09](../09.dummy-systemd-service/README.md) · [All projects](../README.md) · [Next: 11 →](../11.ec2-instance/README.md)
