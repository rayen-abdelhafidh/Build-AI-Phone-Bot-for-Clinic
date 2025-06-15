from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3
import os
import re

router = APIRouter()
templates = Jinja2Templates(directory="templates")

SETTINGS_PATH = "settings.env"

def load_settings():
    settings = {
        "TWILIO_ACCOUNT_SID": os.getenv("TWILIO_ACCOUNT_SID", ""),
        "TWILIO_AUTH_TOKEN": os.getenv("TWILIO_AUTH_TOKEN", ""),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "")
    }
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    settings[k] = v
    return settings

def save_settings(settings):
    with open(SETTINGS_PATH, "w") as f:
        for k, v in settings.items():
            f.write(f"{k}={v}\n")

@router.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    conn = sqlite3.connect("calls.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    departments = [dict(row) for row in c.execute("SELECT id, name FROM departments").fetchall()]
    doctors = [dict(row) for row in c.execute("SELECT id, name, department_id FROM doctors").fetchall()]
    bookings = c.execute("""
        SELECT b.id, b.client_name, b.phone, b.appointment_date, d.name, doc.name
        FROM bookings b
        JOIN departments d ON b.department_id = d.id
        JOIN doctors doc ON b.doctor_id = doc.id
        ORDER BY b.created_at DESC
    """).fetchall()
    conn.close()
    settings = load_settings()
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "departments": departments,
        "doctors": doctors,
        "bookings": bookings,
        "settings": settings
    })

@router.post("/admin/update_settings")
def update_settings(
    request: Request,
    twilio_account_sid: str = Form(...),
    twilio_auth_token: str = Form(...),
    openai_api_key: str = Form(...)
):
    settings = {
        "TWILIO_ACCOUNT_SID": twilio_account_sid,
        "TWILIO_AUTH_TOKEN": twilio_auth_token,
        "OPENAI_API_KEY": openai_api_key
    }
    save_settings(settings)
    os.environ["TWILIO_ACCOUNT_SID"] = twilio_account_sid
    os.environ["TWILIO_AUTH_TOKEN"] = twilio_auth_token
    os.environ["OPENAI_API_KEY"] = openai_api_key
    return RedirectResponse("/admin", status_code=303)

@router.post("/admin/add_department")
def add_department(request: Request, name: str = Form(...)):
    name = name.strip()
    # Must not be empty, not only spaces, not only numbers, and must contain at least one letter
    if not name or not re.search(r'[A-Za-z]', name):
        return RedirectResponse("/admin", status_code=303)
    conn = sqlite3.connect("calls.db")
    c = conn.cursor()
    c.execute("INSERT INTO departments (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    return RedirectResponse("/admin", status_code=303)

@router.post("/admin/delete_department/{dept_id}")
def delete_department(request: Request, dept_id: int):
    conn = sqlite3.connect("calls.db")
    c = conn.cursor()
    c.execute("DELETE FROM departments WHERE id = ?", (dept_id,))
    c.execute("DELETE FROM doctors WHERE department_id = ?", (dept_id,))
    conn.commit()
    conn.close()
    return RedirectResponse("/admin", status_code=303)

@router.post("/admin/add_doctor")
def add_doctor(request: Request, name: str = Form(...), department_id: int = Form(...)):
    name = name.strip()
    # Must not be empty, not only spaces, not only numbers, and must contain at least one letter
    if not name or not re.search(r'[A-Za-z]', name):
        return RedirectResponse("/admin", status_code=303)
    conn = sqlite3.connect("calls.db")
    c = conn.cursor()
    c.execute("INSERT INTO doctors (name, department_id) VALUES (?, ?)", (name, department_id))
    conn.commit()
    conn.close()
    return RedirectResponse("/admin", status_code=303)

@router.post("/admin/delete_doctor/{doctor_id}")
def delete_doctor(request: Request, doctor_id: int):
    conn = sqlite3.connect("calls.db")
    c = conn.cursor()
    c.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
    conn.commit()
    conn.close()
    return RedirectResponse("/admin", status_code=303)

