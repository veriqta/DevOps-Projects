# 12. Pomodoro Timer

[← All projects](../../README.md) · **Intermediate** · HTTP · Docker

Turn a small timer into a deployable, observable static application.

## Prerequisites

Docker and a browser.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Serve the timer

```bash
docker run -d --name pomodoro-lab -p 127.0.0.1:8081:80 -v "$PWD/02.examples/pomodoro:/usr/share/nginx/html:ro" nginx:stable-alpine
curl -fsS http://127.0.0.1:8081
```

### 2. Exercise the controls

Open `http://127.0.0.1:8081`. Start the timer, wait five seconds, pause and confirm the value stops changing. Resume it, then reset: expect 25:00. Click Start twice; it must not count down twice as fast. Refresh: the lab timer intentionally resets.

### 3. Deploy it

In your writable repository, copy `02.examples/pomodoro/index.html` to `06.site/index.html` and complete project 04. Keep the deployment commit so you can roll back.

## Verify completion

Start, pause, resume and reset behave as described. The deployed site matches the local timer.

## Troubleshooting

A missing page usually means the bind mount path is wrong. Run the Docker command from the repository root.

## Cleanup

`docker rm -f pomodoro-lab`; unpublish the Pages site if no longer needed.

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://developer.mozilla.org/en-US/docs/Web/API/Window/setInterval)

---

[← Previous: 11](../11.ec2-instance/README.md) · [All projects](../../README.md) · [Next: 13 →](../13.configuration-management/README.md)
