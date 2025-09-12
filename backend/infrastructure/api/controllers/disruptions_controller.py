from fastapi import APIRouter, Depends, status
from backend.infrastructure.database.core import get_db_conn
from typing import List
from pydantic import BaseModel
from datetime import timezone
import datetime, json

class DisruptionIn(BaseModel):
    type: str
    severity: str
    title: str
    description: str
    affectedFlights: List[str]

class DisruptionOut(DisruptionIn):
    id: int
    timestamp: str

router = APIRouter(prefix="/api/disruptions", tags=["disruptions"])

@router.get("/", response_model=List[DisruptionOut])
async def get_disruptions(conn=Depends(get_db_conn)):
    # Use connection directly, remove repository instantiation
    query = "SELECT * FROM disruptions ORDER BY timestamp DESC"
    async with conn.cursor() as cur:
        await cur.execute(query)
        rows = await cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        disruptions = []
        for row in rows:
            d = dict(zip(columns, row))
            disruptions.append(DisruptionOut(
                id=d["id"],
                type=d["type"],
                severity=d["severity"],
                title=d["title"],
                description=d["description"],
                affectedFlights=d["affected_flights"] if isinstance(d["affected_flights"], list) else [],
                timestamp=d["timestamp"].isoformat() if d["timestamp"] else ""
            ))
        return disruptions

@router.post("/", response_model=DisruptionOut, status_code=status.HTTP_201_CREATED)
async def create_disruption(disruption: DisruptionIn, conn=Depends(get_db_conn)):
    # Fix the INSERT query - it was missing INSERT INTO
    query = """
        INSERT INTO disruptions (type, severity, title, description, affected_flights, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, type, severity, title, description, affected_flights, timestamp
    """
    now = datetime.datetime.now(timezone.utc)
    values = (
        disruption.type,
        disruption.severity,
        disruption.title,
        disruption.description,
        json.dumps(disruption.affectedFlights),
        now
    )
    async with conn.cursor() as cur:
        await cur.execute(query, values)
        row = await cur.fetchone()
        columns = [desc[0] for desc in cur.description]
        d = dict(zip(columns, row))
        return DisruptionOut(
            id=d["id"],
            type=d["type"],
            severity=d["severity"],
            title=d["title"],
            description=d["description"],
            affectedFlights=json.loads(d["affected_flights"]) if d["affected_flights"] else [],
            timestamp=d["timestamp"].isoformat() if d["timestamp"] else ""
        )