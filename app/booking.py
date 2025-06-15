import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

BOOKING_URL = os.getenv("BOOKING_URL", "https://jtsmedicalcentre.com/appointments/")

DOCTOR_LIST = [
    "Dr. John Smith",
    "Dr. Jane Doe",
    "Dr. Ahmed Ali",
    # ...add all available doctors here
]

DEPARTMENT_LIST = [
    "Cardiology",
    "Dermatology",
    "Pediatrics",
    # ...add all available departments here
]

def is_valid_doctor(doctor_name):
    return doctor_name in DOCTOR_LIST

def is_valid_department(department_name):
    return department_name in DEPARTMENT_LIST

def book_appointment(data):
    patient_type = data.get('patient_type', 'new').lower()  # 'new' or 'existing'
    name = data.get('name', '')
    email = data.get('email', '')
    phone = data.get('phone', '')
    doctor = data.get('doctor', '')
    department = data.get('department', '')
    dob = data.get('dob', '')  # Date of birth, format: YYYY-MM-DD
    appointment_date = data.get('appointment_date', '')  # Format: YYYY-MM-DD
    message = data.get('message', '')

    if not is_valid_doctor(doctor):
        print(f"Doctor '{doctor}' is not in the list of available doctors.")
        return

    if not is_valid_department(department):
        print(f"Department '{department}' is not in the list of available departments.")
        return

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(BOOKING_URL, timeout=20000)

            # Step 1: Choose patient type
            if patient_type == 'existing':
                page.click("label#old")
                page.click("button.next-step")
                # Step 2: Registration Detail
                page.fill('input[name="your-phone"]', phone)
                page.fill('input[name="your-dob"]', dob)
                page.click("button.next-step")
                # Step 3: Select Doctor & Time Slots
                page.select_option('select[name="doctor_department"]', department)
                page.select_option('select[name="doctor_name"]', doctor)
                page.fill('input[name="booking-date"]', appointment_date)
                # Optionally: page.click("button#get-time-slots") and select a slot
                page.click("button.next-step")
                # Step 4: About Patient (Name, Email, Message)
                page.fill('input[name="your-name"]', name)
                page.fill('input[name="your-email"]', email)
                page.fill('textarea[name="your-message"]', message)
                page.click("button:has-text('Book Appointment')")
            else:
                # New Patient Flow (template, update selectors as needed)
                page.click("label#new")
                page.click("button.next-step")
                # Step 2: Wait for and fill name/email/phone (update selectors)
                page.wait_for_selector("input[name='your-name']", timeout=20000)
                page.fill("input[name='your-name']", name)
                page.fill("input[name='your-email']", email)
                page.fill("input[name='your-phone']", phone)
                # Step 3: Select department/service/doctor if required (update selectors)
                # Example:
                # page.select_option("select#department", department)
                # page.select_option("select#service", data.get('service', ''))
                # page.select_option("select#doctor", doctor)
                # Step 4: Select date/time if required (update selectors)
                # Example:
                # page.fill("input[name='booking-date']", appointment_date)
                # Step 5: Submit the form (update selector)
                # page.click("button[type=submit]")

            print("Booking completed (form filled, not submitted for safety).")
            browser.close()
    except PlaywrightTimeoutError:
        print("Timeout while loading the booking page.")
    except Exception as e:
        print(f"Error during booking: {e}")