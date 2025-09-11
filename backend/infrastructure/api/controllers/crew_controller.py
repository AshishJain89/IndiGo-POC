from fastapi import APIRouter, Depends
from infrastructure.database.core import get_db_conn
from infrastructure.database.crew_repository import CrewRepository
from domain.entities.crew import Crew
from typing import List

router = APIRouter(prefix="/api/crew", tags=["crew"])

@router.get("/", response_model=List[Crew])
async def get_all_crew(conn=Depends(get_db_conn)):
    repo = CrewRepository(conn)
    query = "SELECT * FROM crew"
    async with conn.cursor() as cur:
        await cur.execute(query)
        rows = await cur.fetchall()
        if not rows:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="No crew found")
        columns = [desc[0] for desc in cur.description]
        return [Crew(**dict(zip(columns, row))) for row in rows]

@router.get("/{crew_id}", response_model=Crew)
async def get_crew_by_id(crew_id: int, conn=Depends(get_db_conn)):
    repo = CrewRepository(conn)
    crew = await repo.get_by_id(crew_id)
    if not crew:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Crew not found")
    return crew
