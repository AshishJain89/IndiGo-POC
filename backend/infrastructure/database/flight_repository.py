from applications.interfaces.flight_repository import IFlightRepository
from domain.entities.flight import Flight
from datetime import datetime
from typing import List, Optional

class FlightRepository(IFlightRepository):
    def __init__(self, conn):
        self.conn = conn

    async def get_by_id(self, flight_id: int) -> Optional[Flight]:
        query = "SELECT * FROM flights WHERE id = %s"
        async with self.conn.cursor() as cur:
            await cur.execute(query, (flight_id,))
            row = await cur.fetchone()
            if row:
                return Flight(**dict(zip([desc[0] for desc in cur.description], row)))
            return None

    async def get_flights_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Flight]:
        query = "SELECT * FROM flights WHERE scheduled_departure >= %s AND scheduled_arrival <= %s"
        async with self.conn.cursor() as cur:
            await cur.execute(query, (start_date, end_date))
            rows = await cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [Flight(**dict(zip(columns, row))) for row in rows]

    async def save(self, flight: Flight) -> Flight:
        # Example: upsert logic (simplified)
        query = """
        INSERT INTO flights (id, flight_number, departure_airport, arrival_airport, scheduled_departure, scheduled_arrival, aircraft_type, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET status = EXCLUDED.status
        RETURNING *
        """
        values = (flight.id, flight.flight_number, flight.departure_airport, flight.arrival_airport, flight.scheduled_departure, flight.scheduled_arrival, flight.aircraft_type, flight.status)
        async with self.conn.cursor() as cur:
            await cur.execute(query, values)
            row = await cur.fetchone()
            return Flight(**dict(zip([desc[0] for desc in cur.description], row)))
