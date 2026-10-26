# 05. Configure Access and Security Boundaries

[← 04. Build the VPC Subnets and Routes](04-build-the-vpc-subnets-and-routes.md) · [Project home](README.md) · [06. Provision the Application Compute Layer →](06-provision-the-application-compute-layer.md)

## Starting state and working directory

Complete chapter 04 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `02.secure-cloud-infrastructure` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 02.secure-cloud-infrastructure
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

An ALB security group is the only internet-facing inbound path. Its source is your /32; the application group accepts traffic from the ALB group rather than arbitrary client addresses. The instance profile enables Systems Manager without exposing SSH. This managed policy is broader than a purpose-built application IAM role but scoped to host management; no database or secret access is granted by the application itself.

## Work through the implementation

Open compute.tf in your editor and trace security-group references into the launch template and ALB. Egress from the application is intentionally broad for bootstrap and SSM in this bounded lab. A production adaptation should constrain destinations with a verified patch/management path. HTTP is used only for dummy content from your source /32; TLS and certificate lifecycle must be added before real data is transmitted.

### Commands in execution order

```bash
terraform -chdir=terraform plan -var-file=dev.tfvars -out=dev.plan
terraform -chdir=terraform show -no-color dev.plan > .lab/dev-plan.txt
grep -n -E 'allowed_cidr|from_port|security_groups|http_tokens|public_ip' .lab/dev-plan.txt
```

### Read the implementation: `terraform/compute.tf`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```hcl
resource "aws_security_group" "edge" {
  name_prefix = "${local.name}-edge-"
  vpc_id      = aws_vpc.main.id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [var.allowed_cidr]
  }
  egress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [var.cidr]
  }
}
resource "aws_security_group" "app" {
  name_prefix = "${local.name}-app-"
  vpc_id      = aws_vpc.main.id
  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.edge.id]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "aws_iam_role" "app" {
  name_prefix        = "${local.name}-"
  assume_role_policy = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow", Principal = { Service = "ec2.amazonaws.com" }, Action = "sts:AssumeRole" }] })
}
resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.app.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}
resource "aws_iam_instance_profile" "app" { role = aws_iam_role.app.name }
resource "aws_launch_template" "app" {
  name_prefix            = "${local.name}-"
  image_id               = data.aws_ssm_parameter.ubuntu.value
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.app.id]
  iam_instance_profile { name = aws_iam_instance_profile.app.name }
  metadata_options { http_tokens = "required" }
  block_device_mappings {
    device_name = "/dev/sda1"
    ebs {
      volume_size           = 10
      volume_type           = "gp3"
      encrypted             = true
      delete_on_termination = true
    }
  }
  user_data = base64encode(<<-SCRIPT
    #!/bin/bash
    set -euxo pipefail
    apt-get update
    apt-get install -y nginx
    printf '<h1>Orders foundation</h1><p>Environment: ${var.environment}</p>\n' > /var/www/html/index.html
    systemctl enable --now nginx
  SCRIPT
  )
}
resource "aws_lb" "edge" {
  name               = local.name
  load_balancer_type = "application"
  subnets            = aws_subnet.public[*].id
  security_groups    = [aws_security_group.edge.id]
}
resource "aws_lb_target_group" "app" {
  name     = local.name
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
  health_check { path = "/" }
}
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.edge.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}
resource "aws_autoscaling_group" "app" {
  name                      = local.name
  min_size                  = 2
  max_size                  = 3
  desired_capacity          = 2
  vpc_zone_identifier       = aws_subnet.private[*].id
  target_group_arns         = [aws_lb_target_group.app.arn]
  health_check_type         = "ELB"
  health_check_grace_period = 300
  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }
  depends_on = [aws_route_table_association.private, aws_iam_role_policy_attachment.ssm]
}
output "url" { value = "http://${aws_lb.edge.dns_name}" }
output "vpc_id" { value = aws_vpc.main.id }
output "target_group_arn" { value = aws_lb_target_group.app.arn }
output "asg_name" { value = aws_autoscaling_group.app.name }
```

## Checkpoint — verify before continuing

Review the source restriction, app group reference, IMDSv2 requirement and encrypted root volumes. Confirm there is no port-22 ingress and no public IP assignment to application instances.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

A public endpoint can still be restricted, but a source of 0.0.0.0/0 would violate this lab contract. Fix the input/rules rather than relying on obscurity of the ALB hostname.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [06. Provision the Application Compute Layer](06-provision-the-application-compute-layer.md). The next chapter assumes the state created here.
