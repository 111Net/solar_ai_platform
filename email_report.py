import smtplib
import sys
from email.message import EmailMessage

PDF_FILE = sys.argv[1] if len(sys.argv) > 1 else "test_report.pdf"
TO_EMAIL = sys.argv[2] if len(sys.argv) > 2 else "team@example.com"
FROM_EMAIL = sys.argv[3] if len(sys.argv) > 3 else "youremail@example.com"
SMTP_SERVER = sys.argv[4] if len(sys.argv) > 4 else "smtp.gmail.com"
SMTP_PORT = int(sys.argv[5]) if len(sys.argv) > 5 else 587
EMAIL_PASSWORD = sys.argv[6] if len(sys.argv) > 6 else ""

# Create email message
msg = EmailMessage()
msg['Subject'] = "Solar SaaS Test Report"
msg['From'] = FROM_EMAIL
msg['To'] = TO_EMAIL
msg.set_content("Attached is the latest automated Solar SaaS test report (PDF).")

# Attach PDF
with open(PDF_FILE, 'rb') as f:
    pdf_data = f.read()
msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=PDF_FILE)

# Send email
try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(FROM_EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)
    print(f"Email sent successfully to {TO_EMAIL}")
except Exception as e:
    print(f"Failed to send email: {e}")

import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

PDF_FILE = sys.argv[1] if len(sys.argv) > 1 else "test_report.pdf"

FROM_EMAIL = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("EMAIL_TO")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# Create email message
msg = EmailMessage()
msg['Subject'] = "Solar SaaS Test Report"
msg['From'] = FROM_EMAIL
msg['To'] = TO_EMAIL
msg.set_content("Attached is the latest automated Solar SaaS test report (PDF).")

# Attach PDF
with open(PDF_FILE, 'rb') as f:
    pdf_data = f.read()
msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=PDF_FILE)

# Send email
try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(FROM_EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)
    print(f"Email sent successfully to {TO_EMAIL}")
except Exception as e:
    print(f"Failed to send email: {e}")