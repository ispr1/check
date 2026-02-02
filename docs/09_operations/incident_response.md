# Incident Response Playbook

## Incident Severity Levels

| Level | Definition | Response Time | Example |
|-------|------------|---------------|---------|
| **P1** | System down, data breach | 15 minutes | Production DB compromised |
| **P2** | Major feature broken | 1 hour | Face match failing for all |
| **P3** | Minor feature issue | 4 hours | One document type failing |
| **P4** | Cosmetic / low impact | 24 hours | Typo in error message |

## Incident Response Steps

### 1. Detect
- Automated alerts (CloudWatch, application logs)
- User reports (Support tickets)
- Monitoring dashboards

### 2. Triage
- Assign severity level
- Page on-call engineer (P1/P2)
- Create incident channel (Slack/Teams)

### 3. Contain
- Identify affected scope
- Disable affected feature if needed
- Communicate to stakeholders

### 4. Remediate
- Apply fix (hotfix or rollback)
- Verify fix in staging
- Deploy to production

### 5. Recover
- Monitor for recurrence
- Restore normal operations
- Clear incident status

### 6. Review
- Conduct post-mortem (within 48h)
- Document root cause
- Create follow-up tasks

## Contact Escalation

| Role | Contact | For |
|------|---------|-----|
| On-call Engineer | PagerDuty | P1/P2 |
| Engineering Lead | Slack | P1 escalation |
| Security Officer | Phone | Data breach |
| CEO | Direct | Customer-facing P1 |

## Communication Templates

### Internal (Slack)
```
🚨 INCIDENT: [Brief description]
Severity: P[X]
Status: Investigating
Lead: [Name]
Channel: #incident-[date]
```

### External (Customer)
```
We are currently experiencing issues with [feature].
Our team is actively investigating.
ETA for resolution: [time]
We will update you within [X] hours.
```
