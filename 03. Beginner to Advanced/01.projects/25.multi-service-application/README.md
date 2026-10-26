# 25. Multi-Service Application

[← All projects](../../README.md) · **Advanced** · Containers · Architecture

Build a gateway, API and worker with separate health and failure boundaries.

## Prerequisites

Docker Compose v2. SQLite-backed lab for one host; it is not a distributed queue.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Start gateway, API and worker

```bash
docker compose -f 02.examples/multiservice/compose.yml up -d --build
curl -fsS localhost:8080/health
curl -fsS -H 'Content-Type: application/json' -d '{"value":"hello devops"}' localhost:8080/jobs
curl -fsS localhost:8080/jobs/1
```

Expect a job ID, then status done with result HELLO DEVOPS. The worker and API share a named volume containing SQLite; each job transformation commits atomically.

### 2. Prove backlog persistence

```bash
docker compose -f 02.examples/multiservice/compose.yml stop worker
curl -fsS -H 'Content-Type: application/json' -d '{"value":"recover me"}' localhost:8080/jobs
```

Query the returned job ID; expect queued. Restart the API and worker:

```bash
docker compose -f 02.examples/multiservice/compose.yml restart api
docker compose -f 02.examples/multiservice/compose.yml start worker
curl -fsS localhost:8080/jobs/2
```

Expect done after a short wait. On a fresh volume the IDs are 1 and 2; if you rerun, use the IDs returned by POST.

### 3. Inspect failure boundaries

Stop the API: the gateway should return 502 while the worker remains alive. Start the API and retry. Review compose logs. For external side effects, replace this transaction-only worker with a queue and idempotent processing before scaling across hosts.

## Verify completion

A queued job survives an API restart and completes when the worker resumes; unknown IDs return 404 and invalid JSON returns 400.

## Troubleshooting

A 502 immediately after startup can be transient; wait for the API. A persistent 502 requires checking API logs and gateway DNS.

## Cleanup

`docker compose -f 02.examples/multiservice/compose.yml down -v` deletes the job database.

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://docs.docker.com/compose/how-tos/startup-order/)

---

[← Previous: 24](../24.prometheus-and-grafana/README.md) · [All projects](../../README.md) · [Next: 26 →](../26.service-discovery/README.md)
