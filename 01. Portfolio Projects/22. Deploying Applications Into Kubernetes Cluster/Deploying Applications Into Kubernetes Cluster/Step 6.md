# USING AWS LOAD BALANCER TO ACCESS YOUR SERVICE IN KUBERNETES.

Note: You will only be able to test this using AWS EKS. You don not have to set this up in current project yet. In the next project,
you will update your Terraform code to build an EKS cluster.

You have previously accessed the Nginx service through ClusterIP, and NodeIP, but there is another service type – 
[Loadbalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer). This type of service does not only 
create a Service object in K8s, but also provisions a real external Load Balancer (e.g. Elastic Load Balancer – ELB in AWS)

To get the experience of this service type, update your service manifest and use the LoadBalancer type. Also, ensure that the
selector references the Pods in the replica set.


```
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: LoadBalancer
  selector:
    tier: frontend
  ports:
    - protocol: TCP
      port: 80 # This is the port the Loadbalancer is listening at
      targetPort: 80 # This is the port the container is listening at
```


Apply the configuration:

```
kubectl apply -f nginx-service.yaml
```

Get the newly created service :

```
kubectl get service nginx-service
```

**output:**

```
NAME            TYPE           CLUSTER-IP      EXTERNAL-IP                                                                  PORT(S)        AGE
nginx-service   LoadBalancer   10.100.71.130   aab159950f39e43d39195e23c77417f8-1167953448.eu-central-1.elb.amazonaws.com   80:31388/TCP   5d18h
```

An ELB resource will be created in your AWS console.

![7032](https://user-images.githubusercontent.com/85270361/210242066-ee1a2942-bb6b-4347-93c5-b93255968b6a.PNG)


A Kubernetes component in the control plane called 
[Cloud-controller-manager](https://kubernetes.io/docs/concepts/architecture/cloud-controller/) is responsible for triggeriong 
this action. It connects to your specific cloud provider’s (AWS) APIs and create resources such as Load balancers. It will ensure that
the resource is appropriately tagged:


![7033](https://user-images.githubusercontent.com/85270361/210242334-a11b5ae5-4379-4bcc-9b99-560bc0847813.PNG)


Get the output of the entire yaml for the service. You will some additional information about this service in which you did not
define them in the yaml manifest. Kubernetes did this for you.

```
kubectl get service nginx-service -o yaml
```

**output:**

```
apiVersion: v1
kind: Service
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"name":"nginx-service","namespace":"default"},"spec":{"ports":[{"port":80,"protocol":"TCP","targetPort":80}],"selector":{"app":"nginx-pod"},"type":"LoadBalancer"}}
  creationTimestamp: "2021-06-18T16:24:21Z"
  finalizers:
  - service.kubernetes.io/load-balancer-cleanup
  name: nginx-service
  namespace: default
  resourceVersion: "21824260"
  selfLink: /api/v1/namespaces/default/services/nginx-service
  uid: c12145d6-a8b5-491d-95ff-8e2c6296b46c
spec:
  clusterIP: 10.100.153.44
  externalTrafficPolicy: Cluster
  ports:
  - nodePort: 31388
    port: 80
    protocol: TCP
    targetPort: 80
  selector:
    tier: frontend
  sessionAffinity: None
  type: LoadBalancer
status:
  loadBalancer:
    ingress:
    - hostname: ac12145d6a8b5491d95ff8e2c6296b46-588706163.eu-central-1.elb.amazonaws.com
```


1. A clusterIP key is updated in the manifest and assigned an IP address. Even though you have specified a Loadbalancer service type, 
internally it still requires a clusterIP to route the external traffic through.
2. In the ports section, nodePort is still used. This is because Kubernetes still needs to use a dedicated port on the worker node to 
route the traffic through. Ensure that port range 30000-32767 is opened in your inbound Security Group configuration.
3. More information about the provisioned balancer is also published in the .status.loadBalancer field.

```
status:
  loadBalancer:
    ingress:
    - hostname: ac12145d6a8b5491d95ff8e2c6296b46-588706163.eu-central-1.elb.amazonaws.com
```

Copy and paste the load balancer’s address to the browser, and you will access the Nginx service


![7034](https://user-images.githubusercontent.com/85270361/210242850-fb18e207-7dd5-4435-b0b1-d0eb2e527861.PNG)
