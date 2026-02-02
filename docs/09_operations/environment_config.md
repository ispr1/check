# Environment Configuration

## Environment Types

| Environment | Purpose | Data |
|-------------|---------|------|
| `local` | Developer machine | Fake/test data |
| `development` | Shared dev server | Fake/test data |
| `staging` | Pre-production testing | Anonymized prod data |
| `production` | Live system | Real data |

## Configuration Variables

### Core Settings

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `SECRET_KEY` | JWT signing key | Yes |
| `ALGORITHM` | JWT algorithm (HS256) | Yes |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token TTL | Yes |

### AWS Settings

| Variable | Description | Required |
|----------|-------------|----------|
| `AWS_ACCESS_KEY_ID` | IAM access key | Yes (prod) |
| `AWS_SECRET_ACCESS_KEY` | IAM secret | Yes (prod) |
| `AWS_REGION` | Region (ap-south-1) | Yes |
| `S3_BUCKET_NAME` | Storage bucket | Yes |

### Vendor Settings

| Variable | Description | Required |
|----------|-------------|----------|
| `SUREPASS_API_KEY` | Surepass token | Yes (prod) |
| `SUREPASS_BASE_URL` | API endpoint | Yes |
| `SUREPASS_ENABLED` | true/false | No (default: false) |

### Feature Flags

| Variable | Description | Default |
|----------|-------------|---------|
| `FACE_PROVIDER` | aws or mock | mock |
| `ENCRYPTION_ENABLED` | Enable PII encryption | true |
| `DEBUG` | Debug mode | false |

## Sample .env File

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/check360

# Auth
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AWS
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=ap-south-1
S3_BUCKET_NAME=check360-documents

# Vendors
SUREPASS_API_KEY=...
SUREPASS_BASE_URL=https://kyc-api.surepass.io/api/v1
SUREPASS_ENABLED=false

# Features
FACE_PROVIDER=mock
ENCRYPTION_ENABLED=true
DEBUG=false
```

## Validation

On startup, the application validates required variables:

```python
# src/main.py
logger.info(f"Environment validation passed: environment={ENVIRONMENT}")
```

Missing required variables cause startup failure.
