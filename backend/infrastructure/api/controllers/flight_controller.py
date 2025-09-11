
from fastapi import APIRouter, Depends
from infrastructure.database.core import get_db_conn
from infrastructure.database.repositories import FlightRepository
from typing import List
from pydantic import BaseModel

class FlightCrew(BaseModel):
    captain: str | None = None
    firstOfficer: str | None = None
    flightAttendants: List[str] = []

class FlightOut(BaseModel):
    id: str
    flightNumber: str
    aircraft: str
    route: dict
    departure: str
    arrival: str
    status: str
    assignedCrew: FlightCrew
    requiredQualifications: List[str]
    conflicts: List[str]

router = APIRouter(prefix="/api/flights", tags=["flights"])

@router.get("/", response_model=List[FlightOut])
async def get_flights(conn=Depends(get_db_conn)):
    repo = FlightRepository(conn)
    flights = await repo.get_all_flights()
    result = []
    for f in flights:
        # Map DB fields to API schema
        assigned_crew = f.get("assigned_crew") or []
        crew_map = {"captain": None, "firstOfficer": None, "flightAttendants": []}
        for crew in assigned_crew:
            pos = (crew.get("crew_position") or "").lower()
            name = f"{crew.get('first_name','')} {crew.get('last_name','')}".strip()
            if pos == "captain":
                crew_map["captain"] = name
            elif pos == "first_officer":
                crew_map["firstOfficer"] = name
            elif pos == "flight_attendant":
                crew_map["flightAttendants"].append(name)
        result.append(FlightOut(
            id=str(f["id"]),
            flightNumber=f["flight_number"],
            aircraft=f["aircraft_type"],
            route={"from": f["departure_airport"], "to": f["arrival_airport"]},
            departure=f["scheduled_departure"].isoformat() if f["scheduled_departure"] else "",
            arrival=f["scheduled_arrival"].isoformat() if f["scheduled_arrival"] else "",
            status=f["status"],
            assignedCrew=FlightCrew(**crew_map),
            requiredQualifications=f.get("crew_requirements") or [],
            conflicts=[] # TODO: Add logic for conflicts if needed
        ))
    return result
