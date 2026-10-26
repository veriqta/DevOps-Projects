# 04. Configure Services Routing and HTTPS

[← 03. Deploy the Workload and Understand Each Manifest](03-deploy-the-workload-and-understand-each-manifest.md) · [Project home](README.md) · [05. Package the Application With Helm →](05-package-the-application-with-helm.md)

## Starting state and working directory

Complete chapter 03 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `03.kubernetes-application-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 03.kubernetes-application-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

The gateway owns the TLS key and presents a certificate for orders.local. curl must resolve that hostname to the loopback forward and verify against the lab certificate. Using -k would hide trust and hostname mistakes, so it is not the success criterion. Internal HTTP is confined to the local cluster; this lab does not implement a service mesh or end-to-end mTLS.

## Work through the implementation

The private key is generated locally, mounted from a Kubernetes Secret and never committed. -nodes produces an unencrypted private key for the Nginx process; its protection comes from local file permissions and cluster access controls in this lab. A production platform needs a managed certificate issuer and renewal procedure rather than this two-day certificate.

### Commands in execution order

```bash
openssl req -x509 -newkey rsa:2048 -nodes -days 2 -keyout .lab/tls.key -out .lab/tls.crt -subj /CN=orders.local -addext subjectAltName=DNS:orders.local
chmod 600 .lab/tls.key
kubectl -n orders create secret tls gateway-tls --cert=.lab/tls.crt --key=.lab/tls.key
kubectl -n orders create configmap gateway-config --from-file=default.conf=platform/nginx.conf
kubectl apply -f platform/gateway.yaml
kubectl -n orders rollout status deployment/gateway --timeout=120s
kubectl -n orders port-forward service/gateway 8443:443
```

### Read the implementation: `platform/gateway.yaml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gateway
  namespace: orders
spec:
  replicas: 1
  selector:
    matchLabels: {app: gateway}
  template:
    metadata:
      labels: {app: gateway}
    spec:
      containers:
        - name: nginx
          image: nginx:stable-alpine
          ports: [{containerPort: 8443}]
          volumeMounts:
            - {name: config, mountPath: /etc/nginx/conf.d, readOnly: true}
            - {name: cert, mountPath: /etc/nginx/tls, readOnly: true}
      volumes:
        - name: config
          configMap: {name: gateway-config}
        - name: cert
          secret: {secretName: gateway-tls}
---
apiVersion: v1
kind: Service
metadata:
  name: gateway
  namespace: orders
spec:
  selector: {app: gateway}
  ports: [{port: 443, targetPort: 8443}]
```

### Read the implementation: `platform/nginx.conf`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```text
server { listen 8443 ssl; server_name orders.local; ssl_certificate /etc/nginx/tls/tls.crt; ssl_certificate_key /etc/nginx/tls/tls.key; location / { proxy_pass http://orders:80; } }
```

## Checkpoint — verify before continuing

In a second terminal from this project directory run curl --cacert .lab/tls.crt --resolve orders.local:8443:127.0.0.1 https://orders.local:8443/health. Expect valid TLS and status ok. An unrelated hostname or missing CA must fail verification. Stop the forward after testing.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

TLS failures are useful evidence: inspect subjectAltName, certificate lifetime and hostname resolution separately. A 502 after valid TLS means the backend Service or endpoints need investigation.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [05. Package the Application With Helm](05-package-the-application-with-helm.md). The next chapter assumes the state created here.
