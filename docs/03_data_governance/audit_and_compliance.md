# Audit and Compliance Framework

## Audit Requirements

CHECK-360 is designed to be audit-ready for:

- **ISO 27001** - Information Security Management
- **SOC 2 Type II** - Security, Availability, Confidentiality
- **DPDP Act** - India's Data Protection Law

## Audit Trail Coverage

Every sensitive action is logged with:

| Field | Description |
|-------|-------------|
| `timestamp` | When action occurred (UTC) |
| `actor_id` | User ID or "SYSTEM" |
| `action` | What happened (CREATED, UPDATED, DELETED) |
| `entity_type` | Table/model affected |
| `entity_id` | Row ID |
| `old_value` | Previous state (encrypted if PII) |
| `new_value` | New state (encrypted if PII) |
| `ip_address` | Client IP |
| `user_agent` | Client software |

## Tables with Audit

| Table | Full Audit | Reason |
|-------|------------|--------|
| `hr_decisions` | ✓ | Legal defensibility |
| `trust_score_overrides` | ✓ | Accountability |
| `trust_scores` | ✓ | Score history |
| `verifications` | ✓ | Process traceability |
| `candidates` | Create/Delete only | PII changes |

## Compliance Controls

### Access Control
- RBAC enforced at API layer.
- No direct database access in production.

### Change Management
- All deployments via CI/CD.
- No manual hotfixes without approval.

### Incident Response
- Security incidents escalated within 4 hours.
- Breach notification within 72 hours (DPDP).

## Audit Reports Available

| Report | Frequency | Audience |
|--------|-----------|----------|
| Access Log Summary | Weekly | Security Team |
| Decision Audit | Monthly | Compliance |
| Data Deletion Log | Quarterly | Legal |
| Vendor Access Review | Quarterly | Security Team |
