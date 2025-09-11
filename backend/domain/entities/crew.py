from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Crew:
    id: int
    employee_id: str
    first_name: str
    last_name: str
    rank: str
    base_airport: str
    hire_date: Optional[datetime]
    seniority_number: Optional[int]
    status: str
    current_location: Optional[str]
    duty_start_time: Optional[datetime]
    duty_end_time: Optional[datetime]
    last_rest_start: Optional[datetime]
    total_flight_hours_month: Optional[float]
    total_duty_hours_month: Optional[float]
    qualifications: Optional[List[str]]
    languages: Optional[List[str]]
    performance_rating: Optional[float]
    preferences: Optional[List[str]]
    medical_expiry: Optional[datetime]
    license_expiry: Optional[datetime]
    fatigue_score: Optional[float]
    predicted_availability: Optional[float]
    optimization_weight: Optional[float]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
