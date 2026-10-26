# 12. Pomodoro Timer

[← All projects](../README.md) · **Intermediate** · HTTP · Docker

Turn a small timer into a deployable, observable static application.

## Prerequisites

Docker and a browser.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Files included

Everything below is inside this project’s `files/` folder.

| File or folder | Use |
| --- | --- |
| `pages.yml` | GitHub Pages workflow for this timer. |
| `pomodoro` | Browser timer application. |

## Walkthrough

From the repository root, enter this project:

```bash
cd 12.pomodoro-timer
```

Run the remaining commands here unless a step explicitly changes directories. The `files/` folder contains the supplied code and configurations for this project.

### 1. Serve the timer

```bash
docker run -d --name pomodoro-lab -p 127.0.0.1:8081:80 -v "$PWD/files/pomodoro:/usr/share/nginx/html:ro" nginx:stable-alpine
curl -fsS http://127.0.0.1:8081
```

### 2. Exercise the controls

Open `http://127.0.0.1:8081`. Start the timer, wait five seconds, pause and confirm the value stops changing. Resume it, then reset: expect 25:00. Click Start twice; it must not count down twice as fast. Refresh: the lab timer intentionally resets.

### 3. Deploy it

Use a writable GitHub repository (project 04 explains initial repository setup). This project includes its own workflow, so no other project's files are needed:

```bash
mkdir -p ../.github/workflows
cp files/pages.yml ../.github/workflows/pomodoro-pages.yml
git add ../.github/workflows/pomodoro-pages.yml
git commit -m "Deploy Pomodoro portfolio lab"
git push
```

Enable GitHub Actions as the Pages source under Settings → Pages, then run the copied workflow. If you installed project 04’s Pages workflow earlier, remove or disable that workflow first so only one workflow publishes this repository's Pages site. Keep the deployment commit so you can roll back.

## Verify completion

Start, pause, resume and reset behave as described. The deployed site matches the local timer.

## Troubleshooting

A missing page usually means the bind mount path is wrong. Run the Docker command from this project folder.

## Cleanup

`docker rm -f pomodoro-lab`; unpublish the Pages site if no longer needed.

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented pomodoro timer in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://developer.mozilla.org/en-US/docs/Web/API/Window/setInterval)

---

[← Previous: 11](../11.ec2-instance/README.md) · [All projects](../README.md) · [Next: 13 →](../13.configuration-management/README.md)
