# CONFIGURE THE WORKER NODES COMPONENTS

9. Configure kubelet:
In the home directory, you should have the certificates and kubeconfig file for each node. A list in the home folder should look like
below:

![7023](https://user-images.githubusercontent.com/85270361/210217585-e9b599af-15aa-4879-a35c-ca4cd5ce98b5.PNG)

Configuring the network

Get the POD_CIDR that will be used as part of network configuration

```
POD_CIDR=$(curl -s http://169.254.169.254/latest/user-data/ \
  | tr "|" "\n" | grep "^pod-cidr" | cut -d"=" -f2)
echo "${POD_CIDR}"
```

In case you are wondering where this POD_CIDR is coming from. Well, this was configured at the time of creating the worker nodes. 
Remember the for loop below? The --user-data flag is where we specified what we want the POD_CIDR to be. It is very important to 
ensure that the CIDR does not overlap with EC2 IPs within the subnet. In the real world, this will be decided in collaboration with
the Network team.

Why do we need a network plugin? And why network configuration is crucial to implementing a Kubernetes cluster?

First, let us understand the Kubernetes networking model:

The networking model assumes a flat network, in which containers and nodes can communicate with each other. That means, regardless 
of which node is running the container in the cluster, Kubernetes expects that all the containers must be able to communicate with
each other. Therefore, any network interface used for a Kubernetes implementation must follow this requirement. Otherwise, containers
running in [pods](https://kubernetes.io/docs/concepts/workloads/pods/) will not be able to communicate. Of course, this has 
security concerns. Because if an attacker is able to get into the cluster through a compromised container, then the entire cluster 
can be exploited.

To mitigate security risks and have a better controlled network topology, Kubernetes uses
[CNI (Container Network Interface)](https://github.com/containernetworking/cni) to manage 
[Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) which can be used to
operate the Pod network through external plugins such as [Calico](https://projectcalico.docs.tigera.io/about/about-calico), 
[Flannel](https://github.com/flannel-io/flannel#flannel) or [Weave Net](https://www.weave.works/oss/net/) to name a few. With these,
you can set policies similar to how you would configure segurity groups in AWS and limit network communications through either
cidr ipBlock, namespaceSelectors, or podSelectors, you will see more of these concepts further on.

To really understand Kubernetes further, let us explore some basic concepts around its networking:

Pods:

[A Pod](https://kubernetes.io/docs/concepts/workloads/pods/) is the basic building block of Kubernetes; it is the smallest and 
simplest unit in the Kubernetes object model that you create or deploy. A Pod represents a running process on your cluster.

It encapsulates a container running an application such as the Tooling website (or, in some cases, multiple containers), storage 
resources, a unique network IP, and options that govern how the container(s) should run. All the containers running inside a Pod 
can reach each other on localhost.

For example, if you deploy both Tooling and MySQL containers inside the same pod, then both of them are considered running on 
localhost. Although this design pattern is not ideal. Most likely they will run in separate Pods. In most cases one Pod contains
just one container, but there are some design patterns that imply multi-container pods (e.g. sidecar, ambassador, adapter) – you
can read more about them in this [article](https://betterprogramming.pub/understanding-kubernetes-multi-container-pod-patterns-577f74690aee).

For a better understanding, of Kubernetes networking, let us assume that we have 2-containers in a single Pod and we have 2 such
Pods (we can actually have as many pods of the same composition as our node resources would allow).

Network configuration will look like this:

![7024](https://user-images.githubusercontent.com/85270361/210218596-85a1d610-c849-41c3-bf05-c682e1c58846.PNG)


Notice, that both containers share a single virtual network interface veth0 that belongs to a virtual network within a single node.
This virtual interface veth0 is used to allow communication from a pod to the outer world through a bridge cbr0 (custom bridge). 
This bridge is an interface that forwards the traffic from the Pods on one node to other nodes through a physical network interface
eth0. Routing between the nodes is done by means of a router with the routing table.


For more detailed explanation of different aspects of Kubernetes networking – [watch this video](https://www.youtube.com/watch?v=5cNrTU6o3Fw).

**Pod Network**

You must decide on the Pod CIDR per worker node. Each worker node will run multiple pods, and each pod will have its own IP address.
IP address of a particular Pod on worker node 1 should be able to communicate with the IP address of another particular Pod on 
worker node 2. For this to become possible, there must be a bridge network with virtual network interfaces that connects them all
together. [Here is an interesting read](https://www.digitalocean.com/community/tutorials/kubernetes-networking-under-the-hood) that 
goes a little deeper into how it works Bookmark that page and read it over and over again after you have completed this project


10 Configure the bridge and loopback networks
Bridge:

```
cat > 172-20-bridge.conf <<EOF
{
    "cniVersion": "0.3.1",
    "name": "bridge",
    "type": "bridge",
    "bridge": "cnio0",
    "isGateway": true,
    "ipMasq": true,
    "ipam": {
        "type": "host-local",
        "ranges": [
          [{"subnet": "${POD_CIDR}"}]
        ],
        "routes": [{"dst": "0.0.0.0/0"}]
    }
}
EOF
```

Loopback:


```
cat > 99-loopback.conf <<EOF
{
    "cniVersion": "0.3.1",
    "type": "loopback"
}
EOF
```

11. Move the files to the network configuration directory:

```
sudo mv 172-20-bridge.conf 99-loopback.conf /etc/cni/net.d/
```

12. Store the worker’s name in a variable:

```
NAME=k8s-cluster-from-ground-up
WORKER_NAME=${NAME}-$(curl -s http://169.254.169.254/latest/user-data/ \
  | tr "|" "\n" | grep "^name" | cut -d"=" -f2)
echo "${WORKER_NAME}"
```

13. Move the certificates and kubeconfig file to their respective configuration directories:

```
sudo mv ${WORKER_NAME}-key.pem ${WORKER_NAME}.pem /var/lib/kubelet/
sudo mv ${WORKER_NAME}.kubeconfig /var/lib/kubelet/kubeconfig
sudo mv kube-proxy.kubeconfig /var/lib/kube-proxy/kubeconfig
sudo mv ca.pem /var/lib/kubernetes/
```

14. Create the kubelet-config.yaml file
Ensure the needed variables exist:

```
NAME=k8s-cluster-from-ground-up
WORKER_NAME=${NAME}-$(curl -s http://169.254.169.254/latest/user-data/ \
  | tr "|" "\n" | grep "^name" | cut -d"=" -f2)
echo "${WORKER_NAME}"
```

```
cat <<EOF | sudo tee /var/lib/kubelet/kubelet-config.yaml
kind: KubeletConfiguration
apiVersion: kubelet.config.k8s.io/v1beta1
authentication:
  anonymous:
    enabled: false
  webhook:
    enabled: true
  x509:
    clientCAFile: "/var/lib/kubernetes/ca.pem"
authorization:
  mode: Webhook
clusterDomain: "cluster.local"
clusterDNS:
  - "10.32.0.10"
resolvConf: "/etc/resolv.conf"
runtimeRequestTimeout: "15m"
tlsCertFile: "/var/lib/kubelet/${WORKER_NAME}.pem"
tlsPrivateKeyFile: "/var/lib/kubelet/${WORKER_NAME}-key.pem"
EOF
```
