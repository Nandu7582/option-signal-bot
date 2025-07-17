import requests
import pyotp

class SmartConnect:
    def __init__(self, api_key):
        self.api_key = api_key
        self.feed_token = None
        self.client_code = None
        self.jwt_token = None

    def generateSession(self, client_code, password, totp):
        url = "https://apiconnect.angelbroking.com/rest/auth/angelbroking/user/v1/loginByPassword"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-API-KEY": self.api_key
        }
        payload = {
            "clientcode": client_code,
            "password": password,
            "totp": totp
        }
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        if data.get("status") == True:
            self.feed_token = data["data"]["feedToken"]
            self.client_code = client_code
            self.jwt_token = data["data"]["jwtToken"]
        return data
