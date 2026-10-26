# 02. Measure the Baseline Under Repeatable Load

[← 01. Prepare the Workload and Cost Assumptions](01-prepare-the-workload-and-cost-assumptions.md) · [Project home](README.md) · [03. Estimate the Infrastructure Configuration →](03-estimate-the-infrastructure-configuration.md)

## Starting state and working directory

Complete chapter 01 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `08.cloud-cost-and-capacity` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 08.cloud-cost-and-capacity
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A useful baseline includes latency, failure ratio and throughput under a stated load, plus the resource consumption observed during that same run. Repeated local runs can vary because of host contention and image cache effects. Run at least three repetitions for a more defensible comparison; preserve individual results rather than averaging away a failed run.

## Work through the implementation

The host-network command is for the documented Ubuntu environment. --user writes reports under the caller’s ownership. For a live resource sample, run docker stats in a second terminal during the test rather than relying only on the after-run snapshot; save both the command and observation window.

### Commands in execution order

```bash
docker run --rm --user "$(id -u):$(id -g)" --network host -v "$PWD:/work" -w /work grafana/k6:1.2.3 run --summary-export .lab/baseline.json load-test.js
docker stats --no-stream > .lab/baseline-resources.txt
python3 -m json.tool .lab/baseline.json > /dev/null
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

The baseline summary exists, contains http_req_duration and http_req_failed, and the run meets the fixed thresholds before optimization. Record the p95, failures and request count.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

A nonzero k6 result means a threshold or runtime failed. Do not begin an optimization comparison from an unexplained failing baseline. Check workload URL, container logs and host contention first.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [03. Estimate the Infrastructure Configuration](03-estimate-the-infrastructure-configuration.md). The next chapter assumes the state created here.
