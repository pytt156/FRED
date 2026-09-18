import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")


def get_connection():
    return psycopg.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )


def save_telemetry(
    time,
    device_id,
    source,
    temperature=None,
    humidity=None,
    light=None,
    motion=None,
    wifi_connected=None,
    rssi=None,
):
    query = """
        INSERT INTO telemetry(
        time, device_id, source, temperature, humidity, light, motion, wifi_connected, rssi)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    values = (
        time,
        device_id,
        source,
        temperature,
        humidity,
        light,
        motion,
        wifi_connected,
        rssi,
    )

    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(query, values)

    print("Telemetry saved to TimescaleDB")
