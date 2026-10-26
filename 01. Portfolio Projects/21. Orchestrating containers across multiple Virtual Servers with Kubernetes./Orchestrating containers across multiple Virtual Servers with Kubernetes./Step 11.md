# QUICK OVERVIEW OF KUBERNETES NETWORK POLICY AND HOW IT IS IMPLEMENTED

Kubernetes network policies are application centric compared to infrastructure/network centric standard firewalls. There are no 
explicit CIDR or IP used for matching source or destination IP’s. Network policies build up on labels and selectors which are key
concepts of Kubernetes that are used for proper organization (for e.g dedicating a namespace to data layer and controlling which app
is able to connect there). A typical network policy that controls who can connect to the database namespace will look like below:

```
apiVersion: extensions/v1beta1
kind: NetworkPolicy
metadata:
  name: database-network-policy
  namespace: tooling-db
spec:
  podSelector:
    matchLabels:
      app: mysql
  ingress:
   - from:
     - namespaceSelector:
       matchLabels:
         app: tooling
     - podSelector:
       matchLabels:
       role: frontend
   ports:
     - protocol: tcp
     port: 3306
```

NOTE: Best practice is to use solutions like RDS for database implementation. So the above is just to help you understand the concept.

3. Disable Swap
If [swap](https://opensource.com/article/18/9/swap-space-linux-systems)) is not disabled, kubelet will not start. It is highly
recommended to allow Kubernetes to handle resource allocation.

Test if swap is already enabled on the host:

```
sudo swapon --show
```

If there is no output, then you are good to go. Otherwise, run below command to turn it off

```
sudo swapoff -a
```


4. Download and install a container runtime. (Docker Or Containerd)
Before you install any container runtime, you need to understand that Docker is now deprecated, and Kubernetes no longer supports 
the Dockershim codebase from v1.20 release

[Read more about this notice here](https://kubernetes.io/blog/2020/12/02/dockershim-faq/)

If you install Docker, it will work. But be aware of this huge change.

NOTE: Do not install docker and containerd on the same machine, you will have to choose which container runtime you want to run on 
the node.


- **Docker**

```
sudo apt update -y && \
sudo apt -y install apt-transport-https ca-certificates curl software-properties-common && \
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && \
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable" && \
sudo apt update -y && \
apt-cache policy docker-ce && \
sudo apt -y install docker-ce && \
sudo usermod -aG docker ${USER} && \
sudo systemctl status docker
```


NOTE: exit the shell and log back in. Otherwise, you will face a permission denied error. Alternatively, you can run newgrp docker
without exiting the shell. But you will need to provide the password of the logged in user


- **Containerd**

Download binaries for runc, cri-ctl, and containerd

```
wget https://github.com/opencontainers/runc/releases/download/v1.0.0-rc93/runc.amd64 \
  https://github.com/kubernetes-sigs/cri-tools/releases/download/v1.21.0/crictl-v1.21.0-linux-amd64.tar.gz \
  https://github.com/containerd/containerd/releases/download/v1.4.4/containerd-1.4.4-linux-amd64.tar.gz 
```

Configure containerd:

```
{
  mkdir containerd
  tar -xvf crictl-v1.21.0-linux-amd64.tar.gz
  tar -xvf containerd-1.4.4-linux-amd64.tar.gz -C containerd
  sudo mv runc.amd64 runc
  chmod +x  crictl runc  
  sudo mv crictl runc /usr/local/bin/
  sudo mv containerd/bin/* /bin/
}
```

```
sudo mkdir -p /etc/containerd/
```

```
cat << EOF | sudo tee /etc/containerd/config.toml
[plugins]
  [plugins.cri.containerd]
    snapshotter = "overlayfs"
    [plugins.cri.containerd.default_runtime]
      runtime_type = "io.containerd.runtime.v1.linux"
      runtime_engine = "/usr/local/bin/runc"
      runtime_root = ""
EOF
```

Create the containerd.service systemd unit file:

```
cat <<EOF | sudo tee /etc/systemd/system/containerd.service
[Unit]
Description=containerd container runtime
Documentation=https://containerd.io
After=network.target

[Service]
ExecStartPre=/sbin/modprobe overlay
ExecStart=/bin/containerd
Restart=always
RestartSec=5
Delegate=yes
KillMode=process
OOMScoreAdjust=-999
LimitNOFILE=1048576
LimitNPROC=infinity
LimitCORE=infinity

[Install]
WantedBy=multi-user.target
EOF
```

5. Create directories for to configure kubelet, kube-proxy, cni, and a directory to keep the kubernetes root ca file:

```
sudo mkdir -p \
  /var/lib/kubelet \
  /var/lib/kube-proxy \
  /etc/cni/net.d \
  /opt/cni/bin \
  /var/lib/kubernetes \
  /var/run/kubernetes
```

6. Download and Install CNI
CNI (Container Network Interface), a [Cloud Native Computing Foundation project](https://www.cncf.io/), 
consists of a specification and libraries for writing plugins to configure network interfaces in Linux containers. It also comes 
with a number of plugins.

Kubernetes uses CNI as an interface between network providers and Kubernetes Pod networking. Network providers create network 
plugin that can be used to implement the Kubernetes networking, and includes additional set of rich features that Kubernetes does 
not provide out of the box.

Download the plugins available from [containernetworking’s GitHub repo ](https://github.com/containernetworking/cni)and read more
about CNIs and why it is being developed.

```
wget -q --show-progress --https-only --timestamping \
  https://github.com/containernetworking/plugins/releases/download/v0.9.1/cni-plugins-linux-amd64-v0.9.1.tgz
```

Install CNI into /opt/cni/bin/

```
sudo tar -xvf cni-plugins-linux-amd64-v0.9.1.tgz -C /opt/cni/bin/
```

The output shows the plugins that comes with the CNI.


```
./
./macvlan
./flannel
./static
./vlan
./portmap
./host-local
./vrf
./bridge
./tuning
./firewall
./host-device
./sbr
./loopback
./dhcp
./ptp
./ipvlan
./bandwidth
```

There are few other plugins that are not included in the CNI, which are also widely used in the industry. They all have their unique 
implementation approach and set of features.

Click to read more about each of the network plugins below:

- [Calico](https://www.tigera.io/project-calico/)
- [Weave Net](https://www.weave.works/docs/net/latest/overview/)
- [flannel](https://github.com/flannel-io/flannel)


![7022](https://user-images.githubusercontent.com/85270361/210216885-fb77837e-2b0d-42f5-88b9-80464159fb49.PNG)

[source](https://ranchermanager.docs.rancher.com/v2.5/faq/container-network-interface-providers)


Sometimes you can combine more than one plugin together to maximize the use of features from different providers. Or simply use
a CNI network provider such as [canal](https://github.com/projectcalico/canal) that gives you the best of Flannel and Calico.


7. Download binaries for kubectl, kube-proxy, and kubelet

```
wget -q --show-progress --https-only --timestamping \
  https://storage.googleapis.com/kubernetes-release/release/v1.21.0/bin/linux/amd64/kubectl \
  https://storage.googleapis.com/kubernetes-release/release/v1.21.0/bin/linux/amd64/kube-proxy \
  https://storage.googleapis.com/kubernetes-release/release/v1.21.0/bin/linux/amd64/kubelet
```

8. Install the downloaded binaries

```
{
  chmod +x  kubectl kube-proxy kubelet  
  sudo mv  kubectl kube-proxy kubelet /usr/local/bin/
}
```





