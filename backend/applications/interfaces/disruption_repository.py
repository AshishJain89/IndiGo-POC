from abc import ABC, abstractmethod
from typing import List
from backend.domain.entities.disruption import Disruption

class DisruptionRepository(ABC):
    @abstractmethod
    async def get_disruptions(self) -> List[Disruption]:
        pass
