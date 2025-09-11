from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.flight import Flight
from datetime import datetime

class IFlightRepository(ABC):
    @abstractmethod
    async def get_by_id(self, flight_id: int) -> Optional[Flight]:
        pass
    @abstractmethod
    async def get_flights_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Flight]:
        pass
    @abstractmethod
    async def save(self, flight: Flight) -> Flight:
        pass
