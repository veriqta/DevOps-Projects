# 26. Service Discovery

[← All projects](../README.md) · **Advanced** · Consul

Register a service and observe health-based discovery.

## Prerequisites

Docker Compose v2 and curl.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Files included

Everything below is inside this project’s `files/` folder.

| File or folder | Use |
| --- | --- |
| `app` | Demo HTTP service, Dockerfile and service unit. |
| `consul` | Service registration and local discovery stack. |

## Walkthrough

From the repository root, enter this project:

```bash
cd 26.service-discovery
```

Run the remaining commands here unless a step explicitly changes directories. The `files/` folder contains the supplied code and configurations for this project.

### 1. Start Consul and the registered app

```bash
docker compose -f files/consul/compose.yml up -d --build
curl -fsS localhost:8500/v1/catalog/services
curl -fsS 'localhost:8500/v1/health/service/demo?passing=true'
```

Open `http://localhost:8500` to inspect the demo service. The mounted service.json registers address app:8080 and an HTTP health check inside the Compose network. Wait up to 10 seconds for passing status.

### 2. Simulate failure

```bash
docker compose -f files/consul/compose.yml stop app
sleep 10
curl -fsS 'localhost:8500/v1/health/service/demo?passing=true'
```

Expect an empty array. The catalog still records the service; healthy discovery filters it out.

### 3. Recover

```bash
docker compose -f files/consul/compose.yml start app
sleep 10
curl -fsS 'localhost:8500/v1/health/service/demo?passing=true'
```

This Consul development agent is local, ephemeral and has no production ACL/TLS configuration.

## Verify completion

Healthy discovery returns one service while running, zero while stopped, then one after recovery.

## Troubleshooting

A passing check must use an address reachable from Consul, which is why the example uses app rather than the host loopback address.

## Cleanup

`docker compose -f files/consul/compose.yml down`

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented service discovery in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://developer.hashicorp.com/consul/api-docs/agent/service)

---

[← Previous: 25](../25.multi-service-application/README.md) · [All projects](../README.md) · [Next: 27 →](../27.local-kubernetes-operations/README.md)
