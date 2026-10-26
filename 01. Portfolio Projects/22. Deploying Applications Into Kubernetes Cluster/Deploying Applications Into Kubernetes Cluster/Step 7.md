# USING DEPLOYMENT CONTROLLERS

Do not Use Replication Controllers – Use Deployment Controllers Instead
Kubernetes is loaded with a lot of features, and with its vibrant open source community, these features are constantly evolving and
adding up.

Previously, you have seen the improvements from ReplicationControllers (RC), to ReplicaSets (RS). In this section you will see 
another K8s object which is highly recommended over Replication objects (RC and RS).

A [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) is another layer above ReplicaSets and Pods, 
newer and more advanced level concept than ReplicaSets. It manages the deployment of ReplicaSets and allows for easy updating of a 
ReplicaSet as well as the ability to roll back to a previous version of deployment. It is declarative and can be used for rolling
updates of micro-services, ensuring there is no downtime.

Officially, it is highly recommended to use Deplyments to manage replica sets rather than using replica sets directly.

Let us see Deployment in action.

1. Delete the ReplicaSet

```
kubectl delete rs nginx-rs
```

2. Understand the layout of the deployment.yaml manifest below. Lets go through the 3 separated sections:

```
# Section 1 - This is the part that defines the deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    tier: frontend

# Section 2 - This is the Replica set layer controlled by the deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      tier: frontend

# Section 3 - This is the Pod section controlled by the deployment and selected by the replica set in section 2.
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
```


3. Putting them altogether

```
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
        - containerPort: 8
```


```
kubectl apply -f deployment.yaml
```

Run commands to get the following

1. Get the Deployment

```
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   3/3     3            3           39s
```


2. Get the ReplicaSet

```
NAME                          DESIRED   CURRENT   READY   AGE
nginx-deployment-56466d4948   3         3         3       24s
```

3. Get the Pods

```
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-56466d4948-5zdbx   1/1     Running   0          12s
nginx-deployment-56466d4948-tg9j8   1/1     Running   0          12s
nginx-deployment-56466d4948-ttn5t   1/1     Running   0          12s
```

4. Scale the replicas in the Deployment to 15 Pods

```
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-56466d4948-58nqx   1/1     Running   0          6s
nginx-deployment-56466d4948-5z4c2   1/1     Running   0          6s
nginx-deployment-56466d4948-5zdbx   1/1     Running   0          17m
nginx-deployment-56466d4948-78j9c   1/1     Running   0          6s
nginx-deployment-56466d4948-gj4fd   1/1     Running   0          6s
nginx-deployment-56466d4948-gsrpz   1/1     Running   0          6s
nginx-deployment-56466d4948-kg9hp   1/1     Running   0          6s
nginx-deployment-56466d4948-qs29b   1/1     Running   0          6s
nginx-deployment-56466d4948-sfft6   1/1     Running   0          6s
nginx-deployment-56466d4948-sg4np   1/1     Running   0          6s
nginx-deployment-56466d4948-tg9j8   1/1     Running   0          17m
nginx-deployment-56466d4948-ttn5t   1/1     Running   0          17m
nginx-deployment-56466d4948-vfmjx   1/1     Running   0          6s
nginx-deployment-56466d4948-vlgbs   1/1     Running   0          6s
nginx-deployment-56466d4948-xctfh   1/1     Running   0          6s
```

5. Exec into one of the Pod’s container to run Linux commands

```
kubectl exec -it nginx-deployment-56466d4948-78j9c bash
```

List the files and folders in the Nginx directory

```
root@nginx-deployment-56466d4948-78j9c:/# ls -ltr /etc/nginx/
total 24
-rw-r--r-- 1 root root  664 May 25 12:28 uwsgi_params
-rw-r--r-- 1 root root  636 May 25 12:28 scgi_params
-rw-r--r-- 1 root root 5290 May 25 12:28 mime.types
-rw-r--r-- 1 root root 1007 May 25 12:28 fastcgi_params
-rw-r--r-- 1 root root  648 May 25 13:01 nginx.conf
lrwxrwxrwx 1 root root   22 May 25 13:01 modules -> /usr/lib/nginx/modules
drwxr-xr-x 1 root root   26 Jun 18 22:08 conf.d
```

Check the content of the default Nginx configuration file

```
root@nginx-deployment-56466d4948-78j9c:/# cat  /etc/nginx/conf.d/default.conf 
server {
    listen       80;
    listen  [::]:80;
    server_name  localhost;

    #access_log  /var/log/nginx/host.access.log  main;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    # proxy the PHP scripts to Apache listening on 127.0.0.1:80
    #
    #location ~ \.php$ {
    #    proxy_pass   http://127.0.0.1;
    #}

    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    #location ~ \.php$ {
    #    root           html;
    #    fastcgi_pass   127.0.0.1:9000;
    #    fastcgi_index  index.php;
    #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
    #    include        fastcgi_params;
    #}

    # deny access to .htaccess files, if Apache's document root
    # concurs with nginx's one
    #
    #location ~ /\.ht {
    #    deny  all;
    #}
}
```

Now, as we have got acquaited with most common Kubernetes workloads to deploy applications:


![7035](https://user-images.githubusercontent.com/85270361/210245593-d2d9217f-0595-4ef2-9c58-028446345ac9.PNG)


it is time to explore how Kubernetes is able to manage persistent data.
