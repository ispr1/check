# System Architecture Overview

## High-Level Topology
CHECK-360 follows a **Modular Monolith** architecture designed for ease of deployment and strict data governance. While currently monolithic in deployment (FastAPI), the domains are strictly decoupled in code to allow future splitting into microservices.

```mermaid
graph TD
    Client[Client (Web/Mobile)] --> API_GW[FastAPI / API Gateway]
    
    subgraph Core_Services
        API_GW --> Sess[Session Manager]
        API_GW --> Cand[Candidate Service]
        API_GW --> HR[HR Service]
    end
    
    subgraph Orchestration
        Sess --> Verify[Verification Orchestrator]
        Verify --> Trust[Trust Score Engine]
    end
    
    subgraph Adapters
        Verify --> SP_Adapt[Surepass Adapter]
        Verify --> REK_Adapt[Rekognition Adapter]
        Verify --> DOC_Adapt[Forensics Adapter]
    end
    
    subgraph Data_Layer
        Verify --> DB[(PostgreSQL)]
        Verify --> S3[(AWS S3 / Local)]
    end
    
    SP_Adapt --> Ext_SP[Surepass API]
    REK_Adapt --> Ext_AWS[AWS Rekognition]
```

## Key Components

### 1. API Layer (`src/api`)
Restful endpoints secured by JWT. Routes are versioned (`/api/v1`).
*   **Public Routes:** Candidate interaction (Verification start, Uploads).
*   **HR Routes:** Reviewer interaction (Summaries, Decisions).

### 2. Service Layer (`src/services`)
Business logic containment.
*   `face/`: Biometric operations.
*   `document/`: Forensic analysis.
*   `trust_score/`: Rule-based scoring.
*   `hr/`: Aggregation logic.

### 3. Data Layer (`src/models`)
SQLAlchemy ORM models.
*   Strict constraints (Foreign Keys, Indexes).
*   Audit trails built into sensitive tables (`hr_decisions`, `trust_score_overrides`).

### 4. Utilities
*   `encryption.py`: AES-256 for PII fields.
*   `face_storage.py`: Abstracted file storage (S3/Local).

## Design Principles
1.  **Orchestration over Capability:** We don't build OCR; we orchestrate OCR providers. We own the *decision*, not the *extraction*.
2.  **Fail-Safe Defaults:** If a vendor fails, the check is `PENDING`, not `PASSED`.
3.  **Strict Typing:** Pydantic models for all I/O.
