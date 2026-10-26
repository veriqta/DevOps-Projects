# ACCESSING THE APP FROM THE BROWSER

Now you have a running Pod. What’s next?

The ultimate goal of any solution is to access it either through a web portal or some application (e.g., mobile app). We have a Pod 
with Nginx container, so we need to access it from the browser. But all you have is a running Pod that has its own IP address which
cannot be accessed through the browser. To achieve this, we need another Kubernetes object called 
[Service](https://kubernetes.io/docs/concepts/services-networking/service/) to accept our request and pass it on to the Pod.

A service is an object that accepts requests on behalf of the Pods and forwards it to the Pod’s IP address. If you run the command 
below, you will be able to see the Pod’s IP address. But there is no way to reach it directly from the outside world.


```
kubectl get pod nginx-pod  -o wide 
```

**Output:**

```
NAME        READY   STATUS    RESTARTS   AGE    IP               NODE                                              NOMINATED NODE   READINESS GATES
nginx-pod   1/1     Running   0          138m   172.50.202.214   ip-172-50-202-161.eu-central-1.compute.internal   <none>           <none>
```

Let us try to access the Pod through its IP address from within the K8s cluster. To do this,

1. We need an image that already has curl software installed. You can check it out [here](https://hub.docker.com/r/dareyregistry/curl)

```
dareyregistry/curl
```

2. Run kubectl to connect inside the container

```
kubectl run curl --image=dareyregistry/curl -i --tty
```

3. Run curl and point to the IP address of the Nginx Pod (Use the IP address of your own Pod)

```
# curl -v 172.50.202.214:80
```


**Output:**

```
> GET / HTTP/1.1
> User-Agent: curl/7.35.0
> Host: 172.50.202.214
> Accept: */*
> 
< HTTP/1.1 200 OK
< Server: nginx/1.21.0
< Date: Sat, 12 Jun 2021 21:12:56 GMT
< Content-Type: text/html
< Content-Length: 612
< Last-Modified: Tue, 25 May 2021 12:28:56 GMT
< Connection: keep-alive
< ETag: "60aced88-264"
< Accept-Ranges: bytes
< 
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

If the use case for your solution is required for internal use ONLY, without public Internet requirement. Then, this should be OK.
But in most cases, it is NOT!

Assuming that your requirement is to access the Nginx Pod internally, using the Pod’s IP address directly as above is not a 
reliable choice because Pods are ephemeral. They are not designed to run forever. When they die and another Pod is brought back
up, the IP address will change and any application that is using the previous IP address directly will break.

To solve this problem, kubernetes uses Service – An object that abstracts the underlining IP addresses of Pods. A service can 
serve as a load balancer, and a reverse proxy which basically takes the request using a human readable DNS name, resolves to a 
Pod IP that is running and forwards the request to it. This way, you do not need to use an IP address. Rather, you can simply 
refer to the service name directly.


Let us create a service to access the Nginx Pod

1. Create a Service yaml manifest file:

```
sudo cat <<EOF | sudo tee ./nginx-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx-pod 
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
EOF
```

2. Create a nginx-service resource by applying your manifest

```
kubectl apply -f nginx-service.yaml
```

**output:**

```
service/nginx-service created
```

3. Check the created service

```
kubectl get service
```

**output:**

```
NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
kubernetes      ClusterIP   10.100.0.1      <none>        443/TCP   68d
nginx-service   ClusterIP   10.100.71.130   <none>        80/TCP    85s
```


**Observation:**

The TYPE column in the output shows that there are [different service types](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types).

- ClusterIP
- NodePort
- LoadBalancer &
- Headless Service

Since we did not specify any type, it is obvious that the default type is ClusterIP

Now that we have a service created, how can we access the app? Since there is no public IP address, we can leverage kubectl's
port-forward functionality.

```
kubectl  port-forward svc/nginx-service 8089:80
```

8089 is an arbitrary port number on your laptop or client PC, and we want to tunnel traffic through it to the port number of 
the nginx-service 80.


![7030](https://user-images.githubusercontent.com/85270361/210234954-c43d01b5-8c1a-47df-9d1d-28c7b0f7333d.PNG)


Unfortunately, this will not work quite yet. Because there is no way the service will be able to select the actual Pod it is meant 
to route traffic to. If there are hundreds of Pods running, there must be a way to ensure that the service only forwards requests
to the specific Pod it is intended for.

To make this work, you must reconfigure the Pod manifest and introduce labels to match the selectors key in the field section of 
the service manifest.

1. Update the Pod manifest with the below and apply the manifest:

```
apiVersion: v1
kind: Pod
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
      protocol: TCP
```


Notice that under the metadata section, we have now introduced labels with a key field called app and its value nginx-pod. This
matches exactly the selector key in the service manifest.

The key/value pairs can be anything you specify. These are not Kubernetes specific keywords. As long as it matches the selector,
the service object will be able to route traffic to the Pod.

Apply the manifest with:

```
kubectl apply -f nginx-pod.yaml
```

2. Run kubectl port-forward command again

```
kubectl  port-forward svc/nginx-service 8089:80
```

**output:**

```
kubectl  port-forward svc/nginx-service 8089:80
Forwarding from 127.0.0.1:8089 -> 80
Forwarding from [::1]:8089 -> 80
```

Then go to your web browser and enter localhost:8089 – You should now be able to see the nginx page in the browser.


![7031](https://user-images.githubusercontent.com/85270361/210235523-4563f346-b29f-40ec-bfed-7fc68394c1cf.PNG)
