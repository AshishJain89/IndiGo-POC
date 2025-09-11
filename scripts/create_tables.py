
"""Database table creation and migration script (psycopg version)"""
import sys, os, csv, logging
from pathlib import Path
from datetime import datetime
import psycopg

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# DB config (reuse backend config logic)
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "crewdb")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DSN = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASS}"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("create_tables")



def create_tables():
    """Create all database tables using raw SQL"""
    try:
        logger.info("Starting database table creation...")
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                # Crew table
                cur.execute('''
                CREATE TABLE IF NOT EXISTS crew (
                    id SERIAL PRIMARY KEY,
                    employee_id VARCHAR(32) NOT NULL,
                    first_name VARCHAR(64),
                    last_name VARCHAR(64),
                    rank VARCHAR(32),
                    base_airport VARCHAR(8),
                    hire_date DATE,
                    seniority_number INT,
                    status VARCHAR(32),
                    current_location VARCHAR(32),
                    duty_start_time TIME,
                    duty_end_time TIME,
                    last_rest_start DATE,
                    total_flight_hours_month FLOAT,
                    total_duty_hours_month FLOAT,
                    qualifications TEXT,
                    languages TEXT,
                    performance_rating FLOAT,
                    preferences TEXT,
                    medical_expiry DATE,
                    license_expiry DATE,
                    fatigue_score FLOAT,
                    predicted_availability FLOAT,
                    optimization_weight FLOAT,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                );''')
                # Flights table
                cur.execute('''
                CREATE TABLE IF NOT EXISTS flights (
                    id SERIAL PRIMARY KEY,
                    flight_number VARCHAR(16) NOT NULL,
                    airline_code VARCHAR(8),
                    departure_airport VARCHAR(8),
                    arrival_airport VARCHAR(8),
                    scheduled_departure TIMESTAMP,
                    scheduled_arrival TIMESTAMP,
                    actual_departure TIMESTAMP,
                    actual_arrival TIMESTAMP,
                    aircraft_type VARCHAR(32),
                    aircraft_registration VARCHAR(32),
                    gate_number VARCHAR(8),
                    flight_type VARCHAR(32),
                    status VARCHAR(32),
                    estimated_flight_time FLOAT,
                    actual_flight_time FLOAT,
                    distance FLOAT,
                    crew_requirements TEXT,
                    minimum_crew_count INT,
                    passenger_count INT,
                    cargo_weight FLOAT,
                    fuel_required FLOAT,
                    priority_level VARCHAR(16),
                    revenue FLOAT,
                    cost_per_delay_hour FLOAT,
                    weather_info VARCHAR(64),
                    special_requirements TEXT,
                    delay_probability FLOAT,
                    crew_utilization_score FLOAT,
                    disruption_impact FLOAT,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                );''')
                # Rosters table
                cur.execute('''
                CREATE TABLE IF NOT EXISTS rosters (
                    id SERIAL PRIMARY KEY,
                    crew_id INT,
                    flight_id INT,
                    assignment_type VARCHAR(32),
                    status VARCHAR(32),
                    crew_position VARCHAR(32),
                    duty_start TIMESTAMP,
                    duty_end TIMESTAMP,
                    report_time TIMESTAMP,
                    release_time TIMESTAMP,
                    assignment_confidence FLOAT,
                    optimization_score FLOAT,
                    constraint_violations INT,
                    actual_duty_hours FLOAT,
                    crew_feedback_rating FLOAT,
                    assigned_by VARCHAR(64),
                    assigned_at TIMESTAMP,
                    updated_at TIMESTAMP
                );''')
                conn.commit()
        logger.info("Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        return False



def create_indexes():
    """Create additional indexes for performance using raw SQL"""
    try:
        logger.info("Creating additional database indexes...")
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE INDEX IF NOT EXISTS idx_crew_status_base ON crew (status, base_airport);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_crew_rank_seniority ON crew (rank, seniority_number);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_crew_performance ON crew (performance_rating DESC);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_flight_departure_date ON flights (scheduled_departure);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_flight_route ON flights (departure_airport, arrival_airport);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_flight_aircraft_status ON flights (aircraft_type, status);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_roster_crew_duty_time ON rosters (crew_id, duty_start, duty_end);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_roster_flight_position ON rosters (flight_id, crew_position);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_roster_duty_period ON rosters (duty_start, duty_end);")
                conn.commit()
        logger.info("Additional indexes created successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to create indexes: {str(e)}")
        return False



def insert_sample_data():
    """Insert sample data from CSVs into the database using psycopg"""
    try:
        logger.info("Inserting sample data...")
        csv_dir = project_root / "data/csvs"
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                # Insert Crew
                crew_file = csv_dir / "crew.csv"
                if crew_file.exists():
                    with open(crew_file, "r", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            cur.execute('''
                                INSERT INTO crew (employee_id, first_name, last_name, rank, base_airport, hire_date, seniority_number, status, current_location, duty_start_time, duty_end_time, last_rest_start, total_flight_hours_month, total_duty_hours_month, qualifications, languages, performance_rating, preferences, medical_expiry, license_expiry, fatigue_score, predicted_availability, optimization_weight, created_at, updated_at)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (employee_id) DO NOTHING;
                            ''', (
                                row["employee_id"], row["first_name"], row.get("last_name"), row.get("rank"), row.get("base_airport"), row.get("hire_date"), row.get("seniority_number"), row.get("status"), row.get("current_location"), row.get("duty_start_time"), row.get("duty_end_time"), row.get("last_rest_start"), row.get("total_flight_hours_month"), row.get("total_duty_hours_month"), row.get("qualifications"), row.get("languages"), row.get("performance_rating"), row.get("preferences"), row.get("medical_expiry"), row.get("license_expiry"), row.get("fatigue_score"), row.get("predicted_availability"), row.get("optimization_weight"), row.get("created_at"), row.get("updated_at")
                            ))
                else:
                    logger.warning(f"CSV file not found: {crew_file}")

                # Insert Flights
                flight_file = csv_dir / "flights.csv"
                if flight_file.exists():
                    with open(flight_file, "r", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            cur.execute('''
                                INSERT INTO flights (flight_number, airline_code, departure_airport, arrival_airport, scheduled_departure, scheduled_arrival, actual_departure, actual_arrival, aircraft_type, aircraft_registration, gate_number, flight_type, status, estimated_flight_time, actual_flight_time, distance, crew_requirements, minimum_crew_count, passenger_count, cargo_weight, fuel_required, priority_level, revenue, cost_per_delay_hour, weather_info, special_requirements, delay_probability, crew_utilization_score, disruption_impact, created_at, updated_at)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (flight_number) DO NOTHING;
                            ''', (
                                row["flight_number"], row.get("airline_code"), row.get("departure_airport"), row.get("arrival_airport"), row.get("scheduled_departure"), row.get("scheduled_arrival"), row.get("actual_departure"), row.get("actual_arrival"), row.get("aircraft_type"), row.get("aircraft_registration"), row.get("gate_number"), row.get("flight_type"), row.get("status"), row.get("estimated_flight_time"), row.get("actual_flight_time"), row.get("distance"), row.get("crew_requirements"), row.get("minimum_crew_count"), row.get("passenger_count"), row.get("cargo_weight"), row.get("fuel_required"), row.get("priority_level"), row.get("revenue"), row.get("cost_per_delay_hour"), row.get("weather_info"), row.get("special_requirements"), row.get("delay_probability"), row.get("crew_utilization_score"), row.get("disruption_impact"), row.get("created_at"), row.get("updated_at")
                            ))
                else:
                    logger.warning(f"CSV file not found: {flight_file}")

                # Insert Rosters
                roster_file = csv_dir / "rosters.csv"
                if roster_file.exists():
                    with open(roster_file, "r", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            cur.execute('''
                                INSERT INTO rosters (crew_id, flight_id, assignment_type, status, crew_position, duty_start, duty_end, report_time, release_time, assignment_confidence, optimization_score, constraint_violations, actual_duty_hours, crew_feedback_rating, assigned_by, assigned_at, updated_at)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (id) DO NOTHING;
                            ''', (
                                row.get("crew_id"), row.get("flight_id"), row.get("assignment_type"), row.get("status"), row.get("crew_position"), row.get("duty_start"), row.get("duty_end"), row.get("report_time"), row.get("release_time"), row.get("assignment_confidence"), row.get("optimization_score"), row.get("constraint_violations"), row.get("actual_duty_hours"), row.get("crew_feedback_rating"), row.get("assigned_by"), row.get("assigned_at"), row.get("updated_at")
                            ))
                else:
                    logger.warning(f"CSV file not found: {roster_file}")
                conn.commit()
        logger.info("CSV sample data inserted successfully")
    except Exception as e:
        logger.error(f"Failed to insert sample data: {str(e)}")



def drop_all_tables():
    """Drop all database tables - USE WITH CAUTION (psycopg)"""
    try:
        logger.warning("Dropping all database tables...")
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS rosters CASCADE;")
                cur.execute("DROP TABLE IF EXISTS flights CASCADE;")
                cur.execute("DROP TABLE IF EXISTS crew CASCADE;")
                conn.commit()
        logger.info("All tables dropped successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to drop tables: {str(e)}")
        return False


def main():
    """Main migration function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Database migration script")
    parser.add_argument("--create", action="store_true", help="Create tables")
    parser.add_argument("--drop", action="store_true", help="Drop all tables")
    parser.add_argument("--indexes", action="store_true", help="Create indexes")
    parser.add_argument("--sample-data", action="store_true", help="Insert sample data")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate all")
    
    args = parser.parse_args()
    
    if args.reset:
        print("Resetting database...")
        drop_all_tables()
        create_tables()
        create_indexes()
        insert_sample_data()
        print("Database reset complete")
        
    elif args.drop:
        confirm = input("Are you sure you want to drop all tables? (yes/no): ")
        if confirm.lower() == 'yes':
            drop_all_tables()
        else:
            print("Operation cancelled")
            
    elif args.create:
        create_tables()
        
    elif args.indexes:
        create_indexes()
        
    elif args.sample_data:
        insert_sample_data()
        
    else:
        print("No action specified. Use --help for options")


if __name__ == "__main__":
    main()
