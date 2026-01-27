# CHECK-360 System Architecture

Understanding how CHECK-360 works internally.

---

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         HR PORTAL                           │
│  • Create Candidates                                        │
│  • Start Verifications                                      │
│  • View Results                                             │
└──────────────────────────┬──────────────────────────────────┘
                           │ JWT Token
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    CHECK-360 BACKEND                        │
│                                                            │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ API Layer (FastAPI)                                  │  │
│  │ • Authentication                                     │  │
│  │ • Candidates                                         │  │
│  │ • Verifications                                      │  │
│  │ • Public Verify                                      │  │
│  └────────────────────────┬────────────────────────────┘  │
│                           │                                │
│  ┌────────────────────────▼────────────────────────────┐  │
│  │ Service Layer                                        │  │
│  │ • Surepass Client                                    │  │
│  │ • Comparison Engine                                  │  │
│  │ • Encryption                                         │  │
│  └────────────────────────┬────────────────────────────┘  │
│                           │                                │
│  ┌────────────────────────▼────────────────────────────┐  │
│  │ Database Layer (SQLAlchemy + PostgreSQL)            │  │
│  │ • Companies, Users, Candidates                       │  │
│  │ • Verifications, Verification Steps                  │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ API Calls
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    SUREPASS (External)                      │
│  • Aadhaar OTP Verification                                │
│  • PAN Verification                                        │
│  • UAN Employment History                                  │
│  (Connects to Government Databases)                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Concept: CHECK-360 is NOT a KYC Provider

| Entity | Role |
|--------|------|
| **Surepass** | Truth Source (connects to govt databases) |
| **CHECK-360** | Orchestrator + Comparator + Audit Engine |

**What CHECK-360 does:**
1. Collects candidate input (what they claim)
2. Calls Surepass (gets truth)
3. Compares input vs truth
4. Stores evidence
5. Flags mismatches
6. Enables HR decisions

---

## Folder Structure

```
backend/
├── src/
│   ├── main.py              # Application entry point
│   ├── database.py          # Database connection
│   │
│   ├── routers/             # API endpoints
│   │   ├── auth.py          # Login/logout
│   │   ├── candidates.py    # Candidate CRUD
│   │   ├── verifications.py # HR verification APIs
│   │   └── verify_public.py # Candidate-facing APIs
│   │
│   ├── models/              # Database models
│   │   ├── user.py
│   │   ├── company.py
│   │   ├── candidate.py
│   │   ├── verification.py
│   │   └── verification_step.py
│   │
│   ├── schemas/             # Request/Response formats
│   │   └── verification.py
│   │
│   ├── services/            # Business logic
│   │   └── surepass/        # Surepass integration
│   │       ├── client.py    # HTTP client
│   │       ├── aadhaar.py   # Aadhaar service
│   │       ├── pan.py       # PAN service
│   │       ├── uan.py       # UAN service
│   │       └── mock_responses.py
│   │
│   └── utils/               # Utilities
│       ├── crypto.py        # Encryption
│       ├── comparison.py    # Name/address matching
│       ├── mapper.py        # Status mapping
│       └── audit.py         # Audit logging
│
├── alembic/                 # Database migrations
│   └── versions/            # Migration scripts
│
├── docs/                    # Documentation
│
├── .env                     # Secret configuration
└── requirements.txt         # Python dependencies
```

---

## Database Schema

### Tables

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│  companies  │────<│    users    │     │   candidates    │
├─────────────┤     ├─────────────┤     ├─────────────────┤
│ id          │     │ id          │     │ id              │
│ name        │     │ email       │     │ company_id  FK  │
│ created_at  │     │ password    │     │ full_name       │
└─────────────┘     │ company_id  │     │ dob             │
                    └─────────────┘     │ email           │
                                        └────────┬────────┘
                                                 │
                                                 │ 1:1
                                                 ▼
┌───────────────────────────────────────────────────────────┐
│                      verifications                         │
├───────────────────────────────────────────────────────────┤
│ id                                                        │
│ candidate_id        FK                                    │
│ company_id          FK                                    │
│ token               (unique, 64 chars)                    │
│ status              (PENDING/IN_PROGRESS/COMPLETED)       │
│ expires_at                                                │
│ trust_score         (Phase 4)                             │
│ created_at                                                │
└──────────────────────────┬────────────────────────────────┘
                           │ 1:many
                           ▼
