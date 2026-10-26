# 08. Investigate Recover and Write the Incident Timeline

[← 07. Generate Load and Introduce a Controlled Failure](07-generate-load-and-introduce-a-controlled-failure.md) · [Project home](README.md) · [09. Measure Results Export Evidence and Clean Up →](09-measure-results-export-evidence-and-clean-up.md)

## Starting state and working directory

Complete chapter 07 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `04.sre-observability-and-incidents` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 04.sre-observability-and-incidents
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Recover the customer action, not only the monitoring screen. Start with the alert, identify failing status codes, correlate one log and trace, and remove the known fault. A delayed alert resolution is normal because the trailing rate window still includes failures. Record detection and recovery times independently instead of assigning the entire exercise duration to MTTR.

## Work through the implementation

Use a short blameless incident report: customer symptom, affected window, evidence, causal mechanism, recovery action, and one prevention improvement with an owner. State that the fault was deliberately injected. Include one trace ID and sanitized log event so a reviewer can follow your reasoning from alert to request, not just see disconnected screenshots.

### Commands in execution order

```bash
docker compose logs --tail=30 app
docker compose exec -T app rm -f /tmp/orders-fault.json
curl -fsS -H 'Content-Type: application/json' -d '{"item":"recovery-proof"}' localhost:8080/checkout
docker run --rm --user "$(id -u):$(id -g)" --network host -v "$PWD:/work" -w /work grafana/k6:1.2.3 run --summary-export .lab/recovered.json load-test.js
```

## Checkpoint — verify before continuing

Checkout returns 201 again, recovered load meets the lab thresholds and the alert returns inactive after the trailing window. Write trigger, detected, diagnosed, restored and verified timestamps.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If health is green but checkout still fails, inspect the fault file and request payload. If customer requests recover but alerts remain firing briefly, inspect the rate window before declaring a second incident.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [09. Measure Results Export Evidence and Clean Up](09-measure-results-export-evidence-and-clean-up.md). The next chapter assumes the state created here.
