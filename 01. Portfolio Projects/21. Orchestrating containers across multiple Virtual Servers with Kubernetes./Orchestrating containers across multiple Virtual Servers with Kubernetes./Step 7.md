# PREPARE THE ETCD DATABASE FOR ENCRYPTION AT REST.

Kubernetes uses etcd (A distributed key value store) to store variety of data which includes the cluster state, application 
configurations, and secrets. By default, the data that is being persisted to the disk is not encrypted. Any attacker that is able to
gain access to this database can exploit the cluster since the data is stored in plain text. Hence, it is a security risk for Kubernetes
that needs to be addressed.

To mitigate this risk, we must prepare to encrypt etcd at rest. "At rest" means data that is stored and persists on a disk. Anytime you
hear "in-flight" or "in transit" refers to data that is being transferred over the network. "In-flight" encryption is done through TLS.

Generate the encryption key and encode it using base64

```
ETCD_ENCRYPTION_KEY=$(head -c 64 /dev/urandom | base64) 
```

See the output that will be generated when called. Yours will be a different random string.

echo $ETCD_ENCRYPTION_KEY

**OUTPUT:**

```
OuxSvV5XUQVid4fNNbeyFEDTUPr1yozZPQ+E6Eqj80m1FSVDB6jOHt9miD/7kMdJIvVshlMgxY80wFajlqItug===$
```

