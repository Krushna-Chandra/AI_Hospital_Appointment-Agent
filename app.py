import os
import io
import re
import json
import uuid
import base64
import sqlite3
import asyncio
import smtplib
from datetime import datetime
from email.message import EmailMessage
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gtts import gTTS
from groq import Groq
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
load_dotenv()
MODEL_NAME = os.environ.get('GROQ_MODEL', 'openai/gpt-oss-120b')
DB_NAME = 'appointments_poc.db'
TICKET_DIR = 'tickets'
os.makedirs(TICKET_DIR, exist_ok=True)
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
app = FastAPI(title='AI Hospital Receptionist System', version='2.0')
GROQ_CLIENT = None

# -------------------- Groq --------------------
def get_groq_client():
    global GROQ_CLIENT
    if GROQ_CLIENT is None:
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            raise RuntimeError('GROQ_API_KEY is not configured in .env')
        GROQ_CLIENT = Groq(api_key=api_key)
    return GROQ_CLIENT

# -------------------- Database --------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('\n\n        CREATE TABLE IF NOT EXISTS doctors (\n\n            id INTEGER PRIMARY KEY,\n\n            name TEXT NOT NULL UNIQUE,\n\n            specialty TEXT\n\n        )\n\n        ')
    cursor.execute('\n\n        CREATE TABLE IF NOT EXISTS appointments (\n\n            id INTEGER PRIMARY KEY,\n\n            patient_name TEXT,\n\n            doctor_name TEXT,\n\n            appointment_time TIMESTAMP,\n\n            patient_email TEXT,\n\n            status TEXT,\n\n            UNIQUE(doctor_name, appointment_time)\n\n        )\n\n        ')
    doctors = [('Dr. Meera Patel', 'Cardiology'), ('Dr. Arjun Rao', 'Neurology')]
    for name, specialty in doctors:
        cursor.execute('\n\n            INSERT OR IGNORE INTO doctors\n\n            (name, specialty)\n\n            VALUES (?, ?)\n\n            ', (name, specialty))
    conn.commit()
    conn.close()
init_db()

