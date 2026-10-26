# 07. Generate Load and Introduce a Controlled Failure

[← 06. Define an SLO and an Actionable Alert](06-define-an-slo-and-an-actionable-alert.md) · [Project home](README.md) · [08. Investigate Recover and Write the Incident Timeline →](08-investigate-recover-and-write-the-incident-timeline.md)

## Starting state and working directory

Complete chapter 06 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `04.sre-observability-and-incidents` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 04.sre-observability-and-incidents
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A repeatable workload makes the before/after comparison meaningful. k6 submits checkout requests and evaluates an error-rate and latency threshold. During the controlled fault the nonzero k6 exit is expected evidence that the service violated its contract. Do not remove the thresholds simply to make the pipeline green. Keep traffic local and bounded.

## Work through the implementation

The mounted .lab directory must be writable by the k6 container. On a fresh Ubuntu project run `mkdir -p .lab; chmod 777 .lab` only for this disposable nonsensitive output directory, or run the container with `--user "$(id -u):$(id -g)"` to avoid broad permissions. Prefer the explicit user option when recording a repeatable test. The load summary is a file, not merely terminal output.

### Commands in execution order

```bash
docker run --rm --user "$(id -u):$(id -g)" --network host -v "$PWD:/work" -w /work grafana/k6:1.2.3 run --summary-export .lab/baseline.json load-test.js
docker compose exec -T app sh -c 'printf "{"fail":true,"delay_ms":800}" > /tmp/orders-fault.json'
docker run --rm --user "$(id -u):$(id -g)" --network host -e DURATION=120s -v "$PWD:/work" -w /work grafana/k6:1.2.3 run --summary-export .lab/fault.json load-test.js
```

### Read the implementation: `load-test.js`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```javascript
import http from 'k6/http';
import {check,sleep} from 'k6';
export const options={vus:Number(__ENV.VUS||5),duration:__ENV.DURATION||'60s',thresholds:{http_req_failed:['rate<0.01'],http_req_duration:['p(95)<500']}};
export default function(){const response=http.post(__ENV.URL||'http://127.0.0.1:8080/checkout',JSON.stringify({item:'portfolio-book'}),{headers:{'Content-Type':'application/json'}});check(response,{'checkout accepted':r=>r.status===201});sleep(.2);}
```

## Checkpoint — verify before continuing

Record baseline p95 and error rate. During the fault, 503s appear in metrics/logs/traces and the alert becomes pending then firing after the configured evaluation window. Save timestamps.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

--network host is the documented Ubuntu Docker-host path. On Docker Desktop its behavior may differ; use the supplied Ubuntu environment. A nonzero k6 exit during the fault is expected, not a reason to stop collecting evidence.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [08. Investigate Recover and Write the Incident Timeline](08-investigate-recover-and-write-the-incident-timeline.md). The next chapter assumes the state created here.
