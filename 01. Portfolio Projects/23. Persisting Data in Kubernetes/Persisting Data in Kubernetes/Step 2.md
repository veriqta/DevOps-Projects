# MANAGING VOLUMES DYNAMICALLY WITH PVS AND PVCS

Kubernetes provides API objects for storage management such that, the lower level details of volume provisioning, storage allocation,
access management etc are all abstracted away from the user, and all you have to do is present manifest files that describes what you
want to get done.

PVs are volume plugins that have a lifecycle completely independent of any individual Pod that uses the PV. This means that even when
a pod dies, the PV remains. A PV is a piece of storage in the cluster that is either provisioned by an administrator through a manifest
file, or it can be dynamically created if a storage class has been pre-configured.

Creating a PV manually is like what we have done previously where with creating the volume from the console. As much as possible, we
should allow PVs to be created automatically just be adding it to the container spec iin deployments. But without a storageclass 
present in the cluster, PVs cannot be automatically created.

If your infrastructure relies on a storage system such as NFS, iSCSI or a cloud provider-specific storage system such as EBS on AWS,
then you can dynamically create a PV which will create a volume that a Pod can then use. This means that there must be a storageClass
resource in the cluster before a PV can be provisioned.

By default, in EKS, there is a default storageClass configured as part of EKS installation. This storageclass is based on gp2 which is
Amazon’s default type of volume for Elastic block storage.gp2 is backled by solid-state drives (SSDs) which means they are suitable
for a broad range of transactional workloads.

Run the command below to check if you already have a storageclass in your cluster kubectl get storageclass


```
kubectl get storageclass
  NAME            PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
  gp2 (default)   kubernetes.io/aws-ebs   Delete          WaitForFirstConsumer   false                  18d
```

Of course, if the cluster is not EKS, then the storage class will be different. For example if the cluster is based on Google’s GKE 
or Azure’s AKS, then the storage class will be different.

If there is no storage class in your cluster, below manifest is an example of how one would be created


```
 kind: StorageClass
  apiVersion: storage.k8s.io/v1
  metadata:
    name: gp2
    annotations:
      storageclass.kubernetes.io/is-default-class: "true"
  provisioner: kubernetes.io/aws-ebs
  parameters:
    type: gp2
    fsType: ext4 
```


A PersistentVolumeClaim (PVC) on the other hand is a request for storage. Just as Pods consume node resources, PVCs consume PV 
resources. Pods can request specific levels of resources (CPU and Memory). Claims can request specific size and access modes (e.g.,
they can be mounted ReadWriteOnce, ReadOnlyMany or ReadWriteMany, see [AccessModes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes)).

Lifecycle of a PV and PVC

PVs are resources in the cluster. PVCs are requests for those resources and also act as claim checks to the resource. The interaction
between PVs and PVCs follows this lifecycle:

1. Provisioning: There are two ways PVs may be provisioned: statically or dynamically.

- Static/Manual Provisioning: A cluster administrator creates a number of PVs using a manifest file which will contain all the details
of the real storage. PVs are not scoped to namespaces, they a clusterwide wide resource, therefore the PV will be available for use
when requested. PVCs on the other hand are namespace scoped.

- Dynamic: When there is no PV matching a PVC’s request, then based on the available StorageClass, a dynamic PV will be created for use
by the PVC. If there is not StorageClass, then the request for a PV by the PVC will fail.

2. Binding: PVCs are bound to specifiv PVs. This binding is exclusive. A PVC to PV binding is a one-to-one mapping. Claims will remain
unbound indefinitely if a matching volume does not exist. Claims will be bound as matching volumes become available. For example, a
cluster provisioned with many 50Gi PVs would not match a PVC requesting 100Gi. The PVC can be bound when a 100Gi PV is added to the
cluster.
3. Using: Pods use claims as volumes. The cluster inspects the claim to find the bound volume and mounts that volume for a Pod. For
volumes that support multiple access modes, the user specifies which mode is desired when using their claim as a volume in a Pod.
Once a user has a claim and that claim is bound, the bound PV belongs to the user for as long as they need it. Users schedule Pods 
and access their claimed PVs by including a persistentVolumeClaim section in a Pod’s volumes block
4. Storage Object in Use Protection: The purpose of the Storage Object in Use Protection feature is to ensure that PersistentVolumeClaims
(PVCs) in active use by a Pod and PersistentVolume (PVs) that are bound to PVCs are not removed from the system, as this may result
in data loss.
Note: PVC is in active use by a Pod when a Pod object exists that is using the PVC. If a user deletes a PVC in active use by a Pod,
the PVC is not removed immediately. PVC removal is postponed until the PVC is no longer actively used by any Pods. Also, if an admin
deletes a PV that is bound to a PVC, the PV is not removed immediately. PV removal is postponed until the PV is no longer bound to 
a PVC.

5. Reclaiming: When a user is done with their volume, they can delete the PVC objects from the API that allows reclamation of the 
resource. The reclaim policy for a PersistentVolume tells the cluster what to do with the volume after it has been released of its
claim. Currently, volumes can either be Retained, Recycled, or Deleted.

