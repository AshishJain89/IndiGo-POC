from abc import ABC, abstractmethod
from typing import List
from backend.domain.entities.audit_log import AuditLog

class IAuditLogRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[AuditLog]:
        pass
