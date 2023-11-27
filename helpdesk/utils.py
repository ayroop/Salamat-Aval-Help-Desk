import requests
import json

def send_sms_via_farazsms(phone_number, message):
    url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"

    payload = json.dumps({
        "code": "m908hr25zg4oa0u",  # Faraz SMS pattern code
        "sender": "+983000505",
        "recipient": phone_number,
        "variable": {
            "verification-code": otp_code,
            "message": message  # Add the message variable
        }
    })
    headers = {
        'apikey': '7E9TgT9spDN5k6NIAaF5suPoY14oLR2HyjO6QqfM5CI=',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()
