# 11. EC2 Instance

[← All projects](../../README.md) · **Beginner** · AWS · SSH

Launch and inspect a disposable Linux instance.

## Prerequisites

AWS account with budget alert, AWS CLI v2 configured with `aws configure sso` or another temporary-credential method, and an SSH key.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Confirm your account

```bash
aws sts get-caller-identity
export AWS_REGION=us-east-1
```

### 2. Launch through the EC2 console

Open EC2 in the selected region → Launch instance. Name it `devops-projects-lab`. Select Ubuntu Server 24.04 LTS, a small available instance type, and create or choose a dedicated key pair. Store a downloaded key outside this repository with mode 600. In network settings choose **Allow SSH from My IP**. Review the hourly price, storage, public IPv4 price, then launch. Wait for both status checks.

### 3. Connect and inspect

```bash
export LAB_HOST=REPLACE_WITH_PUBLIC_IPV4
ssh -i /path/to/your/key.pem ubuntu@"$LAB_HOST"
```

**On the VM**, query metadata using IMDSv2:

```bash
TOKEN=$(curl -fsS -X PUT -H 'X-aws-ec2-metadata-token-ttl-seconds: 60' http://169.254.169.254/latest/api/token)
curl -fsS -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id
unset TOKEN
```

Do not copy temporary role credentials into your notes.

## Verify completion

The instance ID from metadata matches the console, SSH works from your IP, and the security group does not expose SSH to 0.0.0.0/0.

## Troubleshooting

If there is no public IPv4 address, check subnet routing/public-IP settings. Never open SSH globally to solve an incorrect key or username.

## Cleanup

In EC2 select the lab instance → Instance state → Terminate. Check Volumes, Elastic IPs and Snapshots for leftovers; remove only lab resources. Verify termination and inspect billing.

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)

---

[← Previous: 10](../10.basic-dockerfile/README.md) · [All projects](../../README.md) · [Next: 12 →](../12.pomodoro-timer/README.md)
