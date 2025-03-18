import smtplib
from email.message import EmailMessage
import os

def send_email(recipient, subject, email_body):
    email = EmailMessage()
    email['From'] = os.getenv("GMAIL_USERNAME")
    email['To'] = recipient
    email['Subject'] = subject
    email.set_content(email_body)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(os.getenv("GMAIL_USERNAME"), os.getenv("GMAIL_PASSWORD"))
        server.send_message(email)
