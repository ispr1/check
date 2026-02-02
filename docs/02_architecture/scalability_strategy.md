# Scalability Strategy

## Current State (Vertical Scaling)
*   **App:** Stateless FastAPI workers. Can scale by adding processes/containers.
*   **DB:** Single master PostgreSQL.

## Scaling Path (Horizontal)

### 1. Stateless Tier
The API layer is fully stateless.
*   **Strategy:** Deploy behind Load Balancer (ALB/Nginx).
*   **Trigger:** CPU > 70%.

### 2. Asynchronous Processing
Heavy tasks (Forensics, Rekognition) blocks the main thread if not handled securely.
*   **Current:** Synchronous/Asyncio.
*   **Future:** Move `analyze_document` and `compare_faces` to **Celery/RabbitMQ** workers. This allows processing thousands of documents concurrently without stalling the API.

### 3. Database
*   **Read Replicas:** For HR Dashboards (Read-heavy).
*   **Sharding:** Shard `verifications` table by `company_id` if we hit >10M rows.

### 4. Storage
*   **S3:** Infinitely scalable. No action needed.
