from flask import Flask, render_template, request, redirect, url_for, session
import json
import pyrebase
import hashlib
from datetime import datetime
from utils.otp_client import OTP_Client
from utils.email_client import Email_Client
from utils.thingspeak_client import Thingspeak_Client

# import logging
# # Set Logging for website to assets/logs/website.log
# logging.basicConfig(
#     filename="assets/logs/website.log",
#     level=logging.DEBUG,
#     format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
# )


def load_Firebase_Config():
    with open("assets/configs/firebase.json", "r") as fp:
        return json.load(fp)


firebase_config = load_Firebase_Config()
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

thingspeakClient = Thingspeak_Client("assets/configs/thingspeakDatabase.json")

app = Flask(__name__)
app.config["SECRET_KEY"] = "xxxxxxxxx"
loginAttempts = 0
openPod = "CLOSE"


@app.route("/", methods=["GET", "POST"])
def loginPage():
    global loginAttempts
        
    if request.method == "POST":
        username = request.form["login-username"]
        password = request.form["login-password"].encode("utf-8")

        # Hash password using SHA512 which is used for authentication
        hashed_password = hashlib.sha512(password).hexdigest()

        try:
            print(
                f"Login Username is: {username}, Password is {password}, Hashed Password is {hashed_password}"
            )
            session["user"] = username
            session["loginTime"] = str(datetime.now().timestamp())
            session["otp_attempts"] = 0
            print("Added email to session")
            auth.sign_in_with_email_and_password(username, hashed_password)
            print("Authentication Successful")

            loginAttempts = 0

            otp_client = OTP_Client()
            otp_client.genOTP()
            print("OTP Generated")
            otp_client.sendOTP(username)
            print("Email Sent")
            # session["user"] = username
            # print("Added email to session")
            session["otp"] = otp_client.OTP
            print("Added otp to session")
            return redirect(url_for("otpPage"))

        # When Username or Password is wrong
        except:
            thingspeakClient.uploadLoginSuccess(
                session["user"], session["loginTime"], 1
            )
            loginAttempts += 1
            print("Error Username or Password is wrong. Please try again.")
            print(f"loginAttempts = {loginAttempts}")

            # If attempts more than 3, lockout website for 3 minutes, else allow retry
            if loginAttempts < 3:
                return render_template("index.html")
            else:
                loginAttempts = 0
                return redirect(url_for("lockedoutPage"))

    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signupPage():
    if request.method == "POST":
        username = request.form["signup-username"]
        password = request.form["signup-password"].encode("utf-8")
        print(f"Username is: {username}, Password is {password}")

        # Hash password using sha512
        hashed_password = hashlib.sha512(password).hexdigest()

        # Using Firebase Authentication create account with username and password
        auth.create_user_with_email_and_password(username, hashed_password)
        print(f"Signed Up Username is: {username}, Password is {hashed_password}")

        return redirect(url_for("loginPage"))
    return render_template("signup.html")


@app.route("/otp", methods=["GET", "POST"])
def otpPage():
    global loginAttempts
    if request.method == "POST":
        # Gets OTP Input box value and check if its correct
        otp_input = request.form["OTP-input"]
        if otp_input == session["otp"]:

            # Upload Login Success to Firebase
            thingspeakClient.uploadLoginSuccess(
                session["user"], session["loginTime"], 0
            )

            # if OTP is correct redirect to success page
            return redirect(url_for("successfulLoginPage"))
        else:
            loginAttempts += 1
            if session["otp_attempts"] == 1:
                thingspeakClient.uploadLoginSuccess(
                    session["user"], session["loginTime"], 2
                )
                return redirect(url_for("otpError"))
            else:
                session["otp_attempts"] += 1
    return render_template("otp.html")


@app.route("/otpError", methods=["GET", "POST"])
def otpError():
    # Upload useraccount failed to login

    # Removes Session Data
    session.pop("userAccount", None)
    session.pop("user", None)
    session.pop("otp", None)
    session.pop("loginTime", None)
    session.pop("loginAttempts", None)

    return render_template("otpError.html")


@app.route("/successfulLoginPage", methods=["GET", "POST"])
def successfulLoginPage():
    global openPod
    openPod = "OPEN"
    # Sends email to user to notify user has been logged out
    #email_client = Email_Client()
    #email_client.sendEmail(
    #    "Login Successful", session["user"], "Dear Valued User,\n\nYou have log in successfully.\n\nThis is an automatically generated email. Please do not reply to this email as this email account is not monitored.\n\nRegards,\nSMART POD SYSTEM\nSingapore Polytechnic"
    #)
    if request.method == "POST":
        return redirect(url_for("logoutPage"))
    else:
	# Sends email to user to notify user has been logged out
        email_client = Email_Client()
        email_client.sendEmail(
	"Login Successful", session["user"], "Dear Valued User,\n\nYou have log in successfully.\n\nThis is an automatically generated email. Please do not reply to this email as this email account is not monitored.\n\nRegards,\nSMART POD SYSTEM\nSingapore Polytechnic"
        )
    return render_template("successfulLogin.html")


@app.route("/logout", methods=["GET", "POST"])
def logoutPage():
    """
    Function to logout user. Email is sent to notify user has logged out and cleans up user session
    """
    global openPod

    # Sends email to user to notify user has been logged out
    email_client = Email_Client()
    email_client.sendEmail(
        "Logout Successful", session["user"], "Dear Valued User,\n\nYou have log out successfully.\n\nThis is an automatically generated email. Please do not reply to this email as this email account is not monitored.\n\nRegards,\nSMART POD SYSTEM\nSingapore Polytechnic"
    )

    # Removes user and otp from session to show no one is logged in
    session.pop("user", None)
    session.pop("otp", None)

    openPod = "CLOSE"

    return redirect(url_for("loginPage"))


@app.route("/lockedoutPage")
def lockedoutPage():
    return render_template("lockedout.html")

@app.route("/getdata", methods=["GET", "POST"])
def data2arduino():
    global openPod

    return openPod

if __name__ == "__main__":
    context = (
        "./assets/ssl-certificate/website/cert.pem",
        "./assets/ssl-certificate/website/key.pem",
    )  # SSL Certificate
    #app.run(debug=True)
    app.run(debug=True, ssl_context=context, port=8000)
