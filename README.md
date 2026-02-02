# CHECK-360: Enterprise Verification Orchestrator

CHECK-360 is a backend-first platform for verifying candidate identity, documents, and employment history. It acts as a **Truth Comparator**, orchestrating data from trusted sources to generate an explainable **Trust Score**.

## 📚 Documentation
Full documentation is available in the [`docs/`](./docs) directory.

### [00. Overview](./docs/00_overview)
*   [Vision](./docs/00_overview/product_vision.md) - Why this exists.
*   [Glossary](./docs/00_overview/glossary.md) - Key terms.

### [01. Product](./docs/01_product)
*   [PRD](./docs/01_product/prd.md) - Requirements & Constraints.
*   [User Journeys](./docs/01_product/user_journeys.md) - Candidate & HR flows.

### [02. Architecture](./docs/02_architecture)
*   [System Overview](./docs/02_architecture/system_overview.md) - High-level design.
*   [Data Flow](./docs/02_architecture/data_flow.md) - How PII moves.
*   [Security](./docs/02_architecture/security_model.md) - Trust boundaries.

### [03. Decisions (ADRs)](./docs/04_decisions)
*   [Deductive Scoring](./docs/04_decisions/adr_0003_deduction_based_scoring.md) - Why we calculate score this way.
*   [Open Source Forensics](./docs/04_decisions/adr_0005_open_source_forensics.md) - Why we don't use Textract.

### [05. Services Logic](./docs/05_services)
*   [Document Analysis](./docs/05_services/document_analysis.md) - Forensics logic.
*   [Trust Score](./docs/05_services/trust_score_engine.md) - Scoring weights.

### [06. API Contracts](./docs/06_api_contracts)
*   [HR API](./docs/06_api_contracts/hr_api.md) - Reviewer endpoints.

### [09. Operations](./docs/09_operations)
*   [Deployment](./docs/09_operations/deployment_guide.md) - Setup guide.
*   [Testing](./docs/10_testing/test_strategy.md) - Test strategy.

---

## Quick Start

1.  **Install:** `pip install -r requirements.txt`
2.  **Configure:** Set up `.env` (DB, AWS).
3.  **Migrate:** Run SQL scripts in `src/migrations/`.
4.  **Run:** `uvicorn src.main:app --reload`
5.  **Docs:** Visit http://localhost:8000/docs
