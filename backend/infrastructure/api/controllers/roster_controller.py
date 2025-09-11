from fastapi import APIRouter, Depends
from infrastructure.database.core import get_db_conn
from infrastructure.database.roster_repository import RosterRepository
from domain.entities.roster import Roster
from typing import List

router = APIRouter(prefix="/api/rosters", tags=["rosters"])

@router.get("/", response_model=List[Roster])
async def get_all_rosters(conn=Depends(get_db_conn)):
    repo = RosterRepository(conn)
    query = "SELECT * FROM rosters"
    async with conn.cursor() as cur:
        await cur.execute(query)
        rows = await cur.fetchall()
        if not rows:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="No rosters found")
        columns = [desc[0] for desc in cur.description]
        return [Roster(**dict(zip(columns, row))) for row in rows]

@router.get("/{roster_id}", response_model=Roster)
async def get_roster_by_id(roster_id: int, conn=Depends(get_db_conn)):
    repo = RosterRepository(conn)
    query = "SELECT * FROM rosters WHERE id = %s"
    async with conn.cursor() as cur:
        await cur.execute(query, (roster_id,))
        row = await cur.fetchone()
        if not row:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Roster not found")
        columns = [desc[0] for desc in cur.description]
        return Roster(**dict(zip(columns, row)))
