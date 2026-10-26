# PERSISTING DATA IN KUBERNETES

NOTE: Create EKS cluster first before the below section

Now we know that containers are stateless by design, which means that data does not persist in the containers. Even when you run 
the containers in kubernetes pods, they still remain stateless unless you ensure that your configuration supports statefulness.

To achieve statefuleness in kubernetes, you must understand how volumes, persistent volumes, and persistent volume claims work.

Volumes
On-disk files in a container are ephemeral, which presents some problems for non-trivial applications when running in containers. 
One problem is the loss of files when a container crashes. The kubelet restarts the container but with a clean state. A second
problem occurs when sharing files between containers running together in a Pod. The Kubernetes volume abstraction solves both of 
these problems

Docker has a concept of volumes, though it is somewhat looser and less managed. A Docker volume is a directory on disk or in another 
container. Docker provides volume drivers, but the functionality is somewhat limited.

Kubernetes supports many types of volumes. A Pod can use any number of volume types simultaneously. Ephemeral volume types have a 
lifetime of a pod, but persistent volumes exist beyond the lifetime of a pod. When a pod ceases to exist, Kubernetes destroys 
ephemeral volumes; however, Kubernetes does not destroy persistent volumes. For any kind of volume in a given pod, data is 
preserved across container restarts.

At its core, a volume is a directory, possibly with some data in it, which is accessible to the containers in a pod. How that 
directory comes to be, the medium that backs it, and the contents of it are all determined by the particular volume type used. 
This means, you must know some of the different types of volumes available in kubernetes before choosing what is ideal for your 
particular use case.

Lets have a look at a few of them.

awsElasticBlockStore
An awsElasticBlockStore volume mounts an Amazon Web Services (AWS) EBS volume into your pod. The contents of an EBS volume are 
persisted and the volume is only unmmounted when the pod crashes, or terminates. This means that an EBS volume can be pre-populated
with data, and that data can be shared between pods.

Lets see what it looks like for our Nginx pod to persist data using awsElasticBlockStore volume


```
sudo cat <<EOF | sudo tee ./nginx-pod.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    tier: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
      volumes:
      - name: nginx-volume
        # This AWS EBS volume must already exist.
        awsElasticBlockStore:
          volumeID: "<volume id>"
          fsType: ext4
EOF
```

The volume section indicates the type of volume to be used to ensure persistence.

If you notice the config above carefully, you will realise that there is need to provide a volumeID before the deployment will work. 
Therefore, You must create an EBS volume by using aws ec2 create-volume command or the AWS console.

Before you create a volume, lets run the nginx deployment into kubernetes without a volume.


```
sudo cat <<EOF | sudo tee ./nginx-pod.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    tier: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
EOF
```

Tasks

- Verify that the pod is running
- Check the logs of the pod
- Exec into the pod and navigate to the nginx configuration file /etc/nginx/conf.d
- Open the config files to see the default configuration.

NOTE: There are some restrictions when using an awsElasticBlockStore volume:

- The nodes on which pods are running must be AWS EC2 instances
- Those instances need to be in the same region and availability zone as the EBS volume
- EBS only supports a single EC2 instance mounting a volume

Now that we have the pod running without a volume, Lets now create a volume from the AWS console.

1. In your AWS console, head over to the EC2 section and scroll down to the Elastic Block Storage menu.
2. Click on Volumes
3. At the top right, click on Create Volume


