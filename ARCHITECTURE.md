# 🎯 Project Architecture Map

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BROWSER LAYER                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────┐│
│  │ index.html       │  │ chatbot.html     │  │dashboard.html
│  │ ├─Header Nav     │  │ ├─Full Chat      │  │├─Lead Table   
│  │ ├─Hero Section   │  │ ├─Textarea Input │  │├─All Records  
│  │ ├─Chatbot Form   │  │ └─Response Box   │  │└─Timestamps   
│  │ └─Lead Form      │  └──────────────────┘  └────────────┘
│  │    (5 fields)    │
│  └──────────────────┘
│
│  ┌──────────────────────────────────────────────────────────┐
│  │ style.css (220 lines) + script.js (80 lines)           │
│  │ - Modern design with gradients                         │
│  │ - Responsive grid/flexbox                              │
│  │ - Form validation & error display                      │
│  │ - Fetch API calls to backend                           │
│  └──────────────────────────────────────────────────────────┘
└────────────────────┬─────────────────────────────────────────┘
                     │ HTTP/HTTPS (AJAX)
                     │ JSON Requests/Responses
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   FLASK APPLICATION                          │
│                     (app.py)                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Route Handler Layer                                       │
│  ├─GET  /              → render_template("index.html")   │
│  ├─GET  /chatbot       → render_template("chatbot.html") │
│  ├─GET  /dashboard     → render_template("dashboard.html"
│  ├─POST /chat          → chat()                          │
│  ├─POST /submit_lead   → submit_lead()                   │
│  └─GET  /health        → health()                        │
│                                                              │
│  Middleware                                                │
│  ├─Load environment variables (python-dotenv)            │
│  ├─Initialize database (SQLite)                          │
│  ├─Error handling (try-catch)                            │
│  └─Request validation                                    │
└──────────────┬──────────────────────────┬──────────────────┘
               │                          │
         ┌─────▼─────┐           ┌───────▼──────┐
         │  AI Layer │           │  Data Layer  │
         ├───────────┤           ├──────────────┤
         │ Gemini    │           │ SQLite DB    │
         │ Service   │           │              │
         └─────┬─────┘           └───────┬──────┘
               │                          │
         ┌─────▼─────────┐        ┌──────▼──────────┐
         │ Email         │        │ Database        │
         │ Automation    │        │ Connection      │
         └─────┬─────────┘        └──────┬──────────┘
               │                          │
         ┌─────▼─────┐           ┌───────▼──────┐
         │ SMTP       │           │ database.db  │
         │ Service    │           │ (SQLite file)│
         └───────────┘           └──────────────┘
               │
         ┌─────▼─────────┐
         │ Email Server  │
         │ (Gmail/SMTP)  │
         └───────────────┘
```

---

## Request Flow Diagram

### Flow 1: User Asks Chatbot

```
User Types Question
         │
         ▼
    Browser JS
  (script.js)
         │
         ▼
POST /chat
{message: "What is AI?"}
         │
         ▼
    Flask Route
  chat() function
         │
         ▼
  ask_gemini()
  (gemini_service.py)
         │
         ▼
  Configure & Call
  Gemini API
         │
         ▼
  Return response.text
         │
         ▼
  Return JSON to Browser
{reply: "AI is..."}
         │
         ▼
  Display in UI
  (chatResponse div)
         │
         ▼
User Reads Answer
```

---

### Flow 2: User Submits Lead Form

```
User Fills Form
(name, email, phone, course, message)
         │
         ▼
    Browser JS
  Validates fields
         │
         ▼
POST /submit_lead
{JSON with lead data}
         │
         ▼
    Flask Route
  submit_lead() function
         │
         ├─ Validate input
         │
         ├─ Insert to Database
         │   INSERT INTO leads (...) VALUES (...)
         │
         └─ Send Email Notification
                    │
                    ├─ Create EmailMessage
                    │
                    ├─ Connect to SMTP Server
                    │
                    ├─ Authenticate
                    │
                    ├─ Send via TLS/SSL
                    │
                    └─ Disconnect
         │
         ▼
Return JSON Response
{success: true}
         │
         ▼
    Browser JS
  Shows success message
  Resets form
         │
         ▼
User Confirmation
```

---

### Flow 3: Admin Views Dashboard

```
Admin Clicks Dashboard Link
         │
         ▼
    Browser requests
    GET /dashboard
         │
         ▼
    Flask Route
  dashboard() function
         │
         ▼
  Get DB Connection
         │
         ▼
  Execute Query
  SELECT * FROM leads
  ORDER BY created_at DESC
         │
         ▼
  Fetch all results
         │
         ▼
  Pass to template
  dashboard.html
         │
         ▼
  Jinja2 Renders
  FOR loop through leads
  Display table rows
         │
         ▼
Return HTML to Browser
         │
         ▼
Admin Sees Lead Table
(ID, Name, Email, Phone, Course, Message, Timestamp)
```

---

## Component Interaction Map

```
┌────────────────────────────────────────────────────────────────┐
│                       EXTERNAL SERVICES                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────────┐        ┌──────────────────────────┐ │
│  │  Google Gemini API  │        │  Email Service Provider  │ │
│  │  ├─Configure API    │        │  ├─Gmail/Outlook/Yahoo  │ │
│  │  ├─Generate Content │        │  ├─SMTP Server          │ │
│  │  └─Handle Response  │        │  └─Send Email           │ │
│  └────────────┬────────┘        └──────────┬───────────────┘ │
│               │                            │                  │
└───────────────┼────────────────────────────┼──────────────────┘
                │                            │
          (JSON API)                    (SMTP Protocol)
                │                            │
         ┌──────▼──────────────────────────▼─────┐
         │   SERVICES LAYER (Python modules)     │
         ├───────────────────────────────────────┤
         │                                       │
         │  gemini_service.py                   │
         │  ├─ get_gemini_model()              │
         │  └─ ask_gemini(prompt)              │
         │                                       │
         │  email_service.py                    │
         │  └─ send_lead_notification()        │
         │                                       │
         └──────────────┬──────────────────────┘
                        │
                   (Function calls)
                        │
         ┌──────────────▼──────────────┐
         │   CORE APPLICATION LAYER    │
         │      (app.py - Flask)       │
         ├─────────────────────────────┤
         │                             │
         │  Route Handlers:            │
         │  • home()                   │
         │  • chatbot_page()           │
         │  • chat()                   │
         │  • submit_lead()            │
         │  • dashboard()              │
         │  • health()                 │
         │                             │
         └──────────────┬──────────────┘
                        │
         ┌──────────────▼──────────────┐
         │   DATA PERSISTENCE LAYER    │
         ├─────────────────────────────┤
         │                             │
         │  Database Manager:          │
         │  • get_db_connection()     │
         │  • init_db()               │
         │  • SQLite queries          │
         │                             │
         └──────────────┬──────────────┘
                        │
         ┌──────────────▼──────────────┐
         │      LOCAL DATABASE         │
         │     (database.db)           │
         ├─────────────────────────────┤
         │                             │
         │  Table: leads               │
         │  • id (PK)                  │
         │  • name                     │
         │  • email                    │
         │  • phone                    │
         │  • course                   │
         │  • message                  │
         │  • created_at (timestamp)   │
         │                             │
         └─────────────────────────────┘
```

---

## Environment Variable Flow

```
┌──────────────────────────────────────┐
│      .env Configuration File         │
│  (Secrets & Settings Repository)    │
├──────────────────────────────────────┤
│                                      │
│  GEMINI_API_KEY = sk-...            │
│  SMTP_SERVER = smtp.gmail.com       │
│  SMTP_USERNAME = user@gmail.com     │
│  SMTP_PASSWORD = app_password       │
│  EMAIL_SENDER = sender@domain.com   │
│  EMAIL_RECIPIENT = admin@domain.com │
│  DATABASE_PATH = database.db        │
│  FLASK_DEBUG = 1                    │
│  PORT = 5000                        │
│                                      │
└──────────────────┬───────────────────┘
                   │
            (Load via python-dotenv)
                   │
         ┌─────────▼────────────┐
         │  Python Environment  │
         │  os.getenv("KEY")    │
         └─────────┬────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
gemini_service.py  email_service.py  app.py
- API Key setup    - SMTP config     - DB path
- Model selection  - Email addresses - Debug mode
                   - Port selection
```

---

## Deployment Architecture (Render.com)

```
┌─────────────────────────────────────────────────────────┐
│                  RENDER PLATFORM                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐ │
│  │         Web Service Container                    │ │
│  ├──────────────────────────────────────────────────┤ │
│  │                                                  │ │
│  │  Build Stage:                                   │ │
│  │  $ pip install -r requirements.txt             │ │
│  │  $ python -m py_compile *.py                   │ │
│  │                                                  │ │
│  │  Start Command:                                 │ │
│  │  $ gunicorn app:app                            │ │
│  │                                                  │ │
│  │  ┌──────────────────────────────────────────┐  │ │
│  │  │  Running Flask Application               │  │ │
│  │  │  ├─ Host: 0.0.0.0                       │  │ │
│  │  │  ├─ Port: 8000 (assigned by Render)     │  │ │
│  │  │  └─ Workers: Gunicorn (default: 4)      │  │ │
│  │  └──────────────────────────────────────────┘  │ │
│  │                                                  │ │
│  │  ┌──────────────────────────────────────────┐  │ │
│  │  │  Environment Variables (Secrets)         │  │ │
│  │  │  Loaded from Render Dashboard            │  │ │
│  │  └──────────────────────────────────────────┘  │ │
│  │                                                  │ │
│  └──────────────────────────────────────────────────┘ │
│                      │                                │
│  ┌───────────────────▼────────────────────────────┐  │
│  │         Load Balancer & SSL/TLS               │  │
│  │  ├─ Automatic HTTPS                          │  │
│  │  ├─ Free SSL Certificate                     │  │
│  │  └─ HTTP → HTTPS Redirect                    │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
└────────────────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
   Internet              External APIs
   (Domain)             (Google Gemini,
   Users                 Email SMTP)
```

---

## Data Flow Summary

```
INCOMING DATA (User Input)
           │
           ├─ Chatbot Message
           │  └─→ /chat endpoint
           │      └─→ Gemini API
           │          └─→ Response
           │
           └─ Lead Form
              └─→ /submit_lead endpoint
                  ├─→ Database INSERT
                  │   └─→ SQLite storage
                  │
                  └─→ Email Service
                      └─→ SMTP Send
                          └─→ Admin inbox

OUTGOING DATA (Display)
           │
           ├─ Chatbot Response
           │  └─→ Browser display
           │
           ├─ Success/Error Message
           │  └─→ Form feedback
           │
           └─ Dashboard
              └─→ Lead Table
                  └─→ All records
```

---

## Security Architecture

```
┌────────────────────────────────────────────────┐
│          INPUT VALIDATION LAYER                │
├────────────────────────────────────────────────┤
│  • Required field checks                      │
│  • Email format validation                    │
│  • String trimming (prevent padding)          │
│  • Length limits                              │
└─────────────────┬──────────────────────────────┘
                  │
┌─────────────────▼──────────────────────────────┐
│        PARAMETERIZED QUERIES LAYER            │
├────────────────────────────────────────────────┤
│  • SQLite prepared statements                 │
│  • Bind variables (?) usage                   │
│  • Prevent SQL injection                      │
└─────────────────┬──────────────────────────────┘
                  │
┌─────────────────▼──────────────────────────────┐
│      ENVIRONMENT VARIABLE LAYER               │
├────────────────────────────────────────────────┤
│  • .env file (not in code)                   │
│  • No hardcoded credentials                   │
│  • os.getenv() for configuration             │
└─────────────────┬──────────────────────────────┘
                  │
┌─────────────────▼──────────────────────────────┐
│         ERROR HANDLING LAYER                  │
├────────────────────────────────────────────────┤
│  • Try-catch blocks                           │
│  • User-friendly error messages               │
│  • No sensitive data in responses             │
│  • Logging for debugging                      │
└────────────────────────────────────────────────┘
```

---

## File Dependencies

```
app.py
├─ flask (HTTP framework)
├─ sqlite3 (database)
├─ os (environment)
├─ services.gemini_service
│  └─ google.generativeai (Gemini)
│
└─ services.email_service
   ├─ smtplib (email)
   ├─ ssl (encryption)
   └─ email.message (formatting)

templates/*.html
├─ Flask url_for() (routing)
└─ static/style.css

static/script.js
├─ Fetch API (browser)
└─ Form & DOM APIs

requirements.txt
├─ Flask>=2.2
├─ google-generativeai>=0.3.2
├─ python-dotenv>=1.0
└─ gunicorn>=20.1.0 (production)
```

---

This comprehensive architecture ensures:
- ✅ Clean separation of concerns
- ✅ Scalable design
- ✅ Security by default
- ✅ Easy maintenance
- ✅ Production-ready deployment