- Retain: The Retain reclaim policy allows for manual reclamation of the resource. When the PersistentVolumeClaim is deleted, the
 PersistentVolume still exists and the volume is considered "released". But it is not yet available for another claim because the 
 previous claimant’s data remains on the volume.
 
- Delete: For volume plugins that support the Delete reclaim policy, deletion removes both the PersistentVolume object from Kubernetes,
 as well as the associated storage asset in the external infrastructure, such as an AWS EBS. Volumes that were dynamically 
 provisioned inherit the reclaim policy of their StorageClass, which defaults to Delete
 
 
NOTES:

1. When PVCs are created with a specific size, it cannot be expanded except the storageClass is configured to allow expansion with 
the allowVolumeExpansion field is set to true in the manifest YAML file. This is "unset" by default in EKS.

2. When a PV has been provisioned in a specific availability zone, only pods running in that zone can use the PV. If a pod spec 
containing a PVC is created in another AZ and attempts to reuse an already bound PV, then the pod will remain in pending state 
and report volume node affinity conflict. Anytime you see this message, this will help you to understand what the problem is.

3. PVs are not scoped to namespaces, they a clusterwide wide resource. PVCs on the other hand are namespace scoped.

Learn more about the different types of 
[persistent volumes here](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#types-of-persistent-volumes)

Now lets create some persistence for our nginx deployment. We will use 2 different approaches.

Approach 1

1. Create a manifest file for a PVC, and based on the gp2 storageClass a PV will be dynamically created

```
apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: nginx-volume-claim
    spec:
      accessModes:
      - ReadWriteOnce
      resources:
        requests:
          storage: 2Gi
      storageClassName: gp2
```

Apply the manifest file and you will get an output like below

persistentvolumeclaim/nginx-volume-claim created

```
Run get on the pvc and you will notice that it is in pending state. 
```

kubectl get pvc
NAME STATUS VOLUME CAPACITY ACCESS MODES STORAGECLASS AGE
nginx-volume-claim Pending gp2 61s

To troubleshoot this, simply run a describe on the pvc. Then you will see in the Message section that this pvc is waiting for the 
first consumer to be created before binding the PV to a PV


```
Name: nginx-volume-claim
Namespace: default
StorageClass: gp2
Status: Pending
Volume:
Labels:
Annotations:
Finalizers: [kubernetes.io/pvc-protection]
Capacity:
Access Modes:
VolumeMode: Filesystem
Used By:
Events:
Type Reason Age From Message
```

Normal WaitForFirstConsumer 7s (x11 over 2m24s) persistentvolume-controller waiting for first consumer to be created before binding


If you run `kubectl get pv` you will see that no PV is created yet. The *waiting for first consumer to be created before binding* is
a configuration setting from the storageClass. See the `VolumeBindingMode` section below.


```
kubectl describe storageclass gp2
Name: gp2
IsDefaultClass: Yes
Annotations: kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"storage.k8s.io/v1","kind":"StorageClass","metadata":{"annotations":{"storageclass.kubernetes.io/is-default-class":"true"},"name":"gp2"},"parameters":{"fsType":"ext4","type":"gp2"},"provisioner":"kubernetes.io/aws-ebs","volumeBindingMode":"WaitForFirstConsumer"}
,storageclass.kubernetes.io/is-default-class=true
Provisioner: kubernetes.io/aws-ebs
Parameters: fsType=ext4,type=gp2
AllowVolumeExpansion:
MountOptions:
ReclaimPolicy: Delete
VolumeBindingMode: WaitForFirstConsumer
Events:
```


To proceed, simply apply the new deployment configuration below.

2. Then configure the Pod spec to use the PVC


```
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
        - name: nginx-volume-claim
          mountPath: "/tmp/dare"
      volumes:
      - name: nginx-volume-claim
        persistentVolumeClaim:
          claimName: nginx-volume-claim
```


Notice that the volumes section nnow has a `persistentVolumeClaim`. With the new deployment manifest, the `/tmp/dare` directory will 
be persisted, and any data written in there will be sotred permanetly on the volume, which can be used by another Pod if the current 
one gets replaced.

Now lets check the dynamically created PV


kubectl get pv
NAME CAPACITY ACCESS MODES RECLAIM POLICY STATUS CLAIM STORAGECLASS REASON AGE
pvc-89ba00d9-68f4-4039-b19e-a6471aad6a1e 2Gi RWO Delete Bound default/nginx-volume-claim gp2 7s


```
ou can copy the PV Name and search in the AWS console. You will notice that the volum has been dynamically created there.

![](https://www.darey.io/wp-content/uploads/2022/04/PV-volume.png)

Approach 2 (Attempt this on your own). [See an example here](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-volume-claim-templates.html)

1. Create a volumeClaimTemplate within the Pod spec. This approach is simply adding the manifest for PVC right within the Pod spec of the deployment.
2. Then use the PVC name just as Approach 1 above.

So rather than have 2 manifest files, you will define everything within the deployment manifest.
```
