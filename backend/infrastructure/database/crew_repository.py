from applications.interfaces.crew_repository import ICrewRepository
from domain.entities.crew import Crew
from datetime import datetime
from typing import List, Optional

class CrewRepository(ICrewRepository):
    def __init__(self, conn):
        self.conn = conn

    async def get_by_id(self, crew_id: int) -> Optional[Crew]:
        query = "SELECT * FROM crew WHERE id = %s"
        async with self.conn.cursor() as cur:
            await cur.execute(query, (crew_id,))
            row = await cur.fetchone()
            if row:
                return Crew(**dict(zip([desc[0] for desc in cur.description], row)))
            return None

    async def get_available_crew(self, start_time: datetime, end_time: datetime) -> List[Crew]:
        query = """
        SELECT * FROM crew WHERE status = 'available' AND duty_start_time <= %s AND duty_end_time >= %s
        """
        async with self.conn.cursor() as cur:
            await cur.execute(query, (start_time, end_time))
            rows = await cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [Crew(**dict(zip(columns, row))) for row in rows]

    async def save(self, crew: Crew) -> Crew:
        # Example: upsert logic (simplified)
        query = """
        INSERT INTO crew (id, employee_id, first_name, last_name, rank, base_airport, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET status = EXCLUDED.status
        RETURNING *
        """
        values = (crew.id, crew.employee_id, crew.first_name, crew.last_name, crew.rank, crew.base_airport, crew.status)
        async with self.conn.cursor() as cur:
            await cur.execute(query, values)
            row = await cur.fetchone()
            return Crew(**dict(zip([desc[0] for desc in cur.description], row)))
