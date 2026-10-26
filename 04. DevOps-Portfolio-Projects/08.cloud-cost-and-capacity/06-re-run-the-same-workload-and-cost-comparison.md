# 06. Re-run the Same Workload and Cost Comparison

[← 05. Change Capacity and Resource Requests](05-change-capacity-and-resource-requests.md) · [Project home](README.md) · [07. Add Budget and Change Review Checks →](07-add-budget-and-change-review-checks.md)

## Starting state and working directory

Complete chapter 05 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `08.cloud-cost-and-capacity` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 08.cloud-cost-and-capacity
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A comparison script should reject the optimization when the candidate violates the stated performance contract. It should not silently accept missing metrics. The baseline/candidate report preserves raw measurements and makes the SLO decision explicit. The Infracost model compares a cloud SKU separately, allowing you to state which part was measured and which part was estimated.

## Work through the implementation

Use repeated samples to discuss variance. If results differ materially across runs, report the range and likely host contention instead of presenting a single precise saving. Throughput changes should be explained alongside response time; a faster result with fewer completed requests can be misleading.

### Commands in execution order

```bash
python3 scripts/compare.py .lab/baseline.json .lab/candidate.json > .lab/comparison.json
cat .lab/comparison.json
python3 -m unittest discover -s scripts -v
infracost diff --path terraform --terraform-var 'instance_type=t3.micro' --compare-to .lab/base-cost.json
```

### Read the implementation: `scripts/compare.py`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```python
import json,sys
from pathlib import Path

def metric(report,name,field):
    item=report['metrics'][name]
    values=item.get('values',item)
    if field=='value':return values['rate'] if 'rate' in values else values['value']
    return values[field]
def compare(before,after):
    def values(data):return {'p95_ms':metric(data,'http_req_duration','p(95)'), 'failure_rate':metric(data,'http_req_failed','value'), 'requests':metric(data,'http_reqs','count')}
    b,a=values(before),values(after)
    return {'baseline':b,'candidate':a,'candidate_passes_slo':a['p95_ms']<500 and a['failure_rate']<.01}
if __name__=='__main__':
    result=compare(json.loads(Path(sys.argv[1]).read_text()),json.loads(Path(sys.argv[2]).read_text()))
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['candidate_passes_slo'] else 1)
```

### Read the implementation: `scripts/test_compare.py`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```python
import unittest
from compare import compare
class ComparisonTest(unittest.TestCase):
    def test_rejects_candidate_that_breaks_slo(self):
        def report(latency):return {'metrics':{'http_req_duration':{'p(95)':latency},'http_req_failed':{'value':0},'http_reqs':{'count':100}}}
        self.assertFalse(compare(report(100),report(600))['candidate_passes_slo'])
        self.assertTrue(compare(report(100),report(200))['candidate_passes_slo'])

    def test_structured_k6_metrics(self):
        report={'metrics':{'http_req_duration':{'values':{'p(95)':120}},'http_req_failed':{'values':{'rate':0}},'http_reqs':{'values':{'count':100}}}}
        self.assertTrue(compare(report,report)['candidate_passes_slo'])
```

## Checkpoint — verify before continuing

The comparison contains both p95 values, failure ratios, request counts and candidate_passes_slo. A failing candidate causes exit 1. Preserve that failure as a rejected change rather than discarding the report.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Missing metric fields indicate an unexpected k6 export format or a failed run. Inspect the raw JSON before changing the parser. Do not treat missing data as a passing performance result.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [07. Add Budget and Change Review Checks](07-add-budget-and-change-review-checks.md). The next chapter assumes the state created here.
