# Secrets Management

## Secrets Inventory

| Secret | Environment Variable | Storage |
|--------|---------------------|---------|
| Database Password | `DATABASE_URL` | .env / SSM |
| JWT Secret | `SECRET_KEY` | .env / SSM |
| Encryption Key | `DATA_ENCRYPTION_KEY` | .env / Secrets Manager |
| AWS Access Key | `AWS_ACCESS_KEY_ID` | .env / IAM Role |
| AWS Secret Key | `AWS_SECRET_ACCESS_KEY` | .env / IAM Role |
| Surepass API Key | `SUREPASS_API_KEY` | .env / SSM |

## Storage by Environment

| Environment | Method |
|-------------|--------|
| Local Dev | `.env` file (gitignored) |
| Staging | AWS SSM Parameter Store |
| Production | AWS Secrets Manager |

## Access Control

| Role | DB Password | AWS Keys | Encryption Key |
|------|-------------|----------|----------------|
| Developer | No | No (uses local mock) | No |
| DevOps | Yes (encrypted) | Yes | Yes |
| Application | Yes (runtime) | Yes (IAM) | Yes (runtime) |

## Rotation Policy

| Secret | Rotation Frequency | Procedure |
|--------|-------------------|-----------|
| Database Password | 90 days | Update in Secrets Manager → Restart app |
| AWS Keys | 90 days | IAM rotation → Update deployment |
| Encryption Key | Annual | Re-encrypt columns → Deploy |
| JWT Secret | On breach only | Regenerate → All users logged out |
| Surepass API Key | On breach only | Request new from vendor |

## Best Practices

1. **Never commit secrets to git.**
2. **Use environment variables, not config files.**
3. **Prefer IAM roles over static keys in AWS.**
4. **Audit secret access via CloudTrail.**
5. **Encrypt secrets at rest in Secrets Manager.**

## Emergency Revocation

If a secret is compromised:

1. **Revoke immediately** (AWS console / vendor dashboard).
2. **Generate new secret.**
3. **Update deployment configuration.**
4. **Audit for unauthorized access.**
5. **Notify security team.**
