# 03. Deploy the Workload and Understand Each Manifest

[← 02. Build and Load the Application Image](02-build-and-load-the-application-image.md) · [Project home](README.md) · [04. Configure Services Routing and HTTPS →](04-configure-services-routing-and-https.md)

## Starting state and working directory

Complete chapter 02 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `03.kubernetes-application-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 03.kubernetes-application-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

Render the chart before installing it. The Deployment selector and pod labels must agree; the Service selector must match them too. A readiness probe decides when a pod can receive service traffic, whereas a liveness probe can restart a stuck process. Resource requests affect placement and limits bound resource use. These controls solve different problems and should not be treated as interchangeable.

## Work through the implementation

The initial apply uses rendered manifests so you can inspect the plain Kubernetes objects. It is not yet a Helm-managed release. Follow labels and secretKeyRef through the file. The read-only root filesystem works because this service does not need to persist data; adding file writes would require an explicit writable volume.

### Commands in execution order

```bash
helm template orders chart -n orders > .lab/rendered.yaml
kubectl apply -n orders -f .lab/rendered.yaml
kubectl -n orders rollout status deployment/orders --timeout=120s
kubectl -n orders get pods,service,endpointslices
kubectl -n orders port-forward service/orders 8080:80
```

### Read the implementation: `chart/templates/workload.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders
spec:
  replicas: {{ .Values.replicas }}
  selector:
    matchLabels: {app: orders}
  template:
    metadata:
      labels: {app: orders}
    spec:
      containers:
        - name: orders
          image: {{ .Values.image | quote }}
          imagePullPolicy: IfNotPresent
          env:
            - {name: VERSION, value: {{ .Values.version | quote }}}
            - {name: WELCOME_MESSAGE, value: {{ .Values.message | quote }}}
            - name: LAB_TOKEN
              valueFrom:
                secretKeyRef: {name: {{ .Values.secretName }}, key: token}
          ports: [{containerPort: 8080}]
          readinessProbe:
            httpGet: {path: /health, port: 8080}
          livenessProbe:
            httpGet: {path: /health, port: 8080}
            initialDelaySeconds: 5
          resources:
            requests: {cpu: {{ .Values.cpuRequest }}, memory: {{ .Values.memoryRequest }}}
            limits: {cpu: 500m, memory: 128Mi}
          securityContext:
            runAsNonRoot: true
            runAsUser: 10001
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities: {drop: [ALL]}
---
apiVersion: v1
kind: Service
metadata:
  name: orders
spec:
  selector: {app: orders}
  ports: [{name: http, port: 80, targetPort: 8080}]
```

### Read the implementation: `chart/values.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
image: orders:lab
replicas: 2
version: v1
message: Welcome
secretName: orders-runtime
cpuRequest: 100m
memoryRequest: 64Mi
```

## Checkpoint — verify before continuing

In a second terminal, curl localhost:8080/health and POST a valid checkout. Both replicas become Ready and the Service has endpoints. Stop port-forward with Ctrl+C after testing.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

A Running but unready pod will not receive normal Service traffic. Describe the pod and inspect events. A CreateContainerConfigError may mean the Secret from chapter 02 is missing.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [04. Configure Services Routing and HTTPS](04-configure-services-routing-and-https.md). The next chapter assumes the state created here.
