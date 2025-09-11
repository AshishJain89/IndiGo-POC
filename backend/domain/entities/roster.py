from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Roster:
    id: int
    crew_id: int
    flight_id: int
    assignment_type: Optional[str]
    status: Optional[str]
    crew_position: Optional[str]
    duty_start: Optional[datetime]
    duty_end: Optional[datetime]
    report_time: Optional[datetime]
    release_time: Optional[datetime]
    assignment_confidence: Optional[float]
    optimization_score: Optional[float]
    constraint_violations: Optional[int]
    actual_duty_hours: Optional[float]
    crew_feedback_rating: Optional[float]
    assigned_by: Optional[str]
    assigned_at: Optional[datetime]
    updated_at: Optional[datetime]
