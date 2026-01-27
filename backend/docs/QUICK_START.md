# CHECK-360 Quick Start Guide

Get up and running in 10 minutes!

---

## Prerequisites

Make sure you have installed:
- Python 3.10+
- Docker Desktop
- Git

---

## Step 1: Get the Code (1 minute)

```bash
git clone https://github.com/your-org/check-360.git
cd check-360/backend
```

---

## Step 2: Setup Environment (2 minutes)

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Mac/Linux

# Install packages
pip install -r requirements.txt
```

---

## Step 3: Configure Settings (1 minute)

Create `.env` file:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/check360
JWT_SECRET_KEY=dev-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
SUREPASS_ENABLED=false
SUREPASS_BASE_URL=https://sandbox.surepass.io/api/v1
SUREPASS_API_KEY=
DATA_ENCRYPTION_KEY=
ENVIRONMENT=development
```

---

## Step 4: Start Database (1 minute)

```bash
# From project root (go up one folder)
cd ..
docker-compose up -d
cd backend
```

---

## Step 5: Setup Database Tables (1 minute)

```bash
alembic upgrade head
python seed_admin.py
```

---

## Step 6: Start Server (1 minute)

```bash
uvicorn src.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## Step 7: Verify It Works (1 minute)

Open browser: http://localhost:8000

You should see:
```json
{
  "message": "Check360 API is running",
  "version": "2.5.0"
}
```

Open API docs: http://localhost:8000/docs

---

## Step 8: Test Login (1 minute)

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@check360.com", "password": "admin123"}'
```

Should return a token!

---

## 🎉 Done!

You now have a running CHECK-360 instance.

### Next Steps

1. **Read the full docs:** `/backend/docs/`
2. **Create test candidates** via API
3. **Test verification flow**
4. **When ready for live:** Get Surepass API key

---

### Quick Commands Reference

| Task | Command |
|------|---------|
| Start server | `uvicorn src.main:app --reload` |
| Stop server | `Ctrl + C` |
| Start database | `docker-compose up -d` |
| Stop database | `docker-compose down` |
| Run tests | `python test_phase1.py` |
| View API docs | http://localhost:8000/docs |

---

*Quick Start Version: 2.5.0*
