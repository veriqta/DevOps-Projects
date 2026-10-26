terraform {
  required_version = ">= 1.10, < 2.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 6.0" }
  }
}
provider "aws" { region = "us-east-1" }
variable "instance_type" {
  type    = string
  default = "t3.small"
}
resource "aws_instance" "estimate_only" {
  ami           = "ami-00000000000000000"
  instance_type = var.instance_type
  root_block_device { volume_size = 20 }
  lifecycle {
    precondition {
      condition     = var.instance_type == "DO-NOT-APPLY"
      error_message = "Estimate-only fixture: terraform apply is intentionally blocked."
    }
  }
}
