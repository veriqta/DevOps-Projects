# DEPLOY JENKINS WITH HELM

Before we begin to develop our own helm charts, lets make use of publicly available charts to deploy all the tools that we need.

One of the amazing things about helm is the fact that you can deploy applications that are already packaged from a public helm repository
directly with very minimal configuration. An example is Jenkins.


1. Visit [Artifact Hub](https://artifacthub.io/packages/search) to find packaged applications as Helm Charts
2. Search for Jenkins
3. Add the repository to helm so that you can easily download and deploy

```
helm repo add jenkins https://charts.jenkins.io
```

4. Update helm repo

```
helm repo update 
```

5. Install the chart

```
helm install [RELEASE_NAME] jenkins/jenkins --kubeconfig [kubeconfig file]
```

You should see an output like this

```
NAME: jenkins
LAST DEPLOYED: Sun Aug  1 12:38:53 2021
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
1. Get your 'admin' user password by running:
  kubectl exec --namespace default -it svc/jenkins -c jenkins -- /bin/cat /run/secrets/chart-admin-password && echo
2. Get the Jenkins URL to visit by running these commands in the same shell:
  echo http://127.0.0.1:8080
  kubectl --namespace default port-forward svc/jenkins 8080:8080

3. Login with the password from step 1 and the username: admin
4. Configure security realm and authorization strategy
5. Use Jenkins Configuration as Code by specifying configScripts in your values.yaml file, see documentation: http:///configuration-as-code and examples: https://github.com/jenkinsci/configuration-as-code-plugin/tree/master/demos

For more information on running Jenkins on Kubernetes, visit:
https://cloud.google.com/solutions/jenkins-on-container-engine

For more information about Jenkins Configuration as Code, visit:
https://jenkins.io/projects/jcasc/

NOTE: Consider using a custom image with pre-installed plugins
```

6. Check the Helm deployment

```
helm ls --kubeconfig [kubeconfig file]
```

**Output:**

```
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
jenkins default         1               2021-08-01 12:38:53.429471 +0100 BST    deployed        jenkins-3.5.9   2.289.3 
```

7. Check the pods

```
kubectl get pods --kubeconfigo [kubeconfig file]
```

**Output:**

```
NAME        READY   STATUS    RESTARTS   AGE
jenkins-0   2/2     Running   0          6m14s
```

8. Describe the running pod (review the output and try to understand what you see)

```
kubectl describe pod jenkins-0 --kubeconfig [kubeconfig file]
```

9. Check the logs of the running pod

```
kubectl logs jenkins-0 --kubeconfig [kubeconfig file]
```

You will notice an output with an error

```
error: a container name must be specified for pod jenkins-0, choose one of: [jenkins config-reload] or one of the init containers: [init]
```

This is because the pod has a [Sidecar container](https://www.weave.works/blog/container-design-patterns-for-kubernetes/) alongside
with the Jenkins container. As you can see fromt he error output, there is a list of containers inside the pod [jenkins config-reload]
i.e jenkins and config-reload containers. The job of the config-reload is mainly to help Jenkins to reload its configuration without 
recreating the pod.

Therefore we need to let kubectl know, which pod we are interested to see its log. Hence, the command will be updated like:

```
kubectl logs jenkins-0 -c jenkins --kubeconfig [kubeconfig file]
```

10. Now lets avoid calling the [kubeconfig file] everytime. Kubectl expects to find the default kubeconfig file in the location 
~/.kube/config. But what if you already have another cluster using that same file? It doesn’t make sense to overwrite it. What you
will do is to merge all the kubeconfig files together using a kubectl plugin called [konfig](https://github.com/corneliusweig/konfig)
and select whichever one you need to be active.

1. Install a package manager for kubectl called [krew](https://krew.sigs.k8s.io/docs/user-guide/setup/install/) so that it will enable
 you to install plugins to extend the functionality of kubectl. Read more about it [Here](https://github.com/kubernetes-sigs/krew)
 
 2. Install the [konfig plugin](https://github.com/corneliusweig/konfig)
 
 ```
 kubectl krew install konfig
 ```
 
 3. Import the kubeconfig into the default kubeconfig file. Ensure to accept the prompt to overide.

```
sudo kubectl konfig import --save  [kubeconfig file]
```

4. Show all the contexts – Meaning all the clusters configured in your kubeconfig. If you have more than 1 Kubernetes clusters 
configured, you will see them all in the output.

```
 kubectl config get-contexts
```

5. Set the current context to use for all kubectl and helm commands

```
kubectl config use-context [name of EKS cluster]
```

6. Test that it is working without specifying the --kubeconfig flag

```
kubectl get po
```

**Output:**
```
NAME        READY   STATUS    RESTARTS   AGE
  jenkins-0   2/2     Running   0          84m
```

7. Display the current context. This will let you know the context in which you are using to interact with Kubernetes.

```
 kubectl config current-context
```


11. Now that we can use kubectl without the --kubeconfig flag, Lets get access to the Jenkins UI. (In later projects we will further
 configure Jenkins. For now, it is to set up all the tools we need)
 
 1. There are some commands that was provided on the screen when Jenkins was installed with Helm. See number 5 above. Get the 
 password to the admin user
 
 ```
 kubectl exec --namespace default -it svc/jenkins -c jenkins -- /bin/cat /run/secrets/chart-admin-password && echo
 ```
 
 2. Use port forwarding to access Jenkins from the UI

```
kubectl --namespace default port-forward svc/jenkins 8080:8080
```

![7044](https://user-images.githubusercontent.com/85270361/210271727-993112b7-a1ee-4b5d-b3f3-4ea5ae977d36.PNG)

3. Go to the browser localhost:8080 and authenticate with the username and password from number 1 above

![7045](https://user-images.githubusercontent.com/85270361/210271819-b23a0ffd-a8b8-4ffe-8f41-e29b729c1d0e.PNG)
