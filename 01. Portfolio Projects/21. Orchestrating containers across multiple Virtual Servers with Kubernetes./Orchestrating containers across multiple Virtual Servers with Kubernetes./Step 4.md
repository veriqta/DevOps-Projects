# STEP 4 PREPARE THE SELF-SIGNED CERTIFICATE AUTHORITY AND GENERATE TLS CERTIFICATES

The following components running on the Master node will require TLS certificates.

- kube-controller-manager
- kube-scheduler
- etcd
- kube-apiserver
- 
The following components running on the Worker nodes will require TLS certificates.

- kubelet
- kube-proxy

Therefore, you will provision a PKI Infrastructure using cfssl which will have a Certificate Authority. The CA will then generate
certificates for all the individual components.

**Self-Signed Root Certificate Authority (CA)**

Here, you will provision a CA that will be used to sign additional TLS certificates.

Create a directory and cd into it:

```
mkdir ca-authority && cd ca-authority
```

Generate the CA configuration file, Root Certificate, and Private key:

```
{

cat > ca-config.json <<EOF
{
  "signing": {
    "default": {
      "expiry": "8760h"
    },
    "profiles": {
      "kubernetes": {
        "usages": ["signing", "key encipherment", "server auth", "client auth"],
        "expiry": "8760h"
      }
    }
  }
}
EOF

cat > ca-csr.json <<EOF
{
  "CN": "Kubernetes",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "UK",
      "L": "England",
      "O": "Kubernetes",
      "OU": "TOTAL.COM",
      "ST": "London"
    }
  ]
}
EOF

cfssl gencert -initca ca-csr.json | cfssljson -bare ca

}
```


The file defines the following:


```
CN – Common name for the authority

algo – the algorithm used for the certificates

size – algorithm size in bits

C – Country

L – Locality (city)

ST – State or province

O – Organization

OU – Organizational Unit
```


