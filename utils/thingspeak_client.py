import requests
import json

class Thingspeak_Client:
    def __init__(self, configFile):
        self.config = dict()
        
        with open(configFile, "r") as fp:
            self.config = json.load(fp)

        self.channel = self.config["channel_LoginSuccess"]
        self.readAPIKey = self.config["readAPIKey_LoginSuccess"]
        self.writeAPIKey = self.config["writeAPIKey_LoginSuccess"]

    def uploadLoginSuccess(self, username, loginTime, loginStatus):
        requests.get(f"https://api.thingspeak.com/update?api_key={self.writeAPIKey}&field1={username}&field2={loginTime}&field3={loginStatus}")
    