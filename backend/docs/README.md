# CHECK-360 Documentation

Welcome to CHECK-360 - the Background Verification System.

## 📚 Documentation Index

| Document | Description | Best For |
|----------|-------------|----------|
| [**Quick Start**](QUICK_START.md) | Get running in 10 minutes | New developers |
| [**Setup Guide**](SETUP_GUIDE.md) | Complete installation guide | All team members |
| [**Architecture**](ARCHITECTURE.md) | System design & flow | Tech leads, architects |
| [**API Reference**](API_REFERENCE.md) | All API endpoints | Developers, QA |
| [**Surepass Guide**](SUREPASS_GUIDE.md) | Surepass integration | DevOps, developers |

---

## 🚀 Getting Started

**New to CHECK-360?** Start here:

1. Read [Quick Start](QUICK_START.md) - 10 minutes
2. Set up your environment using [Setup Guide](SETUP_GUIDE.md)
3. Test the APIs using [API Reference](API_REFERENCE.md)

---

## 🏗️ System Overview

```
CHECK-360 = Verification Orchestrator + Truth Comparator + Audit Engine
```

| Component | Purpose |
|-----------|---------|
| HR Portal | Create candidates, start verifications |
| Candidate Portal | Submit identity documents |
| Surepass Integration | Verify against government databases |
| Comparison Engine | Match candidate claims vs truth |
| Audit Trail | Legal defensibility |

---

## 💡 Key Concepts

### What CHECK-360 Does

1. **Collects** - Candidate submits their details
2. **Verifies** - Calls Surepass (government data)
3. **Compares** - Matches claim vs truth
4. **Stores** - Evidence for audit
5. **Flags** - Highlights mismatches
6. **Enables** - HR makes informed decisions

### What CHECK-360 Does NOT Do

- ❌ Auto-reject candidates
- ❌ Calculate final scores (yet)
- ❌ Replace HR judgment

---

## 📞 Getting Help

1. Check the relevant documentation
2. Search for error messages in [Setup Guide > Troubleshooting](SETUP_GUIDE.md#troubleshooting)
3. Contact tech lead with:
   - What you were trying to do
   - Error message
   - Environment (dev/staging/prod)

---

## 📋 Version History

| Version | Date | Changes | QA Status |
|---------|------|---------|-----------|
| 2.5.0 | Jan 27, 2026 | Hardening, encryption, audit trail | ✅ 69/69 tests passed |
| 2.0.0 | Jan 2026 | Surepass integration | ✅ Passed |
| 1.0.0 | Jan 2026 | Core verification flow | ✅ Passed |

---

*Documentation maintained by CHECK-360 Team | Last Updated: January 27, 2026*
