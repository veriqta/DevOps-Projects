# STEP 0-INSTALL CLIENT TOOLS BEFORE BOOTSTRAPPING THE CLUSTER.

First, you will need some client tools installed and configurations made on your client workstation:


- [awscli](https://aws.amazon.com/cli/) – is a unified tool to manage your AWS services
- [kubectl](https://kubernetes.io/docs/reference/kubectl/) – this command line utility will be your main control tool to manage your 
K8s cluster. You will use this tool so many times, so you will be able to type ‘kubetcl’ on your keyboard with a speed of light. 
You can always make a shortcut (alias) to just one character ‘k’. Also, add this extremely useful official kubectl Cheat Sheet to 
your bookmarks, it has examples of the most used ‘kubectl’ commands.
- [cfssl](https://blog.cloudflare.com/introducing-cfssl/) – an open source toolkit for everything TLS/SSL from [Cloudflare](https://www.cloudflare.com/)
- [cfssljson](https://github.com/cloudflare/cfssl) – a program, which takes the JSON output from the cfssl and writes certificates, 
keys, [CSRs](https://en.wikipedia.org/wiki/Certificate_signing_request), and bundles to disk.


###### Install and configure AWS CLI

Configure AWS CLI to access all AWS services used, for this you need to have a user with programmatic access keys configured in
AWS Identity and Access Management (IAM):

![7005](https://user-images.githubusercontent.com/85270361/210191009-63846055-15cb-4626-a714-727fd4999e68.PNG)


Generate access keys and store them in a safe place.

On your local workstation download and install the latest version of [AWS CLI](https://aws.amazon.com/cli/)

[To configure your AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) – run your shell 
(or cmd if using Windows) and run:


```
aws configure --profile %your_username%
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: json
```


Test your AWS CLI by running:

```
aws ec2 describe-vpcs
```

and check if you can see VPC details.

###### Install kubectl

Kubernetes cluster has a Web API that can receive HTTP/HTTPS requests, but it is quite cumbersome to curl an API each and every time
you need to send some command, so kubectl command tool was developed to ease a K8s administrator’s life.

With this tool you can easily interact with Kubernetes to deploy applications, inspect and manage cluster resources, view logs and
perform many more administrative operations.


## Installing kubectl

| install kubectl-Linux | Install kubectl-mac |
| :--- | :---: |
| Linux Or Windows using Gitbash or similar tool | Mac OS X |
| Download the binary | Download the binary | 
| wget https://storage.googleapis.com/kubernetes-release/release/v1.21.0/bin/linux/amd64/kubectl | curl -o kubectl https://storage.googleapis.com/kubernetes-release/release/v1.21.0/bin/darwin/amd64/kubectl |
| Make it executable --> chmod +x kubectl | Make it executable --> chmod +x kubectl |
| Move to the Bin directory --> sudo mv kubectl /usr/local/bin/ | Move to the Bin directory --> sudo mv kubectl /usr/local/bin/ |
| Verify that kubectl version 1.21.0 or higher is installed: --> kubectl version --client | | 


**Output:**

```
Client Version: version.Info{Major:"1", Minor:"20+", GitVersion:"v1.20.4-dirty", GitCommit:"e87da0bd6e03ec3fea7933c4b5263d151aafd07c", GitTreeState:"dirty", 
BuildDate:"2021-03-15T10:03:32Z", GoVersion:"go1.16.2", Compiler:"gc", Platform:"darwin/amd64"}
```


####### Install CFSSL and CFSSLJSON

cfssl is an open source tool by **Cloudflare** used to setup a **Public Key Infrastructure** [(PKI Infrastructure)](https://en.wikipedia.org/wiki/Public_key_infrastructure)
for generating, signing and bundling TLS certificates.
In previous projects you have experienced the use of **Letsencrypt** for the similar use case. Here, cfssl will be configured as 
a Certificate Authority which will issue the certificates required to spin up a Kubernetes cluster.

Download, install and verify successful installation of cfssl and cfssljson:


## Install CFSSL and CFSSLJSON-linux

```
wget -q --show-progress --https-only --timestamping \
  https://storage.googleapis.com/kubernetes-the-hard-way/cfssl/1.4.1/linux/cfssl \
  https://storage.googleapis.com/kubernetes-the-hard-way/cfssl/1.4.1/linux/cfssljson
  
```

```
chmod +x cfssl cfssljson
```

```
sudo mv cfssl cfssljson /usr/local/bin/
```



## Install CFSSL and CFSSLJSON-mac

```
curl -o cfssl https://storage.googleapis.com/kubernetes-the-hard-way/cfssl/1.4.1/darwin/cfssl
curl -o cfssljson https://storage.googleapis.com/kubernetes-the-hard-way/cfssl/1.4.1/darwin/cfssljson
```

```
chmod +x cfssl cfssljson
sudo mv cfssl cfssljson /usr/local/bin/
```

If you have issues using the binaries directly, you should consider using the package manager Homebrew and that might be a better
option:


```
brew install cfssl
```

Verify that cfssl version 1.4.1 or higher is installed:

Output:
cfssl version

Version: 1.4.1
Runtime: go1.12.12
cfssljson --version

Version: 1.4.1
Runtime: go1.12.12
