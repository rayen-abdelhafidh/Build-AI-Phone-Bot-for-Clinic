# 🤖 AI Voice Assistant for Clinics

## 🩺 About

This project is an all-in-one **AI-powered phone assistant** and **admin dashboard** for clinics.  
It automates appointment booking via phone calls, manages doctors and departments, and provides a modern web dashboard for easy administration.

**✨ Key Features:**
- 📞 Receives and answers clinic calls using an AI voice assistant (Twilio + TTS)
- 📝 Books appointments by automating the clinic's web form (using Playwright)
- 🌐 **Automated booking is performed on:** [https://jtsmedicalcentre.com/appointments/](https://jtsmedicalcentre.com/appointments/)
- 🗂️ Admin dashboard to manage departments, doctors, and view booking history
- 🔑 Edit API keys (Twilio, OpenAI) from the dashboard
- 🚫 Prevents adding empty, whitespace, or numeric-only names for departments/doctors
- 🗃️ SQLite database for logs, bookings, doctors, and departments

---

## 🛠️ Tech Stack

- **FastAPI** (API & admin dashboard)
- **Jinja2** (dashboard templates)
- **Twilio Voice API**
- **OpenAI** (Whisper + ChatGPT, or Hugging Face/local models)
- **gTTS** / Polly / Google TTS
- **Playwright** (browser automation)
- **SQLite** (database)

---

## 🚀 How to Run

1. **Clone the repo**

2. **Create a `.env` file:**
   ```
   OPENAI_API_KEY=sk-xxx
   TWILIO_ACCOUNT_SID=ACxxx
   TWILIO_AUTH_TOKEN=xxx
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   playwright install
   ```

4. **Run FastAPI server:**
   ```
   uvicorn app.main:app --reload
   ```

5. **Expose with ngrok for Twilio webhook:**
   ```
   ngrok http 8000
   ```

6. **Configure Twilio webhook to point to `/twilio/voice`**

7. **Access the admin dashboard:**
   - Visit [http://localhost:8000/admin](http://localhost:8000/admin) to manage doctors, departments, API keys, and view bookings.

---

## 📝 Notes

- 🗄️ Your SQLite database (`calls.db`) is auto-created with the required tables: `departments`, `doctors`, `bookings`.
- 🚫 The dashboard prevents adding departments or doctors with empty, whitespace, or numeric-only names.
- 🧪 For local AI testing, you can mock AI responses or use open-source models.
- 🛠️ Update selectors in `booking.py` if the clinic website changes.
- ⚡ All add/delete actions in the dashboard use AJAX for a smooth experience.
- 🌐 **Automated booking is performed on:** [https://jtsmedicalcentre.com/appointments/](https://jtsmedicalcentre.com/appointments/)

---

## License

MIT
