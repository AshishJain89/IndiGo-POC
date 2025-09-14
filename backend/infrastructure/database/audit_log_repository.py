from backend.applications.interfaces.audit_log_repository import IAuditLogRepository
from backend.domain.entities.audit_log import AuditLog
from typing import List

class AuditLogRepository(IAuditLogRepository):
    def __init__(self, conn):
        self.conn = conn

    async def get_all(self) -> List[AuditLog]:
        query = "SELECT * FROM audit_log ORDER BY timestamp DESC"
        async with self.conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [AuditLog(**dict(zip(columns, row))) for row in rows]
