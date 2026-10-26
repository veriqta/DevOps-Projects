# CREATE A REPLICA SET

Let us create a rs.yaml manifest for a ReplicaSet object:

```
#Part 1
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: nginx-rs
spec:
  replicas: 3
  selector:
    app: nginx-pod
#Part 2
  template:
    metadata:
      name: nginx-pod
      labels:
         app: nginx-pod
    spec:
      containers:
      - image: nginx:latest
        name: nginx-pod
        ports:
        - containerPort: 80
          protocol: 
```


```
kubectl apply -f rs.yaml
```

The manifest file of ReplicaSet consist of the following fields:

- apiVersion: This field specifies the version of kubernetes Api to which the object belongs. ReplicaSet belongs to apps/v1 apiVersion.
- kind: This field specify the type of object for which the manifest belongs to. Here, it is ReplicaSet.
- metadata: This field includes the metadata for the object. It mainly includes two fields: name and labels of the ReplicaSet.
- spec: This field specifies the label selector to be used to select the Pods, number of replicas of the Pod to be run and the 
container or list of containers which the Pod will run. In the above example, we are running 3 replicas of nginx container.

Let us check what Pods have been created:

```
kubectl get pods
```


```
NAME              READY   STATUS    RESTARTS   AGE     IP               NODE                                              NOMINATED NODE   READINESS GATES
nginx-pod-j784r   1/1     Running   0          7m41s   172.50.197.5     ip-172-50-197-52.eu-central-1.compute.internal    <none>           <none>
nginx-pod-kg7v6   1/1     Running   0          7m41s   172.50.192.152   ip-172-50-192-173.eu-central-1.compute.internal   <none>           <none>
nginx-pod-ntbn4   1/1     Running   0          7m41s   172.50.202.162   ip-172-50-202-18.eu-central-1.compute.internal    <none>           <none>
```


Here we see three ngix-pods with some random suffixes (e.g., -j784r) – it means, that these Pods were created and named
automatically by some other object (higher level of abstraction) such as ReplicaSet.

Try to delete one of the Pods:

```
kubectl delete po nginx-pod-j784r
```

**Output:**

```
pod "nginx-pod-j784r" deleted
```

```
❯ kubectl get pods
NAME              READY   STATUS    RESTARTS   AGE
nginx-rc-7xt8z   1/1     Running   0          22s
nginx-rc-kg7v6   1/1     Running   0          34m
nginx-rc-ntbn4   1/1     Running   0          34m
```

You can see, that we still have all 3 Pods, but one has been recreated (can you differentiate the new one?)

Explore the ReplicaSet created:

```
kubectl get rs -o wide
```


**Output:**

```
NAME        DESIRED   CURRENT   READY   AGE   CONTAINERS   IMAGES         SELECTOR
nginx-rs   3         3         3       34m   nginx-pod    nginx:latest   app=nginx-pod
```


Notice, that ReplicaSet understands which Pods to create by using SELECTOR key-value pair.

Get detailed information of a ReplicaSet

To display detailed information about any Kubernetes object, you can use 2 differen commands:

- kubectl describe %object_type% %object_name% (e.g. kubectl describe rs nginx-rs)
- kubectl get %object_type% %object_name% -o yaml (e.g. kubectl describe rs nginx-rs -o yaml)


Try both commands in action and see the difference. Also try get with -o json instead of -o yaml and decide for yourself which 
output option is more readable for you.

Scale ReplicaSet up and down:
In general, there are 2 approaches of [Kubernetes Object Management](https://kubernetes.io/docs/concepts/overview/working-with-objects/object-management/): 
imperative and declarative.

Let us see how we can use both to scale our Replicaset up and down:

Imperative:

We can easily scale our ReplicaSet up by specifying the desired number of replicas in an imperative command, like this:

```
❯ kubectl scale rs nginx-rs --replicas=5
replicationcontroller/nginx-rc scaled
```

```
❯ kubectl get pods
NAME             READY   STATUS    RESTARTS   AGE
nginx-rc-4kgpj   1/1     Running   0          4m30s
nginx-rc-4z2pn   1/1     Running   0          4m30s
nginx-rc-g4tvg   1/1     Running   0          6s
nginx-rc-kmh8m   1/1     Running   0          6s
nginx-rc-zlgvp   1/1     Running   0          4m30s
```

Scaling down will work the same way, so scale it down to 3 replicas.

**Declarative:**

Declarative way would be to open our rs.yaml manifest, change desired number of replicas in respective section

```
spec:
  replicas: 3
```

and applying the updated manifest:


```
kubectl apply -f rs.yaml
```

There is another method – ‘ad-hoc’, it is definitely not the best practice and we do not recommend using it, but you can edit 
an existing ReplicaSet with following command:


```
kubectl edit -f rs.yaml
```


Advanced label matching
As Kubernetes mature as a technology, so does its features and improvements to k8s objects. ReplicationControllers do not meet
certain complex business requirements when it comes to using selectors. Imagine if you need to select Pods with multiple lables
that represents things like:

- Application tier: such as Frontend, or Backend
- Environment: such as Dev, SIT, QA, Preprod, or Prod


So far, we used a simple selector that just matches a key-value pair and check only ‘equality’:

```
selector:
    app: nginx-pod
```


But in some cases, we want ReplicaSet to manage our existing containers that match certain criteria, we can use the same simple
label matching or we can use some more complex conditions, such as:


```
- in
 - not in
 - not equal
 - etc...
```

Let us look at the following manifest file:

```
apiVersion: apps/v1
kind: ReplicaSet
metadata: 
  name: nginx-rs
spec:
  replicas: 3
  selector:
    matchLabels:
      env: prod
    matchExpressions:
    - { key: tier, operator: In, values: [frontend] }
  template:
    metadata:
      name: nginx
      labels: 
        env: prod
        tier: frontend
    spec:
      containers:
      - name: nginx-container
        image: nginx:latest
        ports:
        - containerPort: 80
          protocol: TCP
```


In the above spec file, under the selector, matchLabels and matchExpression are used to specify the key-value pair. The matchLabel
works exactly the same way as the equality-based selector, and the matchExpression is used to specify the set based selectors.
This feature is the main differentiator between ReplicaSet and previously mentioned obsolete ReplicationController.

Get the replication set:

```
❯ kubectl get rs nginx-rs -o wide
NAME       DESIRED   CURRENT   READY   AGE     CONTAINERS        IMAGES         SELECTOR
nginx-rs   3         3         3       5m34s   nginx-container   nginx:latest   env=prod,tier in (frontend)
```
