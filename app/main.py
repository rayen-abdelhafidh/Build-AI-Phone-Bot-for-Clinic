from fastapi import FastAPI
from app import twilio_routes, ai_logic, booking, admin_dashboard
import sqlite3

app = FastAPI()
app.include_router(twilio_routes.router)
app.include_router(admin_dashboard.router)

# Database setup
def create_db():
    conn = sqlite3.connect("calls.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS departments (id INTEGER PRIMARY KEY, name TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS doctors (id INTEGER PRIMARY KEY, name TEXT, department_id INTEGER)")
    c.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY,
            client_name TEXT,
            phone TEXT,
            appointment_date TEXT,
            department_id INTEGER,
            doctor_id INTEGER,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Tables created.")

create_db()