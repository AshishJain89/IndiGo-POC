# PostgreSQL connection utility using psycopg
import os
import psycopg
from contextlib import asynccontextmanager

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "crewdb")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")

DSN = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASS}"

@asynccontextmanager
async def get_db_conn():
    async with await psycopg.AsyncConnection.connect(DSN) as conn:
        yield conn
