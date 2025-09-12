# PostgreSQL connection utility using psycopg
import os, psycopg
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ["POSTGRES_HOST"]
DB_PORT = os.environ["POSTGRES_PORT"]
DB_NAME = os.environ["POSTGRES_DB"]
DB_USER = os.environ["POSTGRES_USER"]
DB_PASS = os.environ["POSTGRES_PASSWORD"]

DSN = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASS}"

async def get_db_conn():
    conn = await psycopg.AsyncConnection.connect(DSN)
    try:
        yield conn
    finally:
        await conn.close()
