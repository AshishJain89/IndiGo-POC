
"""Debug script to check what data was loaded into the database (psycopg version)"""
import sys
import os
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


def check_database_data():
    """Check what data is currently in the database using psycopg"""
    try:
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                # Crew
                cur.execute("SELECT COUNT(*) FROM crew;")
                crew_row = cur.fetchone()
                crew_count = crew_row[0] if crew_row else 0
                print(f"\U0001F4CA Crew members in database: {crew_count}")
                if crew_count > 0:
                    cur.execute("SELECT employee_id, first_name, last_name, rank, base_airport FROM crew LIMIT 5;")
                    print("\n\U0001F465 Sample crew members:")
                    for row in cur.fetchall():
                        print(f"  - {row[0]}: {row[1]} {row[2]} ({row[3]}) - {row[4]}")

                # Flights
                cur.execute("SELECT COUNT(*) FROM flights;")
                flights_row = cur.fetchone()
                flights_count = flights_row[0] if flights_row else 0
                print(f"\n\U0001F6EB Flights in database: {flights_count}")
                if flights_count > 0:
                    cur.execute("SELECT scheduled_departure FROM flights ORDER BY scheduled_departure ASC LIMIT 1;")
                    earliest = cur.fetchone()
                    cur.execute("SELECT scheduled_departure FROM flights ORDER BY scheduled_departure DESC LIMIT 1;")
                    latest = cur.fetchone()
                    if earliest and latest and earliest[0] and latest[0]:
                        print(f"   \U0001F4C5 Date range: {earliest[0].date()} to {latest[0].date()}")
                    cur.execute("SELECT flight_number, departure_airport, arrival_airport, scheduled_departure FROM flights LIMIT 5;")
                    print("\n\U0001F6EB Sample flights:")
                    for row in cur.fetchall():
                        print(f"  - {row[0]}: {row[1]} → {row[2]} on {row[3].date()}")

                # Rosters
                cur.execute("SELECT COUNT(*) FROM rosters;")
                rosters_row = cur.fetchone()
                rosters_count = rosters_row[0] if rosters_row else 0
                print(f"\n\U0001F4CB Roster entries in database: {rosters_count}")
                if rosters_count > 0:
                    cur.execute("SELECT crew_id, flight_id, crew_position, duty_start FROM rosters LIMIT 5;")
                    print("\n\U0001F4DD Sample roster entries:")
                    for row in cur.fetchall():
                        print(f"  - Crew {row[0]} → Flight {row[1]} ({row[2]}) on {row[3].date()}")
        return True
    except Exception as e:
        print(f"\u274C Error checking database: {e}")
        return False

def check_csv_files():
    """Check if CSV files exist and show their basic info"""
    print("\n\U0001F50D Checking CSV files...")
    
    csv_files = ['crew.csv', 'flights.csv', 'rosters.csv']
    csvs_dir = os.path.join(project_root, "data\\csvs")
    script_dir = Path(__file__).parent

    for csv_file in csv_files:
        csv_path = Path(os.path.join(csvs_dir, csv_file))
        print(csv_file)
        if csv_path.exists():
            try:
                with open(csv_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    print(f"✅ {csv_file}: {len(lines)-1} rows (excluding header)")
                    
                    # Show first data row
                    if len(lines) > 1:
                        headers = lines[0].strip().split(',')
                        first_row = lines[1].strip().split(',')
                        print(f"   Sample: {dict(zip(headers[:3], first_row[:3]))}")
            except Exception as e:
                print(f"\u274C Error reading {csv_file}: {e}")
        else:
            print(f"\u274C {csv_file}: File not found")


def check_flights_for_today():
    """Check if there are flights for today's date using psycopg"""
    try:
        today = datetime.now().date()
        print(f"\n\U0001F4C6 Checking for flights on {today}...")
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COUNT(*) FROM flights
                    WHERE scheduled_departure >= %s AND scheduled_departure < %s;
                """, (datetime.combine(today, datetime.min.time()), datetime.combine(today, datetime.max.time())))
                count_row = cur.fetchone()
                count = count_row[0] if count_row else 0
                print(f"   Found {count} flights for today")
                if count == 0:
                    cur.execute("SELECT scheduled_departure FROM flights ORDER BY scheduled_departure;")
                    all_dates = [row[0].date() for row in cur.fetchall() if row and row[0]]
                    if all_dates:
                        unique_dates = sorted(set(all_dates))
                        print(f"   Available flight dates: {unique_dates[:10]}...")
    except Exception as e:
        print(f"\u274C Error checking today's flights: {e}")

def main():
    print("\U0001F527 Database Debug Script")
    print("=" * 50)
    
    # Check CSV files first
    check_csv_files()
    
    print("\n" + "=" * 50)
    
    # Check database data
    if check_database_data():
        check_flights_for_today()
    
    print("\n" + "=" * 50)
    print("✅ Debug complete!")
    
    # Recommendations
    print("\n💡 Recommendations:")
    print("1. If CSV files are missing, run the data generator script first")
    print("2. If data counts are low, re-run: python create_tables.py --sample-data")
    print("3. If no flights for today, try the API with a different date range")
    print("4. Check the logs above for any specific errors")

if __name__ == "__main__":
    main()
