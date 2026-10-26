# AWS CLOUD RESOURCES FOR KUBERNETES CLUSTER

As we already know, we need some machines to run the control plane and the worker nodes. In this section, you will provision EC2 
Instances required to run your K8s cluster. You can use Terraform for this. But it is highly recommended to start out first with 
manual provisioning using awscli and have thorough knowledge about the whole setup. After that, you can destroy the entire project 
and start all over again using Terraform. This manual approach will solidify your skills and give you the opportunity to face more 
challenges.


Step 1 – Configure Network Infrastructure
**Virtual Private Cloud – **

1. Create a directory named k8s-cluster-from-ground-up
2. Create a VPC and store the ID as a variable:

```
VPC_ID=$(aws ec2 create-vpc \
--cidr-block 172.31.0.0/16 \
--output text --query 'Vpc.VpcId'
)

```


3. Tag the VPC so that it is named:

```
NAME=k8s-cluster-from-ground-up

aws ec2 create-tags \
  --resources ${VPC_ID} \
  --tags Key=Name,Value=${NAME} 
```


**Domain Name System – DNS**

4. Enable DNS support for your VPC:

```
aws ec2 modify-vpc-attribute \
--vpc-id ${VPC_ID} \
--enable-dns-support '{"Value": true}'
```

5. Enable DNS support for hostnames:

```
aws ec2 modify-vpc-attribute \
--vpc-id ${VPC_ID} \
--enable-dns-hostnames '{"Value": true}'
```

![7006](https://user-images.githubusercontent.com/85270361/210191966-626e2e0b-085b-4e64-944e-5d9b789a87d6.PNG)


**AWS Region**

6. Set the required region

```
AWS_REGION=eu-central-1
```


**Dynamic Host Configuration Protocol – DHCP**

7. Configure DHCP Options Set:

[Dynamic Host Configuration Protocol (DHCP)](https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol)is a network 
management protocol used on Internet Protocol networks for automatically assigning IP addresses and other communication parameters
to devices connected to the network using a client–server architecture.

**AWS** automatically creates and associates a DHCP option set for your **Amazon VPC** upon creation and sets two options: 
domain-name-servers (defaults to AmazonProvidedDNS) and **domain-name** (defaults to the domain name for your set region). 
**AmazonProvidedDNS** is an Amazon Domain Name System (DNS) server, and this option enables DNS for instances to communicate using
DNS names.

By default EC2 instances have fully qualified names like ip-172-50-197-106.eu-central-1.compute.internal. 
But you can set your own configuration using an example below.


```
DHCP_OPTION_SET_ID=$(aws ec2 create-dhcp-options \
  --dhcp-configuration \
    "Key=domain-name,Values=$AWS_REGION.compute.internal" \
    "Key=domain-name-servers,Values=AmazonProvidedDNS" \
  --output text --query 'DhcpOptions.DhcpOptionsId')
```


8. Tag the DHCP Option set:

```
aws ec2 create-tags \
  --resources ${DHCP_OPTION_SET_ID} \
  --tags Key=Name,Value=${NAME}
```


![7007](https://user-images.githubusercontent.com/85270361/210192103-d973f4af-3a3f-4ad9-8536-d087c8529855.PNG)


9. Associate the DHCP Option set with the VPC:

```
aws ec2 associate-dhcp-options \
  --dhcp-options-id ${DHCP_OPTION_SET_ID} \
  --vpc-id ${VPC_ID}
```

![7008](https://user-images.githubusercontent.com/85270361/210192123-64f6e029-84d5-4ae1-b550-e244f54328cb.PNG)


**Subnet**

10. Create the Subnet:

```
SUBNET_ID=$(aws ec2 create-subnet \
  --vpc-id ${VPC_ID} \
  --cidr-block 172.31.0.0/24 \
  --output text --query 'Subnet.SubnetId')
```


```
aws ec2 create-tags \
  --resources ${SUBNET_ID} \
  --tags Key=Name,Value=${NAME}
```

**Internet Gateway – IGW**

11. Create the Internet Gateway and attach it to the VPC:

```
INTERNET_GATEWAY_ID=$(aws ec2 create-internet-gateway \
  --output text --query 'InternetGateway.InternetGatewayId')
aws ec2 create-tags \
  --resources ${INTERNET_GATEWAY_ID} \
  --tags Key=Name,Value=${NAME}
```


```
aws ec2 attach-internet-gateway \
  --internet-gateway-id ${INTERNET_GATEWAY_ID} \
  --vpc-id ${VPC_ID}
```



**Route tables**

12. Create route tables, associate the route table to subnet, and create a route to allow external traffic to the Internet through 
the Internet Gateway:

```
ROUTE_TABLE_ID=$(aws ec2 create-route-table \
  --vpc-id ${VPC_ID} \
  --output text --query 'RouteTable.RouteTableId')
aws ec2 create-tags \
  --resources ${ROUTE_TABLE_ID} \
  --tags Key=Name,Value=${NAME}
aws ec2 associate-route-table \
  --route-table-id ${ROUTE_TABLE_ID} \
  --subnet-id ${SUBNET_ID}
aws ec2 create-route \
  --route-table-id ${ROUTE_TABLE_ID} \
  --destination-cidr-block 0.0.0.0/0 \
  --gateway-id ${INTERNET_GATEWAY_ID}
 ```
 
 
 
**OUTPUT:**
 
 ```
 {
    "AssociationId": "rtbassoc-07a8877e92504def7",
    "AssociationState": {
        "State": "associated"
    }
}
{
    "Return": true
}
```
