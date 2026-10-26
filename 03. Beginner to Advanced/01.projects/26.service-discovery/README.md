# 26. Service Discovery

[← All projects](../../README.md) · **Advanced** · Consul

Register a service and observe health-based discovery.

## Prerequisites

Docker Compose v2 and curl.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Start Consul and the registered app

```bash
docker compose -f 02.examples/consul/compose.yml up -d --build
curl -fsS localhost:8500/v1/catalog/services
curl -fsS 'localhost:8500/v1/health/service/demo?passing=true'
```

Open `http://localhost:8500` to inspect the demo service. The mounted service.json registers address app:8080 and an HTTP health check inside the Compose network. Wait up to 10 seconds for passing status.

### 2. Simulate failure

```bash
docker compose -f 02.examples/consul/compose.yml stop app
sleep 10
curl -fsS 'localhost:8500/v1/health/service/demo?passing=true'
```

Expect an empty array. The catalog still records the service; healthy discovery filters it out.

### 3. Recover

```bash
docker compose -f 02.examples/consul/compose.yml start app
sleep 10
curl -fsS 'localhost:8500/v1/health/service/demo?passing=true'
```

This Consul development agent is local, ephemeral and has no production ACL/TLS configuration.

## Verify completion

Healthy discovery returns one service while running, zero while stopped, then one after recovery.

## Troubleshooting

A passing check must use an address reachable from Consul, which is why the example uses app rather than the host loopback address.

## Cleanup

`docker compose -f 02.examples/consul/compose.yml down`

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://developer.hashicorp.com/consul/api-docs/agent/service)

---

[← Previous: 25](../25.multi-service-application/README.md) · [All projects](../../README.md) · [Next: 27 →](../27.local-kubernetes-operations/README.md)
