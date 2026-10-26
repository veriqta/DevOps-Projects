# COMMON KUBERNETES OBJECTS

- Pod
- Namespace
- ResplicaSet (Manages Pods)
- DeploymentController (Manages Pods)
- StatefulSet
- DaemonSet
- Service
- ConfigMap
- Volume
- Job/Cronjob


The very first concept to understand is the difference between how Docker and Kubernetes run containers – with Docker, every docker 
run command will run an image (representing an application) as a container. The running container is a Docker’s smallest entity,
it is the most basic deployable object. Kubernetes on the other hand operates with pods instead of containers, a pods encapsulates
a container. Kubernetes uses pods as its smallest, and most basic deployable object with a unique feature that allows it to run
multiple containers within a single Pod. It is not the most common pattern – to have more than one container in a Pod, but there 
are cases when this capability comes in handy.

In the world of docker, or docker compose, to run the Tooling app, you must deploy separate containers for the application and the
database. But in the world of Kubernetes, you can run both: application and database containers in the same Pod. When multiple
containers run within the same Pod, they can directly communicate with each other as if they were running on the same localhost.
Although running both the application and database in the same Pod is NOT a recommended approach.

A Pod that contains one container is called single container pod and it is the most common Kubernetes use case. A Pod that contains
multiple co-related containers is called multi-container pod. There are few patterns for multi-container Pods; one of them is
the [sidecar](https://medium.com/bb-tutorials-and-thoughts/kubernetes-learn-sidecar-container-pattern-6d8c21f873d) container 
pattern – it means that in the same Pod there is a main container and an auxiliary one that extends and enhances the functionality 
of the main one without changing it.

There are other patterns, such as: [init container](https://medium.com/bb-tutorials-and-thoughts/kubernetes-learn-init-container-pattern-7a757742de6b) 
[adapter container](https://medium.com/bb-tutorials-and-thoughts/kubernetes-learn-adaptor-container-pattern-97674285983c), 
[ambassador container](https://medium.com/bb-tutorials-and-thoughts/kubernetes-learn-ambassador-container-pattern-bc2e1331bd3a). These
are more advanced topics that you can study on your own, let us continue with the other objects.

We will not go into the theoretical details of all the objects, rather we will begin to experience them in action.

Understanding the common YAML fields for every Kubernetes object
Every Kubernetes object includes object fields that govern the object’s configuration:


- **kind:** Represents the type of kubernetes object created. It can be a Pod, DaemonSet, Deployments or Service.
- **version:** Kubernetes api version used to create the resource, it can be v1, v1beta and v2. Some of the kubernetes features 
can be released under beta and available for general public usage.
- **metadata:** provides information about the resource like name of the Pod, namespace under which the Pod will be running,
labels and annotations.
- **spec:** consists of the core information about Pod. Here we will tell kubernetes what would be the expected state of resource, 
Like container image, number of replicas, environment variables and volumes.
- **status:** consists of information about the running object, status of each container. Status field is supplied and updated by 
Kubernetes after creation. This is not something you will have to put in the YAML manifest.


Deploying a random Pod
Lets see what it looks like to have a Pod running in a k8s cluster. This section is just to illustrate and get you to familiarise
with how the object’s fields work. Lets deploy a basic Nginx container to run inside a Pod.

- apiVersion is v1
- kind is Pod
- metatdata has a name which is set to nginx-pod
- The spec section has further information about the Pod. Where to find the image to run the container – (This defaults to Docker Hub),
 the port and protocol.
The structure is similar for any Kubernetes objects, and you will get to see them all as we progress.

1. Create a Pod yaml manifest on your master node

```
sudo cat <<EOF | sudo tee ./nginx-pod.yaml
apiVersion: v1
kind: Pod
metadata:
name: nginx-pod
spec:
containers:
- image: nginx:latest
name: nginx-pod
ports:
- containerPort: 80
  protocol: TCP
EOF
```

2. Apply the manifest with the help of kubectl

```
kubectl apply -f nginx-pod.yaml
```

**Output:**

```
pod/nginx-pod created
```

3. Get an output of the pods running in the cluster

```
kubectl get pods
```

**Output:*8
```
NAME        READY   STATUS    RESTARTS   AGE
nginx-pod   1/1     Running   0          19m
```

4. If the Pods were not ready for any reason, for example if there are no worker nodes, you will see something like the below output.

```
NAME        READY   STATUS    RESTARTS   AGE
nginx-pod   0/1     Pending   0          111s
```

5. To see other fields introduced by kubernetes after you have deployed the resource, simply run below command, and examine the
output. You will see other fields that kubernetes updates from time to time to represent the state of the resource within the
cluster. -o simply means the output format.

```
kubectl get pod nginx-pod -o yaml 
```

or

```
kubectl describe pod nginx-pod
```


