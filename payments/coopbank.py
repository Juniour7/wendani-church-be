import base64
import requests
import datetime
from django.conf import settings


# ------------------------------------------------------
# Generate Co-op Bank OAuth Token
# ------------------------------------------------------
def generate_token():
    headers = {
        "Authorization": settings.COOPBANK_AUTH_HEADER,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = "grant_type=client_credentials"

    response = requests.post(settings.COOPBANK_TOKEN_URL, headers=headers, data=data)
    response.raise_for_status()
    return response.json().get("access_token")


# ------------------------------------------------------
# Send STK Push
# ------------------------------------------------------
def stk_push_request(phone, amount, reference, other_details, description):
    """
    phone:       2547XXXXXXXX
    amount:      Total amount
    reference:   Unique ID (your checkout_request_id)
    other_details: list of {"Name": "<purpose>", "Value": "<amount>"}
    description: narration (e.g., MULTI or TITHE)
    """

    token = generate_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "MessageReference": reference,
        "CallBackUrl": settings.COOPBANK_CALLBACK_URL,
        "OperatorCode": settings.COOPBANK_OPERATOR_CODE,
        "UserId": settings.COOPBANK_USER_ID,
        "TransactionCurrency": "KES",
        "MobileNumber": phone,
        "Narration": description,
        "Amount": amount,
        "MessageDateTime": datetime.datetime.utcnow().isoformat() + "Z",
        "OtherDetails": other_details,
    }

    response = requests.post(settings.COOPBANK_STK_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
