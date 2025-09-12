from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime, timezone

class Conflict(BaseModel):
    id: str
    type: Literal["hard", "soft"]
    severity: Literal["low", "medium", "high"]
    title: str
    description: str
    affectedCrew: List[str]
    affectedFlights: List[str]
    timestamp: datetime

router = APIRouter(prefix="/api/conflicts", tags=["conflicts"])

@router.get("/", response_model=List[Conflict])
async def get_conflicts():
    # Return empty list for now; UI shows "No conflicts detected".
    # Replace with logic that analyzes rosters/flights to detect conflicts.
    return []