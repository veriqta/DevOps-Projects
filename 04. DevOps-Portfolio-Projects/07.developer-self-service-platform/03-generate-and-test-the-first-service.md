# 03. Generate and Test the First Service

[← 02. Define the Service Template and Inputs](02-define-the-service-template-and-inputs.md) · [Project home](README.md) · [04. Add the Delivery Workflow and Repository Integration →](04-add-the-delivery-workflow-and-repository-integration.md)

## Starting state and working directory

Complete chapter 02 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `07.developer-self-service-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 07.developer-self-service-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

A complete request should be reproducible and safe to repeat. The first orders-api request creates the service; a second request is rejected rather than silently overwriting developer work. The generated test starts the real HTTP handler on an ephemeral port and checks service and owner identity. This catches a rendering error that a file-existence assertion alone would miss.

## Work through the implementation

Inspect the generated README and source before treating generation as an onboarding success. Save a directory listing and the actual health JSON. The template is intentionally small, but the platform outcome is a working service with delivery artifacts rather than a static scaffold.

### Commands in execution order

```bash
python3 automation/generate.py orders-api --team payments
python3 -m unittest discover -s .generated/orders-api -v
python3 .generated/orders-api/server.py
```

### Read the implementation: `template/test_service.py`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```python
import json,threading,unittest
from http.server import HTTPServer
from urllib.request import urlopen
from server import Handler
class ServiceTest(unittest.TestCase):
    def test_health_identifies_service_and_owner(self):
        server=HTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            with urlopen(f'http://127.0.0.1:{server.server_port}/health') as response:
                result=json.load(response);self.assertEqual(result['service'],'@@NAME@@');self.assertEqual(result['team'],'@@TEAM@@')
        finally:server.shutdown();server.server_close();thread.join()
```

## Checkpoint — verify before continuing

In another terminal curl localhost:8080/health and expect service orders-api and team payments. Stop the server with Ctrl+C. Repeat generation with the same name and confirm a nonzero duplicate error while existing files remain unchanged.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If port 8080 is busy, stop the previous lab. A generated file still containing @@ tokens indicates a template/input mapping error; fix the generator/template, not just the one generated copy.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [04. Add the Delivery Workflow and Repository Integration](04-add-the-delivery-workflow-and-repository-integration.md). The next chapter assumes the state created here.
