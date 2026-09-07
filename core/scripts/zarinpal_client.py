import requests
import json
from django.conf import settings

class ZarinPalSandbox:
    _payment_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    _payment_verify_url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    _payment_page_url = "https://sandbox.zarinpal.com/pg/StartPay/"
    _callback_url = "http://127.0.0.1:8000/payment/verify"



    def __init__(self,merchant_id=None):
        self.merchant_id = merchant_id or settings.MERCHANT_ID


    def payment_request(self, amount, callback_url=None, description="پرداختی کاربر"):
        payload = {
            "merchant_id": self.merchant_id,
            "amount": int(amount),
            "callback_url": callback_url or self._callback_url,
            "description": description,
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        response = requests.post(
            self._payment_request_url, headers=headers, json=payload,
        timeout=15)
        print("_" * 50)
        print("STATUS CODE:", response.status_code)
        print("HEADERS:", response.headers)
        print("RESPONSE TEXT:", repr(response.text))
        print("" * 50)

        response.raise_for_status()
        data = response.json()
        if data.get("errors"):
            raise Exception(f"ZarinPal Error: {data['errors']}")
        return data


    def payment_verify(self, amount, authority):
        payload = {
            "merchant_id": self.merchant_id,
            "amount": int(amount),
            "authority": authority,
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        response = requests.post(
            self._payment_verify_url, headers=headers, json=payload,
        timeout=15)

        print("-" * 50)
        print("ZARINPAL VERIFY")
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)
        print("-" * 50)

        response.raise_for_status()
        data = response.json()
        if data.get("errors"):
            raise Exception(f"ZarinPal Error: {data['errors']}")
        return data


    def generate_payment_url(self, authority):
        return self._payment_page_url + authority


if __name__ == "__main__":
    zarinpal = ZarinPalSandbox(merchant_id="4ced0a1e-4ad8-4309-9668-3ea3ae8e8897")
    response = zarinpal.payment_request(15000)

    print(response)
    input("proceed to generating payment url?")
    authority = response["data"]["authority"]
    print(zarinpal.generate_payment_url(authority))

   
    input("check the payment?")
    response = zarinpal.payment_verify(
        15000,
        authority
    )  
    print(response)
