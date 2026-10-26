# 10. Basic Dockerfile

[← All projects](../../README.md) · **Beginner** · Docker

Package the demo HTTP service in an unprivileged container.

## Prerequisites

Docker. Port 8080 must be available.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Build and run

```bash
docker build -t devops-demo:lab 02.examples/app
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

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://docs.docker.com/build/concepts/dockerfile/)

---

[← Previous: 09](../09.dummy-systemd-service/README.md) · [All projects](../../README.md) · [Next: 11 →](../11.ec2-instance/README.md)
