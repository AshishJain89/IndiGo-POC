from abc import ABC, abstractmethod
from typing import List, Optional
from backend.domain.entities.crew import Crew
from datetime import datetime

class ICrewRepository(ABC):
    @abstractmethod
    async def get_by_id(self, crew_id: int) -> Optional[Crew]:
        pass
    @abstractmethod
    async def get_available_crew(self, start_time: datetime, end_time: datetime) -> List[Crew]:
        pass
    @abstractmethod
    async def save(self, crew: Crew) -> Crew:
        pass

    @abstractmethod
    async def get_total_active_count(self) -> int:
        pass
