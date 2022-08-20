import random
from utils.email_client import Email_Client


class OTP_Client:
    def __init__(self):
        self.OTP = ""

    def genOTP(self):
        """
        Generates a 3 digit number from 0-999, if its less than 3 digits pad number with 0s
        Do this 2 times and join the 2 numbers together to form a 6 digit number
        """
        self.OTP = "".join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])

    def sendOTP(self, emailAddress):
        """
        Sends email about OTP
        """
        emailClient = Email_Client()
        emailClient.sendEmail(
            "OTP for Study Pod",
            emailAddress,
            f"Dear Valued User,\n\nYour One-Time Password (OTP) is {self.OTP}\nThis OTP will expire in 3 mins.\n\nPlease ignore this email if you did not make the request.\n\nThis is an automatically generated email. Please do not reply to this email as this email account is not monitored.\n\nRegards,\nSMART POD SYSTEM\nSingapore Polytechnic\n",
        )
