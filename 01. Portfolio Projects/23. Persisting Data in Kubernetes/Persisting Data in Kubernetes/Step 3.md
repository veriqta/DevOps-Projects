# CONFIGMAP

Using configMaps for persistence is not something you would consider for data storage. Rather it is a way to manage configuration 
files and ensure they are not lost as a result of Pod replacement.

to demonstrate this, we will use the HTML file that came with Nginx. This file can be found in /usr/share/nginx/html/index.html 
directory.

Lets go through the below process so that you can see an example of a configMap use case.

1. Remove the volumeMounts and PVC sections of the manifest and use kubectl to apply the configuration

2. port forward the service and ensure that you are able to see the "Welcome to nginx" page

3. exec into the running container and keep a copy of the index.html file somewhere. For example

```
kubectl exec -it nginx-deployment-79d8c764bc-j6sp9 -- bash
```

```
 cat /usr/share/nginx/html/index.html 
```

![7043](https://user-images.githubusercontent.com/85270361/210257580-f5d5e89e-3480-4415-bc2b-1924306683bc.PNG)


4. Copy the output and save the file on your local pc because we will need it to create a configmap.

Persisting configuration data with [configMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
According to the official documentation of configMaps, A ConfigMap is an API object used to store non-confidential data in key-value
pairs. Pods can consume ConfigMaps as environment variables, command-line arguments, or as configuration files in a volume.

In our own use case here, We will use configMap to create a file in a volume.

The manifest file we look like:

```
cat <<EOF | tee ./nginx-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: website-index-file
data:
  # file to be mounted inside a volume
  index-file: |
    <!DOCTYPE html>
    <html>
    <head>
    <title>Welcome to nginx!</title>
    <style>
    html { color-scheme: light dark; }
    body { width: 35em; margin: 0 auto;
    font-family: Tahoma, Verdana, Arial, sans-serif; }
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
EOF
```

- Apply the new manifest file

```
kubectl apply -f nginx-configmap.yaml 
```

- Update the deployment file to use the configmap in the volumeMounts section


```
cat <<EOF | tee ./nginx-pod-with-cm.yaml
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
          - name: config
            mountPath: /usr/share/nginx/html
            readOnly: true
      volumes:
      - name: config
        configMap:
          name: website-index-file
          items:
          - key: index-file
            path: index.html
EOF
```

- Now the index.html file is no longer ephemeral because it is using a configMap that has been mounted onto the filesystem. This is 
now evident when you exec into the pod and list the /usr/share/nginx/html directory


```
root@nginx-deployment-84b799b888-fqzwk:/# ls -ltr  /usr/share/nginx/html
  lrwxrwxrwx 1 root root 17 Feb 19 16:16 index.html -> ..data/index.html
```

You can now see that the index.html is now a soft link to ../data

- Accessing the site will not change anything at this time because the same html file is being loaded through configmap.

- But if you make any change to the content of the html file through the configmap, and restart the pod, all your changes will persist.

Lets try that;

- List the available configmaps. You can either use kubectl get configmap or kubectl get cm


```
kubectl get cm
NAME                 DATA   AGE
kube-root-ca.crt     1      17d
website-index-file   1      46m
```

We are interested in the website-index-file configmap

- Update the configmap. You can either update the manifest file, or the kubernetes object directly. Lets use the latter approach 
this time.


```
kubectl edit cm website-index-file 
```

It will open up a vim editor, or whatever default editor your system is configured to use. Update the content as you like. "Only 
the html data section", then save the file.

You should see an output like this

```
configmap/website-index-file edited
```


```
apiVersion: v1
kind: ConfigMap
metadata:
  name: website-index-file
data:
  # file to be mounted inside a volume
  index-file: |
    <!DOCTYPE html>
    <html>
    <head>
    <title>Welcome to TOTAL!</title>
    <style>
    html { color-scheme: light dark; }
    body { width: 35em; margin: 0 auto;
    font-family: Tahoma, Verdana, Arial, sans-serif; }
    </style>
    </head>
    <body>
    <h1>Welcome to TOTAL!</h1>
    <p>If you see this page, It means you have successfully updated the configMap data in Kubernetes.</p>

    <p>For online documentation and support please refer to
    <a href="http://TOTAL/">TOTAL</a>.<br/>
    Commercial support is available at
    <a href="http://TOTAL/">TOTAL</a>.</p>

    <p><em>Thank you and make sure you are on Darey's Masterclass Program.</em></p>
    </body>
    </html>
```

Without restarting the pod, your site should be loaded automatically.



If you wish to restart the deployment for any reason, simply use the command

```
kubectl rollout restart deploy nginx-deployment
```

output:

```
deployment.apps/nginx-deployment restarted
```


This will terminate the running pod and spin up a new one.

Congratulations!!!

In the next project

- You will also be introduced to packaging Kubernetes manifests using [Helm](https://helm.sh/)
- Deploying applications into Kubernetes using Helm Charts
- And many more awesome technologies

