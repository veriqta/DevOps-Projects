# 23. Blue-Green Deployment

[← All projects](../../README.md) · **Advanced** · Nginx · Docker

Switch traffic between two healthy application releases and roll back.

## Prerequisites

Docker Compose v2; port 8080 free.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Start blue and green behind a proxy

```bash
mkdir -p 02.examples/bluegreen/config
cp 02.examples/bluegreen/blue.conf 02.examples/bluegreen/config/default.conf
docker compose -f 02.examples/bluegreen/compose.yml up -d --build
curl -fsS localhost:8080/health
```

Expect version blue.

### 2. Validate green before switching

```bash
docker compose -f 02.examples/bluegreen/compose.yml exec -T proxy wget -qO- http://green:8080/health
cp 02.examples/bluegreen/green.conf 02.examples/bluegreen/config/default.conf
docker compose -f 02.examples/bluegreen/compose.yml exec -T proxy nginx -t
docker compose -f 02.examples/bluegreen/compose.yml exec -T proxy nginx -s reload
curl -fsS localhost:8080/health
```

Expect green. In a second terminal run repeated requests during another switch and record any failures.

### 3. Roll back

```bash
cp 02.examples/bluegreen/blue.conf 02.examples/bluegreen/config/default.conf
docker compose -f 02.examples/bluegreen/compose.yml exec -T proxy nginx -t
docker compose -f 02.examples/bluegreen/compose.yml exec -T proxy nginx -s reload
curl -fsS localhost:8080/health
```

Both backends remain running during a switch. Real database migrations must remain compatible with both releases; this stateless demo avoids that complication.

## Verify completion

Observe blue → green → blue through the same host port. Confirm each nginx -t succeeds before reload.

## Troubleshooting

Mount the config directory as supplied. Replacing a single bind-mounted file by rename can leave a container seeing the old file inode.

## Cleanup

```bash
docker compose -f 02.examples/bluegreen/compose.yml down
rm -rf 02.examples/bluegreen/config
```

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://nginx.org/en/docs/http/ngx_http_upstream_module.html)

---

[← Previous: 22](../22.vpn-server-setup/README.md) · [All projects](../../README.md) · [Next: 24 →](../24.prometheus-and-grafana/README.md)
