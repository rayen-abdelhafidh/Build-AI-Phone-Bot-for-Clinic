from gtts import gTTS
from fastapi.requests import Request
from rapidfuzz import process
from app.booking import DOCTOR_LIST, DEPARTMENT_LIST, book_appointment

def match_name(input_name, name_list):
    match, score, _ = process.extractOne(input_name, name_list)
    if score > 80:
        return match
    else:
        return None

async def process_voice(request: Request):
    # Initial greeting with 2-second pause
    greeting = "Hello sir, I am here to help you for booking. Please say if you are an old client or new, then give your phone number, birthday date, appointment date, department, and doctor name."
    tts = gTTS(greeting)
    mp3_path = "static/greeting.mp3"
    tts.save(mp3_path)
    return await request.url_for("static", path="greeting.mp3")

async def handle_ai_booking(ai_data, request: Request):
    """
    ai_data: dict with keys: doctor, department, etc.
    Returns a reply audio URL for Twilio to play.
    """
    # Match department
    department_name = ai_data.get('department', '')
    matched_department = match_name(department_name, DEPARTMENT_LIST)
    if not matched_department:
        reply = "The department is not recognized. Please say the department name again."
        tts = gTTS(reply)
        mp3_path = "static/reply.mp3"
        tts.save(mp3_path)
        return await request.url_for("static", path="reply.mp3")
    ai_data['department'] = matched_department

    # Match doctor
    doctor_name = ai_data.get('doctor', '')
    matched_doctor = match_name(doctor_name, DOCTOR_LIST)
    if not matched_doctor:
        reply = "The doctor is not recognized. Please say the name of the doctor again."
        tts = gTTS(reply)
        mp3_path = "static/reply.mp3"
        tts.save(mp3_path)
        return await request.url_for("static", path="reply.mp3")
    ai_data['doctor'] = matched_doctor

    # Continue with booking
    book_appointment(ai_data)
    reply = f"Your appointment with {matched_doctor} in {matched_department} is being booked."
    tts = gTTS(reply)
    mp3_path = "static/reply.mp3"
    tts.save(mp3_path)
    return await request.url_for("static", path="reply.mp3")