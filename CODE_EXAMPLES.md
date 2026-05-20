# Code Examples & Snippets

## Complete Working Code Samples

### 1. Python: Flask Route Handling

**File: app.py (Submit Lead Route)**

```python
@app.route("/submit_lead", methods=["POST"])
def submit_lead():
    # Get data from request (supports both JSON and form)
    payload = request.get_json(silent=True) or request.form
    
    # Extract and clean input
    name = payload.get("name", "").strip()
    email = payload.get("email", "").strip()
    phone = payload.get("phone", "").strip()
    course = payload.get("course", "").strip()
    message = payload.get("message", "").strip()

    # Validate required fields
    if not name or not email or not phone or not course:
        return jsonify({
            "success": False, 
            "message": "Please complete all required fields."
        }), 400

    try:
        # Insert into database
        with get_db_connection() as conn:
            conn.execute(
                """INSERT INTO leads 
                   (name, email, phone, course, message) 
                   VALUES (?, ?, ?, ?, ?)""",
                (name, email, phone, course, message),
            )
            conn.commit()

        # Try to send email (fail gracefully if it doesn't work)
        try:
            send_lead_notification(name, email, phone, course, message)
        except Exception as email_error:
            # Log but don't fail - lead is already saved
            app.logger.warning("Email notification failed: %s", email_error)

        return jsonify({
            "success": True, 
            "message": "Lead submitted successfully."
        })
        
    except Exception as error:
        return jsonify({
            "success": False, 
            "message": f"Lead submission error: {error}"
        }), 500
```

---

### 2. Python: Gemini Service

**File: services/gemini_service.py (AI Integration)**

```python
import os
import google.generativeai as genai


def get_gemini_model():
    """Initialize and return Gemini model"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is required in environment variables.")

    genai.configure(api_key=api_key)
    model_name = os.getenv("GEMINI_MODEL", "gemini-pro")
    return genai.GenerativeModel(model_name)


def ask_gemini(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the response
    
    Args:
        prompt (str): User's question or prompt
        
    Returns:
        str: Gemini's response text
        
    Raises:
        ValueError: If API key is missing
    """
    model = get_gemini_model()
    
    # Generate content with specific parameters
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.45,        # Balanced creativity
            "max_output_tokens": 450,   # Keep responses concise
        },
    )

    # Handle different response formats
    if hasattr(response, "text") and response.text:
        return response.text
    if hasattr(response, "content"):
        return str(response.content)

    return str(response)
```

---

### 3. Python: Email Service

**File: services/email_service.py (SMTP Automation)**

```python
import os
import ssl
import smtplib
from email.message import EmailMessage


def send_lead_notification(name: str, email: str, phone: str, 
                          course: str, message: str) -> None:
    """
    Send email notification when a lead is captured
    
    Args:
        name, email, phone, course, message: Lead information
        
    Raises:
        ValueError: If SMTP settings are missing
    """
    
    # Load SMTP configuration from environment
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    use_tls = os.getenv("SMTP_USE_TLS", "true").lower() not in ("false", "0")

    sender = os.getenv("EMAIL_SENDER")
    recipient = os.getenv("EMAIL_RECIPIENT")

    # Validate all required settings
    if not all([smtp_server, smtp_username, smtp_password, sender, recipient]):
        raise ValueError("Missing SMTP or email settings in environment variables.")

    # Compose email
    email_message = EmailMessage()
    email_message["Subject"] = f"New Lead Received: {name}"
    email_message["From"] = sender
    email_message["To"] = recipient
    email_message.set_content(
        f"""New lead submitted from the AI Business Assistant website.

Name: {name}
Email: {email}
Phone: {phone}
Course Interested: {course}
Message:
{message}
"""
    )

    # Create SSL context
    context = ssl.create_default_context()

    # Send via TLS or SSL
    if use_tls:
        # TLS: Start with plain, then upgrade to encrypted
        with smtplib.SMTP(smtp_server, smtp_port, timeout=20) as server:
            server.starttls(context=context)
            server.login(smtp_username, smtp_password)
            server.send_message(email_message)
    else:
        # SSL: Encrypted from start
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context, timeout=20) as server:
            server.login(smtp_username, smtp_password)
            server.send_message(email_message)
```

---

### 4. JavaScript: Form Handling

**File: static/script.js (Frontend Logic)**

