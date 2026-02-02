# Data Retention Policy

## Retention Periods

| Data Category | Retention Period | Justification |
|---------------|------------------|---------------|
| Candidate PII | 3 years | Employment law compliance |
| Verification Results | 7 years | Audit trail requirements |
| Trust Scores | 7 years | Decision traceability |
| HR Decisions | 7 years | Legal defensibility |
| System Logs | 90 days | Debugging / Security |
| Session Tokens | 24 hours | Security |

## Lifecycle Stages

```
Active → Archived → Purged
```

1. **Active:** Data accessible in primary database.
2. **Archived:** After 1 year, moved to cold storage (S3 Glacier).
3. **Purged:** After retention period, permanently deleted.

## Candidate-Initiated Deletion

Under DPDP Act, candidates can request data deletion:

1. Request received via API or support ticket.
2. Identity verified (email confirmation).
3. Data anonymized within 30 days.
4. Audit entry logged: `DATA_DELETION_REQUESTED`.

## Exceptions

| Scenario | Retention Override |
|----------|-------------------|
| Active Legal Dispute | Retain until resolution + 2 years |
| Regulatory Investigation | Retain per regulator instruction |
| Fraud Case | Retain indefinitely |

## Automated Enforcement

*Future Implementation:*

```python
# Scheduled job (daily)
def purge_expired_records():
    cutoff = datetime.now() - timedelta(days=2555)  # 7 years
    db.execute("DELETE FROM verifications WHERE created_at < ?", cutoff)
```
