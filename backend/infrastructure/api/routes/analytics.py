from fastapi import APIRouter

router = APIRouter()

@router.get("/metrics")
def get_metrics():
    # Placeholder for actual metrics data
    return [
        {"title": "Total Flights", "value": "1250", "change": "5%", "trend": "up", "icon": "TrendingUp"},
        {"title": "Active Crew", "value": "350", "change": "2%", "trend": "up", "icon": "Users"},
        {"title": "Compliance Rate", "value": "98%", "change": "0%", "trend": "stable", "icon": "Shield"},
        {"title": "Disruptions", "value": "15", "change": "10%", "trend": "down", "icon": "AlertTriangle"},
    ]

@router.get("/violations")
def get_violations():
    # Placeholder for actual violations data
    return [
        {"id": "v1", "rule": "Rest Period Violation", "description": "Crew member exceeded maximum duty hours.", "severity": "high", "crew": "CRW789", "timestamp": "2023-10-27T10:00:00Z"},
        {"id": "v2", "rule": "Mandatory Training Missed", "description": "Crew member failed to complete recurrent training.", "severity": "medium", "crew": "CRW123", "timestamp": "2023-10-26T15:30:00Z"},
    ]

@router.get("/auditlog")
def get_audit_log():
    # Placeholder for actual audit log data
    return [
        {"id": "a1", "timestamp": "2023-10-27T11:00:00Z", "user": "admin", "action": "Roster Update", "details": "Roster for flight AI101 updated.", "type": "roster_change"},
        {"id": "a2", "timestamp": "2023-10-27T09:30:00Z", "user": "system", "action": "System Maintenance", "details": "Database backup completed.", "type": "system"},
    ]