```javascript
/**
 * Display status message in target element
 * @param {string} elementId - ID of element to update
 * @param {string} message - Message text
 * @param {boolean} success - Success (true) or error (false)
 */
function showStatus(elementId, message, success = true) {
    const target = document.getElementById(elementId);
    if (!target) return;
    
    target.textContent = message;
    target.className = success ? "status-box success" : "status-box error";
}

/**
 * Handle chatbot message submission
 * @param {Event} event - Form submit event
 */
async function sendMessage(event) {
    if (event) event.preventDefault();

    const input = document.getElementById("userMessage");
    const replyBox = document.getElementById("chatResponse");
    const message = input.value.trim();

    if (!message) {
        showStatus("leadStatus", "Please type a message before sending.", false);
        return;
    }

    replyBox.textContent = "Thinking...";

    try {
        // Send to backend
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();
        replyBox.textContent = data.reply || "No response received.";
    } catch (error) {
        replyBox.textContent = `Chat error: ${error}`;
    }
}

/**
 * Handle lead form submission
 * @param {Event} event - Form submit event
 */
async function submitLead(event) {
    if (event) event.preventDefault();

    const form = document.getElementById("leadForm");
    if (!form) return;

    // Extract form data
    const formData = new FormData(form);
    const payload = {
        name: formData.get("name") || "",
        email: formData.get("email") || "",
        phone: formData.get("phone") || "",
        course: formData.get("course") || "",
        message: formData.get("message") || "",
    };

    showStatus("leadStatus", "Submitting lead...", true);

    try {
        // Send to backend
        const response = await fetch("/submit_lead", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        const data = await response.json();
        
        // Check response
        if (response.ok && data.success) {
            showStatus("leadStatus", data.message, true);
            form.reset();  // Clear form
        } else {
            showStatus("leadStatus", data.message || "Unable to submit lead.", false);
        }
    } catch (error) {
        showStatus("leadStatus", `Submission error: ${error}`, false);
    }
}

// Attach event listeners when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
    const leadForm = document.getElementById("leadForm");
    if (leadForm) {
        leadForm.addEventListener("submit", submitLead);
    }

    const chatForm = document.getElementById("chatForm");
    if (chatForm) {
        chatForm.addEventListener("submit", sendMessage);
    }
});
```

---

### 5. HTML: Form Template

**File: templates/index.html (Lead Form)**

```html
<!-- Lead Capture Form -->
<form id="leadForm" class="lead-form">
    <label>
        Name
        <input type="text" name="name" placeholder="Full name" required />
    </label>
    
    <label>
        Email
        <input type="email" name="email" placeholder="Email address" required />
    </label>
    
    <label>
        Phone
        <input type="text" name="phone" placeholder="Phone number" required />
    </label>
    
    <label>
        Course Interested
        <input type="text" name="course" placeholder="Service or product" required />
    </label>
    
    <label>
        Message
        <textarea name="message" placeholder="Additional details"></textarea>
    </label>
    
    <button type="submit">Submit Lead</button>
</form>

<div id="leadStatus" class="status-box"></div>
```

---

### 6. CSS: Responsive Design

**File: static/style.css (Modern Styling)**

```css
/* Root color scheme */
:root {
    color-scheme: light;
    font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background-color: #eef2f7;
    color: #111827;
}

/* Modern gradient background */
body {
    margin: 0;
    min-height: 100vh;
    background: linear-gradient(180deg, #f7fbff 0%, #eef2f7 100%);
}

/* Card styling */
.card {
    background: #ffffff;
    border: 1px solid rgba(15, 23, 42, 0.08);
    border-radius: 24px;
    padding: 28px;
    box-shadow: 0 20px 60px rgba(15, 23, 42, 0.08);
}

/* Form styling */
input, textarea {
    width: 100%;
    min-height: 44px;
    padding: 14px 16px;
    border: 1px solid #cbd5e1;
    border-radius: 14px;
    background: #f8fafc;
    transition: border-color 0.2s ease;
    font: inherit;
}

input:focus, textarea:focus {
    outline: none;
    border-color: #2563eb;
    background: #fff;
}

/* Button styling */
button {
    width: fit-content;
    border: none;
    border-radius: 14px;
    background: #2563eb;
    color: white;
    font-weight: 700;
    padding: 14px 24px;
    cursor: pointer;
    transition: transform 0.2s ease, background-color 0.2s ease;
}

button:hover {
    background: #1e40af;
    transform: translateY(-1px);
}

/* Status message styling */
.status-box {
    margin-top: 16px;
    padding: 18px;
    border-radius: 16px;
    background: #f8fafc;
    border: 1px solid rgba(148, 163, 184, 0.2);
}

.status-box.success {
    border-color: #16a34a;
    background: #ecfdf5;
    color: #166534;
}

.status-box.error {
    border-color: #dc2626;
    background: #fef2f2;
    color: #991b1b;
}

/* Responsive grid */
.grid-layout {
    display: grid;
    gap: 24px;
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

@media (max-width: 900px) {
    .grid-layout {
        grid-template-columns: 1fr;
    }
}
```

