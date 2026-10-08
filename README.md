# 🏥 City Hospital — AI Appointment Agent

> **Voice-first AI hospital receptionist for intelligent appointment booking.**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![gTTS](https://img.shields.io/badge/gTTS-Voice-8E44AD?style=for-the-badge)
![ReportLab](https://img.shields.io/badge/ReportLab-PDF-CC0000?style=for-the-badge)

---

# ✨ Overview

**City Hospital AI Appointment Agent** is a voice-first AI receptionist built with **Python, FastAPI, Groq, SQLite, gTTS, ReportLab, and Gmail SMTP**.

The application allows a patient to enter their basic details, start a voice conversation with **Sarah**, the AI receptionist, and complete an appointment workflow naturally.

The agent can:

- 👨‍⚕️ List hospital doctors
- 🗓️ Check appointment availability
- ✅ Book appointments
- 🔒 Prevent duplicate doctor/time bookings
- 🎫 Generate a PDF appointment ticket
- 📧 Automatically email the confirmation ticket
- 🔊 Convert AI responses into speech
- 🌐 Support English, Hindi, and Telugu
- 🧠 Maintain session-based conversation context
- ⏱️ Automatically end the call after successful booking

> **Note:** This README describes the current **Groq-powered** implementation. Earlier Gemini-based versions are not part of the current architecture.

---
# 🖥️ User Interface Preview

### 🏠 Home Page

![Home Page](https://github.com/user-attachments/assets/a6fa58ad-d08a-4067-8777-68712cb7401d)

### 🎙️ Voice Call

![Voice Call](https://github.com/user-attachments/assets/2db022b1-fc98-403e-85b5-a18a7426f933)

### ✅ Appointment Booked

![Appointment Booked](https://github.com/user-attachments/assets/b6a221b0-9d4d-4037-8346-bfc8972ba0cb)

### 📄 PDF Download

![PDF Download](https://github.com/user-attachments/assets/0fbc0af6-6942-4f87-8f2a-093ee59659b5)

---

The interface is designed as a clean, modern hospital voice-assistant experience with patient details, language selection, AI voice-call status, appointment confirmation, and PDF ticket download.

# 🎯 How It Works

```text
                    ┌─────────────────────┐
                    │       Patient       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   City Hospital UI  │
                    │    frontend.html    │
                    └──────────┬──────────┘
                               │
                         Voice / JSON
                               │
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI API     │
                    │       app.py        │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
                 ▼             ▼             ▼
             ┌───────┐    ┌─────────┐   ┌─────────┐
             │ Groq  │    │ SQLite  │   │  gTTS   │
             │  LLM  │    │   DB    │   │  Audio  │
             └───┬───┘    └────┬────┘   └────┬────┘
                 │             │             │
                 └─────────────┼─────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Appointment Ticket │
                    │       ReportLab     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Gmail SMTP Email  │
                    │  Patient Confirmation│
                    └─────────────────────┘
```

---

# 🚀 Core Features

| Feature | Description |
|---|---|
| 🤖 **AI Receptionist** | Sarah handles appointment conversations naturally |
| ⚡ **Groq LLM** | Fast AI inference through Groq |
| 🎙️ **Voice-first UI** | Designed around a voice-call experience |
| 🌐 **Multilingual** | English, Hindi, and Telugu |
| 👨‍⚕️ **Doctor Listing** | Retrieves doctors from SQLite |
| 🕐 **Availability Check** | Checks the requested appointment slot |
| 🔐 **Duplicate Protection** | Prevents duplicate doctor/time bookings |
| 🎫 **PDF Ticket** | Generates a downloadable appointment ticket |
| 📧 **Email Automation** | Sends the ticket to the patient's email |
| 🔊 **Text-to-Speech** | Converts AI responses into MP3 audio |
| 🧠 **Session Memory** | Maintains conversation context |
| ⏱️ **Automatic Call End** | Ends the voice session after successful booking |
| 🔒 **Environment Secrets** | API credentials remain outside source code |

---

# 🖥️ User Interface

The application uses a modern, minimal hospital-style interface.

### 🏠 Patient Home Screen

The patient provides:

- Patient name
- Email address
- Preferred language

Then selects:

> **🎙 Start Voice Call**

### 🎙️ AI Voice Screen

The interface presents:

- Animated AI assistant ring
- Sarah — AI Receptionist
- Connection/listening/speaking status
- Call timer
- Voice-call controls
- Appointment confirmation section

### 🎫 Appointment Confirmation

After successful booking, the UI displays:

- Appointment ID
- Doctor
- Specialty
- Appointment time
- Email delivery status
- PDF download option

---


#

# 🧰 Technology Stack

### Backend

- **Python**
- **FastAPI**
- **Uvicorn**
- **Pydantic**
- **SQLite**
- **python-dotenv**

### AI

- **Groq API**
- **Groq Python SDK**
- **`openai/gpt-oss-120b`**

### Voice

- **gTTS**
- Base64 encoded MP3 responses
- Browser audio playback

### PDF

- **ReportLab**

### Email

- Python `smtplib`
- Gmail SMTP
- Google App Password

### Frontend

- HTML5
- JavaScript
- Tailwind CSS
- Font Awesome

---

# 📁 Project Structure

```text
AI-Hospital-Appointment-Agent/
│
├── app.py
├── frontend.html
├── .env
├── .gitignore
├── requirements.txt
├── README.md
│
├── appointments_poc.db
│
├── tickets/
│   └── CH-000001.pdf
│
└── docs/
    └── ui-preview.svg
```

### Runtime files

The following are generated or used at runtime:

```text
appointments_poc.db
tickets/
```

For GitHub, it is recommended to ignore these unless you intentionally want to distribute sample data.

---

# ⚙️ Prerequisites

Install:

- Python **3.10+**
- pip
- Git
- A Groq account
- A Google account
- Gmail with **2-Step Verification**
- A Gmail App Password

Python **3.11 or 3.12** is recommended for local development.

---

# 1️⃣ Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
cd AI-Hospital-Appointment-Agent
```

If the project already exists locally:

```bash
cd AI-Hospital-Appointment-Agent
```

---

# 2️⃣ Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 3️⃣ Install Dependencies

Create `requirements.txt`:

```txt
fastapi
uvicorn
python-dotenv
groq
gTTS
reportlab
pydantic
```

Install:

```bash
pip install -r requirements.txt
```

---

# 🔑 4️⃣ Configure Groq API

The AI receptionist uses Groq as the primary LLM provider.

### Step 1 — Create a Groq account

Open:

https://console.groq.com/

### Step 2 — Open API Keys

https://console.groq.com/keys

### Step 3 — Create an API key

Create a key such as:

```text
city-hospital-agent
```

Copy the generated API key.

### Step 4 — Add it to `.env`

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

### 🔐 Important

Never place the API key directly inside:

```text
app.py
frontend.html
GitHub
README.md
```

---

# 📧 5️⃣ Configure Gmail SMTP

The application automatically sends the appointment PDF to the **patient email entered on the Home Page**.

The hospital email remains the fixed sender.

```text
supportcityhospital@gmail.com
          │
          │ Gmail SMTP
          ▼
patient@example.com
```

SMTP configuration:

```text
SMTP Host : smtp.gmail.com
Port      : 587
Security  : STARTTLS
```

---

# 🔐 6️⃣ Create a Google App Password

Do **not** use your normal Gmail password.

### Step 1 — Enable 2-Step Verification

Open:

https://myaccount.google.com/security

Enable:

```text
2-Step Verification
```

### Step 2 — Open App Passwords

Open:

https://myaccount.google.com/apppasswords

### Step 3 — Generate an App Password

Create an App Password for the application.

Google will generate a 16-character password.

Example format:

```text
abcd efgh ijkl mnop
```

Use that value as `EMAIL_PASSWORD`.

> ⚠️ Never share your App Password publicly.

---

# 🧾 7️⃣ Create `.env`

Create:

```text
.env
```

in the same folder as `app.py`.

Example:

```env
# ==============================
# GROQ
# ==============================

GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b


# ==============================
# GMAIL SMTP
# ==============================

EMAIL_USER=supportcityhospital@gmail.com
EMAIL_PASSWORD=your_google_app_password_here
```

### Credential flow

```text
GROQ_API_KEY
     │
     ▼
   Groq LLM

EMAIL_USER + EMAIL_PASSWORD
     │
     ▼
 Gmail SMTP
     │
     ▼
 Patient Email
```

The patient's email does **not** belong in `.env`.

It is supplied from the Home Page during the appointment session.

---

# 🛡️ 8️⃣ Protect Secrets with `.gitignore`

If you plan to upload this project to **GitHub, GitLab, or another public repository, create and configure `.gitignore` before your first commit**.

Create a file named:

```text
.gitignore
```

Add:

```gitignore
# Environment
.env

# Python
__pycache__/
*.py[cod]
*.pyo

# Virtual environment
venv/
.venv/

# Database
*.db
*.sqlite
*.sqlite3

# Generated tickets
tickets/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

## 🚨 Before uploading to GitHub

Make sure these files are **not committed**:

```text
.env
appointments_poc.db
tickets/
venv/
__pycache__/
```

Your `.env` contains sensitive credentials such as:

```text
GROQ_API_KEY
EMAIL_PASSWORD
```

Never upload these values to GitHub.

### If you have not committed anything yet

Use:

```bash
git add .
git status
```

Check the output carefully before committing.

Then:

```bash
git commit -m "Initial project setup"
git push
```

### If `.env` was already tracked by Git

Adding `.env` to `.gitignore` does not remove an already-tracked file.

Run:

```bash
git rm --cached .env
git add .gitignore
git commit -m "Remove environment secrets from repository"
git push
```

> **Important:** If a real API key or App Password has already been pushed to GitHub, immediately revoke/rotate that credential. Do not rely only on deleting the file from the latest commit.

# Environment
.env

# Python
__pycache__/
*.py[cod]
*.pyo

# Virtual environment
venv/
.venv/

# Database
*.db
*.sqlite
*.sqlite3

# Generated tickets
tickets/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

### Never commit

```text
.env
```

to GitHub.

---

# 🗄️ Database

The project uses SQLite:

```text
appointments_poc.db
```

The database stores doctor and appointment information.

Current example doctors:

| Doctor | Specialty |
|---|---|
| Dr. Meera Patel | Cardiology |
| Dr. Arjun Rao | Neurology |

The database can later be extended with:

- Doctor schedules
- Working hours
- Doctor leave
- Departments
- Appointment status
- Hospital branches
- Consultation information

---

# 🤖 AI Appointment Workflow

The AI does not simply invent appointment availability.

The intended workflow is:

```text
Patient Request
      │
      ▼
Identify Doctor + Date + Time
      │
      ▼
Check Slot
      │
 ┌────┴────┐
 │         │
 ▼         ▼
Available  Busy
 │         │
 ▼         ▼
Book       Suggest Another Slot
 │
 ▼
Generate Appointment ID
 │
 ▼
Generate PDF
 │
 ▼
Send Email
 │
 ▼
Confirm Appointment
 │
 ▼
Close Voice Call
```

This makes the LLM an **agent connected to real backend actions**, rather than a simple text chatbot.

---

# 🧠 Agent Tools

The backend provides appointment-related tools to the AI.

### `list_doctors`

Returns doctors stored in the hospital database.

### `check_slot`

Checks whether a requested doctor/time is available.

### `book_appointment`

Creates the appointment after required information and availability have been validated.

Conceptually:

```text
                 ┌─────────────┐
                 │    Groq     │
                 │     LLM     │
                 └──────┬──────┘
                        │
              ┌─────────┼─────────┐
              ▼         ▼         ▼
       list_doctors  check_slot  book_appointment
              │         │         │
              └─────────┼─────────┘
                        ▼
                  SQLite Database
```

---

# 🎫 PDF Appointment Ticket

After successful booking, ReportLab generates a PDF ticket.

Example:

```text
CH-000001.pdf
```

The ticket contains information such as:

```text
CITY HOSPITAL

Appointment Confirmed

Appointment ID : CH-000001
Patient        : John Doe
Doctor         : Dr. Meera Patel
Specialty      : Cardiology
Appointment    : 2026-10-10 11:00

Status         : CONFIRMED
```

The frontend displays the ticket and provides a download option.

---

# 📩 Automatic Email Confirmation

After the appointment is successfully created:

```text
Appointment Created
        │
        ▼
Generate PDF Ticket
        │
        ▼
Attach PDF
        │
        ▼
Gmail SMTP
        │
        ▼
Patient Email
```

The backend returns an email status:

```json
{
  "email_sent": true
}
```

If email delivery fails, the appointment database record is not automatically undone.

This prevents an email-service failure from silently losing a valid appointment.

---

# 🔊 Voice Processing

The voice-response pipeline is:

```text
Patient
   │
   ▼
Browser Voice Interaction
   │
   ▼
FastAPI
   │
   ▼
Groq
   │
   ▼
AI Response
   │
   ▼
gTTS
   │
   ▼
Base64 MP3
   │
   ▼
Browser Audio
```

The interface is intentionally designed around a **voice receptionist experience** instead of a conventional chat window.

---

# 🌐 Supported Languages

| Language | Code |
|---|---|
| 🇮🇳 English | `en-IN` |
| 🇮🇳 Hindi | `hi-IN` |
| 🇮🇳 Telugu | `te-IN` |

The selected language is passed to the backend with each agent request.

---

# 🔌 API Endpoints

## `GET /`

Loads the main hospital interface.

```http
GET /
```

Returns:

```text
frontend.html
```

---

## `POST /agent/new_session`

Creates a new AI session.

Example response:

```json
{
  "session_id": "example-session-id",
  "greeting": "Good evening. Welcome to City Hospital...",
  "audio": "BASE64_AUDIO_DATA"
}
```

---

## `POST /agent/message`

Sends a patient message to the AI agent.

Example:

```json
{
  "session_id": "example-session-id",
  "text": "I want to book a cardiology appointment tomorrow at 11 AM",
  "language_code": "en-IN",
  "patient_name": "John Doe",
  "patient_email": "john@example.com"
}
```

A successful booking can return:

```json
{
  "auto_end": true,
  "voice_text": "Your appointment has been confirmed.",
  "audio": "BASE64_AUDIO_DATA",
  "ticket": {
    "email_sent": true,
    "appointment_code": "CH-000001",
    "doctor_name": "Dr. Meera Patel",
    "specialty": "Cardiology",
    "appointment_time": "2026-10-10 11:00",
    "download_url": "/tickets/CH-000001.pdf"
  },
  "closing_text": "Thank you for choosing City Hospital.",
  "closing_audio": "BASE64_AUDIO_DATA"
}
```

---

## `GET /tickets/{filename}`

Downloads a generated appointment ticket.

Example:

```http
GET /tickets/CH-000001.pdf
```

---

# ▶️ Run the Application

Activate the virtual environment first.

### Direct Python

```bash
python app.py
```

### Uvicorn

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

### Development mode

```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

---

# 🌐 Open the Application

Visit:

```text
http://127.0.0.1:8000
```

You should see:

```text
🏥 City Hospital
AI Appointment Assistant
```

Enter:

```text
Patient Name
Email Address
Language
```

Then click:

```text
🎙 Start Voice Call
```

---

# 🧪 End-to-End Test

### 1. Start the voice call

Expected:

```text
Sarah greets the patient.
```

### 2. Ask about doctors

Example:

```text
Which doctors are available?
```

### 3. Ask about availability

Example:

```text
Is Dr. Meera Patel available tomorrow at 11 AM?
```

The backend checks the database.

### 4. Confirm the booking

Example:

```text
Book that appointment for me.
```

The system:

```text
Checks availability
       ↓
Creates appointment
       ↓
Generates PDF
       ↓
Sends email
       ↓
Shows ticket
       ↓
Ends call
```

### 5. Verify the email

Check the patient's inbox for:

```text
Appointment confirmation
+
PDF ticket attachment
```

---

# 💬 Example Conversation

```text
Sarah:
Good evening. Welcome to City Hospital.
I am Sarah, your AI receptionist.
How may I help you with your appointment today?

Patient:
I want to see a cardiologist.

Sarah:
We have Dr. Meera Patel in Cardiology.
What date and time would you prefer?

Patient:
Tomorrow at 11 AM.

Sarah:
Let me check that appointment time.

[Database availability check]

Sarah:
That slot is available. May I book it for you?

Patient:
Yes.

[Appointment created]
[PDF generated]
[Email sent]

Sarah:
Your appointment is confirmed.
Your appointment ID is CH-000001.
The confirmation ticket has been sent to your email.

Thank you for choosing City Hospital.
```

---

# 🔒 Security

### Keep API keys server-side

Never expose:

```text
GROQ_API_KEY
EMAIL_PASSWORD
```

inside frontend JavaScript.

The architecture should remain:

```text
Browser
   │
   │ No secret keys
   ▼
FastAPI
   │
   ├── Groq API
   └── Gmail SMTP
```

### Use Google App Password

Never use the normal Gmail account password for SMTP.

### If a credential is exposed

Immediately:

1. Revoke the credential.
2. Generate a new credential.
3. Update `.env`.
4. Remove exposed secrets from Git history if necessary.

---

# 🐛 Troubleshooting

## Groq API error

Check:

```env
GROQ_API_KEY=your_key
```

Make sure `.env` is next to `app.py`.

Restart the server after changing `.env`.

---

## Gmail authentication error

Check:

```env
EMAIL_USER=supportcityhospital@gmail.com
EMAIL_PASSWORD=your_app_password
```

Confirm:

- 2-Step Verification is enabled
- App Password exists
- App Password has not been revoked
- No accidental spaces were added

---

## SMTP connection error

Current configuration:

```text
smtp.gmail.com
587
STARTTLS
```

---

## PDF ticket not found

Make sure the generated ticket exists inside:

```text
tickets/
```

Example:

```text
tickets/
└── CH-000001.pdf
```

---

## Port already in use

Run:

```bash
uvicorn app:app --host 127.0.0.1 --port 8001
```

Then open:

```text
http://127.0.0.1:8001
```

---

## gTTS error

Check:

- Internet connection
- gTTS installation
- Supported language code
- Application console logs

---

# ☁️ Deployment Notes

This project is suitable as a **portfolio project, prototype, or proof of concept**.

Before real hospital deployment, consider adding:

- HTTPS
- Authentication
- Role-based access control
- PostgreSQL or another production database
- Secure cloud secret management
- Production logging
- Monitoring
- Audit trails
- Data retention controls
- Encryption
- Healthcare/privacy compliance

Do not use real patient medical information with this prototype unless the required security, privacy, and compliance controls are in place.

---

# 👨‍💻 Skills Demonstrated

```text
Python
FastAPI
REST API Development
Groq API
LLM Integration
AI Agents
Tool Calling
Prompt Engineering
SQLite
Database Operations
gTTS
Voice Interfaces
ReportLab
PDF Generation
SMTP
Email Automation
HTML
JavaScript
Tailwind CSS
Session Management
Environment Variables
API Security
```

---

# 📚 Official Documentation

- Groq: https://console.groq.com/
- Groq API Keys: https://console.groq.com/keys
- Groq Quickstart: https://console.groq.com/docs/quickstart
- FastAPI: https://fastapi.tiangolo.com/
- Google Security: https://myaccount.google.com/security
- Google App Passwords: https://myaccount.google.com/apppasswords

---

#

---

**Built with ❤️ using Python, FastAPI, Groq, SQLite, gTTS, ReportLab and modern web technologies.**