![7037](https://user-images.githubusercontent.com/85270361/210249210-c7d8b090-c45d-435a-ae15-78535bf6ead8.PNG)


Part of the requirements is to ensure that the volume exists in the same region and availability zone as the EC2 instance running 
the pod. Hence, we need to find out

- Which node is running the pod (replace the pod name with yours)

```
kubectl get po nginx-deployment-6fdcffd8fc-thcfp -o wide
```


**Output:**
```
NAME                                READY   STATUS    RESTARTS   AGE   IP           NODE                                       NOMINATED NODE   READINESS GATES
nginx-deployment-6fdcffd8fc-thcfp   1/1     Running   0          64m   10.0.3.159   ip-10-0-3-233.eu-west-2.compute.internal   <none>           <none>
```

The NODE column shows the node the pode is running on

- In which Availability Zone the node is running.

```
kubectl describe node ip-10-0-3-233.eu-west-2.compute.internal 
```

The information is written in the labels section of the descibe command.


![7038](https://user-images.githubusercontent.com/85270361/210250681-38c07c29-9ff7-471e-b121-213c2d5940f3.PNG)


So, in the case above, we know the AZ for the node is in eu-west-2c hence, the volume must be created in the same AZ. Choose the 
size of the required volume.

The create volume selection should be like:


![7039](https://user-images.githubusercontent.com/85270361/210250976-f2fa6644-b225-4669-8662-f40edd17e171.PNG)


5. Copy the VolumeID


![7040](https://user-images.githubusercontent.com/85270361/210251775-3492571a-4f5f-42ef-b52c-576d27110534.PNG)


6. Update the deployment configuration with the volume spec.

```
sudo cat <<EOF | sudo tee ./nginx-pod.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    tier: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
      volumes:
      - name: nginx-volume
        # This AWS EBS volume must already exist.
        awsElasticBlockStore:
          volumeID: "vol-0e194e56f1b5302ee"
          fsType: ext4
EOF
```

Apply the new configuration and check the pod. As you can see, the old pod is being terminated while the updated one is up and running.


![7041](https://user-images.githubusercontent.com/85270361/210252124-4b42d5c3-b728-4964-990a-a3fad4d0df09.PNG)


Now, the new pod has a volume attached to it, and can be used to run a container for statefuleness. Go ahead and explore the 
running pod. Run describe on both the pod and deployment

At this point, even though the pod can be used for a stateful application, the configuration is not yet complete. This is because, 
the volume is not yet mounted onto any specific filesystem inside the container. The directory /usr/share/nginx/html which holds 
the software/website code is still ephemeral, and if there is any kind of update to the index.html file, the new changes will only 
be there for as long as the pod is still running. If the pod dies after, all previously written data will be erased.

To complete the configuration, we will need to add another section to the deployment yaml manifest. The volumeMounts which basically 
answers the question "Where should this Volume be mounted inside the container?" Mounting a volume to a directory means that all data
written to the directory will be stored on that volume.

Lets do that now.


```
cat <<EOF | tee ./nginx-pod.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    tier: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
        volumeMounts:
        - name: nginx-volume
          mountPath: /usr/share/nginx/
      volumes:
      - name: nginx-volume
        # This AWS EBS volume must already exist.
        awsElasticBlockStore:
          volumeID: "  vol-07b537651bbe68be0"
          fsType: ext4
EOF
```

Notice the newly added section:

```
 volumeMounts:
        - name: nginx-volume
          mountPath: /usr/share/nginx/
```


- The value provided to name in volumeMounts must be the same value used in the volumes section. It basically means mount the 
volume with the name provided, to the provided mountpath

In as much as we now have a way to persist data, we also have new problems.

1. If you port forward the service and try to reach the endpoint, you will get a 403 error. This is because mounting a volume on a
 filesystem that already contains data will automatically erase all the existing data. This strategy for statefulness is preferred
 if the mounted volume already contains the data which you want to be made available to the container
 
 
![7042](https://user-images.githubusercontent.com/85270361/210252594-005fa78b-ec52-4274-9db6-c1b2a00efefc.PNG)

2. It is still a manual process to create a volume, manually ensure that the volume created is in the same Avaioability zone in
 which the pod is running, and then update the manifest file to use the volume ID. All of these is against DevOps principles because
 it will mean having a lot of road blocks to getting a simple thing done.

The more elegant way to achieve this is through Persistent Volume and Persistent Volume claims.

In kubernetes, there are many elegant ways of persisting data. Each of which is used to satisfy different use cases. Lets take a 
look at the different options available.

1. Persistent Volume (PV) and Persistent Volume Claim (PVC)
2. configMap

 
