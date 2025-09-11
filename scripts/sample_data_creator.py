import csv, random, string
from datetime import datetime, timedelta

# Set random seed for reproducibility
random.seed(101)

def random_date(start_date, end_date):
    """Generate a random date between start_date and end_date"""
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    return start_date + timedelta(days=random_days)

def random_time():
    """Generate a random time"""
    hour = random.randint(0, 23)
    minute = random.choice([0, 15, 30, 45])
    return f"{hour:02d}:{minute:02d}"

def random_datetime():
    """Generate a random datetime string"""
    base_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    random_dt = random_date(base_date, end_date)
    random_hr = random.randint(0, 23)
    random_min = random.choice([0, 15, 30, 45])
    return f"{random_dt.strftime('%Y-%m-%d')} {random_hr:02d}:{random_min:02d}:00"

CREW_ROWS = 100
# Set date range for flights and rosters
FLIGHT_START_DATE = datetime(2025, 7, 1)
FLIGHT_END_DATE = datetime(2025, 9, 30)

# Calculate number of days in range
NUM_DAYS = (FLIGHT_END_DATE - FLIGHT_START_DATE).days + 1
# Let's generate about 10 flights per day for good coverage
FLIGHT_ROWS = NUM_DAYS * 10
# Let's generate about 30 rosters per day
ROSTER_ROWS = NUM_DAYS * 30

# ===================== ENUM-COMPATIBLE VALUES =====================
# Crew Enums
ranks = ["captain", "first_officer", "flight_engineer", "cabin_crew", "senior_cabin_crew"]
statuses = ["available", "on_duty", "rest", "sick_leave", "vacation", "training", "grounded"]

# Flight Enums
flight_types = ["domestic", "international", "cargo", "charter", "training", "positioning"]
flight_statuses = ["scheduled", "active", "delayed", "cancelled", "completed", "diverted"]

# Roster Enums
assignment_types = ["flight_duty", "standby", "training", "reserve", "rest"]
assignment_statuses = ["assigned", "confirmed", "standby", "cancelled", "completed"]
crew_positions = ["captain", "first_officer", "senior_cabin_crew", "cabin_crew", "flight_engineer"]

# =================================================================

# Generate CREW data (100 rows)
crew_data = []
airports = ['JFK', 'LAX', 'ORD', 'DFW', 'DEN', 'ATL', 'SFO', 'SEA', 'MIA', 'BOS']
languages = ['English', 'Spanish', 'French', 'German', 'Mandarin', 'Japanese', 'Portuguese']
qualifications = ['B737', 'A320', 'B777', 'A330', 'B747', 'Emergency Response', 'First Aid', 'CPR']

first_names = ['John', 'Sarah', 'Michael', 'Emily', 'David', 'Jessica', 'Robert', 'Ashley', 'James', 'Amanda',
               'William', 'Stephanie', 'Christopher', 'Jennifer', 'Daniel', 'Lisa', 'Matthew', 'Angela', 
               'Anthony', 'Heather', 'Mark', 'Nicole', 'Donald', 'Amy', 'Steven', 'Kimberly', 'Paul', 'Donna']

last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
              'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
              'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson']

for i in range(CREW_ROWS):
    hire_date = random_date(datetime(2015, 1, 1), datetime(2024, 6, 1))
    crew_data.append([
        i + 1,  # id
        f"EMP{1000 + i}",  # employee_id
        random.choice(first_names),  # first_name
        random.choice(last_names),  # last_name
        random.choice(ranks),  # rank (enum-compliant)
        random.choice(airports),  # base_airport
        hire_date.strftime('%Y-%m-%d'),  # hire_date
        random.randint(1, 20),  # seniority_number
        random.choice(statuses),  # status (enum-compliant)
        random.choice(airports),  # current_location
        random_time(),  # duty_start_time
        random_time(),  # duty_end_time
        random_date(datetime(2024, 8, 1), datetime(2024, 9, 10)).strftime('%Y-%m-%d'),  # last_rest_start
        random.randint(80, 120),  # total_flight_hours_month
        random.randint(150, 200),  # total_duty_hours_month
        ','.join(random.sample(qualifications, random.randint(2, 4))),  # qualifications
        ','.join(random.sample(languages, random.randint(1, 3))),  # languages
        round(random.uniform(3.5, 5.0), 1),  # performance_rating
        random.choice(['window', 'aisle', 'no_preference']),  # preferences
        random_date(datetime(2024, 6, 1), datetime(2025, 12, 1)).strftime('%Y-%m-%d'),  # medical_expiry
        random_date(datetime(2024, 6, 1), datetime(2025, 12, 1)).strftime('%Y-%m-%d'),  # license_expiry
        random.randint(1, 10),  # fatigue_score
        round(random.uniform(0.7, 1.0), 2),  # predicted_availability
        random.randint(150, 200),  # optimization_weight
        random_datetime(),  # created_at
        random_datetime()  # updated_at
    ])

