from backend.applications.interfaces.roster_repository import IRosterRepository
from backend.domain.entities.roster import Roster
from datetime import datetime
from typing import List, Optional

class RosterRepository(IRosterRepository):
    def __init__(self, conn):
        self.conn = conn

    async def get_by_crew_and_date(self, crew_id: int, start_date: datetime, end_date: datetime) -> List[Roster]:
        query = "SELECT * FROM rosters WHERE crew_id = %s AND duty_start >= %s AND duty_end <= %s"
        async with self.conn.cursor() as cur:
            await cur.execute(query, (crew_id, start_date, end_date))
            rows = await cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [Roster(**dict(zip(columns, row))) for row in rows]

    async def save(self, roster: Roster) -> Roster:
        # Example: upsert logic (simplified)
        query = """
        INSERT INTO rosters (id, crew_id, flight_id, assignment_type, status, crew_position, duty_start, duty_end)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET status = EXCLUDED.status
        RETURNING *
        """
        values = (roster.id, roster.crew_id, roster.flight_id, roster.assignment_type, roster.status, roster.crew_position, roster.duty_start, roster.duty_end)
        async with self.conn.cursor() as cur:
            await cur.execute(query, values)
            row = await cur.fetchone()
            return Roster(**dict(zip([desc[0] for desc in cur.description], row)))

    async def bulk_save(self, rosters: List[Roster]) -> List[Roster]:
        # Example: bulk insert/update
        results = []
        for roster in rosters:
            results.append(await self.save(roster))
        return results
