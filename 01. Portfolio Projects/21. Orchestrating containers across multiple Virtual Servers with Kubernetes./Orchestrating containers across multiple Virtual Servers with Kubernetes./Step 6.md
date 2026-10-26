# `KUBECTL` TO GENERATE KUBERNETES CONFIGURATION FILES FOR AUTHENTICATION

All the work you are doing right now is ensuring that you do not face any difficulties by the time the Kubernetes cluster is up and 
running. In this step, you will create some files known as kubeconfig, which enables Kubernetes clients to locate and authenticate to 
the Kubernetes API Servers.

You will need a client tool called kubectl to do this. And, by the way, most of your time with Kubernetes will be spent using kubectl
commands.

Now it’s time to generate kubeconfig files for the kubelet, controller manager, kube-proxy, and scheduler clients and then the admin
user.

First, let us create a few environment variables for reuse by multiple commands.


```
KUBERNETES_API_SERVER_ADDRESS=$(aws elbv2 describe-load-balancers --load-balancer-arns 
${LOAD_BALANCER_ARN} --output text --query 'LoadBalancers[].DNSName')
```

1. Generate the kubelet kubeconfig file
For each of the nodes running the kubelet component, it is very important that the client certificate configured for that node is used
to generate the kubeconfig. This is because each certificate has the node’s DNS name or IP Address configured at the time the 
certificate was generated. It will also ensure that the appropriate authorization is applied to that node through the Node Authorizer

Below command must be run in the directory where all the certificates were generated.

```
for i in 0 1 2; do

instance="${NAME}-worker-${i}"
instance_hostname="ip-172-31-0-2${i}"

 # Set the kubernetes cluster in the kubeconfig file
  kubectl config set-cluster ${NAME} \
    --certificate-authority=ca.pem \
    --embed-certs=true \
    --server=https://$KUBERNETES_API_SERVER_ADDRESS:6443 \
    --kubeconfig=${instance}.kubeconfig

# Set the cluster credentials in the kubeconfig file
  kubectl config set-credentials system:node:${instance_hostname} \
    --client-certificate=${instance}.pem \
    --client-key=${instance}-key.pem \
    --embed-certs=true \
    --kubeconfig=${instance}.kubeconfig

# Set the context in the kubeconfig file
  kubectl config set-context default \
    --cluster=${NAME} \
    --user=system:node:${instance_hostname} \
    --kubeconfig=${instance}.kubeconfig

  kubectl config use-context default --kubeconfig=${instance}.kubeconfig
done
```


**Output:**

```
Cluster "k8s-cluster-from-ground-up" set.

User "system:node:ip-172-31-0-20.eu-central-1.compute.internal" set.

Context "default" created.

Switched to context "default".

Cluster "k8s-cluster-from-ground-up" set.

User "system:node:ip-172-31-0-21.eu-central-1.compute.internal" set.

Context "default" created.

Switched to context "default".

Cluster "k8s-cluster-from-ground-up" set.

User "system:node:ip-172-31-0-22.eu-central-1.compute.internal" set.

Context "default" created.

Switched to context "default".
```


**List the output**

```
ls -ltr *.kubeconfig
```

**OUTPUT:**

```
-rw-------  1 ann  staff  6602 22 Jun 20:40 k8s-cluster-from-ground-up-worker-0.kubeconfig
-rw-------  1 ann  staff  6602 22 Jun 20:40 k8s-cluster-from-ground-up-worker-1.kubeconfig
-rw-------  1 ann  staff  6606 22 Jun 20:40 k8s-cluster-from-ground-up-worker-2.kubeconfig
```

Open up the kubeconfig files generated and review the 3 different sections that have been configured:

- Cluster
- Credentials
- And Kube Context

Kubeconfig file is used to organize information about clusters, users, namespaces and authentication mechanisms. By default, kubectl
looks for a file named config in the $HOME/.kube directory. You can specify other kubeconfig files by setting the KUBECONFIG 
environment variable or by setting the --kubeconfig flag. To get to know more how to create your own kubeconfig files – 
[read this documentation](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/).

Context part of kubeconfig file defines three main parameters: cluster, namespace and user. You can save several different contexts
with any convenient names and switch between them when needed.

```
kubectl config use-context %context-name%
```

2. Generate the kube-proxy kubeconfig

```
{
  kubectl config set-cluster ${NAME} \
    --certificate-authority=ca.pem \
    --embed-certs=true \
    --server=https://${KUBERNETES_API_SERVER_ADDRESS}:6443 \
    --kubeconfig=kube-proxy.kubeconfig

  kubectl config set-credentials system:kube-proxy \
    --client-certificate=kube-proxy.pem \
    --client-key=kube-proxy-key.pem \
    --embed-certs=true \
    --kubeconfig=kube-proxy.kubeconfig

  kubectl config set-context default \
    --cluster=${NAME} \
    --user=system:kube-proxy \
    --kubeconfig=kube-proxy.kubeconfig

  kubectl config use-context default --kubeconfig=kube-proxy.kubeconfig
}
```

3. Generate the Kube-Controller-Manager kubeconfig
Notice that the --server is set to use 127.0.0.1. This is because, this component runs on the API-Server so there is no point 
routing through the Load Balancer.

```
{
  kubectl config set-cluster ${NAME} \
    --certificate-authority=ca.pem \
    --embed-certs=true \
    --server=https://127.0.0.1:6443 \
    --kubeconfig=kube-controller-manager.kubeconfig

  kubectl config set-credentials system:kube-controller-manager \
    --client-certificate=kube-controller-manager.pem \
    --client-key=kube-controller-manager-key.pem \
    --embed-certs=true \
    --kubeconfig=kube-controller-manager.kubeconfig

  kubectl config set-context default \
    --cluster=${NAME} \
    --user=system:kube-controller-manager \
    --kubeconfig=kube-controller-manager.kubeconfig

  kubectl config use-context default --kubeconfig=kube-controller-manager.kubeconfig
}
```


4. Generating the Kube-Scheduler Kubeconfig

```
{
  kubectl config set-cluster ${NAME} \
    --certificate-authority=ca.pem \
    --embed-certs=true \
    --server=https://127.0.0.1:6443 \
    --kubeconfig=kube-scheduler.kubeconfig

  kubectl config set-credentials system:kube-scheduler \
    --client-certificate=kube-scheduler.pem \
    --client-key=kube-scheduler-key.pem \
    --embed-certs=true \
    --kubeconfig=kube-scheduler.kubeconfig

  kubectl config set-context default \
    --cluster=${NAME} \
    --user=system:kube-scheduler \
    --kubeconfig=kube-scheduler.kubeconfig

  kubectl config use-context default --kubeconfig=kube-scheduler.kubeconfig
}
```

5. Finally, generate the kubeconfig file for the admin user

```
{
  kubectl config set-cluster ${NAME} \
    --certificate-authority=ca.pem \
    --embed-certs=true \
    --server=https://${KUBERNETES_API_SERVER_ADDRESS}:6443 \
    --kubeconfig=admin.kubeconfig

  kubectl config set-credentials admin \
    --client-certificate=admin.pem \
    --client-key=admin-key.pem \
    --embed-certs=true \
    --kubeconfig=admin.kubeconfig

  kubectl config set-context default \
    --cluster=${NAME} \
    --user=admin \
    --kubeconfig=admin.kubeconfig

  kubectl config use-context default --kubeconfig=admin.kubeconfig
}
```

**TASK: Distribute the files to their respective servers, using scp and a for loop like we have done previously. This is a test to 
validate that you understand which component must go to which node.**

