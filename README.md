# AI Business Automation Assistant

A beginner-friendly Flask application that uses the Gemini API to power an AI chatbot, capture leads into SQLite, send automated email notifications, and display leads in an admin dashboard.

## Features

- **Gemini chatbot** — Powered by Google's Gemini API
- **Lead capture form** — Collect prospect information with validation
- **SQLite database** — Store leads with timestamps
- **Email automation** — Send notifications when new leads submit
- **Admin dashboard** — View and manage all captured leads
- **Responsive UI** — Mobile-friendly design with modern styling
- **Render-ready** — Configured for deployment on Render.com

## Folder Structure

```
.
├── app.py                  # Flask application entry point
├── services/
│   ├── gemini_service.py  # Gemini chat integration
│   └── email_service.py   # Email notification automation
├── templates/
│   ├── index.html         # Home page (lead form + mini chatbot)
│   ├── chatbot.html       # Full chatbot page
│   └── dashboard.html     # Admin lead dashboard
├── static/
│   ├── style.css          # Responsive styling
│   └── script.js          # Form handling and API calls
├── database.db            # SQLite database (created at runtime)
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── render.yaml            # Render deployment config
└── README.md              # This file
```

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the environment

**Windows PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
.\.venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy the example file and edit it with your credentials:

```bash
copy .env.example .env
```

Edit `.env` and fill in your credentials. Do not leave placeholder values such as `your_openai_api_key_here` or `your_smtp_username`.

## Run Locally

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Environment Variables

| Variable | Description |
|----------|-------------|
| GEMINI_API_KEY | Your Google Gemini API key |
| GEMINI_MODEL | Model name (default: gemini-pro) |
| SMTP_SERVER | Email server (default: smtp.gmail.com) |
| SMTP_PORT | Email port (default: 587) |
| SMTP_USE_TLS | Use TLS (default: true) |
| SMTP_USERNAME | Email account username |
| SMTP_PASSWORD | Email account password or app-specific password |
| EMAIL_SENDER | From email address |
| EMAIL_RECIPIENT | Where to send lead notifications |
| DATABASE_PATH | SQLite database file path |
| FLASK_DEBUG | Debug mode (1 for development, 0 for production) |

## Deployment on Render

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Set all environment variables in Render dashboard
5. Build command: `pip install -r requirements.txt`
6. Start command: `gunicorn app:app`
7. Deploy!

## Key Components

**app.py** — Main Flask application with routes:
- `/` — Home page with lead form and chatbot
- `/chatbot` — Full-page chatbot
- `/chat` — API for chatbot responses
- `/submit_lead` — API to capture leads
- `/dashboard` — Admin view of all leads
- `/health` — Health check endpoint

**services/gemini_service.py** — Gemini chat wrapper with error handling

**services/email_service.py** — Email notification system supporting TLS/SSL

**templates/** — HTML templates with Jinja2 templating

**static/** — CSS and JavaScript for responsive UI

## Important Notes

- Database is created automatically on first run
- If email fails, leads are still saved and error is logged
- All sensitive data should be in .env file, never in code
- Use Gunicorn for production deployment

## Troubleshooting

**Chatbot not responding?**
- Check GEMINI_API_KEY is valid in .env
- Verify API key has access to the selected Gemini model

**Leads not saving?**
- Check database.db file permissions
- Verify DATABASE_PATH in .env

**Emails not sending?**
- For Gmail: Use an app-specific password
- Verify SMTP credentials are correct
- Check SMTP_SERVER and SMTP_PORT

## License

MIT License - Feel free to use and modify!
