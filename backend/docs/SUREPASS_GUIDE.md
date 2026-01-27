# Surepass Integration Guide

Complete guide to understanding and configuring Surepass for CHECK-360.

---

## What is Surepass?

Surepass is a **third-party API service** that connects to Indian government databases.

**Think of it like:**
- You give Surepass an Aadhaar number
- Surepass asks UIDAI (government) "Is this person real? What's their name?"
- UIDAI responds with official government data
- Surepass sends that data back to you

CHECK-360 uses Surepass so we don't have to directly connect to government systems.

---

## Surepass APIs We Use

| API | Purpose | Government Source |
|-----|---------|-------------------|
| Aadhaar OTP | Verify identity with OTP | UIDAI |
| PAN | Verify PAN card details | Income Tax |
| UAN | Get employment history | EPFO |

---

## Mock Mode vs Live Mode

### Mock Mode (Development)

```env
SUREPASS_ENABLED=false
SUREPASS_API_KEY=      # Can be empty
```

**What happens:**
- No real API calls
- Returns fake but realistic data
- Costs ₹0
- Safe for development

**Example mock response for Aadhaar:**
```json
{
  "full_name": "Rajesh Kumar Sharma",
  "dob": "15-05-1990",
  "gender": "M",
  "address": {
    "house": "123",
    "street": "100 Feet Road",
    "po": "Koramangala",
    "dist": "Bangalore Urban",
    "state": "Karnataka",
    "pincode": "560034"
  }
}
```

### Live Mode (Production)

```env
SUREPASS_ENABLED=true
SUREPASS_API_KEY=your_actual_key
SUREPASS_BASE_URL=https://kyc-api.surepass.io/api/v1
```

**What happens:**
- Real API calls to Surepass
- Returns actual government data
- Costs ₹2-5 per call
- Required for production

---

## Getting Surepass API Keys

### Step 1: Create Account

1. Go to https://surepass.io
2. Click "Sign Up" or "Get Started"
3. Fill in company details
4. Verify email

### Step 2: Choose Plan

Surepass offers different plans:

| Plan | Best For | Price |
|------|----------|-------|
| Trial | Testing | Free (limited calls) |
| Startup | Small companies | Pay per call |
| Enterprise | Large volume | Custom pricing |

### Step 3: Get API Key

1. Login to Surepass dashboard
2. Go to "API Keys" or "Credentials"
3. Copy your API key (looks like: `eyJhbGciOiJSUzI1NiIs...`)
4. Keep it secret!

### Step 4: Configure CHECK-360

Open your `.env` file and add:

```env
SUREPASS_ENABLED=true
SUREPASS_BASE_URL=https://kyc-api.surepass.io/api/v1
SUREPASS_API_KEY=eyJhbGciOiJSUzI1NiIs...
```

### Step 5: Restart Server

```bash
# Stop server (Ctrl+C)
# Start again
uvicorn src.main:app --reload
```

---

## Testing Surepass Integration

### Test 1: Check Server Logs

When server starts, you should see:
```
INFO: Environment validation passed: environment=production, surepass_enabled=True
```

### Test 2: Make a Test Verification

1. Create a candidate
2. Start verification
3. Open verification link
4. Enter test Aadhaar number
5. Check if OTP is sent

### Test 3: Check Surepass Dashboard

Login to Surepass and check:
- API call logs
- Success/failure rates
- Remaining credits

---

## Surepass API Details

### 1. Aadhaar OTP Flow

**Step 1: Generate OTP**

```
POST https://kyc-api.surepass.io/api/v1/aadhaar-v2/generate-otp
```

Request:
```json
{
  "id_number": "123456789012"
}
```

Response:
```json
{
  "data": {
    "client_id": "abc123xyz",
    "otp_sent": true
  },
  "success": true
}
```

**Step 2: Submit OTP**

```
POST https://kyc-api.surepass.io/api/v1/aadhaar-v2/submit-otp
```

Request:
```json
{
  "client_id": "abc123xyz",
  "otp": "123456"
}
```

