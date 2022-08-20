import smtplib
from email.message import EmailMessage
import json

class Email_Client:
    def __init__(self):
        pass

    def sendEmail(self, subject, receivingEmail, message):
        email_config = dict()
        with open("assets/configs/smtp.json") as fp:
            email_config = json.load(fp)
        print("smtp.json loaded")
        with smtplib.SMTP("smtp.office365.com", 587) as smtp:
            print("Connected to smtp.office365.com")
            smtp.ehlo() # Can be omitted due to it being implicit, but put in just in case
            smtp.starttls() # Secure the connection using TLS
            smtp.ehlo() # Can be omitted due to it being implicit, but put in just in case
            smtp.login(email_config["email"], email_config["password"])

            # Set up email message and send it
            email_message = EmailMessage()
            email_message["Subject"] = subject
            email_message["From"] = email_config["email"]
            email_message["To"] = receivingEmail
            email_message.set_content(message)
            smtp.send_message(email_message)
