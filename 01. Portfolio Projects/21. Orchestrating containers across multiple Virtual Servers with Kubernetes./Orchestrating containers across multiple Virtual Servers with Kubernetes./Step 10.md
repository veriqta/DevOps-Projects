# CONFIGURING THE KUBERNETES WORKER NODES

Before we begin to bootstrap the worker nodes, it is important to understand that the K8s API Server authenticates to the kubelet as
the kubernetes user using the same kubernetes.pem certificate.

We need to configure Role Based Access (RBAC) for Kubelet Authorization:


1. Configure RBAC permissions to allow the Kubernetes API Server to access the Kubelet API on each worker node. Access to the Kubelet 
API is required for retrieving metrics, logs, and executing commands in pods.

Create the system:kube-apiserver-to-kubelet [ClusterRole](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#role-and-clusterrole)
with permissions to access the Kubelet API and perform most common tasks associated with managing pods on the worker nodes:

Run the below script on the Controller node:

```
cat <<EOF | kubectl apply --kubeconfig admin.kubeconfig -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
  labels:
    kubernetes.io/bootstrapping: rbac-defaults
  name: system:kube-apiserver-to-kubelet
rules:
  - apiGroups:
      - ""
    resources:
      - nodes/proxy
      - nodes/stats
      - nodes/log
      - nodes/spec
      - nodes/metrics
    verbs:
      - "*"
EOF
```

2. Bind the system:kube-apiserver-to-kubelet ClusterRole to the kubernetes user so that API server can authenticate successfully 
to the kubelets on the worker nodes:

```
cat <<EOF | kubectl apply --kubeconfig admin.kubeconfig -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: system:kube-apiserver
  namespace: ""
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:kube-apiserver-to-kubelet
subjects:
  - apiGroup: rbac.authorization.k8s.io
    kind: User
    name: kubernetes
EOF
```


## Bootstraping components on the worker nodes
The following components will be installed on each node:

- **kubelet**
- **kube-proxy**
- **Containerd or Docker**
- **Networking plugins**

1. SSH into the worker nodes

- Worker-1

```
worker_1_ip=$(aws ec2 describe-instances \
--filters "Name=tag:Name,Values=${NAME}-worker-0" \
--output text --query 'Reservations[].Instances[].PublicIpAddress')
ssh -i k8s-cluster-from-ground-up.id_rsa ubuntu@${worker_1_ip}
```

- Worker-2

```
worker_2_ip=$(aws ec2 describe-instances \
--filters "Name=tag:Name,Values=${NAME}-worker-1" \
--output text --query 'Reservations[].Instances[].PublicIpAddress')
ssh -i k8s-cluster-from-ground-up.id_rsa ubuntu@${worker_2_ip}
```

- Worker-3

```
worker_3_ip=$(aws ec2 describe-instances \
--filters "Name=tag:Name,Values=${NAME}-worker-2" \
--output text --query 'Reservations[].Instances[].PublicIpAddress')
ssh -i k8s-cluster-from-ground-up.id_rsa ubuntu@${worker_3_ip}
```


2. **Install OS dependencies:**

```
{
  sudo apt-get update
  sudo apt-get -y install socat conntrack ipset
}
```


## More about the dependencies:

- [socat](https://www.redhat.com/sysadmin/getting-started-socat). Socat is the default implementation for Kubernetes port-forwarding when 
using dockershim for the kubelet runtime. You will get to experience port-forwarding with Kubernetes in the next project. But what
is Dockershim?

- Dockershim was a temporary solution proposed by the Kubernetes community to add support for Docker so that it could serve as its
container runtime. You should always remember that Kubernetes can use different container runtime to run containers inside its pods.
For many years, Docker has been adopted widely and has been used as the container runtime for kubernetes. Hence the implementation 
that allowed docker is called the Dockershim. If you check the source [code of Dockershim](https://github.com/kubernetes/kubernetes/blob/770d3f181c5d7ed100d1ba43760a74093fc9d9ef/pkg/kubelet/dockershim/docker_streaming_others.go#L42), 
you will see that socat was used to implement the port-forwarding functionality.

- conntrack Connection tracking (“conntrack”) is a core feature of the Linux kernel’s networking stack. It allows the kernel to keep
track of all logical network connections or flows, and thereby identify all of the packets which make up each flow so they can be 
handled consistently together. It is essential for performant complex networking of Kubernetes where nodes need to track connection
information between thousands of pods and services.

- ipset is an extension to iptables which is used to configure firewall rules on a Linux server. ipset is a module extension to 
iptables that allows firewall configuration on a "set" of IP addresses. Compared with how iptables does the configuration linearly, 
ipset is able to store sets of addresses and index the data structure, making lookups very efficient, even when dealing with large
sets. Kubernetes uses ipsets to implement a distributed firewall solution that enforces network policies within the cluster. 
This can then help to further restrict communications across pods or namespaces. For example, if a namespace is configured with
DefaultDeny isolation type (Meaning no connection is allowed to the namespace from another namespace), network policies can be 
configured in the namespace to whitelist the traffic to the pods in that namespace.


