# 08. Test Failed Requests Retry and Rollback

[← 07. Run a Complete Developer Onboarding Journey](07-run-a-complete-developer-onboarding-journey.md) · [Project home](README.md) · [09. Measure Onboarding Results and Clean Up →](09-measure-onboarding-results-and-clean-up.md)

## Starting state and working directory

Complete chapter 07 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `07.developer-self-service-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 07.developer-self-service-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A failed render must not publish half a service. The --fail-after-render flag deliberately stops after files are written to temporary staging but before the atomic rename. A valid retry with the same service name should then succeed because no final target was created. This rollback covers local generation, not remote repository or cluster side effects that have already been explicitly requested.

### Commands in execution order

```bash
python3 automation/generate.py recovery-api --team payments --fail-after-render
# Expected failure: verify no final output was published.
test ! -e .generated/recovery-api
python3 automation/generate.py recovery-api --team payments
python3 -m unittest discover -s .generated/recovery-api -v
find .generated -maxdepth 1 -name '*.request-*' -print
```

### Read the implementation: `automation/test_generate.py`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```python
import tempfile,unittest
from pathlib import Path
from generate import generate
class GeneratorTest(unittest.TestCase):
    def test_complete_service_and_duplicate_protection(self):
        with tempfile.TemporaryDirectory() as temp:
            generate('orders-api','payments',temp)
            self.assertTrue((Path(temp)/'orders-api/.github/workflows/check.yml').exists())
            self.assertNotIn('@@NAME@@',(Path(temp)/'orders-api/server.py').read_text())
            with self.assertRaises(ValueError):generate('orders-api','payments',temp)
    def test_invalid_input_and_team(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):generate('../../escape','payments',temp)
            with self.assertRaises(ValueError):generate('orders-api','unknown',temp)
    def test_failed_request_does_not_publish_partial_service(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(RuntimeError):generate('orders-api','payments',temp,fail=True)
            self.assertEqual(list(Path(temp).iterdir()),[])
    def test_dry_run_does_not_publish(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertTrue(generate('orders-api','payments',temp,dry_run=True)['files'])
            self.assertEqual(list(Path(temp).iterdir()),[])
```

## Checkpoint — verify before continuing

The failed request leaves no recovery-api directory or staging leftovers; retry creates a complete service and its HTTP test passes.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If staging directories remain after failure, inspect the finally cleanup path. If external GitHub publication succeeded before a later failure, report that side effect and remove it explicitly; do not claim it was rolled back automatically.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [09. Measure Onboarding Results and Clean Up](09-measure-onboarding-results-and-clean-up.md). The next chapter assumes the state created here.
