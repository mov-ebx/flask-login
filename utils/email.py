import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

API_KEY = open('secrets/SendGridAPI', 'r').readlines()[0]
FROM_EMAIL = open('secrets/SendGridEMAIL', 'r').readlines()[0]
client = SendGridAPIClient(API_KEY)

def send_email(email, subject, content):
    try:
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=email,
            subject=subject,
            html_content=content
        )
        client.send(message)
    except:
        print("Email failed to send, perhaps your SendGrid is incorrectly setup?")