** Create an encryption-config.yaml file as 
[documented officially by kubernetes](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/#understanding-the-encryption-at-rest-configuration)


```
cat > encryption-config.yaml <<EOF
kind: EncryptionConfig
apiVersion: v1
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: ${ETCD_ENCRYPTION_KEY}
      - identity: {}
EOF
```

Send the encryption file to the Controller nodes using scp and a for loop.

**Bootstrap etcd cluster**
TIPS: Use a terminal multi-plexer like [multi-tabbed putty](https://youtu.be/0c1cWrMnZlc) or [tmux](https://youtu.be/Yl7NFenTgIo) to
work with multiple terminal sessions simultaneously. It will make your life easier, especially when you need to work on multiple 
nodes and run the same command across all nodes. Imagine repeating the same commands on 10 different nodes, and you don not intend
to start automating with a configuration management tool like Ansible yet.

The primary purpose of the etcd component is to store the state of the cluster. This is because Kubernetes itself is stateless.
Therefore, all its stateful data will persist in etcd. Since Kubernetes is a distributed system – it needs a distributed storage
to keep persistent data in it. etcd is a highly-available key value store that fits the purpose. All K8s cluster configurations
are stored in a form of key value pairs in etcd, it also stores the actual and desired states of the cluster. etcd cluster is
intelligent enough to watch for changes made on one instance and almost instantly replicate those changes to the rest of the
instances, so all of them will be always reconciled.

**NOTE:** Don not just copy and paste the commands, ensure that you go through each and understand exactly what they will do on your
servers. Use tools like tmux to make it easy to run commands on multiple terminal screens at once.

1. SSH into the controller server

- Master-1

```
master_1_ip=$(aws ec2 describe-instances \
--filters "Name=tag:Name,Values=${NAME}-master-0" \
--output text --query 'Reservations[].Instances[].PublicIpAddress')
ssh -i k8s-cluster-from-ground-up.id_rsa ubuntu@${master_1_ip}
```

- Master-2

```
master_2_ip=$(aws ec2 describe-instances \
--filters "Name=tag:Name,Values=${NAME}-master-1" \
--output text --query 'Reservations[].Instances[].PublicIpAddress')
ssh -i k8s-cluster-from-ground-up.id_rsa ubuntu@${master_2_ip}
```

- Master-3

```
master_3_ip=$(aws ec2 describe-instances \
--filters "Name=tag:Name,Values=${NAME}-master-2" \
--output text --query 'Reservations[].Instances[].PublicIpAddress')
ssh -i k8s-cluster-from-ground-up.id_rsa ubuntu@${master_3_ip}
```

You should have a a similar pane like below. You should be able to see all the files that have been sent to the nodes.

![7017](https://user-images.githubusercontent.com/85270361/210205971-b0fd812f-d764-4ed9-9e9f-9c9c98b4d378.PNG)


2. Download and install etcd

```
 wget -q --show-progress --https-only --timestamping \
  "https://github.com/etcd-io/etcd/releases/download/v3.4.15/etcd-v3.4.15-linux-amd64.tar.gz"
```

3. Extract and install the etcd server and the etcdctl command line utility:

```
{
tar -xvf etcd-v3.4.15-linux-amd64.tar.gz
sudo mv etcd-v3.4.15-linux-amd64/etcd* /usr/local/bin/
}
```

4. Configure the etcd server

```
{
  sudo mkdir -p /etc/etcd /var/lib/etcd
  sudo chmod 700 /var/lib/etcd
  sudo cp ca.pem master-kubernetes-key.pem master-kubernetes.pem /etc/etcd/
}
```

5. The instance internal IP address will be used to serve client requests and communicate with etcd cluster peers. Retrieve the
 internal IP address for the current compute instance:
 
 ```
 export INTERNAL_IP=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)
 ```
 
 6. Each etcd member must have a unique name within an etcd cluster. Set the etcd name to node Private IP address so it will uniquely 
 identify the machine:

```
ETCD_NAME=$(curl -s http://169.254.169.254/latest/user-data/ \
  | tr "|" "\n" | grep "^name" | cut -d"=" -f2)

echo ${ETCD_NAME}
```

7. Create the etcd.service systemd unit file:
The flags are well documented [here](https://www.bookstack.cn/read/etcd-3.2.17-en/717bafd59fa87192.md)

```
cat <<EOF | sudo tee /etc/systemd/system/etcd.service
[Unit]
Description=etcd
Documentation=https://github.com/coreos

[Service]
Type=notify
ExecStart=/usr/local/bin/etcd \\
  --name ${ETCD_NAME} \\
  --trusted-ca-file=/etc/etcd/ca.pem \\
  --peer-trusted-ca-file=/etc/etcd/ca.pem \\
  --peer-client-cert-auth \\
  --client-cert-auth \\
  --listen-peer-urls https://${INTERNAL_IP}:2380 \\
  --listen-client-urls https://${INTERNAL_IP}:2379,https://127.0.0.1:2379 \\
  --advertise-client-urls https://${INTERNAL_IP}:2379 \\
  --initial-cluster-token etcd-cluster-0 \\
  --initial-cluster master-0=https://172.31.0.10:2380,master-1=https://172.31.0.11:2380,master-2=https://172.31.0.12:2380 \\
  --cert-file=/etc/etcd/master-kubernetes.pem \\
  --key-file=/etc/etcd/master-kubernetes-key.pem \\
  --peer-cert-file=/etc/etcd/master-kubernetes.pem \\
  --peer-key-file=/etc/etcd/master-kubernetes-key.pem \\
  --initial-advertise-peer-urls https://${INTERNAL_IP}:2380 \\
  --initial-cluster-state new \\
  --data-dir=/var/lib/etcd
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

8. Start and enable the etcd Server

```
{
sudo systemctl daemon-reload
sudo systemctl enable etcd
sudo systemctl start etcd
}
```

9. Verify the etcd installation

```
sudo ETCDCTL_API=3 etcdctl member list \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/etcd/ca.pem \
  --cert=/etc/etcd/master-kubernetes.pem \
  --key=/etc/etcd/master-kubernetes-key.pem
```


**Output:** 
```
6709c481b5234095, started, master-0, https://172.31.0.10:2380, https://172.31.0.10:2379, false
ade74a4f39c39f33, started, master-1, https://172.31.0.11:2380, https://172.31.0.11:2379, false
ed33b44c0b153ee3, started, master-2, https://172.31.0.12:2380, https://172.31.0.12:2379, false
```


```
systemctl status etcd
```

![7018](https://user-images.githubusercontent.com/85270361/210208317-3f56bbad-6ad4-49e7-a371-0eebce37fdc6.PNG)