# Generate FLIGHTS data (for July-Sept 2025)
flights_data = []
airlines = ['AA', 'DL', 'UA', 'WN', 'B6', 'AS', 'NK', 'F9']
aircraft_types = ['Boeing 737-800', 'Airbus A320', 'Boeing 777-200', 'Airbus A330-200', 'Boeing 747-400']
weather_conditions = ['clear', 'cloudy', 'rainy', 'stormy', 'foggy']

for i in range(FLIGHT_ROWS):
    airline = random.choice(airlines)
    flight_num = random.randint(100, 9999)
    # Random date in range
    departure_time = FLIGHT_START_DATE + timedelta(days=random.randint(0, NUM_DAYS-1), hours=random.randint(0, 23), minutes=random.choice([0, 15, 30, 45]))
    arrival_time = departure_time + timedelta(hours=random.randint(1, 12))
    
    flights_data.append([
        i + 1,  # id
        f"{airline}{flight_num}",  # flight_number
        airline,  # airline_code
        random.choice(airports),  # departure_airport
        random.choice(airports),  # arrival_airport
        departure_time.strftime('%Y-%m-%d %H:%M:%S'),  # scheduled_departure
        arrival_time.strftime('%Y-%m-%d %H:%M:%S'),  # scheduled_arrival
        (departure_time + timedelta(minutes=random.randint(-15, 30))).strftime('%Y-%m-%d %H:%M:%S'),  # actual_departure
        (arrival_time + timedelta(minutes=random.randint(-15, 45))).strftime('%Y-%m-%d %H:%M:%S'),  # actual_arrival
        random.choice(aircraft_types),  # aircraft_type
        f"N{random.randint(100, 999)}{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}",  # registration
        f"A{random.randint(1, 50)}",  # gate_number
        random.choice(flight_types),  # flight_type (enum-compliant)
        random.choice(flight_statuses),  # status (enum-compliant)
        f"{random.randint(2, 8)}:{random.choice(['00', '15', '30', '45'])}",  # estimated_flight_time
        f"{random.randint(2, 8)}:{random.choice(['00', '15', '30', '45'])}",  # actual_flight_time
        random.randint(500, 3000),  # distance
        random.choice(['2_pilot', '3_crew', 'full_crew']),  # crew_requirements
        random.randint(2, 8),  # minimum_crew_count
        random.randint(50, 300),  # passenger_count
        random.randint(1000, 15000),  # cargo_weight
        random.randint(5000, 25000),  # fuel_required
        random.choice(['normal', 'high', 'urgent']),  # priority_level
        random.randint(50000, 500000),  # revenue
        random.randint(1000, 5000),  # cost_per_delay_hour
        random.choice(weather_conditions),  # weather_info
        random.choice(['wheelchair', 'unaccompanied_minor', 'pet_transport', 'none']),  # special_requirements
        round(random.uniform(0.1, 0.3), 2),  # delay_probability
        round(random.uniform(0.7, 1.0), 2),  # crew_utilization_score
        random.randint(1, 5),  # disruption_impact
        random_datetime(),  # created_at
        random_datetime()  # updated_at
    ])

