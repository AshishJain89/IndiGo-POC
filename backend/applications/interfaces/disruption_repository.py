from abc import ABC, abstractmethod
from typing import List
from backend.domain.entities.disruption import Disruption

class IDisruptionRepository(ABC):
    @abstractmethod
    async def get_disruptions(self) -> List[Disruption]:
        pass

    @abstractmethod
    async def get_total_count(self) -> int:
        pass
