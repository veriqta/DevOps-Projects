# DEPLOYING CERT-MANAGER AND MANAGING TLS/SSL FOR INGRESS

Transport Layer Security (TLS), the successor of the now-deprecated Secure Sockets Layer (SSL), is a cryptographic protocol designed
to provide communications security over a computer network.

The TLS protocol aims primarily to provide cryptography, including privacy (confidentiality), integrity, and authenticity through 
the use of certificates, between two or more communicating computer applications.

The certificates required to implement TLS must be issued by a trusted Certificate Authority (CA).

To see the list of trusted root Certification Authorities (CA) and their certificates used by Google Chrome, you need to use the 
Certificate Manager built inside Google Chrome as shown below:

1. Open the settings section of google chrome

2. Search for security

![9021](https://user-images.githubusercontent.com/85270361/210282861-f82a2bd0-a9db-4df9-9132-5d911940031b.PNG)

3. Select Manage Certificates

![9022](https://user-images.githubusercontent.com/85270361/210282892-57905860-6018-40c8-a84d-cb3aa470cc66.PNG)

4. View the installed certificates in your browser

![9023](https://user-images.githubusercontent.com/85270361/210282908-ad1b6d20-8358-4a07-b710-2d9749027794.PNG)


## Certificate Management in Kubernetes
Ensuring that trusted certificates can be requested and issued from certificate authorities dynamically is a tedious process.
Managing the certificates per application and keeping track of expiry is also a lot of overhead.

To do this, administrators will have to write complex scripts or programs to handle all the logic.

[Cert-Manager](https://cert-manager.io/) comes to the rescue!

cert-manager adds certificates and certificate issuers as resource types in Kubernetes clusters, and simplifies the process of
obtaining, renewing and using those certificates.

Similar to how Ingress Controllers are able to enable the creation of Ingress resource in the cluster, so also cert-manager enables
the possibility to create certificate resource, and a few other resources that makes certificate management seamless.

It can issue certificates from a variety of supported sources, including [Let’s Encrypt](https://letsencrypt.org/),
[HashiCorp Vault](https://www.vaultproject.io/), and [Venafi](https://www.venafi.com/) as well as 
[private PKI](https://www.csoonline.com/article/3400836/what-is-pki-and-how-it-secures-just-about-everything-online.html). The issued
certificates get stored as kubernetes secret which holds both the private key and public certificate.


![9024](https://user-images.githubusercontent.com/85270361/210283377-d57f9bd0-27b1-41f8-a330-29e89581b33e.PNG)


In this project, We will use Let’s Encrypt with cert-manager. The certificates issued by Let’s Encrypt will work with most browsers
because the root certificate that validates all it’s certificates is called “ISRG Root X1” which is already trusted by most browsers
and servers.

You will find ISRG Root X1 in the list of certificates already installed in your browser.


![9025](https://user-images.githubusercontent.com/85270361/210283444-88f87752-c5f7-4d55-aa12-db4078f53cf3.PNG)

Read the [official documentation here](https://letsencrypt.org/docs/certificate-compatibility/)

Cert-maanager will ensure certificates are valid and up to date, and attempt to renew certificates at a configured time before expiry.

## Cert-Manager high Level Architecture

Cert-manager works by having administrators create a resource in kubernetes called certificate issuer which will be configured to
work with supported sources of certificates. This issuer can either be scoped globally in the cluster or only local to the namespace
it is deployed to.

Whenever it is time to create a certificate for a specific host or website address, the process follows the pattern seen in the 
image below.

![9026](https://user-images.githubusercontent.com/85270361/210283598-ccac17e1-54b0-46c7-9764-8c9d182a2439.PNG)


After we have deployed cert-manager, you will see all of this in action.

## Deploying Cert-manager

**Self Challenge** Task Find cert-manager helm chart in Artifact Hub, follow the installation guide and deploy into Kubernetes
You should see an output like this

```
NAME: cert-manager
LAST DEPLOYED: Fri Mar 11 14:15:51 2022
NAMESPACE: cert-manager
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
cert-manager v1.7.1 has been deployed successfully!

In order to begin issuing certificates, you will need to set up a ClusterIssuer
or Issuer resource (for example, by creating a 'letsencrypt-staging' issuer).

More information on the different types of issuers and how to configure them
can be found in our documentation:

https://cert-manager.io/docs/configuration/

For information on how to configure cert-manager to automatically provision
Certificates for Ingress resources, take a look at the `ingress-shim`
documentation:

https://cert-manager.io/docs/usage/ingress/
```


**Certificate Issuer**
Next, is to create an Issuer. We will use a Cluster Issuer so that it can be scoped globally. Assuming that we will be using
total.com domain. Simply update this yaml file and deploy with kubectl. In the section that follows, we will break down each part
of the file.

```
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  namespace: "cert-manager"
  name: "letsencrypt-prod"
spec:
  acme:
    server: "https://acme-v02.api.letsencrypt.org/directory"
    email: "infradev@oldcowboyshop.com"
    privateKeySecretRef:
      name: "letsencrypt-prod"
    solvers:
    - selector:
        dnsZones:
          - "darey.io"
      dns01:
        route53:
          region: "eu-west-2"
          hostedZoneID: "Z2CD4NTR2FDPZ"
```

Lets break down the content to undertsand all the sections

Section 1 – The standard kubernetes section that defines the apiVersion, Kind, and metadata. The Kind here is a ClusterIssuer 
which means it is scoped globally.

```
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
namespace: "cert-manager"
name: "letsencrypt-prod"
```

Section 2 – In the spec section, an [ACME](https://cert-manager.io/docs/configuration/acme/) – Automated Certificate Management 
Environment issuer type is specified here. When you create a new ACME Issuer, cert-manager will generate a private key which is 
used to identify you with the ACME server.

Certificates issued by public ACME servers are typically trusted by client’s computers by default. This means that, for example, 
visiting a website that is backed by an ACME certificate issued for that URL, will be trusted by default by most client’s web 
browsers. ACME certificates are typically free.

Let’s Encrypt uses the ACME protocol to verify that you control a given domain name and to issue you a certificate. You can either
use the let’s encrypt Production server address https://acme-v02.api.letsencrypt.org/directory which can be used for all production
websites. Or it can be replaced with the staging URL https://acme-staging-v02.api.letsencrypt.org/directory for all Non-Production 
sites.

The privateKeySecretRef has configuration for the private key name you prefer to use to store the ACME account private key. This 
can be anything you specify, for example letsencrypt-prod


````
spec:
 acme:
    # The ACME server URL
    server: "https://acme-v02.api.letsencrypt.org/directory"
    email: "infradev@darey.io"
    # Name of a secret used to store the ACME account private key
    privateKeySecretRef:
    name: "letsencrypt-prod" 
````


section 3 – This section is part of the spec that configures solvers which determines the domain address that the issued
certificate will be registered with. dns01 is one of the different challenges that cert-manager uses to verify domain ownership.
[Read more on DNS01 Challenge here](https://letsencrypt.org/docs/challenge-types/#dns-01-challenge). With the DNS01 configuration,
you will need to specify the Route53 DNS Hosted Zone ID and region. Since we are using EKS in AWS, the IAM permission of the worker
nodes will be used to access Route53. Therefore if appropriate permissions is not set for EKS worker nodes, it is possible that
certificate challenge with Route53 will fail, hence certificates will not get issued.

The other possible option is the [HTTP01](https://cert-manager.io/docs/configuration/acme/http01/#configuring-the-http01-ingress-solver)
challenge, but we won’t be using that here.


```
solvers:
- selector:
    dnsZones:
    - "total.com"
dns01:
    route53:
    region: "eu-west-2"
    hostedZoneID: "Z2CD4NTR2FDPZ"  
```


With the ClusterIssuer properlu configured, it is now time to start getting certificates issued.

Lets see what that looks like in the next section.
