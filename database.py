import psycopg2
import streamlit as st


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="air_pollution_db",
        user="postgres",
        password=st.secrets["db_password"]
    )


def save_traffic(vehicle_type_id, count, speed, distance):
    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO TrafficRecords (
                        vehicle_type_id,
                        user_id,
                        vehicle_count,
                        average_speed,
                        distance_km,
                        traffic_intensity,
                        record_date
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE)
                    RETURNING id
                    """,
                    (
                        vehicle_type_id,
                        2,
                        count,
                        speed,
                        distance,
                        "Середня"
                    )
                )

                record_id = cursor.fetchone()[0]

        return record_id

    finally:
        conn.close()
