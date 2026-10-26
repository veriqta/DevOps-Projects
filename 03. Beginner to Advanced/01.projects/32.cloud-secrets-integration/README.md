# 32. Cloud Secrets Integration

[← All projects](../../README.md) · **Advanced** · AWS · Azure · Google Cloud

Retrieve a lab secret at runtime using workload identity.

## Prerequisites

AWS CLI v2, jq, an existing EC2 lab instance, and an administrator identity able to create a dedicated IAM role and secret. This walkthrough uses AWS instance-profile credentials.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Create a disposable secret from your computer

Use only a dummy value and the same region as the instance:

```bash
export AWS_REGION=us-east-1
export LAB_INSTANCE_ID=REPLACE_WITH_EC2_INSTANCE_ID
export LAB_ROLE=devops-projects-secret-reader
export LAB_PROFILE=devops-projects-secret-profile
SECRET_ARN=$(aws secretsmanager create-secret --name devops-projects-lab-secret --secret-string 'lab-value-v1' --query ARN --output text)
mkdir -p .lab/secrets
printf '%s\n' "$SECRET_ARN" > .lab/secrets/arn
```

### 2. Create a role scoped to this one secret

```bash
cat > .lab/secrets/trust.json <<'JSON'
{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"ec2.amazonaws.com"},"Action":"sts:AssumeRole"}]}
JSON
jq -n --arg arn "$SECRET_ARN" '{Version:"2012-10-17",Statement:[{Effect:"Allow",Action:"secretsmanager:GetSecretValue",Resource:$arn}]}' > .lab/secrets/read.json
aws iam create-role --role-name "$LAB_ROLE" --assume-role-policy-document file://.lab/secrets/trust.json
aws iam put-role-policy --role-name "$LAB_ROLE" --policy-name ReadOneLabSecret --policy-document file://.lab/secrets/read.json
aws iam create-instance-profile --instance-profile-name "$LAB_PROFILE"
aws iam add-role-to-instance-profile --instance-profile-name "$LAB_PROFILE" --role-name "$LAB_ROLE"
```

Wait for IAM propagation, then attach to an instance with no existing instance profile:

```bash
ASSOCIATION_ID=$(aws ec2 associate-iam-instance-profile --instance-id "$LAB_INSTANCE_ID" --iam-instance-profile Name="$LAB_PROFILE" --query IamInstanceProfileAssociation.AssociationId --output text)
printf '%s\n' "$ASSOCIATION_ID" > .lab/secrets/association
```

### 3. Read without logging the value — on the VM

Install AWS CLI v2 using SETUP.md’s official installer instructions. Do not copy administrator credentials to the VM. Set its region and the ARN from step 1:

```bash
export AWS_REGION=us-east-1
export SECRET_ARN=REPLACE_WITH_LAB_SECRET_ARN
aws sts get-caller-identity
VALUE=$(aws secretsmanager get-secret-value --secret-id "$SECRET_ARN" --query SecretString --output text)
test "$VALUE" = lab-value-v1 && echo 'runtime read passed'
unset VALUE
```

### 4. Rotate and verify

Back on your computer:

```bash
aws secretsmanager put-secret-value --secret-id "$SECRET_ARN" --secret-string lab-value-v2
```

On the VM repeat the read and test against lab-value-v2. Request an unrelated secret your administrator created and confirm AccessDenied. A nonexistent ARN does not prove an authorization boundary; use an existing unrelated lab secret for this check.

For other cloud platforms, repeat this pattern using [Azure managed identity + Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/authentication) or [Google service accounts + Secret Manager](https://cloud.google.com/secret-manager/docs/access-secret-version). Those are optional provider extensions.

## Verify completion

The VM caller is the dedicated role; it reads only the authorized secret and sees v2 after rotation. No long-lived cloud credential is stored on the VM.

## Troubleshooting

Role/profile creation is eventually consistent. Wait and retry association if the profile is not found. If the VM has an existing profile, use a separate lab instance instead of replacing a production role.

## Cleanup

From your administrator session, run the following after setting the same variables:

```bash
aws ec2 disassociate-iam-instance-profile --association-id "$(cat .lab/secrets/association)"
aws iam remove-role-from-instance-profile --instance-profile-name "$LAB_PROFILE" --role-name "$LAB_ROLE"
aws iam delete-instance-profile --instance-profile-name "$LAB_PROFILE"
aws iam delete-role-policy --role-name "$LAB_ROLE" --policy-name ReadOneLabSecret
aws iam delete-role --role-name "$LAB_ROLE"
aws secretsmanager delete-secret --secret-id "$SECRET_ARN" --recovery-window-in-days 7
```

The secret is scheduled for deletion, not immediately erased. Destroy the EC2 lab instance when finished.

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)

---

[← Previous: 31](../31.backup-and-recovery-drill/README.md) · [All projects](../../README.md) · [Next: 33 →](../33.cloud-cost-management/README.md)
