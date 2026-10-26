# DEPLOYING AND PACKAGING APPLICATIONS INTO KUBERNETES WITH HELM

In the previous project, you started experiencing helm as a tool used to deploy an application into Kubernetes. You probably also 
tried installing more tools apart from Jenkins.

In this project, you will experience deploying more DevOps tools, get familiar with some of the real world issues faced during such
deployments and how to fix them. You will learn how to tweak helm values files to automate the configuration of the applications 
you deploy. Finally, once you have most of the DevOps tools deployed, you will experience using them and relate with the DevOps 
cycle and how they fit into the entire ecosystem.

Our focus will be on the following tools.

1. Artifactory
2. Hashicorp Vault
3. Prometheus
4. Grafana
5. Elasticsearch ELK using [ECK](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-install-helm.html)


For the tools that require paid license, don’t worry, you will also learn how to get the license for free and have true experience
exactly how they are used in the real world.

Lets start first with Artifactory. What is it exactly?

Artifactory is part of a suit of products from a company called [Jfrog](https://jfrog.com/). Jfrog started out as an artifact repository
where software binaries in different formats are stored. Today, Jfrog has transitioned from an artifact repository to a DevOps 
Platform that includes CI and CD capabilities. This has been achieved by offering more products in which Jfrog Artifactory is part of.
Other offerings include

- JFrog Pipelines – a CI-CD product that works well with its Artifactory repository. Think of this product as an alternative to Jenkins.
- JFrog Xray – a security product that can be built-into various steps within a JFrog pipeline. Its job is to scan for security 
vulnerabilities in the stored artifacts. It is able to scan all dependent code.

In this project, the requirement is to use Jfrog Artifactory as a private registry for the organisation’s Docker images and Helm 
charts. This requirement will satisfy part of the company’s corporate security policies to never download artifacts directly from 
the public into production systems. We will eventually have a CI pipeline that initially pulls public docker images and helm charts 
from the internet, store in artifactory and scan the artifacts for security vulnerabilities before deploying into the corporate
infrastructure. Any found vulnerabilities will immediately trigger an action to quarantine such artifacts.

Lets get into action and see how all of these work.

Deploy Jfrog Artifactory into Kubernetes

The best approach to easily get Artifactory into kubernetes is to use helm.

1. Search for an official helm chart for Artifactory on [Artifact Hub](https://artifacthub.io/)

![8000](https://user-images.githubusercontent.com/85270361/210272917-d5dc3ab5-d4a5-4a8a-8315-b65f963af3d3.PNG)


2. Click on See all results
3. Use the filter checkbox on the left to limit the return data. As you can see in the image below, "Helm" is selected. In some cases, 
you might select "Official". Then click on the first option from the result.


![8001](https://user-images.githubusercontent.com/85270361/210273215-3ca5db39-4e60-4c03-b38c-9ea5c60b0e1a.PNG)



4. Review the Artifactory page

![8002](https://user-images.githubusercontent.com/85270361/210273335-882cb43c-7da2-465e-8cf5-68821de578b2.PNG)



5. Click on the install menu on the right to see the installation commands.

![8003](https://user-images.githubusercontent.com/85270361/210273502-4e15fbbd-9016-4e7c-8e9a-0d01386eb33e.PNG)


6. Add the jfrog remote repository on your laptop/computer

```
helm repo add jfrog https://charts.jfrog.io
```

7. Create a namespace called tools where all the tools for DevOps will be deployed. (In previous project, you installed Jenkins in
 the default namespace. You should uninstall Jenkins there and install in the new namespace)
 
 ```
 kubectl create ns tools
 ```
 
 8. Update the helm repo index on your laptop/computer

```
helm repo update
```

9. Install artifactory

```
helm upgrade --install artifactory jfrog/artifactory --version 107.38.10 -n tools
```

```
Release "artifactory" does not exist. Installing it now.
NAME: artifactory
LAST DEPLOYED: Sat May 28 09:26:08 2022
NAMESPACE: tools
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Congratulations. You have just deployed JFrog Artifactory!

1. Get the Artifactory URL by running these commands:

   NOTE: It may take a few minutes for the LoadBalancer IP to be available.
         You can watch the status of the service by running 'kubectl get svc --namespace tools -w artifactory-artifactory-nginx'
   export SERVICE_IP=$(kubectl get svc --namespace tools artifactory-artifactory-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
   echo http://$SERVICE_IP/

2. Open Artifactory in your browser
   Default credential for Artifactory:
   user: admin
   password: password
```


**NOTE:**

- We have used upgrade --install flag here instead of helm install artifactory jfrog/artifactory This is a better practice, especially
when developing CI pipelines for helm deployments. It ensures that helm does an upgrade if there is an existing installation.
But if there isn’t, it does the initial install. With this strategy, the command will never fail. It will be smart enough to 
determine if an upgrade or fresh installation is required.

- The helm chart version to install is very important to specify. So, the version at the time of writing may be different from what 
you will see from Artifact Hub. So, replace the version number to the desired. You can see all the versions by clicking on "see all"
as shown in the image below.


![8004](https://user-images.githubusercontent.com/85270361/210274176-5e792691-dcd5-4a32-926e-490222de24ad.PNG)


![8006](https://user-images.githubusercontent.com/85270361/210274201-bcc314c8-c89d-4fed-a60b-8f55d76c7279.PNG)


The output from the installation already gives some Next step directives.

Getting the Artifactory URL
Lets break down the first Next Step.

1. The artifactory helm chart comes bundled with the Artifactory software, a PostgreSQL database and an Nginx proxy which it uses 
to configure routes to the different capabilities of Artifactory. Getting the pods after some time, you should see something like 
the below.


![8007](https://user-images.githubusercontent.com/85270361/210274370-89e91c40-d367-4cb7-84dd-51e691e01fca.PNG)


2. Each of the deployed application have their respective services. This is how you will be able to reach either of them.

![8008](https://user-images.githubusercontent.com/85270361/210274474-722de4fb-b507-4743-aa50-ff282cb5c036.PNG)


3. Notice that, the Nginx Proxy has been configured to use the service type of LoadBalancer. Therefore, to reach Artifactory, we will
need to go through the Nginx proxy’s service. Which happens to be a load balancer created in the cloud provider. Run the kubectl
command to retrieve the Load Balancer URL.

 kubectl get svc artifactory-artifactory-nginx -n tools
 
 4. Copy the URL and paste in the browser

![8009](https://user-images.githubusercontent.com/85270361/210274613-2d4d5f5b-4d80-4b3b-9676-4f007cd08359.PNG)


5. The default username is admin

6. The default password is password


![8010](https://user-images.githubusercontent.com/85270361/210274729-cb6aed80-e30c-4eff-a00c-aaa27f8c0f95.PNG)


## How the Nginx URL for Artifactory is configured in Kubernetes
Without clicking further on the Get Started page, lets dig a bit more into Kubernetes and Helm. How did Helm configure the URL in
kubernetes?

Helm uses the values.yaml file to set every single configuration that the chart has the capability to configure. THe best place to 
get started with an off the shelve chart from artifacthub.io is to get familiar with the DEFAULT VALUES

- click on the DEFAULT VALUES section on Artifact hub

![8011](https://user-images.githubusercontent.com/85270361/210274889-be0526a8-656f-421a-ab3f-c1276cc4099b.PNG)

- Here you can search for key and value pairs

![8012](https://user-images.githubusercontent.com/85270361/210274984-2f56c719-ae18-4f22-95da-ee9c2815706f.PNG)

- For example, when you type nginx in the search bar, it shows all the configured options for the nginx proxy.


![8013](https://user-images.githubusercontent.com/85270361/210275282-cf8c991f-e8ee-4485-8cbb-e8868b434981.PNG)


- selecting nginx.enabled from the list will take you directly to the configuration in the YAML file.


![8014](https://user-images.githubusercontent.com/85270361/210275574-44b15341-4676-48ce-a793-d6c161143ecd.PNG)

- Search for nginx.service and select nginx.service.type

![8015](https://user-images.githubusercontent.com/85270361/210275729-209f149e-8b9d-42f7-aa8f-d9447e646844.PNG)


- You will see the confired type of Kubernetes service for Nginx. As you can see, it is LoadBalancer by default


![8016](https://user-images.githubusercontent.com/85270361/210275886-4ad33f36-c24b-4f66-96e3-ea662172fe6b.PNG)

- To work directly with the values.yaml file, you can download the file locally by clicking on the download icon.


![8017](https://user-images.githubusercontent.com/85270361/210276075-3b0cea7a-1ebb-466d-9258-831350d916e2.PNG)


Is the Load Balancer Service type the Ideal configuration option to use in the Real World?

Setting the service type to Load Balancer is the easiest way to get started with exposing applications running in kubernetes
externally. But provissioning load balancers for each application can become very expensive over time, and more difficult to manage.
Especially when tens or even hundreds of applications are deployed.

The best approach is to use [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) instead. But to do
that, we will have to deploy an [Ingress Controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/).

A huge benefit of using the ingress controller is that we will be able to use a single load balancer for different applications we 
deploy. Therefore, Artifactory and any other tools can reuse the same load balancer. Which reduces cloud cost, and overhead of
managing multiple load balancers. more on that later.

For now, we will leave artifactory, move on to the next phase of configuration (Ingress, DNS(Route53) and Cert Manager), and then 
return to Artifactory to complete the setup so that it can serve as a private docker registry and repository for private helm charts.
