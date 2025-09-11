# Repository for flights data access
from typing import List, Dict, Any
from infrastructure.database.core import get_db_conn

class FlightRepository:
    def __init__(self, conn):
        self.conn = conn

    async def get_all_flights(self) -> List[Dict[str, Any]]:
        query = """
        SELECT f.*, 
            json_agg(json_build_object(
                'crew_id', r.crew_id,
                'crew_position', r.crew_position,
                'first_name', c.first_name,
                'last_name', c.last_name
            )) AS assigned_crew
        FROM flights f
        LEFT JOIN rosters r ON f.id = r.flight_id
        LEFT JOIN crew c ON r.crew_id = c.id
        GROUP BY f.id
        ORDER BY f.scheduled_departure
        """
        async with self.conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in rows]