# Generate ROSTERS data (for July-Sept 2025)
rosters_data = []
for i in range(ROSTER_ROWS):
    crew_id = random.randint(1, CREW_ROWS)
    flight_id = random.randint(1, FLIGHT_ROWS)
    # Random date in range
    duty_start = FLIGHT_START_DATE + timedelta(days=random.randint(0, NUM_DAYS-1), hours=random.randint(0, 23), minutes=random.choice([0, 15, 30, 45]))
    duty_end = duty_start + timedelta(hours=random.randint(6, 12))
    report_time = duty_start - timedelta(hours=1)
    release_time = duty_end + timedelta(minutes=30)
    
    rosters_data.append([
        i + 1,  # id
        crew_id,  # crew_id
        flight_id,  # flight_id
        random.choice(assignment_types),  # assignment_type (enum-compliant)
        random.choice(assignment_statuses),  # status (enum-compliant)
        random.choice(crew_positions),  # crew_position (enum-compliant)
        duty_start.strftime('%Y-%m-%d %H:%M:%S'),  # duty_start
        duty_end.strftime('%Y-%m-%d %H:%M:%S'),  # duty_end
        report_time.strftime('%Y-%m-%d %H:%M:%S'),  # report_time
        release_time.strftime('%Y-%m-%d %H:%M:%S'),  # release_time
        round(random.uniform(0.7, 1.0), 2),  # assignment_confidence
        round(random.uniform(0.6, 1.0), 2),  # optimization_score
        random.randint(0, 3),  # constraint_violations
        round(random.uniform(6.0, 12.0), 1),  # actual_duty_hours
        round(random.uniform(3.0, 5.0), 1),  # crew_feedback_rating
        f"scheduler_{random.randint(1, 5)}",  # assigned_by
        random_datetime(),  # assigned_at
        random_datetime()  # updated_at
    ])

# Write to CSV files
def write_csv(filename, headers, data):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

# Crew CSV
crew_headers = ['id', 'employee_id', 'first_name', 'last_name', 'rank', 'base_airport', 'hire_date', 
                'seniority_number', 'status', 'current_location', 'duty_start_time', 'duty_end_time',
                'last_rest_start', 'total_flight_hours_month', 'total_duty_hours_month', 'qualifications',
                'languages', 'performance_rating', 'preferences', 'medical_expiry', 'license_expiry',
                'fatigue_score', 'predicted_availability', 'optimization_weight', 'created_at', 'updated_at']

write_csv('crew.csv', crew_headers, crew_data)

# Flights CSV
flights_headers = ['id', 'flight_number', 'airline_code', 'departure_airport', 'arrival_airport',
                   'scheduled_departure', 'scheduled_arrival', 'actual_departure', 'actual_arrival',
                   'aircraft_type', 'aircraft_registration', 'gate_number', 'flight_type', 'status',
                   'estimated_flight_time', 'actual_flight_time', 'distance', 'crew_requirements',
                   'minimum_crew_count', 'passenger_count', 'cargo_weight', 'fuel_required',
                   'priority_level', 'revenue', 'cost_per_delay_hour', 'weather_info',
                   'special_requirements', 'delay_probability', 'crew_utilization_score',
                   'disruption_impact', 'created_at', 'updated_at']

write_csv('flights.csv', flights_headers, flights_data)

# Rosters CSV
rosters_headers = ['id', 'crew_id', 'flight_id', 'assignment_type', 'status', 'crew_position',
                   'duty_start', 'duty_end', 'report_time', 'release_time', 'assignment_confidence',
                   'optimization_score', 'constraint_violations', 'actual_duty_hours',
                   'crew_feedback_rating', 'assigned_by', 'assigned_at', 'updated_at']

write_csv('rosters.csv', rosters_headers, rosters_data)

print(f"Generated {CREW_ROWS} rows for crew.csv")
print(f"Generated {FLIGHT_ROWS} rows for flights.csv (covering {FLIGHT_START_DATE.date()} to {FLIGHT_END_DATE.date()})")
print(f"Generated {ROSTER_ROWS} rows for rosters.csv (covering {FLIGHT_START_DATE.date()} to {FLIGHT_END_DATE.date()})")