![7015](https://user-images.githubusercontent.com/85270361/210201383-28c7d624-6423-42f6-a5ba-92332e99c35d.PNG)


List the directory to see the created files

```
ls -ltr

-rw-r--r--  1 ann  ann   232 16 May 20:18 ca-config.json
-rw-r--r--  1 ann  ann   207 16 May 20:18 ca-csr.json
-rw-r--r--  1 ann  ann  1306 16 May 20:18 ca.pem
-rw-------  1 ann  ann  1679 16 May 20:18 ca-key.pem
-rw-r--r--  1 ann  ann  1001 16 May 20:18 ca.csr
```

The 3 important files here are:

- ca.pem – The Root Certificate
- ca-key.pem – The Private Key
- ca.csr – The Certificate Signing Request

Generating TLS Certificates For Client and Server

You will need to provision Client/Server certificates for all the components. It is a MUST to have encrypted communication within 
the cluster. Therefore, the server here are the master nodes running the api-server component. While the client is every other 
component that needs to communicate with the api-server.

Now we have a certificate for the Root CA, we can then begin to request more certificates which the different Kubernetes components,
i.e. clients and server, will use to have encrypted communication.

Remember, the clients here refer to every other component that will communicate with the api-server. These are:

- kube-controller-manager
- kube-scheduler
- etcd
- kubelet
- kube-proxy
-  Admin User

Let us begin with the Kubernetes API-Server Certificate and Private Key

The certificate for the Api-server must have IP addresses, DNS names, and a Load Balancer address included. Otherwise, you will have
a lot of difficulties connecting to the api-server.

1. Generate the Certificate Signing Request (CSR), Private Key and the Certificate for the Kubernetes Master Nodes.

```
{
cat > master-kubernetes-csr.json <<EOF
{
  "CN": "kubernetes",
   "hosts": [
   "127.0.0.1",
   "172.31.0.10",
   "172.31.0.11",
   "172.31.0.12",
   "ip-172-31-0-10",
   "ip-172-31-0-11",
   "ip-172-31-0-12",
   "ip-172-31-0-10.${AWS_REGION}.compute.internal",
   "ip-172-31-0-11.${AWS_REGION}.compute.internal",
   "ip-172-31-0-12.${AWS_REGION}.compute.internal",
   "${KUBERNETES_PUBLIC_ADDRESS}",
   "kubernetes",
   "kubernetes.default",
   "kubernetes.default.svc",
   "kubernetes.default.svc.cluster",
   "kubernetes.default.svc.cluster.local"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "UK",
      "L": "England",
      "O": "Kubernetes",
      "OU": "TOTAL.COM",
      "ST": "London"
    }
  ]
}
EOF

cfssl gencert \
  -ca=ca.pem \
  -ca-key=ca-key.pem \
  -config=ca-config.json \
  -profile=kubernetes \
  master-kubernetes-csr.json | cfssljson -bare master-kubernetes
}
```

Creating the other certificates: for the following Kubernetes components:

- Scheduler Client Certificate
-  Proxy Client Certificate
- Controller Manager Client Certificate
- Kubelet Client Certificates
- K8s admin user Client Certificate

2. kube-scheduler Client Certificate and Private Key

```
{

cat > kube-scheduler-csr.json <<EOF
{
  "CN": "system:kube-scheduler",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "UK",
      "L": "England",
      "O": "system:kube-scheduler",
      "OU": "TOTAL.COM",
      "ST": "London"
    }
  ]
}
EOF

cfssl gencert \
  -ca=ca.pem \
  -ca-key=ca-key.pem \
  -config=ca-config.json \
  -profile=kubernetes \
  kube-scheduler-csr.json | cfssljson -bare kube-scheduler

}
```


*If you see any warning message, it is safe to ignore it.*

3. kube-proxy **Client Certificate and Private Key**


```
{

cat > kube-proxy-csr.json <<EOF
{
  "CN": "system:kube-proxy",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "UK",
      "L": "England",
      "O": "system:node-proxier",
      "OU": "TOTAL.COM",
      "ST": "London"
    }
  ]
}
EOF

cfssl gencert \
  -ca=ca.pem \
  -ca-key=ca-key.pem \
  -config=ca-config.json \
  -profile=kubernetes \
  kube-proxy-csr.json | cfssljson -bare kube-proxy

}
```


4. kube-controller-manager **Client Certificate and Private Key**


```
{
cat > kube-controller-manager-csr.json <<EOF
{
  "CN": "system:kube-controller-manager",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "UK",
      "L": "England",
      "O": "system:kube-controller-manager",
      "OU": "TOTAL.COM",
      "ST": "London"
    }
  ]
}
EOF

cfssl gencert \
  -ca=ca.pem \
  -ca-key=ca-key.pem \
  -config=ca-config.json \
  -profile=kubernetes \
  kube-controller-manager-csr.json | cfssljson -bare kube-controller-manager

}
```

5. kubelet Client **Certificate and Private Key**
Similar to how you configured the api-server's certificate, Kubernetes requires that the hostname of each worker node is included in
the client certificate.

Also, Kubernetes uses a special-purpose authorization mode called Node Authorizer, that specifically authorizes API requests made 
by kubelet services. In order to be authorized by the Node Authorizer, kubelets must use a credential that identifies them as being
in the system:nodes group, with a username of system:node:<nodeName>. Notice the "CN": "system:node:${instance_hostname}", in the
below code.

Therefore, the certificate to be created must comply to these requirements. In the below example, there are 3 worker nodes, hence 
we will use bash to loop through a list of the worker nodes’ hostnames, and based on each index, the respective Certificate Signing
Request (CSR), private key and client certificates will be generated.
  
  
  
```
for i in 0 1 2; do
  instance="${NAME}-worker-${i}"
  instance_hostname="ip-172-31-0-2${i}"
  cat > ${instance}-csr.json <<EOF
{
  "CN": "system:node:${instance_hostname}",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "UK",
      "L": "England",
      "O": "system:nodes",
      "OU": "TOTAL.COM",
      "ST": "London"
    }
  ]
}
EOF

  external_ip=$(aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=${instance}" \
    --output text --query 'Reservations[].Instances[].PublicIpAddress')

  internal_ip=$(aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=${instance}" \
    --output text --query 'Reservations[].Instances[].PrivateIpAddress')

  cfssl gencert \
    -ca=ca.pem \
    -ca-key=ca-key.pem \
    -config=ca-config.json \
    -hostname=${instance_hostname},${external_ip},${internal_ip} \
    -profile=kubernetes \
    ${NAME}-worker-${i}-csr.json | cfssljson -bare ${NAME}-worker-${i}
done
```
  
  
6. Finally, kubernetes admin user's **Client Certificate and Private Key**
  

```
{
cat > admin-csr.json <<EOF
{
  "CN": "admin",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "UK",
      "L": "England",
      "O": "system:masters",
      "OU": "TOTAL.COM",
      "ST": "London"
    }
  ]
}
EOF

cfssl gencert \
  -ca=ca.pem \
  -ca-key=ca-key.pem \
  -config=ca-config.json \
  -profile=kubernetes \
  admin-csr.json | cfssljson -bare admin
}
```
  
  
7. Actually, we are not done yet! :tired_face:
There is one more pair of certificate and private key we need to generate. That is for the Token Controller: a part of the Kubernetes 
Controller Manager kube-controller-manager responsible for generating and signing service account tokens which are used by pods or
other resources to establish connectivity to the api-server. Read more about Service Accounts from the official documentation.

Alright, let us quickly create the last set of files, and we are done with PKIs
  
  
```
{

cat > service-account-csr.json <<EOF
{
  "CN": "service-accounts",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "UK",
      "L": "England",
      "O": "Kubernetes",
      "OU": "TOTAL.COM",
      "ST": "London"
    }
  ]
}
EOF

cfssl gencert \
  -ca=ca.pem \
  -ca-key=ca-key.pem \
  -config=ca-config.json \
  -profile=kubernetes \
  service-account-csr.json | cfssljson -bare service-account
}
```