def get_doctor_details(doctor_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('\n\n        SELECT name, specialty\n\n        FROM doctors\n\n        WHERE LOWER(name) = LOWER(?)\n\n        ', (doctor_name,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {'name': row[0], 'specialty': row[1]}

def list_doctors_tool():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('\n\n        SELECT name, specialty\n\n        FROM doctors\n\n        ORDER BY name\n\n        ')
    rows = cursor.fetchall()
    conn.close()
    doctors = [{'name': row[0], 'specialty': row[1]} for row in rows]
    return {'status': 'success', 'doctors': doctors}

def check_slot_tool(doctor_name: str, appointment_time: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("\n\n        SELECT id\n\n        FROM appointments\n\n        WHERE LOWER(doctor_name) = LOWER(?)\n\n        AND appointment_time = ?\n\n        AND status = 'CONFIRMED'\n\n        ", (doctor_name, appointment_time))
    booked = cursor.fetchone()
    conn.close()
    if booked:
        return {'status': 'booked', 'message': 'The doctor is already booked for this time.'}
    return {'status': 'available', 'message': 'The appointment slot is available.'}

# -------------------- PDF ticket --------------------
def generate_appointment_pdf(appointment_id, patient_name, patient_email, doctor_name, specialty, appointment_time):
    appointment_code = f'CH-{int(appointment_id):06d}'
    filename = f'{appointment_code}.pdf'
    filepath = os.path.join(TICKET_DIR, filename)
    pdf_buffer = io.BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4
    pdf.setFont('Helvetica-Bold', 24)
    pdf.drawCentredString(width / 2, height - 35 * mm, 'CITY HOSPITAL')
    pdf.setFont('Helvetica', 12)
    pdf.drawCentredString(width / 2, height - 44 * mm, 'AI Appointment Confirmation')
    pdf.line(25 * mm, height - 50 * mm, width - 25 * mm, height - 50 * mm)
    y = height - 70 * mm
    pdf.setFont('Helvetica-Bold', 14)
    pdf.drawString(30 * mm, y, f'Appointment ID: {appointment_code}')
    y -= 15 * mm
    details = [('Patient Name', patient_name), ('Patient Email', patient_email), ('Doctor', doctor_name), ('Specialty', specialty), ('Appointment Time', appointment_time), ('Status', 'CONFIRMED')]
    for label, value in details:
        pdf.setFont('Helvetica-Bold', 11)
        pdf.drawString(30 * mm, y, f'{label}:')
        pdf.setFont('Helvetica', 11)
        pdf.drawString(75 * mm, y, str(value))
        y -= 12 * mm
    y -= 10 * mm
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(30 * mm, y, 'Please arrive a little before your appointment time.')
    y -= 20 * mm
    pdf.setFont('Helvetica', 10)
    pdf.drawString(30 * mm, y, 'Thank you for choosing City Hospital.')
    pdf.save()
    pdf_buffer.seek(0)
    pdf_bytes = pdf_buffer.getvalue()
    with open(filepath, 'wb') as file:
        file.write(pdf_bytes)
    return {'appointment_code': appointment_code, 'filename': filename, 'filepath': filepath, 'pdf_bytes': pdf_bytes}

# -------------------- Email --------------------
def send_booking_confirmation_email(patient_email, patient_name, doctor_name, specialty, appointment_time, appointment_code, pdf_bytes):
    try:
        sender_email = os.environ.get('EMAIL_USER')
        sender_password = os.environ.get('EMAIL_PASSWORD')
        if not sender_email:
            print('❌ EMAIL_USER missing')
            return False
        if not sender_password:
            print('❌ EMAIL_PASSWORD missing')
            return False
        if not patient_email:
            print('❌ Patient email missing')
            return False
        message = EmailMessage()
        message['Subject'] = f'City Hospital Appointment Confirmation - {appointment_code}'
        message['From'] = sender_email
        message['To'] = patient_email
        message.set_content(f'\n\nDear {patient_name},\n\n\n\nYour City Hospital appointment has been successfully confirmed.\n\n\n\nAppointment Details\n\n-------------------\n\n\n\nAppointment ID: {appointment_code}\n\nPatient Name: {patient_name}\n\nDoctor: {doctor_name}\n\nSpecialty: {specialty}\n\nAppointment Time: {appointment_time}\n\nStatus: CONFIRMED\n\n\n\nYour appointment ticket is attached to this email.\n\n\n\nPlease arrive a little before your appointment time.\n\n\n\nThank you for choosing City Hospital.\n\n\n\nCity Hospital\n\nAI Receptionist\n\n')
        message.add_attachment(pdf_bytes, maintype='application', subtype='pdf', filename=f'{appointment_code}.pdf')
        smtp_host = 'smtp.gmail.com'
        smtp_port = 587
        print('📧 Connecting to Gmail SMTP STARTTLS...')
        print(f'📧 Sender: {sender_email}')
        print(f'📧 Recipient: {patient_email}')
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
            print('✅ SMTP connection established')
            server.ehlo()
            print('📧 Starting TLS...')
            server.starttls()
            server.ehlo()
            print('✅ TLS connection established')
            print('📧 Logging into Gmail...')
            server.login(sender_email, sender_password)
            print('✅ Gmail login successful')
            print('📧 Sending appointment email...')
            server.send_message(message)
            print(f'✅ Appointment email sent successfully to {patient_email}')
        return True
    except smtplib.SMTPAuthenticationError as e:
        print('❌ Gmail authentication failed')
        print(f'❌ Details: {e}')
        print('⚠️ Make sure EMAIL_PASSWORD is a Google App Password, not your normal Gmail password.')
        return False
    except smtplib.SMTPServerDisconnected as e:
        print('❌ Gmail SMTP server disconnected')
        print(f'❌ Details: {e}')
        return False
    except smtplib.SMTPConnectError as e:
        print('❌ Gmail SMTP connection failed')
        print(f'❌ Details: {e}')
        return False
    except smtplib.SMTPException as e:
        print('❌ SMTP error')
        print(f'❌ Error type: {type(e).__name__}')
        print(f'❌ Details: {e}')
        return False
    except Exception as e:
        print('❌ Email sending error')
        print(f'❌ Error type: {type(e).__name__}')
        print(f'❌ Details: {e}')
        return False

# -------------------- Booking --------------------
def book_appointment_tool(doctor_name: str, appointment_time: str, patient_name: str, patient_email: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        doctor = get_doctor_details(doctor_name)
        if not doctor:
            return {'status': 'error', 'message': 'Doctor not found. Please select a doctor from the available doctors.'}
        cursor.execute("\n\n            SELECT id\n\n            FROM appointments\n\n            WHERE LOWER(doctor_name) = LOWER(?)\n\n            AND appointment_time = ?\n\n            AND status = 'CONFIRMED'\n\n            ", (doctor_name, appointment_time))
        if cursor.fetchone():
            return {'status': 'conflict', 'message': 'The doctor is already booked for this appointment time.'}
        cursor.execute('\n\n            INSERT INTO appointments\n\n            (\n\n                patient_name,\n\n                doctor_name,\n\n                appointment_time,\n\n                patient_email,\n\n                status\n\n            )\n\n            VALUES (?, ?, ?, ?, ?)\n\n            ', (patient_name, doctor['name'], appointment_time, patient_email, 'CONFIRMED'))
        appointment_id = cursor.lastrowid
        conn.commit()
        print(f'✅ Appointment confirmed: {appointment_id}')
        ticket = generate_appointment_pdf(appointment_id=appointment_id, patient_name=patient_name, patient_email=patient_email, doctor_name=doctor['name'], specialty=doctor['specialty'], appointment_time=appointment_time)
        appointment_code = ticket['appointment_code']
        email_sent = send_booking_confirmation_email(patient_email=patient_email, patient_name=patient_name, doctor_name=doctor['name'], specialty=doctor['specialty'], appointment_time=appointment_time, appointment_code=appointment_code, pdf_bytes=ticket['pdf_bytes'])
        return {'status': 'success', 'appointment_id': appointment_id, 'appointment_code': appointment_code, 'patient_name': patient_name, 'patient_email': patient_email, 'doctor_name': doctor['name'], 'specialty': doctor['specialty'], 'appointment_time': appointment_time, 'email_sent': email_sent, 'download_url': f"/tickets/{ticket['filename']}"}
    except sqlite3.IntegrityError:
        conn.rollback()
        return {'status': 'conflict', 'message': 'This doctor is already booked for the requested time.'}
    except Exception as e:
        conn.rollback()
        print(f'❌ Booking error: {e}')
        return {'status': 'error', 'message': 'Unable to complete the booking.'}
    finally:
        conn.close()
# -------------------- Groq tools --------------------
TOOL_FUNCTIONS = {'list_doctors': list_doctors_tool, 'check_slot': check_slot_tool, 'book_appointment': book_appointment_tool}
TOOL_SCHEMAS = [{'type': 'function', 'function': {'name': 'list_doctors', 'description': 'List all available hospital doctors and specialties.', 'parameters': {'type': 'object', 'properties': {}, 'required': []}}}, {'type': 'function', 'function': {'name': 'check_slot', 'description': "Check whether a doctor's requested appointment time is available.", 'parameters': {'type': 'object', 'properties': {'doctor_name': {'type': 'string', 'description': 'Full doctor name.'}, 'appointment_time': {'type': 'string', 'description': 'Requested appointment date and time.'}}, 'required': ['doctor_name', 'appointment_time']}}}, {'type': 'function', 'function': {'name': 'book_appointment', 'description': 'Book an appointment only after all required details are available.', 'parameters': {'type': 'object', 'properties': {'doctor_name': {'type': 'string', 'description': 'Full doctor name.'}, 'appointment_time': {'type': 'string', 'description': 'Appointment date and time.'}, 'patient_name': {'type': 'string', 'description': 'Patient full name.'}, 'patient_email': {'type': 'string', 'description': 'Patient email.'}}, 'required': ['doctor_name', 'appointment_time', 'patient_name', 'patient_email']}}}]

# -------------------- Voice / TTS --------------------
def clean_text_for_audio(text):
    if not text:
        return ""

    text = re.sub(r"[*_#`]", "", text)
    text = re.sub(r"\([^)]*\)", "", text)

    return " ".join(text.split())

async def generate_audio_gtts(text, lang_code='en-IN'):
    if not text:
        return None
    clean_text = clean_text_for_audio(text)
    if not clean_text:
        return None
    try:
        language = 'en'
        tld = 'co.in'
        if lang_code.startswith('hi'):
            language = 'hi'
            tld = 'com'
        elif lang_code.startswith('te'):
            language = 'te'
            tld = 'com'

        def create_audio():
            buffer = io.BytesIO()
            tts = gTTS(text=clean_text, lang=language, tld=tld, slow=False)
            tts.write_to_fp(buffer)
            buffer.seek(0)
            return buffer.getvalue()
        audio_bytes = await asyncio.to_thread(create_audio)
        return base64.b64encode(audio_bytes).decode('utf-8')
    except Exception as e:
        print(f'❌ TTS Error: {e}')
        return None
BASE_PROMPT = "\n\nYou are Sarah, the AI receptionist of City Hospital.\n\n\n\nYour ONLY job is to help patients with hospital appointments.\n\n\n\nYou can:\n\n\n\n1\\. List hospital doctors.\n\n2\\. Check appointment availability.\n\n3\\. Book appointments.\n\n4\\. Confirm appointments.\n\n\n\nSTRICT RULES:\n\n\n\n\\- Do not behave like a general-purpose chatbot.\n\n\\- Do not answer unrelated questions.\n\n\\- If asked something unrelated, politely say that you can only help\n\n  with City Hospital appointments.\n\n\\- Never invent doctors.\n\n\\- Never invent appointment slots.\n\n\\- Never claim a slot is available without using check_slot.\n\n\\- Never claim an appointment is booked unless book_appointment\n\n  returns status success.\n\n\\- Always use list_doctors when doctor information is required.\n\n\\- Always check the requested slot before booking.\n\n\\- Ask for missing information instead of guessing.\n\n\n\nRequired booking information:\n\n\n\n\\- Patient name\n\n\\- Patient email\n\n\\- Doctor\n\n\\- Appointment date/time\n\n\n\nThe patient's name and email provided by the application are trusted.\n\n\n\nAfter successful booking:\n\n\n\n\\- Clearly confirm the appointment.\n\n\\- Give the appointment ID.\n\n\\- Tell the patient that the confirmation has been sent by email\n\n  when email_sent is true.\n\n\\- Do not continue asking appointment questions after booking.\n\n\\- The application will automatically end the call.\n\n\n\nKeep responses short and natural because responses are converted\n\ninto voice audio.\n\n\n\nDo not use markdown.\n\n\n\nNever expose internal tool names to the patient.\n\n"

# -------------------- API models --------------------
class AgentMessageRequest(BaseModel):
    session_id: str | None = None
    text: str
    language_code: str | None = 'en-IN'
    patient_name: str | None = None
    patient_email: str | None = None
AGENT_SESSIONS = {}

def get_chat_session(session_id=None):
    get_groq_client()
    if not session_id or session_id not in AGENT_SESSIONS:
        session_id = str(uuid.uuid4())
        AGENT_SESSIONS[session_id] = [{'role': 'system', 'content': BASE_PROMPT}]
    return (session_id, AGENT_SESSIONS[session_id])

@app.get('/')
def read_root():
    return FileResponse('frontend.html', media_type='text/html')

@app.get('/tickets/{filename}')
def download_ticket(filename: str):
    safe_filename = os.path.basename(filename)
    filepath = os.path.join(TICKET_DIR, safe_filename)
    if not os.path.exists(filepath):
        return {'error': 'Ticket not found'}
    return FileResponse(filepath, media_type='application/pdf', filename=safe_filename)

@app.post('/agent/new_session')
async def new_session():
    sid, messages = get_chat_session()
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = 'Good morning. Welcome to City Hospital. I am Sarah, your AI receptionist. How may I help you with your appointment today?'
    elif current_hour < 17:
        greeting = 'Good afternoon. Welcome to City Hospital. I am Sarah, your AI receptionist. How may I help you with your appointment today?'
    else:
        greeting = 'Good evening. Welcome to City Hospital. I am Sarah, your AI receptionist. How may I help you with your appointment today?'
    audio = await generate_audio_gtts(greeting, 'en-IN')
    return {'session_id': sid, 'greeting': greeting, 'audio': audio}

@app.post('/agent/message')
async def agent_message(req: AgentMessageRequest):
    sid, messages = get_chat_session(req.session_id)
    client = get_groq_client()
    language = req.language_code or 'en-IN'
    language_instruction = {'en-IN': 'Respond only in English.', 'hi-IN': 'Respond only in Hindi. Use Hindi script.', 'te-IN': 'Respond only in Telugu. Use Telugu script.'}.get(language, 'Respond only in English.')
    patient_name = (req.patient_name or '').strip()
    patient_email = (req.patient_email or '').strip()
    patient_context = f"\n\n\n\n[HOME PAGE PATIENT DETAILS]\n\n\n\nPatient Name:\n\n{patient_name or 'Not provided'}\n\n\n\nPatient Email:\n\n{patient_email or 'Not provided'}\n\n\n\nThe Home Page patient email is the ONLY email address\n\nthat should be used for confirmation.\n\n"
    messages.append({'role': 'user', 'content': f'{req.text}\n\n[LANGUAGE INSTRUCTION]\n{language_instruction}\n{patient_context}'})
    try:
        booking_result = None
        final_text = ''
        for _ in range(6):
            response = await asyncio.to_thread(client.chat.completions.create, model=MODEL_NAME, messages=messages, tools=TOOL_SCHEMAS, tool_choice='auto', temperature=0.1, max_tokens=500)
            assistant_message = response.choices[0].message
            message_dict = {'role': 'assistant', 'content': assistant_message.content or ''}
            tool_calls = assistant_message.tool_calls
            if tool_calls:
                message_dict['tool_calls'] = []
                for call in tool_calls:
                    message_dict['tool_calls'].append({'id': call.id, 'type': 'function', 'function': {'name': call.function.name, 'arguments': call.function.arguments}})
            messages.append(message_dict)
            if not tool_calls:
                final_text = assistant_message.content or ''
                break
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                try:
                    function_args = json.loads(tool_call.function.arguments or '{}')
                except Exception:
                    function_args = {}
                tool_result = None
                if function_name == 'book_appointment':
                    if not patient_email:
                        tool_result = {'status': 'error', 'message': 'Patient email is missing from the Home Page.'}
                    elif not patient_name:
                        tool_result = {'status': 'error', 'message': 'Patient name is missing from the Home Page.'}
                    else:
                        function_args['patient_email'] = patient_email
                        function_args['patient_name'] = patient_name
                        tool_result = TOOL_FUNCTIONS[function_name](**function_args)
                        if tool_result and tool_result.get('status') == 'success':
                            booking_result = tool_result
                elif function_name in TOOL_FUNCTIONS:
                    tool_result = TOOL_FUNCTIONS[function_name](**function_args)
                else:
                    tool_result = {'status': 'error', 'message': 'Unknown operation.'}
                messages.append({'role': 'tool', 'tool_call_id': tool_call.id, 'name': function_name, 'content': json.dumps(tool_result, ensure_ascii=False)})
            if booking_result:
                confirmation_response = await asyncio.to_thread(client.chat.completions.create, model=MODEL_NAME, messages=messages, tools=TOOL_SCHEMAS, tool_choice='none', temperature=0.1, max_tokens=300)
                final_text = confirmation_response.choices[0].message.content or ''
                messages.append({'role': 'assistant', 'content': final_text})
                break
        if not final_text:
            final_text = 'How may I help you with your hospital appointment?'
        if booking_result:
            appointment_code = booking_result.get('appointment_code')
            doctor_name = booking_result.get('doctor_name')
            specialty = booking_result.get('specialty')
            appointment_time = booking_result.get('appointment_time')
            email_sent = booking_result.get('email_sent', False)
            download_url = booking_result.get('download_url')
            if language == 'hi-IN':
                final_text = f'आपकी अपॉइंटमेंट सफलतापूर्वक कन्फर्म हो गई है। आपका अपॉइंटमेंट आईडी {appointment_code} है। '
                if email_sent:
                    final_text += 'कन्फर्मेशन और टिकट आपके ईमेल पर भेज दिया गया है।'
            elif language == 'te-IN':
                final_text = f'మీ అపాయింట్\u200cమెంట్ విజయవంతంగా కన్ఫర్మ్ అయింది. మీ అపాయింట్\u200cమెంట్ ఐడి {appointment_code}. '
                if email_sent:
                    final_text += 'కన్ఫర్మేషన్ మరియు టికెట్ మీ ఈమెయిల్\u200cకు పంపబడింది.'
            else:
                final_text = f'Your appointment has been successfully confirmed. Your appointment ID is {appointment_code}. '
                if email_sent:
                    final_text += 'The confirmation and appointment ticket have been sent to your email.'
            if language == 'hi-IN':
                closing_text = 'Thank you for choosing City Hospital. Have a wonderful day. Goodbye.'
            elif language == 'te-IN':
                closing_text = 'City Hospital ను ఎంచుకున్నందుకు ధన్యవాదాలు. మీ రోజు శుభంగా ఉండాలి. గుడ్\u200cబై.'
            else:
                closing_text = 'Thank you for choosing City Hospital. Have a wonderful day. Goodbye.'
            audio_b64 = await generate_audio_gtts(final_text, language)
            closing_audio = await generate_audio_gtts(closing_text, language)
            return {'session_id': sid, 'text': final_text, 'voice_text': final_text, 'audio': audio_b64, 'closing_text': closing_text, 'closing_audio': closing_audio, 'auto_end': True, 'ticket': {'appointment_code': appointment_code, 'doctor_name': doctor_name, 'specialty': specialty, 'appointment_time': appointment_time, 'email_sent': email_sent, 'download_url': download_url}}
        audio_b64 = await generate_audio_gtts(final_text, language)
        return {'session_id': sid, 'text': final_text, 'voice_text': final_text, 'audio': audio_b64, 'auto_end': False}
    except Exception as e:
        print(f'❌ Agent Error: {e}')
        error_text = 'I am sorry, I am having a technical issue. Please try again.'
        error_audio = await generate_audio_gtts(error_text, language)
        return {'session_id': sid, 'text': error_text, 'voice_text': error_text, 'audio': error_audio, 'auto_end': False}
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, reload=False)
