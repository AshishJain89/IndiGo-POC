from dataclasses import dataclass
from datetime import datetime

@dataclass
class AuditLog:
    id: int
    timestamp: datetime
    user: str
    action: str
    details: str
    type: str
