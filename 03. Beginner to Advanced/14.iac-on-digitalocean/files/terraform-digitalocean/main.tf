terraform {
  required_version = ">= 1.6, < 2.0"
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}
variable "do_token" {
  type      = string
  sensitive = true
}
variable "ssh_key_fingerprint" { type = string }
provider "digitalocean" { token = var.do_token }
resource "digitalocean_droplet" "lab" {
  name     = "devops-projects-lab"
  region   = "nyc3"
  size     = "s-1vcpu-1gb"
  image    = "ubuntu-24-04-x64"
  ssh_keys = [var.ssh_key_fingerprint]
  tags     = ["devops-lab"]
}
output "address" { value = digitalocean_droplet.lab.ipv4_address }
