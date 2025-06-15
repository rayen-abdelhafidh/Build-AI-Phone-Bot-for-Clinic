import sqlite3

def log_call(transcript, response):
    try:
        conn = sqlite3.connect("calls.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, transcript TEXT, response TEXT)")
        c.execute("INSERT INTO logs (transcript, response) VALUES (?, ?)", (transcript, response))
        conn.commit()
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def fetch_bookings():
    """
    Fetch all bookings from the bookings table.
    Assumes a table 'bookings' with columns: patient_type, name, email, phone
    """
    bookings = []
    try:
        conn = sqlite3.connect("calls.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY, patient_type TEXT, name TEXT, email TEXT, phone TEXT)")
        for row in c.execute("SELECT patient_type, name, email, phone FROM bookings"):
            bookings.append({
                "patient_type": row[0],
                "name": row[1],
                "email": row[2],
                "phone": row[3]
            })
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        conn.close()
    return bookings