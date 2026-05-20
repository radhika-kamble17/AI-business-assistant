# SETUP GUIDE - AI Business Automation Assistant

## Quick Start (5 minutes)

### Step 1: Install Python Dependencies

Run this in the project folder:

```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

Create a `.env` file in the project root with your settings:

```bash
copy .env.example .env
```

Edit `.env` with your actual values:

```
GEMINI_API_KEY=sk-xxxxxx
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here
EMAIL_SENDER=your_email@gmail.com
EMAIL_RECIPIENT=admin@your_company.com
```

### Step 3: Run the Application

```bash
python app.py
```

Visit http://localhost:5000 in your browser.

---

## Detailed Configuration

### Getting Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key and add to `.env` as GEMINI_API_KEY

### Setting Up Gmail Email Notifications

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an app-specific password:
   - Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - Select "Mail" and "Windows Computer"
   - Copy the 16-character password
3. Use this password as SMTP_PASSWORD in `.env`

### Using Other Email Providers

**Outlook/Hotmail:**
```
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
```

**Yahoo Mail:**
```
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

**SendGrid:**
```
SMTP_SERVER=smtp.sendgrid.net
SMTP_USERNAME=apikey
SMTP_PASSWORD=SG.xxxxxxxxxxxxx
```

---

## Project Structure Explained

```
AI business assistant/
│
├── app.py                          # Main Flask application
│   ├── Routes: /, /chatbot, /dashboard, /chat, /submit_lead, /health
│   ├── Database initialization
│   └── Error handling
│
├── services/
│   ├── gemini_service.py          # Gemini AI integration
│   │   ├── get_gemini_model()     # Initialize model
│   │   └── ask_gemini()           # Generate responses
│   │
│   └── email_service.py           # Email sending
│       └── send_lead_notification() # Send notification emails
│
├── templates/
│   ├── index.html                 # Home page (lead form + mini chat)
│   ├── chatbot.html               # Full chatbot page
│   └── dashboard.html             # Admin lead dashboard
│
├── static/
│   ├── style.css                  # Responsive design (modern + clean)
│   └── script.js                  # Form handling and API integration
│
├── database.db                     # SQLite database (auto-created)
│
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── render.yaml                    # Render deployment config
├── .gitignore                     # Git ignore rules
├── README.md                      # Documentation
└── SETUP.md                       # This file
```

---

## Application Flow

### 1. User Visits Home Page (/)

- Loads index.html with two side-by-side sections
- Left: AI Chatbot (mini version)
- Right: Lead Capture Form

### 2. User Asks Chatbot

- JavaScript sends message to `/chat` endpoint
- Flask calls `ask_gemini()` from services
- Gemini generates response
- Response displayed in real-time

### 3. User Submits Lead Form

- Form data sent to `/submit_lead` endpoint
- Data validated and saved to SQLite
- Email notification triggered automatically
- If email fails, lead still saved (logged)
- Success message shown to user

### 4. Admin Views Dashboard (/dashboard)

- All leads displayed in table format
- Shows: ID, Name, Email, Phone, Course, Message, Timestamp
- Newest leads appear first

---

## Database Schema

### Leads Table

```sql
CREATE TABLE leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    course TEXT NOT NULL,
    message TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
```

---

## API Endpoints

### GET /
Returns the home page with lead form and chatbot.

### GET /chatbot
Returns the full-page chatbot interface.

### POST /chat
Submit a message to the Gemini chatbot.

**Request:**
```json
{
    "message": "Your question here"
}
```

**Response:**
```json
{
    "reply": "Gemini's answer"
}
```

### POST /submit_lead
Capture a new lead and send notification email.

**Request:**
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "course": "Service Name",
    "message": "Additional details"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Lead submitted successfully."
}
```

### GET /dashboard
Display all captured leads.

### GET /health
Health check endpoint.

**Response:**
```json
{
    "status": "ok"
}
```

---

## Deployment to Render

### Prerequisites
- GitHub account with your repository
- Render account (free at render.com)

### Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create Render Service**
   - Log in to Render dashboard
   - Click "New +" > "Web Service"
   - Select your GitHub repository
   - Configure settings:
     - **Name:** ai-business-assistant
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`
     - **Plan:** Starter (free tier)

3. **Set Environment Variables**
   - Go to "Environment" section
   - Add all variables from your `.env`:
     - GEMINI_API_KEY
     - SMTP_SERVER
     - SMTP_PORT
     - SMTP_USERNAME
     - SMTP_PASSWORD
     - EMAIL_SENDER
     - EMAIL_RECIPIENT
     - DATABASE_PATH=database.db
     - FLASK_DEBUG=0

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy automatically
   - Your app will be live at: `https://your-service-name.onrender.com`

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'google'"

**Solution:**
```bash
pip install google-generativeai
```

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Chatbot says "GEMINI_API_KEY is required"

**Solution:**
- Check `.env` file exists
- Verify GEMINI_API_KEY is set correctly
- Make sure no spaces before/after the key

### Issue: Emails not sending

**Solution:**
- Test SMTP connection separately
- For Gmail: Use app-specific password, not regular password
- Check Email_RECIPIENT is correct
- Verify port 587 or 465 is accessible

### Issue: Database locked error

**Solution:**
- SQLite locks when too many writes happen
- For production, consider PostgreSQL instead
- On Render, use Render PostgreSQL addon

### Issue: Page shows "500 Error"

**Solution:**
- Check browser console for errors (F12)
- Check Render logs for Python errors
- Verify all imports in Python files
- Test locally first: `python app.py`

---

## Performance Tips

1. **Caching Responses:** Add Redis for session management
2. **Database Optimization:** Create indexes on frequently queried columns
3. **Load Testing:** Use Apache JMeter to test under load
4. **Monitoring:** Set up error tracking with Sentry

---

## Security Best Practices

1. **Never commit .env** — Keep it in .gitignore
2. **Use environment variables** — Never hardcode secrets
3. **Enable HTTPS** — Render provides free SSL
4. **Validate inputs** — All forms have validation
5. **CSRF Protection** — Consider adding flask-talisman
6. **Rate limiting** — Add flask-limiter for API endpoints

---

## Next Steps

- [ ] Set up Google Gemini API key
- [ ] Configure email settings
- [ ] Test locally: `python app.py`
- [ ] Create GitHub repository
- [ ] Deploy to Render
- [ ] Test all features on live deployment
- [ ] Set up monitoring/alerts

---

## Support & Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Gemini API Docs](https://ai.google.dev/)
- [Render Deployment Guide](https://render.com/docs)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

Good luck with your AI Business Assistant! 🚀
