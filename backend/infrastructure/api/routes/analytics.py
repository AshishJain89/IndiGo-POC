from fastapi import APIRouter, Depends
from backend.infrastructure.database.core import get_db_conn
from backend.infrastructure.database.flight_repository import FlightRepository
from backend.infrastructure.database.crew_repository import CrewRepository
from backend.infrastructure.database.disruption_repository import DisruptionRepositoryImpl
from backend.infrastructure.database.audit_log_repository import AuditLogRepository

router = APIRouter()

@router.get("/metrics")
async def get_metrics(conn=Depends(get_db_conn)):
    flight_repo = FlightRepository(conn)
    crew_repo = CrewRepository(conn)
    disruption_repo = DisruptionRepositoryImpl(conn)

    total_flights = await flight_repo.get_total_count()
    active_crew = await crew_repo.get_total_active_count()
    total_disruptions = await disruption_repo.get_total_count()

    compliance_rate = 0
    if total_flights > 0:
        compliance_rate = round((total_flights - total_disruptions) / total_flights * 100)

    return [
        {"title": "Total Flights", "value": str(total_flights), "change": "5%", "trend": "up", "icon": "TrendingUp"},
        {"title": "Active Crew", "value": str(active_crew), "change": "2%", "trend": "up", "icon": "Users"},
        {"title": "Compliance Rate", "value": f"{compliance_rate}%", "change": "0%", "trend": "stable", "icon": "Shield"},
        {"title": "Disruptions", "value": str(total_disruptions), "change": "10%", "trend": "down", "icon": "AlertTriangle"},
    ]

@router.get("/violations")
async def get_violations(conn=Depends(get_db_conn)):
    disruption_repo = DisruptionRepositoryImpl(conn)
    disruptions = await disruption_repo.get_disruptions()
    return [
        {
            "id": d.id,
            "rule": d.title,
            "description": d.description,
            "severity": d.severity,
            "crew": "CRW789",  # Placeholder
            "timestamp": d.timestamp,
        }
        for d in disruptions
    ]

@router.get("/auditlog")
async def get_audit_log(conn=Depends(get_db_conn)):
    audit_log_repo = AuditLogRepository(conn)
    audit_logs = await audit_log_repo.get_all()
    return audit_logs
