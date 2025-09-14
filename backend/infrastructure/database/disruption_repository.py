from backend.applications.interfaces.disruption_repository import IDisruptionRepository
from backend.domain.entities.disruption import Disruption
from backend.infrastructure.database.core import get_db_conn
from typing import List

class DisruptionRepositoryImpl(IDisruptionRepository):
    def __init__(self, conn):
        self.conn = conn

    async def get_disruptions(self) -> List[Disruption]:
        query = "SELECT * FROM disruptions ORDER BY timestamp DESC"
        async with self.conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            disruptions = []
            for row in rows:
                d = dict(zip(columns, row))
                disruptions.append(Disruption(
                    id=d["id"],
                    type=d["type"],
                    severity=d["severity"],
                    title=d["title"],
                    description=d["description"],
                    affected_flights=d["affected_flights"] if isinstance(d["affected_flights"], list) else [],
                    timestamp=d["timestamp"].isoformat() if d["timestamp"] else ""
                ))
            return disruptions

    async def get_total_count(self) -> int:
        query = "SELECT COUNT(*) FROM disruptions"
        async with self.conn.cursor() as cur:
            await cur.execute(query)
            row = await cur.fetchone()
            return row[0] if row else 0
