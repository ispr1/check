# CHECK-360 Documentation

## About CHECK-360

CHECK-360 is an **Enterprise Verification Orchestration Platform**. It verifies candidate identity, documents, and employment history, generating an explainable **Trust Score** to aid hiring decisions.

---

## 📚 Documentation Index

### 00. Overview
| Document | Description |
|----------|-------------|
| [Product Vision](./00_overview/product_vision.md) | Why CHECK-360 exists |
| [Problem Statement](./00_overview/problem_statement.md) | The crisis we solve |
| [Non-Goals](./00_overview/non_goals.md) | What we don't do |
| [Glossary](./00_overview/glossary.md) | Key terminology |

### 01. Product
| Document | Description |
|----------|-------------|
| [PRD](./01_product/prd.md) | Product requirements |
| [User Personas](./01_product/user_personas.md) | Who uses the system |
| [User Journeys](./01_product/user_journeys.md) | End-to-end flows |
| [Success Metrics](./01_product/success_metrics.md) | How we measure success |
| [Release Plan](./01_product/release_plan.md) | Phase timeline |

### 02. Architecture
| Document | Description |
|----------|-------------|
| [System Overview](./02_architecture/system_overview.md) | High-level design |
| [Data Flow](./02_architecture/data_flow.md) | How data moves |
| [Security Model](./02_architecture/security_model.md) | Trust boundaries |
| [Scalability](./02_architecture/scalability_strategy.md) | Growth strategy |

### 03. Data Governance
| Document | Description |
|----------|-------------|
| [Data Classification](./03_data_governance/data_classification.md) | Data categories |
| [PII Handling](./03_data_governance/pii_handling.md) | Privacy controls |
| [Encryption Policy](./03_data_governance/encryption_policy.md) | Encryption standards |
| [Retention Policy](./03_data_governance/retention_policy.md) | Data lifecycle |
| [Audit & Compliance](./03_data_governance/audit_and_compliance.md) | Audit framework |

### 04. Decisions (ADRs)
| Document | Description |
|----------|-------------|
| [ADR 001: Orchestrator Model](./04_decisions/adr_0001_orchestrator_model.md) | Why we orchestrate |
| [ADR 002: Surepass](./04_decisions/adr_0002_surepass_as_truth_source.md) | Why Surepass |
| [ADR 003: Deductive Scoring](./04_decisions/adr_0003_deduction_based_scoring.md) | Why subtract from 100 |
| [ADR 004: AWS Rekognition](./04_decisions/adr_0004_aws_rekognition.md) | Why Rekognition |
| [ADR 005: Open Source Forensics](./04_decisions/adr_0005_open_source_forensics.md) | Why not Textract |

### 05. Services
| Document | Description |
|----------|-------------|
| [Verification Session](./05_services/verification_session.md) | Session lifecycle |
| [Surepass Integration](./05_services/surepass_integration.md) | ID verification |
| [Face Verification](./05_services/face_verification.md) | Biometric match |
| [Document Analysis](./05_services/document_analysis.md) | Forensic engine |
| [Trust Score Engine](./05_services/trust_score_engine.md) | Scoring logic |
| [HR Review Service](./05_services/hr_review_service.md) | HR operations |

### 06. API Contracts
| Document | Description |
|----------|-------------|
| [Candidate API](./06_api_contracts/public_candidate_api.md) | Candidate endpoints |
| [HR API](./06_api_contracts/hr_api.md) | HR endpoints |
| [Trust Score API](./06_api_contracts/trust_score_api.md) | Score endpoints |
| [Error Codes](./06_api_contracts/error_codes.md) | Error reference |
| [Webhooks](./06_api_contracts/webhooks.md) | Event notifications |

### 07. Workflows
| Document | Description |
|----------|-------------|
| [Candidate Flow](./07_workflows/candidate_verification_flow.md) | Full verification |
| [HR Review Flow](./07_workflows/hr_review_flow.md) | Decision process |
| [Fallback Flow](./07_workflows/fallback_without_aadhaar.md) | No-Aadhaar path |
| [Override Flow](./07_workflows/manual_override_flow.md) | Exception handling |

### 08. Security
| Document | Description |
|----------|-------------|
| [Threat Model](./08_security/threat_model.md) | STRIDE analysis |
| [Attack Vectors](./08_security/attack_vectors.md) | Known attacks |
| [Secrets Management](./08_security/secrets_management.md) | Key handling |
| [Vendor Risk](./08_security/vendor_risk.md) | Third-party risk |

### 09. Operations
| Document | Description |
|----------|-------------|
| [Deployment Guide](./09_operations/deployment_guide.md) | Setup instructions |
| [Environment Config](./09_operations/environment_config.md) | Configuration |
| [Incident Response](./09_operations/incident_response.md) | Incident playbook |

### 10. Testing
| Document | Description |
|----------|-------------|
| [Test Strategy](./10_testing/test_strategy.md) | Testing approach |

### 11. Onboarding
| Document | Description |
|----------|-------------|
| [Backend KT](./11_onboarding/backend_kt.md) | Engineer onboarding |
| [HR Training](./11_onboarding/hr_training.md) | HR user guide |

### 12. Compliance
| Document | Description |
|----------|-------------|
| [DPDP India](./12_compliance/dpdp_india.md) | Indian data law |
| [SOC 2 Readiness](./12_compliance/soc2_readiness.md) | Certification status |

---

## Quick Links

- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Version:** 4.0.0
