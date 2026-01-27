# CHECK-360 Technical Documentation

Complete guide for setting up and running the CHECK-360 Verification System.

## Table of Contents

1. [What is CHECK-360?](#what-is-check-360)
2. [Prerequisites](#prerequisites)
3. [Installation Guide](#installation-guide)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [Running the Application](#running-the-application)
7. [API Testing Guide](#api-testing-guide)
8. [Surepass Integration](#surepass-integration)
9. [Troubleshooting](#troubleshooting)

---

## What is CHECK-360?

CHECK-360 is a **Background Verification System** that helps companies verify candidate information during hiring.

### How It Works (Simple Explanation)

```
1. HR creates a candidate profile
2. System sends verification link to candidate
3. Candidate submits their details (Aadhaar, PAN, etc.)
4. System verifies details against government databases (via Surepass)
5. HR sees the verification results (match/mismatch)
```

### Key Terms

| Term | Meaning |
|------|---------|
| **Aadhaar** | 12-digit Indian identity number |
| **PAN** | 10-character tax ID (e.g., ABCDE1234F) |
| **UAN** | 12-digit Universal Account Number for PF |
| **Surepass** | 3rd party API that connects to government databases |
| **Mock Mode** | Testing without real government data |

---

## Prerequisites

### Software You Need

| Software | Version | Purpose | Download Link |
|----------|---------|---------|---------------|
| **Python** | 3.10+ | Backend language | [python.org](https://www.python.org/downloads/) |
| **PostgreSQL** | 14+ | Database | [postgresql.org](https://www.postgresql.org/download/) |
| **Docker** | Latest | Run database easily | [docker.com](https://www.docker.com/products/docker-desktop/) |
| **Git** | Latest | Code versioning | [git-scm.com](https://git-scm.com/downloads) |

### Check If Already Installed

Open **Command Prompt** (Windows) or **Terminal** (Mac/Linux) and run:

```bash
# Check Python
python --version
# Should show: Python 3.10.x or higher

# Check Docker
docker --version
# Should show: Docker version 24.x.x or similar

# Check Git
git --version
# Should show: git version 2.x.x
```

---

## Installation Guide

### Step 1: Download the Code

```bash
# Navigate to where you want the project
cd C:\Projects

# Clone the repository (replace with your actual repo URL)
git clone https://github.com/your-org/check-360.git

# Enter the project folder
cd check-360
```

### Step 2: Create Python Virtual Environment

A virtual environment keeps project dependencies isolated.

```bash
# Navigate to backend folder
cd backend

# Create virtual environment (Windows)
python -m venv venv

# Activate it (Windows - Command Prompt)
venv\Scripts\activate

# Activate it (Windows - PowerShell)
.\venv\Scripts\Activate.ps1

# Activate it (Mac/Linux)
source venv/bin/activate
```

**You'll see `(venv)` at the start of your command line when activated.**

### Step 3: Install Python Packages

```bash
# Make sure you're in the backend folder
cd backend

# Install all required packages
pip install -r requirements.txt

# This may take 2-5 minutes
```

**Common packages installed:**

| Package | Purpose |
|---------|---------|
| fastapi | Web framework |
| uvicorn | Web server |
| sqlalchemy | Database ORM |
| psycopg2 | PostgreSQL connector |
| cryptography | Encryption |
| httpx | HTTP client for APIs |

---

## Environment Configuration

### What is a .env File?

A `.env` file stores **secret settings** that should never be shared publicly.

### Step 1: Create Your .env File

The project includes a sample. Copy it:

```bash
# In the backend folder
copy .env.example .env
```

### Step 2: Configure Each Setting

Open `.env` in any text editor (Notepad, VS Code, etc.):

```env
# ===== DATABASE =====
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/check360
# Format: postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME
# Default: username=postgres, password=postgres, database=check360

# ===== AUTHENTICATION =====
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
# This is used to create login tokens
# In production, use a long random string

JWT_ALGORITHM=HS256
# Don't change this

JWT_EXPIRE_MINUTES=1440
# 1440 = 24 hours (how long login lasts)

# ===== SUREPASS API =====
SUREPASS_ENABLED=false
# false = Use fake data for testing (SAFE)
# true = Call real government APIs (NEEDS API KEY)

SUREPASS_BASE_URL=https://sandbox.surepass.io/api/v1
# Sandbox = Testing environment
# Production = https://kyc-api.surepass.io/api/v1

SUREPASS_API_KEY=
# Get this from Surepass after purchasing
# Leave empty for mock mode

# ===== ENCRYPTION =====
DATA_ENCRYPTION_KEY=
# IMPORTANT: Generate using the command below
# Leave empty in development (you'll get a warning, that's OK)

ENVIRONMENT=development
# development = Allows empty encryption key, mock mode
# production = Requires all keys, real Surepass
```

### Step 3: Generate Encryption Key

The encryption key protects sensitive data (Aadhaar, PAN numbers).

**Run this command:**

```bash
# In the backend folder, with venv activated
python -c "import os, base64; print(base64.b64encode(os.urandom(32)).decode())"
```

**Example output:**
```
K7xHJ4nLQR5pM2vB9zC3gT8wN1fD6jS0iU7mE4qY5aO=
```

**Copy this output and paste it into your .env:**

```env
DATA_ENCRYPTION_KEY=K7xHJ4nLQR5pM2vB9zC3gT8wN1fD6jS0iU7mE4qY5aO=
```

> ⚠️ **WARNING:** Never share your encryption key. Each environment (dev, staging, production) should have a different key.

---

## Database Setup

### Option A: Using Docker (Recommended)

Docker makes database setup easy with one command.

**Step 1: Start PostgreSQL**

```bash
# In the project root folder (where docker-compose.yml is)
cd ..
docker-compose up -d
```

**What this does:**
- Downloads PostgreSQL if needed
- Creates a container named `check360-postgres`
- Creates database `check360`
- Sets username: `postgres`, password: `postgres`
- Exposes port `5432`

**Step 2: Verify It's Running**

```bash
docker ps
```

You should see a row with `check360-postgres` and status `Up`.

### Option B: Local PostgreSQL

If you installed PostgreSQL directly:

1. Open **pgAdmin** or **psql**
2. Create database: `CREATE DATABASE check360;`
3. Update `.env` with your credentials

### Step 3: Run Database Migrations

Migrations create the database tables.

```bash
# In the backend folder
cd backend

# Run migrations
alembic upgrade head
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Running upgrade xxx -> yyy
INFO  [alembic.runtime.migration] Running upgrade yyy -> zzz
```

### Step 4: Create Admin User

```bash
python seed_admin.py
```

**This creates:**
- Email: `admin@check360.com`
- Password: `admin123`

---

## Running the Application

### Start the Server

```bash
# In the backend folder, with venv activated
uvicorn src.main:app --reload
```

**Expected output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Environment validation passed: environment=development
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Access Points

| URL | Purpose |
|-----|---------|
| http://localhost:8000 | API root |
| http://localhost:8000/docs | Interactive API documentation |
| http://localhost:8000/health | Health check |

### Stop the Server

Press `Ctrl + C` in the terminal.

---

## API Testing Guide

### Using the Interactive Docs

1. Open http://localhost:8000/docs in your browser
2. You'll see all available APIs
3. Click any API → Click "Try it out" → Fill in data → Click "Execute"

### Manual API Testing with curl

**1. Health Check**

```bash
curl http://localhost:8000/health
```

Expected: `{"status": "healthy", "version": "2.5.0"}`

**2. Login as Admin**

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@check360.com", "password": "admin123"}'
```

Expected: `{"access_token": "eyJ...", "token_type": "bearer"}`

**3. Create a Candidate** (use token from login)

```bash
curl -X POST http://localhost:8000/api/v1/candidates \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"full_name": "Rajesh Kumar", "email": "rajesh@test.com", "dob": "1990-05-15"}'
```

### Testing with Python Scripts

We provide ready-made test scripts:

```bash
# Comprehensive QA Test (all 69 tests)
python test_comprehensive.py

# Targeted verification flow test
python test_flow.py

# Phase 1 basic flow
python test_phase1.py

# Phase 2.5 encryption tests
python test_phase25.py
```

**Expected output from comprehensive test:**
```
============================================================
  QA TEST SUMMARY
============================================================

  [PASS] Passed: 69
  [FAIL] Failed: 0
  [INFO] Total:  69

  ALL TESTS PASSED!
  CHECK-360 is ready for Phase 3.
============================================================
```

---

## Surepass Integration

### What is Surepass?

Surepass is a third-party service that connects to Indian government databases (UIDAI for Aadhaar, Income Tax for PAN, EPFO for UAN).

### Mock Mode vs Live Mode

| Mode | SUREPASS_ENABLED | What Happens |
|------|------------------|--------------|
| **Mock** | `false` | Uses fake data, no real API calls |
| **Live** | `true` | Calls real Surepass APIs |

### How to Get Surepass API Key

1. Go to https://surepass.io
2. Sign up for an account
3. Choose a plan (they have trial options)
4. Get your API key from the dashboard
5. Add to `.env`:
   ```env
   SUREPASS_ENABLED=true
   SUREPASS_API_KEY=your_api_key_here
   ```

### Surepass Pricing (Approximate)

| API | Cost per call |
|-----|---------------|
| Aadhaar OTP | ₹2-5 |
| PAN Verification | ₹1-3 |
| UAN Verification | ₹2-4 |

> Check their website for current pricing.

---

## Troubleshooting

### Common Errors and Solutions

#### 1. "Connection refused" to database

**Problem:**
```
sqlalchemy.exc.OperationalError: connection to server failed
```

**Solution:**
```bash
# Check if Docker is running
docker ps

# If no containers, start them
docker-compose up -d
```

#### 2. "Module not found" errors

**Problem:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# Make sure venv is activated (you should see (venv) in terminal)
# If not:
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Then reinstall packages
pip install -r requirements.txt
```

#### 3. "Duplicate enum type" during migration

**Problem:**
```
DuplicateObject: type "verificationstatus" already exists
```

**Solution:**
```bash
# The migration handles this automatically, but if it persists:
# Connect to database and drop the conflicting objects
# Then run migration again
alembic upgrade head
```

#### 4. Server crashes on startup

**Problem:**
```
RuntimeError: Environment validation failed
```

**Solution:**  
Check your `.env` file. In production mode, all keys are required.
For development, set `ENVIRONMENT=development`.

#### 5. Encryption key error

**Problem:**
```
EncryptionError: DATA_ENCRYPTION_KEY must be 32 bytes
```

**Solution:**
Generate a new key using the command in [Environment Configuration](#step-3-generate-encryption-key).

---

## Quick Reference Card

### Commands You'll Use Daily

| Task | Command |
|------|---------|
| Activate venv | `venv\Scripts\activate` |
| Start server | `uvicorn src.main:app --reload` |
| Run migrations | `alembic upgrade head` |
| Start database | `docker-compose up -d` |
| Stop database | `docker-compose down` |
| Run tests | `python test_comprehensive.py` |

### File Locations

| File | Purpose |
|------|---------|
| `backend/.env` | Secret configuration |
| `backend/src/main.py` | Application entry point |
| `backend/src/routers/` | API endpoints |
| `backend/src/models/` | Database models |
| `backend/src/services/` | Business logic |
| `backend/alembic/versions/` | Database migrations |

---

## Getting Help

1. **Check this documentation first**
2. **Search error messages** in this file
3. **Ask team lead** with:
   - What you were trying to do
   - The exact error message
   - Your `.env` settings (DON'T share actual keys!)

---

*Documentation Version: 2.5.0 | Last Updated: January 2026*
