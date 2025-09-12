from fastapi import APIRouter, Depends, Query
from backend.infrastructure.database.core import get_db_conn
from backend.domain.entities.roster import Roster
from typing import List
from datetime import datetime

router = APIRouter(prefix="/api/rosters", tags=["rosters"])

@router.get("/", response_model=List[Roster])
async def get_all_rosters(
    conn=Depends(get_db_conn),
    start_date: str = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(None, description="End date (YYYY-MM-DD)")
):
    base_query = "SELECT * FROM rosters"
    params = []
    if start_date and end_date:
        base_query += " WHERE duty_start >= %s AND duty_start <= %s"
        params = [start_date, end_date]
    elif start_date:
        base_query += " WHERE duty_start >= %s"
        params = [start_date]
    elif end_date:
        base_query += " WHERE duty_start <= %s"
        params = [end_date]
    query = base_query
    async with conn.cursor() as cur:
        await cur.execute(query, params)
        rows = await cur.fetchall()
        if not rows:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="No rosters found")
        columns = [desc[0] for desc in cur.description]
        return [Roster(**dict(zip(columns, row))) for row in rows]

@router.get("/{roster_id}", response_model=Roster)
async def get_roster_by_id(roster_id: int, conn=Depends(get_db_conn)):
    query = "SELECT * FROM rosters WHERE id = %s"
    async with conn.cursor() as cur:
        await cur.execute(query, (roster_id,))
        row = await cur.fetchone()
        if not row:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Roster not found")
        columns = [desc[0] for desc in cur.description]
        return Roster(**dict(zip(columns, row)))