┌───────────────────────────────────────────────────────────┐
│                   verification_steps                       │
├───────────────────────────────────────────────────────────┤
│ id                                                        │
│ verification_id     FK                                    │
│ step_type           (AADHAAR/PAN/UAN/etc.)               │
│ is_mandatory                                              │
│ status              (PENDING/COMPLETED/FAILED)            │
│ input_data          JSONB (candidate's submission)        │
│ raw_response        JSONB (Surepass response) [ENCRYPTED] │
│ score_contribution  (Phase 4)                             │
│ flags               JSONB (overlaps, mismatches)          │
│ source              (surepass/manual)                     │
│ verified_at                                               │
│ review_assets       JSONB (HR-viewable files)             │
│ hr_notes            (HR comments)                         │
│ audit_trail         JSONB (action history)                │
└───────────────────────────────────────────────────────────┘
```

---

## Verification Flow

```
Step 1: HR creates candidate
         ↓
Step 2: HR starts verification
         ↓
Step 3: System generates unique token (7-day expiry)
         ↓
Step 4: Candidate opens verification link
         ↓
Step 5: Candidate submits each step:
         │
         ├── Personal Info → Stored
         ├── Face Selfie → Stored (ML in Phase 3)
         ├── Aadhaar OTP → Surepass → Compare → Store
         ├── PAN → Surepass → Compare → Store
         └── UAN → Surepass → Analyze → Store
         ↓
Step 6: Candidate clicks Submit
         ↓
Step 7: HR sees results with flags
```

---

## Surepass Integration Flow

```
┌─────────────────┐
│  Candidate      │
│  enters Aadhaar │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  CHECK-360      │
│  validates      │
│  format only    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│  Mock Mode?     │─No─▶│  Call Surepass  │
│  (SUREPASS_     │     │  API            │
│  ENABLED=false) │     └────────┬────────┘
└────────┬────────┘              │
         │ Yes                   │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  Return mock    │     │  Return real    │
│  response       │     │  response       │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
         ┌─────────────────────┐
         │  Comparison Engine  │
         │  • Fuzzy name match │
         │  • DOB exact match  │
         │  • Address similar  │
         └──────────┬──────────┘
                    │
                    ▼
         ┌─────────────────────┐
         │  Result:            │
         │  MATCH / PARTIAL /  │
         │  MISMATCH           │
         └──────────┬──────────┘
                    │
                    ▼
         ┌─────────────────────┐
         │  Store in DB        │
         │  • raw_response     │
         │    (encrypted)      │
         │  • flags            │
         │  • audit_trail      │
         └─────────────────────┘
```

---

## Encryption Boundary

### What Gets Encrypted

| Data | Encrypted | Why |
|------|-----------|-----|
| Aadhaar response | ✅ Yes | Government identity |
| PAN response | ✅ Yes | Financial identity |
| UAN response | ✅ Yes | Employment records |
| Surepass IDs | ✅ Yes | API secrets |

### What Stays Plain (HR Viewable)

| Data | Encrypted | Why |
|------|-----------|-----|
| Face images | ❌ No | HR needs to see |
| Documents | ❌ No | HR needs to review |
| Flags | ❌ No | HR dashboard |
| HR notes | ❌ No | HR comments |

---

## Security Layers

### Layer 1: Authentication
- JWT tokens (24 hours)
- Password hashing (bcrypt)

### Layer 2: Authorization
- Company isolation (users see only their candidates)
- Token-based verification access

### Layer 3: Data Protection
- AES-256-GCM encryption for sensitive data
- Masked logging (no full Aadhaar/PAN in logs)

### Layer 4: Environment Safety
- Startup validation
- Production requires all keys
- Mock mode blocked in production

---

## Phase Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| 1 | Core verification flow | ✅ Complete |
| 2 | Surepass integration | ✅ Complete |
| 2.5 | Hardening & compliance | ✅ Complete |
| 3 | Face ML, QR, Forensics | 🔜 Next |
| 4 | Trust Score Engine | ⏳ Planned |
| 5 | Reports, Exports, Audit | ⏳ Planned |

---

*Architecture Version: 2.5.0 | Last Updated: January 2026*
