# SET UP A VIRTUAL PRIVATE NETWORK (VPC)

Set Up a Virtual Private Network (VPC)
Always make reference to the architectural diagram and ensure that your configuration is aligned with it.

1. Create a [VPC](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
2. Create subnets as shown in the architecture
3. Create a route table and associate it with public subnets
4. Create a route table and associate it with private subnets
5. Create an [Internet Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html)
6. Edit a route in public route table, and associate it with the Internet Gateway. (This is what allows a public subnet to be accisble 
from the Internet)
7. Create 3 [Elastic IPs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html)
8. Create a Nat Gateway and assign one of the Elastic IPs (*The other 2 will be used by 
[Bastion hosts](https://aws.amazon.com/solutions/implementations/linux-bastion/))
9. Create a Security Group for:


- Nginx Servers: Access to Nginx should only be allowed from a Application Load balancer (ALB). At this point, we have not created a 
load balancer, therefore we will update the rules later. For now, just create it and put some dummy records as a place holder.

- Bastion Servers: Access to the Bastion servers should be allowed only from workstations that need to SSH into the bastion servers.
Hence, you can use your workstation public IP address. To get this information, simply go to your terminal and type 
curl www.canhazip.com

- Application Load Balancer: ALB will be available from the Internet

- Webservers: Access to Webservers should only be allowed from the Nginx servers. Since we do not have the servers created yet, just
put some dummy records as a place holder, we will update it later.

- Data Layer: Access to the Data layer, which is comprised of Amazon Relational Database Service (RDS) and Amazon Elastic File 
System (EFS) must be carefully desinged – only webservers should be able to connect to RDS, while Nginx and Webservers will have 
access to EFS Mountpoint.


Proceed With Compute Resources
You will need to set up and configure compute resources inside your VPC. The recources related to compute are:

- EC2 Instances
- Launch Templates
- Target Groups
- Autoscaling Groups
- TLS Certificates
- Application Load Balancers (ALB)


## Set Up Compute Resources for Nginx
Provision EC2 Instances for Nginx

1. Create an EC2 Instance based on CentOS Amazon Machine Image (AMI) in any 2 Availability Zones (AZ) in any AWS Region 
(it is recommended to use the Region that is closest to your customers). Use EC2 instance of T2 family (e.g. t2.micro or similar)

2. Ensure that it has the following software installed:

- python
- ntp
- net-tools
- vim
- wget
- telnet
- epel-release
- htop


3. Create an AMI out of the EC2 instance

Prepare Launch Template For Nginx (One Per Subnet)
1. Make use of the AMI to set up a launch template
2. Ensure the Instances are launched into a public subnet
3. Assign appropriate security group
4. Configure Userdata to update yum package repository and install nginx


## Configure Target Groups

1. Select Instances as the target type
2. Ensure the protocol HTTPS on secure TLS port 443
3. Ensure that the health check path is /healthstatus
4. Register Nginx Instances as targets
5. Ensure that health check passes for the target group

## Configure Autoscaling For Nginx

1. Select the right launch template
2. Select the VPC
3. Select both public subnets
4. Enable Application Load Balancer for the AutoScalingGroup (ASG)
5. Select the target group you created before
6. Ensure that you have health checks for both EC2 and ALB
7. The desired capacity is 2
8. Minimum capacity is 2
9. Maximum capacity is 4
10. Set scale out if CPU utilization reaches 90%



## Set Up Compute Resources for Bastion
Provision the EC2 Instances for Bastion

1. Create an EC2 Instance based on CentOS Amazon Machine Image (AMI) per each Availability Zone in the same Region and same AZ 
where you created Nginx server
2. Ensure that it has the following software installed

- python
- ntp
- net-tools
- vim
- wget
- telnet
- epel-release
- htop


3. Associate an Elastic IP with each of the Bastion EC2 Instances
4. Create an AMI out of the EC2 instance

Prepare Launch Template For Bastion (One per subnet)

1. Make use of the AMI to set up a launch template
2. Ensure the Instances are launched into a public subnet
3. Assign appropriate security group
4. Configure Userdata to update yum package repository and install Ansible and git


Configure Target Groups

1. Select Instances as the target type
2. Ensure the protocol is TCP on port 22
3. Register Bastion Instances as targets
4. Ensure that health check passes for the target group


Configure Autoscaling For Bastion

1. Select the right launch template
2. Select the VPC
3. Select both public subnets
4. Enable Application Load Balancer for the AutoScalingGroup (ASG)
5. Select the target group you created before
6. Ensure that you have health checks for both EC2 and ALB
7. The desired capacity is 2
8. Minimum capacity is 2
9. Maximum capacity is 4
10. Set scale out if CPU utilization reaches 90%
11. Ensure there is an SNS topic to send scaling notifications


Set Up Compute Resources for Webservers

Provision the EC2 Instances for Webservers
Now, you will need to create 2 separate launch templates for both the WordPress and Tooling websites

1. Create an EC2 Instance (Centos) each for WordPress and Tooling websites per Availability Zone (in the same Region).

2. Ensure that it has the following software installed

- python
- ntp
- net-tools
- vim
- wget
- telnet
- epel-release
- htop
- php



3. Create an AMI out of the EC2 instance

Prepare Launch Template For Webservers (One per subnet)

1. Make use of the AMI to set up a launch template
2. Ensure the Instances are launched into a public subnet
3. Assign appropriate security group
4. Configure Userdata to update yum package repository and install wordpress (Only required on the WordPress launch template)




TLS Certificates From Amazon Certificate Manager (ACM)

You will need TLS certificates to handle secured connectivity to your Application Load Balancers (ALB).

1. Navigate to AWS ACM
2. Request a public wildcard certificate for the domain name you registered in Freenom
3. Use DNS to validate the domain name
4. Tag the resource
