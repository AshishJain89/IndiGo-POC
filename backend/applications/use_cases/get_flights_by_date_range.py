from backend.applications.interfaces.flight_repository import IFlightRepository
from backend.domain.entities.flight import Flight
from typing import List
from datetime import datetime

class GetFlightsByDateRangeUseCase:
    def __init__(self, flight_repo: IFlightRepository):
        self.flight_repo = flight_repo

    async def execute(self, start_date: datetime, end_date: datetime) -> List[Flight]:
        return await self.flight_repo.get_flights_by_date_range(start_date, end_date)
