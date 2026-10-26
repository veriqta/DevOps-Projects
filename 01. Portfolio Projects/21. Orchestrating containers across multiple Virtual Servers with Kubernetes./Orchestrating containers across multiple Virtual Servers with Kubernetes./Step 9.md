# TEST THAT EVERYTHING IS WORKING FINE

1. To get the cluster details run:

```
kubectl cluster-info  --kubeconfig admin.kubeconfig
```

**OUTPUT:**

```
Kubernetes control plane is running at https://k8s-api-server.svc.total.io:6443

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

2. To get the current namespaces:

```
kubectl get namespaces --kubeconfig admin.kubeconfig
```

![7019](https://user-images.githubusercontent.com/85270361/210211191-7f775ab0-533f-40ec-aae0-2f2662eb2090.PNG)


3. To reach the Kubernetes API Server publicly

```
curl --cacert /var/lib/kubernetes/ca.pem https://$INTERNAL_IP:6443/version
```

![7020](https://user-images.githubusercontent.com/85270361/210211357-537df061-762f-4180-8c08-bccefc37a566.PNG)


4. To get the status of each component:

```
kubectl get componentstatuses --kubeconfig admin.kubeconfig
```

![7021](https://user-images.githubusercontent.com/85270361/210212939-8514d8c6-b276-45de-a682-9b7cde6cf588.PNG)


5. On one of the controller nodes, configure Role Based Access Control (RBAC) so that the api-server has necessary authorization for 
for the kubelet.

Create the ClusterRole:

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

Create the ClusterRoleBinding to bind the kubernetes user with the role created above:

```
cat <<EOF | kubectl --kubeconfig admin.kubeconfig  apply -f -
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