---

### 7. SQL: Database Queries

**Database Initialization**

```python
# Create leads table
cursor.execute("""
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    course TEXT NOT NULL,
    message TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")
```

**Common Queries**

```python
# Insert a lead
cursor.execute("""
INSERT INTO leads (name, email, phone, course, message) 
VALUES (?, ?, ?, ?, ?)
""", (name, email, phone, course, message))

# Get all leads (newest first)
cursor.execute("""
SELECT * FROM leads 
ORDER BY created_at DESC
""")
leads = cursor.fetchall()

# Get leads by date
cursor.execute("""
SELECT * FROM leads 
WHERE created_at > ? 
ORDER BY created_at DESC
""", ('2024-01-01',))

# Count leads
cursor.execute("SELECT COUNT(*) FROM leads")
count = cursor.fetchone()[0]

# Search leads
cursor.execute("""
SELECT * FROM leads 
WHERE name LIKE ? OR email LIKE ?
""", (f'%{search_term}%', f'%{search_term}%'))
```

---

### 8. Configuration: Environment Template

**File: .env.example**

```ini
# ============= GEMINI AI =============
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-pro

# ============= SMTP EMAIL =============
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here

# ============= EMAIL ADDRESSES =============
EMAIL_SENDER=noreply@yourcompany.com
EMAIL_RECIPIENT=admin@yourcompany.com

# ============= DATABASE =============
DATABASE_PATH=database.db

# ============= DEPLOYMENT =============
FLASK_DEBUG=1
PORT=5000
```

---

### 9. Deployment: Render Configuration

**File: render.yaml**

```yaml
services:
  - type: web_service
    name: ai-business-assistant
    env: python
    region: oregon
    plan: starter
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
```

---

### 10. Testing: Manual API Tests

**Using curl from command line:**

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test chatbot
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello, what is AI?"}'

# Test lead submission
curl -X POST http://localhost:5000/submit_lead \
  -H "Content-Type: application/json" \
  -d '{
    "name":"John Doe",
    "email":"john@example.com",
    "phone":"+1234567890",
    "course":"Web Development",
    "message":"Interested in learning more"
  }'
```

---

### 11. Python: Database Helper Functions

```python
def get_db_connection():
    """Get SQLite database connection with Row factory"""
    connection = sqlite3.connect(app.config["DATABASE"])
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Initialize database and create tables"""
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                course TEXT NOT NULL,
                message TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def add_lead(name: str, email: str, phone: str, course: str, message: str) -> int:
    """Add a new lead to database"""
    with get_db_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO leads (name, email, phone, course, message) VALUES (?, ?, ?, ?, ?)",
            (name, email, phone, course, message),
        )
        conn.commit()
        return cursor.lastrowid


def get_all_leads():
    """Get all leads sorted by creation date (newest first)"""
    with get_db_connection() as conn:
        leads = conn.execute(
            "SELECT * FROM leads ORDER BY created_at DESC"
        ).fetchall()
    return leads
```

---

### 12. Error Handling Pattern

```python
@app.route("/some-route", methods=["POST"])
def some_handler():
    try:
        # 1. Get and validate input
        data = request.get_json(silent=True) or {}
        required_field = data.get("field", "").strip()
        
        if not required_field:
            return jsonify({
                "success": False,
                "message": "Required field is missing"
            }), 400

        # 2. Process request
        result = do_something(required_field)

        # 3. Return success
        return jsonify({
            "success": True,
            "data": result
        })
        
    except ValueError as ve:
        # Handle validation errors
        return jsonify({
            "success": False,
            "message": f"Validation error: {ve}"
        }), 422
        
    except Exception as e:
        # Handle unexpected errors
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred"
        }), 500
```

---

## Best Practices

✅ **Always validate input on server side**
✅ **Use parameterized queries to prevent SQL injection**
✅ **Store secrets in environment variables**
✅ **Handle exceptions gracefully**
✅ **Log errors for debugging**
✅ **Return meaningful error messages**
✅ **Use try-catch in async operations**
✅ **Test locally before deploying**

---

These code examples demonstrate production-ready patterns and best practices!
