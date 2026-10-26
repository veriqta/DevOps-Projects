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