Response:
```json
{
  "data": {
    "full_name": "RAJESH KUMAR SHARMA",
    "dob": "15-05-1990",
    "gender": "M",
    "address": {...},
    "photo_link": "data:image/jpeg;base64,..."
  },
  "success": true
}
```

### 2. PAN Verification

```
POST https://kyc-api.surepass.io/api/v1/pan/pan
```

Request:
```json
{
  "id_number": "ABCDE1234F"
}
```

Response:
```json
{
  "data": {
    "pan": "ABCDE1234F",
    "full_name": "RAJESH KUMAR SHARMA",
    "category": "Individual"
  },
  "success": true
}
```

### 3. UAN Verification

```
POST https://kyc-api.surepass.io/api/v1/uan/get-data
```

Request:
```json
{
  "id_number": "123456789012"
}
```

Response:
```json
{
  "data": {
    "uan_number": "123456789012",
    "member_name": "RAJESH KUMAR SHARMA",
    "dob": "15-05-1990",
    "establishments": [
      {
        "establishment_name": "ABC Tech Pvt Ltd",
        "date_of_joining": "2020-01-01",
        "date_of_exit": "2022-12-31"
      },
      {
        "establishment_name": "XYZ Corp",
        "date_of_joining": "2023-01-15",
        "date_of_exit": null
      }
    ]
  },
  "success": true
}
```

---

## Common Errors

### Error: "Invalid API Key"

**Message:**
```json
{"success": false, "message": "Invalid API Key"}
```

**Solution:**
1. Check if API key is correct in `.env`
2. Check if key is not expired
3. Check if key has credits remaining

### Error: "Rate Limit Exceeded"

**Message:**
```json
{"success": false, "message": "Rate limit exceeded"}
```

**Solution:**
1. Wait a few minutes
2. Contact Surepass to increase limits

### Error: "Invalid Aadhaar Number"

**Message:**
```json
{"success": false, "message": "Invalid Aadhaar"}
```

**Solution:**
1. Aadhaar must be 12 digits
2. Must pass Verhoeff checksum
3. Ask candidate to re-enter

---

## Cost Estimation

### Per Verification

| Check | Cost |
|-------|------|
| Aadhaar OTP | ₹2-5 |
| PAN | ₹1-3 |
| UAN | ₹2-4 |
| **Total per candidate** | **₹5-12** |

### Monthly Estimate

| Volume | Cost |
|--------|------|
| 100 candidates/month | ₹500-1,200 |
| 500 candidates/month | ₹2,500-6,000 |
| 1,000 candidates/month | ₹5,000-12,000 |

> Prices are approximate. Check Surepass for current rates.

---

## Security Best Practices

### ✅ DO

- Store API key in `.env` only
- Use HTTPS for all calls
- Encrypt responses before storing
- Log only masked data

### ❌ DON'T

- Put API key in code
- Share API key publicly
- Log full Aadhaar numbers
- Store unencrypted responses

---

## Sandbox vs Production URLs

| Environment | URL |
|-------------|-----|
| Sandbox (Testing) | `https://sandbox.surepass.io/api/v1` |
| Production (Live) | `https://kyc-api.surepass.io/api/v1` |

### When to Use Sandbox

- During development
- When testing new features
- When debugging

### When to Use Production

- When candidates are real
- When data accuracy matters
- In production deployment

---

## Switching Environments

### From Mock to Sandbox

```env
SUREPASS_ENABLED=true
SUREPASS_BASE_URL=https://sandbox.surepass.io/api/v1
SUREPASS_API_KEY=your_sandbox_key
```

### From Sandbox to Production

```env
SUREPASS_ENABLED=true
SUREPASS_BASE_URL=https://kyc-api.surepass.io/api/v1
SUREPASS_API_KEY=your_production_key
```

---

## Checklist Before Going Live

- [ ] Surepass production API key obtained
- [ ] `.env` updated with production key
- [ ] Production URL configured
- [ ] Encryption key set
- [ ] Test with real (dummy) Aadhaar
- [ ] Verify costs are acceptable
- [ ] Backup plan if Surepass is down

---

*Surepass Integration Version: 2.5.0 | Last Updated: January 2026*
