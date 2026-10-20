"""Send plain-text emails from a Gmail account."""

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

# Settings from .env
SENDER_EMAIL = os.getenv("SENDER_EMAIL")          # Gmail address the email is sent from
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")    # Gmail App Password, not the normal password
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")    # where every email goes

def send_email(subject, body):
    """Send an email with the given subject and body to RECIPIENT_EMAIL."""
    message = EmailMessage()
    message['From'] = SENDER_EMAIL
    message['To'] = RECIPIENT_EMAIL
    message['Subject'] = subject
    message.set_content(body)

    # Connect to Gmail's mail server over SSL, log in and send
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(message)
