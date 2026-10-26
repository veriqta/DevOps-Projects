# CONFIGURE APPLICATION LOAD BALANCER (ALB)

## Application Load Balancer To Route Traffic To NGINX
Nginx EC2 Instances will have configurations that accepts incoming traffic only from Load Balancers. No request should go directly
to Nginx servers. With this kind of setup, we will benefit from intelligent routing of requests from the ALB to Nginx servers 
across the 2 Availability Zones. We will also be able to offload SSL/TLS certificates on the ALB instead of Nginx. Therefore, 
Nginx will be able to perform faster since it will not require extra compute resources to valifate certificates for every request.


1. Create an Internet facing ALB
2. Ensure that it listens on HTTPS protocol (TCP port 443)
3. Ensure the ALB is created within the appropriate VPC | AZ | Subnets
4. Choose the Certificate from ACM
5. Select Security Group
6. Select Nginx Instances as the target group


## Application Load Balancer To Route Traffic To Web Servers
Since the webservers are configured for auto-scaling, there is going to be a problem if servers get dynamically scalled out or in. 
Nginx will not know about the new IP addresses, or the ones that get removed. Hence, Nginx will not know where to direct the traffic.

To solve this problem, we must use a load balancer. But this time, it will be an internal load balancer. Not Internet facing since
the webservers are within a private subnet, and we do not want direct access to them.


1. Create an Internal ALB
2. Ensure that it listens on HTTPS protocol (TCP port 443)
3. Ensure the ALB is created within the appropriate VPC | AZ | Subnets
4. Choose the Certificate from ACM
5. Select Security Group
6. Select webserver Instances as the target group
7. Ensure that health check passes for the target group


## NOTE: This process must be repeated for both WordPress and Tooling websites.

## Setup EFS
Amazon Elastic File System (Amazon EFS) provides a simple, scalable, fully managed elastic Network File System (NFS) for use with
AWS Cloud services and on-premises resources. In this project, we will utulize EFS service and mount filesystems on both Nginx 
and Webservers to store data.

1. Create an EFS filesystem
2. Create an EFS mount target per AZ in the VPC, associate it with both subnets dedicated for data layer
3. Associate the Security groups created earlier for data layer.
4. Create an EFS access point. (Give it a name and leave all other settings as default)


## Setup RDS
Pre-requisite: Create a KMS key from Key Management Service (KMS) to be used to encrypt the database instance.

Amazon Relational Database Service (Amazon RDS) is a managed distributed relational database service by Amazon Web Services. 
This web service running in the cloud designed to simplify setup, operations, maintenans & scaling of relational databases. 
Without RDS, Database Administrators (DBA) have more work to do, due to RDS, some DBAs have become jobless

To ensure that yout databases are highly available and also have failover support in case one availability zone fails, we will 
configure a multi-AZ set up of RDS MySQL database instance. In our case, since we are only using 2 AZs, we can only failover to
one, but the same concept applies to 3 Availability Zones. We will not consider possible failure of the whole Region, but for 
this AWS also has a solution – this is a more advanced concept that will be discussed in following projects.

To configure RDS, follow steps below:

1. Create a subnet group and add 2 private subnets (data Layer)
2. Create an RDS Instance for mysql 8.*.*
3. To satisfy our architectural diagram, you will need to select either Dev/Test or Production Sample Template. But to minimize AWS 
cost, you can select the Do not create a standby instance option under Availability & durability sample template (The production 
template will enable Multi-AZ deployment)
4. Configure other settings accordingly (For test purposes, most of the default settings are good to go). In the real world, you will
need to size the database appropriately. You will need to get some information about the usage. If it is a highly transactional 
database that grows at 10GB weekly, you must bear that in mind while configuring the initial storage allocation, storage autoscaling, 
and maximum storage threshold.
5. Configure VPC and security (ensure the database is not available from the Internet)
6. Configure backups and retention
7. Encrypt the database using the KMS key created earlier
8.Enable CloudWatch monitoring and export Error and Slow Query logs (for production, also include Audit)


## Note This service is an expensinve one. Ensure to review the monthly cost before creating. (DO NOT LEAVE ANY SERVICE RUNNING FOR LONG)

## Configuring DNS with Route53
Earlier in this project you registered a free domain with Freenom and configured a hosted zone in Route53. But that is not all 
that needs to be done as far as DNS configuration is concerned.

You need to ensure that the main domain for the WordPress website can be reached, and the subdomain for Tooling website can also be 
reached using a browser.

Create other records such as CNAME, alias and A records.

**NOTE:** You can use either CNAME or alias records to achieve the same thing. But alias record has better functionality because it is 
a faster to resolve DNS record, and can coexist with other records on that name. Read here to get to know more about the differences.


- Create an alias record for the root domain and direct its traffic to the ALB DNS name.
- Create an alias record for tooling.<yourdomain>.com and direct its traffic to the ALB DNS name.
  
  
Congratulations!


![6093](https://user-images.githubusercontent.com/85270361/210172232-c67f275b-621a-4338-bf19-dec4fc0e08be.PNG)

You have just created a secured, scalable and cost-effective infrastructure to host 2 enterprise websites using various Cloud services
from AWS. At this point, your infrastructure is ready to host real websites’ load. Since it is a pretty expensive infrastructure
to keep it up and running, we are going to start using Infrastructure as Code tool Terraform to easily provision and destroy this
set up.

Move on for more amazing and challenging projects ahead!

