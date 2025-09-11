from dataclasses import dataclass
from typing import List

@dataclass
class Disruption:
    id: int
    type: str
    severity: str
    title: str
    description: str
    affected_flights: List[str]
    timestamp: str
