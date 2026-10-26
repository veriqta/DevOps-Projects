# 23. Blue-Green Deployment

[← All projects](../README.md) · **Advanced** · Nginx · Docker

Switch traffic between two healthy application releases and roll back.

## Prerequisites

Docker Compose v2; port 8080 free.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Files included

Everything below is inside this project’s `files/` folder.

| File or folder | Use |
| --- | --- |
| `app` | Demo HTTP service, Dockerfile and service unit. |
| `bluegreen` | Proxy configurations and deployment stack. |

## Walkthrough

From the repository root, enter this project:

```bash
cd 23.blue-green-deployment
```

Run the remaining commands here unless a step explicitly changes directories. The `files/` folder contains the supplied code and configurations for this project.

### 1. Start blue and green behind a proxy

```bash
mkdir -p files/bluegreen/config
cp files/bluegreen/blue.conf files/bluegreen/config/default.conf
docker compose -f files/bluegreen/compose.yml up -d --build
curl -fsS localhost:8080/health
```

Expect version blue.

### 2. Validate green before switching

```bash
docker compose -f files/bluegreen/compose.yml exec -T proxy wget -qO- http://green:8080/health
cp files/bluegreen/green.conf files/bluegreen/config/default.conf
docker compose -f files/bluegreen/compose.yml exec -T proxy nginx -t
docker compose -f files/bluegreen/compose.yml exec -T proxy nginx -s reload
curl -fsS localhost:8080/health
```

Expect green. In a second terminal run repeated requests during another switch and record any failures.

### 3. Roll back

```bash
cp files/bluegreen/blue.conf files/bluegreen/config/default.conf
docker compose -f files/bluegreen/compose.yml exec -T proxy nginx -t
docker compose -f files/bluegreen/compose.yml exec -T proxy nginx -s reload
curl -fsS localhost:8080/health
```

Both backends remain running during a switch. Real database migrations must remain compatible with both releases; this stateless demo avoids that complication.

## Verify completion

Observe blue → green → blue through the same host port. Confirm each nginx -t succeeds before reload.

## Troubleshooting

Mount the config directory as supplied. Replacing a single bind-mounted file by rename can leave a container seeing the old file inode.

## Cleanup

```bash
docker compose -f files/bluegreen/compose.yml down
rm -rf files/bluegreen/config
```

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented blue-green container deployments behind Nginx and demonstrated health-gated switching and rollback.”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://nginx.org/en/docs/http/ngx_http_upstream_module.html)

---

[← Previous: 22](../22.vpn-server-setup/README.md) · [All projects](../README.md) · [Next: 24 →](../24.prometheus-and-grafana/README.md)
