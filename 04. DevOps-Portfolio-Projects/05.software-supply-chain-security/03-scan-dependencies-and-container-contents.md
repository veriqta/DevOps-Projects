# 03. Scan Dependencies and Container Contents

[← 02. Establish a Reproducible Baseline Build](02-establish-a-reproducible-baseline-build.md) · [Project home](README.md) · [04. Produce and Inspect the SBOM →](04-produce-and-inspect-the-sbom.md)

## Starting state and working directory

Complete chapter 02 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `05.software-supply-chain-security` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 05.software-supply-chain-security
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

The policy distinguishes exploitable-risk triage from mechanical gating. This lab blocks fixed HIGH/CRITICAL findings because an actionable update exists; unfixed findings remain visible and need a documented decision. A scanner exit code of zero only means the scan command completed when configured for JSON output; evaluate.py makes the separate policy decision.

## Work through the implementation

Record the scan date, tool version, database metadata and the exact digest. Review Results entries to see which package and layer introduced a finding. The policy is deliberately small enough to inspect; before using it for real releases, add ownership, documented exceptions and expiry instead of silently adding broad ignores.

### Commands in execution order

```bash
trivy image --format json --output .lab/scan.json "$IMAGE"
python3 policy/evaluate.py .lab/scan.json
python3 -m unittest discover -s policy -v
trivy --version
```

### Read the implementation: `policy/evaluate.py`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```python
import json,sys
from pathlib import Path

def violations(report):
    if not isinstance(report,dict) or not isinstance(report.get('Results'),list):
        raise ValueError('Scan report must contain a Results array; missing data is not a clean scan')
    failures=[]
    for result in report.get('Results',[]):
        for item in result.get('Vulnerabilities') or []:
            if item.get('Severity') in ['HIGH','CRITICAL'] and item.get('FixedVersion'):
                failures.append(item['VulnerabilityID'])
    return sorted(set(failures))
if __name__=='__main__':
    found=violations(json.loads(Path(sys.argv[1]).read_text()))
    print(json.dumps({'blocked_vulnerabilities':found}))
    raise SystemExit(1 if found else 0)
```

### Read the implementation: `policy/test_policy.py`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```python
import unittest
from evaluate import violations
class PolicyTest(unittest.TestCase):
    def test_fixed_high_blocks(self):self.assertEqual(violations({'Results':[{'Vulnerabilities':[{'VulnerabilityID':'LAB-1','Severity':'HIGH','FixedVersion':'2'}]}]}),['LAB-1'])
    def test_lower_severity_and_unfixed_are_report_only(self):self.assertEqual(violations({'Results':[{'Vulnerabilities':[{'VulnerabilityID':'LAB-2','Severity':'LOW','FixedVersion':'2'},{'VulnerabilityID':'LAB-3','Severity':'HIGH'}]}]}),[])

    def test_missing_report_fails_closed(self):
        with self.assertRaises(ValueError):violations({})
```

## Checkpoint — verify before continuing

A real scan file contains Results and scanner metadata. If the gate fails, identify each blocked CVE and fixed version, update the base image, rebuild/push and scan the new digest. Never edit the report to turn a failure into a pass.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Database download failures are not clean scan results. Preserve the error and retry when connected. A different scan date can legitimately change the findings even for the same digest.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [04. Produce and Inspect the SBOM](04-produce-and-inspect-the-sbom.md). The next chapter assumes the state created here.
