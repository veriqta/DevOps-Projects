# AWS ROUTES

Create a file called route_tables.tf and use it to create routes for both public and private subnets, create the below resources.
Ensure they are properly tagged.

- aws_route_table
- aws_route
- aws_route_table_association


```
# create private route table
resource "aws_route_table" "private-rtb" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name = format("%s-Private-Route-Table", var.name)
    },
  )
}

# associate all private subnets to the private route table
resource "aws_route_table_association" "private-subnets-assoc" {
  count          = length(aws_subnet.private[*].id)
  subnet_id      = element(aws_subnet.private[*].id, count.index)
  route_table_id = aws_route_table.private-rtb.id
}

# create route table for the public subnets
resource "aws_route_table" "public-rtb" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name = format("%s-Public-Route-Table", var.name)
    },
  )
}

# create route for the public route table and attach the internet gateway
resource "aws_route" "public-rtb-route" {
  route_table_id         = aws_route_table.public-rtb.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.ig.id
}

# associate all public subnets to the public route table
resource "aws_route_table_association" "public-subnets-assoc" {
  count          = length(aws_subnet.public[*].id)
  subnet_id      = element(aws_subnet.public[*].id, count.index)
  route_table_id = aws_route_table.public-rtb.id
}

```


Now if you run terraform plan and terraform apply it will add the following resources to AWS in multi-az set up:


## Our main vpc
– 2 Public subnets
– 4 Private subnets
– 1 Internet Gateway
– 1 NAT Gateway
– 1 EIP
– 2 Route tables


Now, we are done with Networking part of AWS set up, let us move on to Compute and Access Control configuration automation using 
Terraform!

AWS Identity and Access Management
IaM and Roles
We want to pass an IAM role our EC2 instances to give them access to some specific resources, so we need to do the following:


1. Create AssumeRole
Assume Role uses Security Token Service (STS) API that returns a set of temporary security credentials that you can use to access AWS 
resources that you might not normally have access to. These temporary credentials consist of an access key ID, a secret access key, 
and a security token. Typically, you use AssumeRole within your account or for cross-account access.

Add the following code to a new file named roles.tf


```
resource "aws_iam_role" "ec2_instance_role" {
name = "ec2_instance_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })

  tags = merge(
    var.tags,
    {
      Name = "aws assume role"
    },
  )
}

```


In this code we are creating AssumeRole with AssumeRole policy. It grants to an entity, in our case it is an EC2, permissions to 
assume the role.

2. Create IAM policy for this role

This is where we need to define a required policy (i.e., permissions) according to our requirements. For example, allowing an IAM
role to perform action describe applied to EC2 instances:



```
resource "aws_iam_policy" "policy" {
  name        = "ec2_instance_policy"
  description = "A test policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ec2:Describe*",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]

  })

  tags = merge(
    var.tags,
    {
      Name =  "aws assume policy"
    },
  )

}

```


3. Attach the Policy to the IAM Role
This is where, we will be attaching the policy which we created above, to the role we created in the first step.


```
 resource "aws_iam_role_policy_attachment" "test-attach" {
        role       = aws_iam_role.ec2_instance_role.name
        policy_arn = aws_iam_policy.policy.arn
    }
    
```


4. Create an Instance Profile and interpolate the IAM Role

```
resource "aws_iam_instance_profile" "ip" {
        name = "aws_instance_profile_test"
        role =  aws_iam_role.ec2_instance_role.name
    }
    
```



We are pretty much done with Identity and Management part for now, let us move on and create other resources required.

Resources to be created
As per our architecture we need to do the following:

1. Create Security Groups
2. Create Target Group for Nginx, WordPress and Tooling
3. Create certificate from AWS certificate manager
4. Create an External Application Load Balancer and Internal Application Load Balancer.
5. create launch template for Bastion, Tooling, Nginx and WordPress
6. Create an Auto Scaling Group (ASG) for Bastion, Tooling, Nginx and WordPress
7. Create Elastic Filesystem
8. Create Relational Database (RDS)

Let us create some Terraform configuration code to accomplish these tasks.
