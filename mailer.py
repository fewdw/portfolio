from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os

smtp_email = "frederic.alefebvre@gmail.com"
smtp_password = "kdqhtwbnesoakare"

def send_mail(email, subject, message):

    message = f"""
    
    NEW EMAIL FROM {email}

    {subject}

    {message}
    
    """

    try:
        msg = MIMEMultipart()
        msg["From"] = email
        msg["To"] = smtp_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message))

        with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(smtp_email, smtp_password)
            smtp.send_message(msg)
    except Exception as e:
        print(e)
