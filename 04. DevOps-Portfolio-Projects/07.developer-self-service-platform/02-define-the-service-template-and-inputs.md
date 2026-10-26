# 02. Define the Service Template and Inputs

[← 01. Run the Platform Locally](01-run-the-platform-locally.md) · [Project home](README.md) · [03. Generate and Test the First Service →](03-generate-and-test-the-first-service.md)

## Starting state and working directory

Complete chapter 01 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `07.developer-self-service-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 07.developer-self-service-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Every token in the template has a named input or a platform-controlled value. Allowing arbitrary strings inside source or YAML would invite malformed files or injection into generated workflows. The name regex excludes path separators and shell metacharacters; the team must appear in a small allowlist. Those checks protect generation integrity but do not authenticate a person’s actual team membership.

## Work through the implementation

Open the template and find every @@NAME@@ and @@TEAM@@ token. A token must not survive into a generated service. The generator reads only its own template directory and never interprets the developer input as a path. A production portal would map authenticated identity to allowed owners rather than trust a --team argument.

### Commands in execution order

```bash
cat automation/teams.json
find template -type f | sort
python3 automation/generate.py invalid/name --team payments --dry-run
# Expect rejection; then inspect a valid plan.
python3 automation/generate.py orders-api --team payments --dry-run
```

### Read the implementation: `automation/teams.json`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```json
{"teams":["payments","platform"]}
```

### Read the implementation: `template/server.py`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```python
import json,os
from http.server import BaseHTTPRequestHandler,HTTPServer
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        code=200 if self.path=='/health' else 404
        body=json.dumps({'service':'@@NAME@@','team':'@@TEAM@@','healthy':code==200}).encode()
        self.send_response(code);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
if __name__=='__main__':HTTPServer(('0.0.0.0',int(os.environ.get('PORT','8080'))),Handler).serve_forever()
```

### Read the implementation: `template/deployment.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: @@NAME@@
  labels: {team: @@TEAM@@}
spec:
  replicas: 2
  selector:
    matchLabels: {app: @@NAME@@}
  template:
    metadata:
      labels: {app: @@NAME@@, team: @@TEAM@@}
    spec:
      containers:
        - name: service
          image: @@NAME@@:lab
          imagePullPolicy: IfNotPresent
          ports: [{containerPort: 8080}]
          readinessProbe:
            httpGet: {path: /health, port: 8080}
          resources:
            requests: {cpu: 50m, memory: 32Mi}
            limits: {cpu: 250m, memory: 64Mi}
---
apiVersion: v1
kind: Service
metadata: {name: @@NAME@@}
spec:
  selector: {app: @@NAME@@}
  ports: [{port: 80, targetPort: 8080}]
```

## Checkpoint — verify before continuing

Invalid names are rejected before rendering. The valid plan names application, test, Dockerfile, README, deployment YAML and .github/workflows/check.yml.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Do not bypass name validation to accept a display label with spaces. Add a separate validated display-name field if the product needs it; keep machine identifiers constrained.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [03. Generate and Test the First Service](03-generate-and-test-the-first-service.md). The next chapter assumes the state created here.
