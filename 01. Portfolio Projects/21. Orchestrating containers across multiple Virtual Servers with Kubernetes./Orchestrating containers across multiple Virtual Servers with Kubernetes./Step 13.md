# FINAL STEPS

Let us talk about the configuration file kubelet-config.yaml and the actual configuration for a bit. Before creating the systemd file
for kubelet, it is recommended to create the kubelet-config.yaml and set the configuration there rather than using multiple startup 
flags in systemd. You will simply point to the yaml file.

The config file specifies where to find certificates, the DNS server, and authentication information. As you already know, kubelet
is responsible for the containers running on the node, regardless if the runtime is Docker or Containerd; as long as the containers
are being created through Kubernetes, kubelet manages them. If you run any docker or cri commands directly on a worker to create a
container, bear in mind that Kubernetes is not aware of it, therefore kubelet will not manage those. Kubelet’s major responsibility
is to always watch the containers in its care, by default every 20 seconds, and ensuring that they are always running. Think of it as
a process watcher.

The clusterDNS is the address of the DNS server. As of Kubernetes v1.12, CoreDNS is the recommended DNS Server, hence we will go
with that, rather than using legacy kube-dns.

Note: The CoreDNS Service is named kube-dns(When you see kube-dns, just know that it is using CoreDNS). This is more of a backward 
compatibility reasons for workloads that relied on the legacy kube-dns Service name.

In Kubernetes, Pods are able to find each other using service names through the internal DNS server. Every time a service is created,
it gets registered in the DNS server.

In Linux, the /etc/resolv.conf file is where the DNS server is configured. If you want to use Google’s public DNS server (8.8.8.8) 
your /etc/resolv.conf file will have following entry:

nameserver 8.8.8.8

In Kubernetes, the kubelet process on a worker node configures each pod. Part of the configuration process is to create the 
file /etc/resolv.conf and specify the correct DNS server.

15. Configure the kubelet systemd service

```
cat <<EOF | sudo tee /etc/systemd/system/kubelet.service
[Unit]
Description=Kubernetes Kubelet
Documentation=https://github.com/kubernetes/kubernetes
After=containerd.service
Requires=containerd.service
[Service]
ExecStart=/usr/local/bin/kubelet \\
  --config=/var/lib/kubelet/kubelet-config.yaml \\
  --cluster-domain=cluster.local \\
  --container-runtime=remote \\
  --container-runtime-endpoint=unix:///var/run/containerd/containerd.sock \\
  --image-pull-progress-deadline=2m \\
  --kubeconfig=/var/lib/kubelet/kubeconfig \\
  --network-plugin=cni \\
  --register-node=true \\
  --v=2
Restart=on-failure
RestartSec=5
[Install]
WantedBy=multi-user.target
EOF
```

16. Create the kube-proxy.yaml file

```
cat <<EOF | sudo tee /var/lib/kube-proxy/kube-proxy-config.yaml
kind: KubeProxyConfiguration
apiVersion: kubeproxy.config.k8s.io/v1alpha1
clientConnection:
  kubeconfig: "/var/lib/kube-proxy/kubeconfig"
mode: "iptables"
clusterCIDR: "172.31.0.0/16"
EOF
```

17. Configure the Kube Proxy systemd service

```
cat <<EOF | sudo tee /etc/systemd/system/kube-proxy.service
[Unit]
Description=Kubernetes Kube Proxy
Documentation=https://github.com/kubernetes/kubernetes
[Service]
ExecStart=/usr/local/bin/kube-proxy \\
  --config=/var/lib/kube-proxy/kube-proxy-config.yaml
Restart=on-failure
RestartSec=5
[Install]
WantedBy=multi-user.target
EOF
```


18. Reload configurations and start both services

```
{
  sudo systemctl daemon-reload
  sudo systemctl enable containerd kubelet kube-proxy
  sudo systemctl start containerd kubelet kube-proxy
}
```

Now you should have the worker nodes joined to the cluster, and in a READY state.

![7025](https://user-images.githubusercontent.com/85270361/210220368-9ba0b7a0-40b1-43e1-8f51-11387d43d66d.PNG)


Troubleshooting Tips: If you have issues at this point. Consider the below:

1. Use journalctl -u <service name> to get the log output and read what might be wrong with starting up the service. You can redirect 
the output into a file and analyse it.
2. Review your PKI setup again. Ensure that the certificates you generated have the hostnames properly configured.
3. It is okay to start all over again. Each time you attempt the solution is an opportunity to learn something.


**Congratulations!**
You have created your first Kubernetes cluster From-Ground-Up! It was not an easy task, but you have learned how different components
of K8s work together – it will help you not just in creation your clusters in the real work experience, but also to maintain and
troubleshoot them further.
  
  
![7026](https://user-images.githubusercontent.com/85270361/210220671-d8b9b135-c3a6-4ddf-b422-1ee4f047c2ba.PNG)
 
  
Proceed to the next exciting PBL projects to practice more Kubernetes and other cool technologies with us!
