from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Roster:
    id: int
    crew_id: int
    flight_id: int
    assignment_type: Optional[str] = None
    status: Optional[str] = None
    crew_position: Optional[str] = None
    duty_start: Optional[datetime] = None
    duty_end: Optional[datetime] = None
    report_time: Optional[datetime] = None
    release_time: Optional[datetime] = None
    assignment_confidence: Optional[float] = None
    optimization_score: Optional[float] = None
    constraint_violations: Optional[int] = None
    actual_duty_hours: Optional[float] = None
    crew_feedback_rating: Optional[float] = None
    assigned_by: Optional[str] = None
    assigned_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
