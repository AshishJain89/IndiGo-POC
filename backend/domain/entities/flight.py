from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Flight:
    id: int
    flight_number: str
    airline_code: Optional[str]
    departure_airport: str
    arrival_airport: str
    scheduled_departure: Optional[datetime]
    scheduled_arrival: Optional[datetime]
    actual_departure: Optional[datetime]
    actual_arrival: Optional[datetime]
    aircraft_type: str
    aircraft_registration: Optional[str]
    gate_number: Optional[str]
    flight_type: Optional[str]
    status: str
    estimated_flight_time: Optional[float]
    actual_flight_time: Optional[float]
    distance: Optional[float]
    crew_requirements: Optional[list]
    minimum_crew_count: Optional[int]
    passenger_count: Optional[int]
    cargo_weight: Optional[float]
    fuel_required: Optional[float]
    priority_level: Optional[int]
    revenue: Optional[float]
    cost_per_delay_hour: Optional[float]
    weather_info: Optional[str]
    special_requirements: Optional[list]
    delay_probability: Optional[float]
    crew_utilization_score: Optional[float]
    disruption_impact: Optional[float]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
