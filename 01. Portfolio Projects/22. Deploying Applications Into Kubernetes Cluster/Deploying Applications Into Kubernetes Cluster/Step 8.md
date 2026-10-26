# PERSISTING DATA FOR PODS

Deployments are stateless by design. Hence, any data stored inside the Pod’s container does not persist when the Pod dies.

If you were to update the content of the index.html file inside the container, and the Pod dies, that content will not be
lost since a new Pod will replace the dead one.

Let us try that:

1. Scale the Pods down to 1 replica.

```
NAME                                READY   STATUS        RESTARTS   AGE
nginx-deployment-56466d4948-58nqx   0/1     Terminating   0          45m
nginx-deployment-56466d4948-5z4c2   1/1     Terminating   0          45m
nginx-deployment-56466d4948-5zdbx   0/1     Terminating   0          62m
nginx-deployment-56466d4948-78j9c   1/1     Terminating   0          45m
nginx-deployment-56466d4948-gj4fd   1/1     Terminating   0          45m
nginx-deployment-56466d4948-gsrpz   0/1     Terminating   0          45m
nginx-deployment-56466d4948-kg9hp   1/1     Terminating   0          45m
nginx-deployment-56466d4948-qs29b   0/1     Terminating   0          45m
nginx-deployment-56466d4948-sfft6   0/1     Terminating   0          45m
nginx-deployment-56466d4948-sg4np   0/1     Terminating   0          45m
nginx-deployment-56466d4948-tg9j8   1/1     Running       0          62m
nginx-deployment-56466d4948-ttn5t   1/1     Terminating   0          62m
nginx-deployment-56466d4948-vfmjx   0/1     Terminating   0          45m
nginx-deployment-56466d4948-vlgbs   1/1     Terminating   0          45m
nginx-deployment-56466d4948-xctfh   0/1     Terminating   0          45m
```

```
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-56466d4948-tg9j8   1/1     Running   0          64m
```

2. Exec into the running container (figure out the command yourself)

3. Install vim so that you can edit the file


```
apt-get update
apt-get install vim
```

4. Update the content of the file and add the code below /usr/share/nginx/html/index.html

```
<!DOCTYPE html>
<html>
<head>
<title>Welcome to TOTAL!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to TOTAL!</h1>
<p>I love experiencing Kubernetes</p>

<p>Learning by doing is absolutely the best strategy at 
<a href="https://darey.io/">www.total.com</a>.<br/>
for skills acquisition
<a href="https://darey.io/">www.total.com</a>.</p>

<p><em>Thank you TOTAL</em></p>
</body>
</html>
```

5. Check the browser – You should see a message

6. Now, delete the only running Pod

```
kubectl delete po nginx-deployment-56466d4948-tg9j8
pod "nginx-deployment-56466d4948-tg9j8" deleted
```

7. Refresh the web page – You will see that the content you saved in the container is no longer there. That is because Pods do
not store data when they are being recreated – that is why they are called ephemeral or stateless. (But not to worry, we will
address this with persistent volumes in the next project)


![7036](https://user-images.githubusercontent.com/85270361/210247251-470fae45-71bc-4c79-a5ec-1bc0027b69c7.PNG)


Storage is a critical part of running containers, and Kubernetes offers some powerful primitives for managing it. Dynamic volume
provisioning, a feature unique to Kubernetes, which allows storage volumes to be created on-demand. Without dynamic provisioning, 
DevOps engineers must manually make calls to the cloud or storage provider to create new storage volumes, and then create 
PersistentVolume objects to represent them in Kubernetes. The dynamic provisioning feature eliminates the need for DevOps to
pre-provision storage. Instead, it automatically provisions storage when it is requested by users.

To make the data persist in case of a Pod’s failure, you will need to configure the Pod to use following objects:

[Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) or pv – is a piece of storage in the
cluster that has been provisioned by an administrator or dynamically provisioned using Storage Classes.
[Persistent Volume Claim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims) or pvc. 
Persistent Volume Claim is simply a request for storage, hence the "claim" in its name. But where is it requesting this storage 
from?..

In the next project,

1. You will use Terraform to create a Kubernetes EKS cluster in AWS, and begin to use some powerful features such as PV, PVCs, ConfigMaps.
2. You will also be introduced to packaging Kubernetes manifests using Helm
3. Experience Dynamic provisioning of volumes to make your Pods stateful, using Kubernetes Statefulset
4. Deploying applications into Kubernetes using Helm Charts
