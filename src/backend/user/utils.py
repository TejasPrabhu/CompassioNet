import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

GOOGLE_API_key = os.environ.get("GOOGLE_API_key")


def send_verification_email(email, verification_link):
    subject = "Email Verification"
    sender_email = "verify@compassionate.com"
    recipient_email = email

    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient_email

    text = f"Please click the following link to verify your email: {verification_link}"
    html = f"<html><body><p>{text}</p></body></html>"

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    try:
        server = smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525)
        server.starttls()
        server.login("94bf8cea2c7689", "4e87924a3bfba4")
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
