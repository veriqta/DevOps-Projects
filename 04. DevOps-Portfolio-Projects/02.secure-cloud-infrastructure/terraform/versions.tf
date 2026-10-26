terraform {
  required_version = ">= 1.10, < 2.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 6.0" }
  }
  backend "s3" {}
}
provider "aws" {
  region = var.region
  default_tags { tags = { Project = "orders-foundation", Environment = var.environment, ManagedBy = "Terraform" } }
}
variable "region" { type = string }
variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "prod"], var.environment)
    error_message = "Use dev or prod."
  }
}
variable "allowed_cidr" {
  type = string
  validation {
    condition     = can(cidrnetmask(var.allowed_cidr)) && endswith(var.allowed_cidr, "/32")
    error_message = "Use your public IPv4 /32."
  }
}
variable "cidr" { type = string }
data "aws_availability_zones" "available" { state = "available" }
data "aws_ssm_parameter" "ubuntu" { name = "/aws/service/canonical/ubuntu/server/24.04/stable/current/amd64/hvm/ebs-gp3/ami-id" }
locals {
  name = "orders-${var.environment}"
  azs  = slice(data.aws_availability_zones.available.names, 0, 2)
}
