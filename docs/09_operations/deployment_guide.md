# Deployment Guide

## Prerequisites
*   Python 3.10+
*   PostgreSQL 14+
*   AWS Credentials (S3 + Rekognition access)

## Environment Variables
Required in `.env`:
*   `DATABASE_URL`: Postgres connection string.
*   `AWS_ACCESS_KEY_ID`: For Rekognition/S3.
*   `AWS_SECRET_ACCESS_KEY`: For Rekognition/S3.
*   `S3_BUCKET_NAME`: Bucket for docs.

## Steps

1.  **Clone & Install:**
    ```bash
    git clone <repo>
    pip install -r requirements.txt
    ```

2.  **Migrations:**
    ```bash
    # We use raw SQL migrations
    psql -d check360 -f src/migrations/001_init.sql
    psql -d check360 -f src/migrations/002_face_comparisons.sql
    psql -d check360 -f src/migrations/003_document_verifications.sql
    psql -d check360 -f src/migrations/004_trust_score.sql
    psql -d check360 -f src/migrations/005_hr_review.sql
    ```

3.  **Run Server:**
    ```bash
    uvicorn src.main:app --host 0.0.0.0 --port 8000
    ```

## Health Check
GET `/health` should return `{"status": "healthy"}`.
