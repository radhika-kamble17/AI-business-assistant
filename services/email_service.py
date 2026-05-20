import os
import ssl
import smtplib
from email.message import EmailMessage


def send_lead_notification(name: str, email: str, phone: str, course: str, message: str) -> None:
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    use_tls = os.getenv("SMTP_USE_TLS", "true").lower() not in ("false", "0", "no")

    sender = os.getenv("EMAIL_SENDER")
    recipient = os.getenv("EMAIL_RECIPIENT")

    if not all([smtp_server, smtp_username, smtp_password, sender, recipient]):
        raise ValueError("Missing SMTP or email settings in environment variables.")

    email_message = EmailMessage()
    email_message["Subject"] = f"New Lead Received: {name}"
    email_message["From"] = sender
    email_message["To"] = recipient
    email_message.set_content(
        f"""
New lead submitted from the AI Business Assistant website.

Name: {name}
Email: {email}
Phone: {phone}
Course Interested: {course}
Message:
{message}
"""
    )

    context = ssl.create_default_context()

    if use_tls:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=20) as server:
            server.starttls(context=context)
            server.login(smtp_username, smtp_password)
            server.send_message(email_message)
    else:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context, timeout=20) as server:
            server.login(smtp_username, smtp_password)
            server.send_message(email_message)
