Before we go deeper into automating other parts of our infrastructure on AWS, it is very important to fully understand certain concepts
around Networking (in case this is completely new area to you). Networking is a very broad topic and some of internals of Terraform 
modules related to Networking, like cidrsubnet(), may still not be fully clear to you.

To fully clear your understanding, we highly recommend you watching Networking videos by Eli the Computer Guy on YouTube, and in 
addition to that, read following golden articles on Networking Terminology, Interfaces, Protocols, IP Address, Subnets, and CIDR
Notation by Justin Ellingwood from Digital Ocean.

Eli the Computer Guy videos
- [Introduction to Networking](https://youtu.be/rL8RSFQG8do)
- [TCP/IP and Subnet Masking](https://youtu.be/EkNq4TrHP_U)


If you are interested to dive deeper into Networking domain, you can watch the entire playlist
[here](https://www.youtube.com/playlist?list=PLF360ED1082F6F2A5)

Justin Ellingwood blog posts
**WARNING:** You may initially feel overwhelmed by the information provided in these articles. It is fine if you don not fully understand
them the first time. Bookmark the pages, read them again and again for the next few days. Find other articles talking about the same
topics on Google and watch YouTube videos about them. Subconsciously, you will begin to understand them over time.

- [Networking Part 1](https://www.digitalocean.com/community/tutorials/an-introduction-to-networking-terminology-interfaces-and-protocols)
- [Networking Part 1](https://www.digitalocean.com/community/tutorials/understanding-ip-addresses-subnets-and-cidr-notation-for-networking#netmasks-and-subnets)


Continue Infrastructure Automation with Terraform
Let us continue from where we have stopped in Project 16.

Based on the knowledge from the previous project lets keep on creating AWS resources!

## Networking
Private subnets & best practices
Create 4 private subnets keeping in mind following principles:

- Make sure you use variables or length() function to determine the number of AZs
- Use variables and cidrsubnet() function to allocate vpc_cidr for subnets
- Keep variables and resources in separate files for better code structure and readability
- Tags all the resources you have created so far. Explore how to use format() and count functions to automatically tag subnets 
with its respective number.


A little bit more about Tagging
Tagging is a straightforward, but a very powerful concept that helps you manage your resources much more efficiently:

- Resources are much better organized in ‘virtual’ groups
- They can be easily filtered and searched from console or programmatically
- Billing team can easily generate reports and determine how much each part of infrastructure costs how much (by department, by type, 
by environment, etc.)
- You can easily determine resources that are not being used and take actions accordingly
- If there are different teams in the organisation using the same account, tagging can help differentiate who owns which resources.


**Note:** You can add multiple tags as a default set. for example, in out terraform.tfvars file we can have default tags 
defined.

```
tags = {
  Enviroment      = "production" 
  Owner-Email     = "dare@darey.io"
  Managed-By      = "Terraform"
  Billing-Account = "1234567890"
}
```

Now you can tag all you resources using the format below

```
tags = merge(
    var.tags,
    {
      Name = "Name of the resource"
    },
  )
```

**NOTE:** Update the variables.tf to declare the variable tags used in the format above;

```
variable "tags" {
  description = "A mapping of tags to assign to all resources."
  type        = map(string)
  default     = {}
}
```


The nice thing about this is – anytime we need to make a change to the tags, we simply do that in one single place (terraform.tfvars).

But, our key-value pairs are hard coded. So, go ahead and work out a fix for that. Simply create variables for each value and use 
var.variable_name as the value to each of the keys.

Apply the same best practices for all other resources you will create further.

Internet Gateways & format() function
Create an Internet Gateway in a separate Terraform file internet_gateway.tf


```
resource "aws_internet_gateway" "ig" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name = format("%s-%s!", aws_vpc.main.id,"IG")
    } 
  )
}
```


Did you notice how we have used format() function to dynamically generate a unique name for this resource? The first part of the %s
takes the interpolated value of aws_vpc.main.id while the second %s appends a literal string IG and finally an exclamation mark is 
added in the end.

If any of the resources being created is either using the count function, or creating multiple resources using a loop, then a 
key-value pair that needs to be unique must be handled differently.

For example, each of our subnets should have a unique name in the tag section. Without the format() function, we would not be able 
to see uniqueness. With the format function, each private subnet’s tag will look like this.


```
Name = PrvateSubnet-0
Name = PrvateSubnet-1
Name = PrvateSubnet-2
```

Lets try and see that in action.

```
tags = merge(
    var.tags,
    {
      Name = format("PrivateSubnet-%s", count.index)
    } 
  )
```


NAT Gateways
Create 1 NAT Gateways and 1 Elastic IP (EIP) addresses

Now use similar approach to create the NAT Gateways in a new file called natgateway.tf.

Note: We need to create an Elastic IP for the NAT Gateway, and you can see the use of depends_on to indicate that the Internet Gateway
resource must be available before this should be created. Although Terraform does a good job to manage dependencies, but in some 
cases, it is good to be explicit.

You can read more on dependencies [here](https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on)

```
resource "aws_eip" "nat_eip" {
  vpc        = true
  depends_on = [aws_internet_gateway.ig]

  tags = merge(
    var.tags,
    {
      Name = format("%s-EIP", var.name)
    },
  )
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = element(aws_subnet.public.*.id, 0)
  depends_on    = [aws_internet_gateway.ig]

  tags = merge(
    var.tags,
    {
      Name = format("%s-Nat", var.name)
    },
  )
}

```

