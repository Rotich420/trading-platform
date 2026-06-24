import base64
import requests
from datetime import datetime
from decouple import config

CONSUMER_KEY = config("MPESA_CONSUMER_KEY", default="")
CONSUMER_SECRET = config("MPESA_CONSUMER_SECRET", default="")
SHORTCODE = config("MPESA_SHORTCODE", default="")
PASSKEY = config("MPESA_PASSKEY", default="")

AUTH_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
STK_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"


def get_access_token():
    response = requests.get(
        AUTH_URL,
        auth=(CONSUMER_KEY, CONSUMER_SECRET)
    )

    response.raise_for_status()

    return response.json()["access_token"]


def generate_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")


def generate_password(timestamp):
    password = f"{SHORTCODE}{PASSKEY}{timestamp}"

    return base64.b64encode(
        password.encode()
    ).decode()


def stk_push(phone, amount):

    access_token = get_access_token()

    timestamp = generate_timestamp()

    password = generate_password(timestamp)

    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "TradingPlatform",
        "TransactionDesc": "Wallet Deposit"
    }

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.post(
        STK_URL,
        json=payload,
        headers=headers
    )

    return response.json()