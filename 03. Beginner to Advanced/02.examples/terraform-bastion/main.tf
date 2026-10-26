terraform {
  required_version = ">= 1.6, < 2.0"
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}
provider "aws" { region = var.region }
variable "region" {
  type = string
  default = "us-east-1"
}
variable "my_ip_cidr" {
  type = string
  description = "Your public IPv4 /32 for SSH"
  validation {
    condition = can(cidrnetmask(var.my_ip_cidr)) && endswith(var.my_ip_cidr, "/32")
    error_message = "Supply your public IPv4 address followed by /32."
  }
}
variable "key_name" { type = string }
data "aws_ssm_parameter" "ubuntu" {
  name = "/aws/service/canonical/ubuntu/server/24.04/stable/current/amd64/hvm/ebs-gp3/ami-id"
}
resource "aws_vpc" "lab" {
  cidr_block = "10.88.0.0/16"
  tags = { Name = "devops-bastion-lab" }
}
resource "aws_subnet" "public" {
  vpc_id = aws_vpc.lab.id
  cidr_block = "10.88.1.0/24"
  map_public_ip_on_launch = true
}
resource "aws_subnet" "private" {
  vpc_id = aws_vpc.lab.id
  cidr_block = "10.88.2.0/24"
}
resource "aws_internet_gateway" "lab" { vpc_id = aws_vpc.lab.id }
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.lab.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.lab.id
  }
}
resource "aws_route_table_association" "public" {
  subnet_id = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}
resource "aws_security_group" "bastion" {
  name_prefix = "devops-bastion-"
  vpc_id = aws_vpc.lab.id
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = [var.my_ip_cidr]
  }
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "aws_security_group" "private" {
  name_prefix = "devops-private-"
  vpc_id = aws_vpc.lab.id
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    security_groups = [aws_security_group.bastion.id]
  }
}
resource "aws_instance" "bastion" {
  ami = data.aws_ssm_parameter.ubuntu.value
  instance_type = "t3.micro"
  subnet_id = aws_subnet.public.id
  key_name = var.key_name
  vpc_security_group_ids = [aws_security_group.bastion.id]
  metadata_options { http_tokens = "required" }
  tags = { Name = "devops-bastion-lab" }
}
resource "aws_instance" "private" {
  ami = data.aws_ssm_parameter.ubuntu.value
  instance_type = "t3.micro"
  subnet_id = aws_subnet.private.id
  key_name = var.key_name
  associate_public_ip_address = false
  vpc_security_group_ids = [aws_security_group.private.id]
  metadata_options { http_tokens = "required" }
  tags = { Name = "devops-private-lab" }
}
output "bastion_ip" { value = aws_instance.bastion.public_ip }
output "private_ip" { value = aws_instance.private.private_ip }
