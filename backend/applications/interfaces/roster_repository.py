from abc import ABC, abstractmethod
from typing import List, Optional
from backend.domain.entities.roster import Roster
from datetime import datetime

class IRosterRepository(ABC):
    @abstractmethod
    async def get_by_crew_and_date(self, crew_id: int, start_date: datetime, end_date: datetime) -> List[Roster]:
        pass
    @abstractmethod
    async def save(self, roster: Roster) -> Roster:
        pass
    @abstractmethod
    async def bulk_save(self, rosters: List[Roster]) -> List[Roster]:
        pass
